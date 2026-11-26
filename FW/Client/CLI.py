import argparse
import queue
import re
import threading
import time
import tkinter as tk
from tkinter import ttk

import serial
import serial.tools.list_ports

VID = 0x303A # normally esp32
BAUD = 115200

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
BUTTONS = [(21, "1"), (22, "2"), (23, "3"), (24, "4"), (25, "5"), (26, "6"),
           (31, "Enc 1 push"), (32, "Enc 2 push")]
BUTTON_NAMES = {21: "Button 1", 22: "Button 2", 23: "Button 3", 24: "Button 4",
                25: "Button 5", 26: "Button 6", 31: "Encoder 1 push", 32: "Encoder 2 push"}

RE_EV = re.compile(r"^EV:(\d+):(-?\d+)$")
RE_NT = re.compile(r"^NT:(\d+):(\d+)$")
RE_ST = re.compile(r"^ST:(\d+):(\d+):(\d+):(-?\d+)$")

# colour thing
BG, CARD, FG, DIM = "#14161c", "#1e222b", "#e8eaf0", "#8a91a3"
ACCENT, GOOD, BAD = "#ffb020", "#3ddc84", "#ff5c5c"
WHITE_KEY, BLACK_KEY = "#ffffff", "#000000"


def note_name(n):
    return f"{NOTE_NAMES[n % 12]}{n // 12 - 1}"


def parse_line(line):
    for rx, kind in ((RE_EV, "input"), (RE_NT, "note"), (RE_ST, "state")):
        m = rx.match(line.strip())
        if m:
            return kind, tuple(int(g) for g in m.groups())
    return None


# serial
def find_port(forced):
    for p in serial.tools.list_ports.comports():
        if (forced and p.device == forced) or (not forced and p.vid == VID):
            return p.device
    return None


def serial_thread(forced, rx_q, tx_q):
    """Finds the keyboard, does the handshake, forwards messages both ways."""
    ser, buf, connected, last_ping = None, b"", False, 0.0
    while True:
        try:
            if ser is None:
                dev = find_port(forced)
                if dev is None:
                    time.sleep(1)
                    continue
                ser = serial.Serial()
                ser.port, ser.baudrate, ser.timeout = dev, BAUD, 0.05
                ser.dtr = ser.rts = False          # don't reset the board when opening
                ser.open()
                buf, connected, last_ping = b"", False, 0.0
                rx_q.put(("port", dev))
                rx_q.put(("status", "connecting"))
            if find_port(forced) is None:
                raise OSError("unplugged")
            if time.time() - last_ping >= 1:
                ser.write(b"EZMIDI:PING\n" if connected else b"EZMIDI:HELLO\n")
                last_ping = time.time()
            while not tx_q.empty():
                ser.write(tx_q.get_nowait().encode() + b"\n")
            buf += ser.read(256)
            while b"\n" in buf:
                raw, buf = buf.split(b"\n", 1)
                text = raw.decode("utf-8", errors="replace").strip()
                if text == "EZMIDI:OK":
                    if not connected:
                        connected = True
                        rx_q.put(("status", "connected"))
                elif text == "EZMIDI:READY":
                    if connected:
                        connected = False
                        rx_q.put(("status", "connecting"))
                elif text:
                    rx_q.put(parse_line(text) or ("log", text))
        except Exception:
            if ser is not None:
                try:
                    ser.close()
                except Exception:
                    pass
                ser = None
                rx_q.put(("status", "unplugged"))
            time.sleep(1)


# UI
class Card(tk.Frame):
    """A setting card: title and big value."""

    def __init__(self, parent, title):
        super().__init__(parent, bg=CARD, padx=14, pady=10)
        tk.Label(self, text=title, bg=CARD, fg=DIM, font=("TkDefaultFont", 9)).pack()
        self.value = tk.Label(self, text="-", bg=CARD, fg=FG, font=("TkDefaultFont", 22, "bold"), width=5)
        self.value.pack()

    def set(self, text):
        self.value.config(text=text)


class App:
    def __init__(self, root, rx_q, tx_q):
        self.root, self.rx_q, self.tx_q = root, rx_q, tx_q
        self.state = dict(OCT=4, VEL=100, CH=1, TR=0)
        self.held = {}                  # midi note -> True
        self.enc = {41: 0, 42: 0}
        self.down = set()               # pads currently touched
        root.title("EZMIDI")
        root.configure(bg=BG)
        root.geometry("760x680")
        root.resizable(False, False)    # fixed size, no maximize / fullscreen

        # header
        head = tk.Frame(root, bg=BG)
        head.pack(fill="x", padx=16, pady=(14, 6))
        self.dot = tk.Canvas(head, width=14, height=14, bg=BG, highlightthickness=0)
        self.dot.pack(side="left")
        self.dot_id = self.dot.create_oval(2, 2, 12, 12, fill=BAD, outline="")
        self.status = tk.Label(head, text="Not plugged in", bg=BG, fg=FG, font=("TkDefaultFont", 13, "bold"))
        self.status.pack(side="left", padx=8)
        self.port = tk.Label(head, text="", bg=BG, fg=DIM)
        self.port.pack(side="left")

        #settings
        cards = tk.Frame(root, bg=BG)
        cards.pack(fill="x", padx=16, pady=6)
        self.cards = {}
        for i, (key, title) in enumerate([("OCT", "OCTAVE"), ("VEL", "VELOCITY"),
                                          ("CH", "CHANNEL"), ("TR", "TRANSPOSE")]):
            c = Card(cards, title)
            c.grid(row=0, column=i, padx=(0, 8), sticky="nsew")
            cards.columnconfigure(i, weight=1)
            self.cards[key] = c
        self.refresh_cards()

        # notes held
        self.notes = tk.Label(root, text="", bg=BG, fg=ACCENT, font=("TkDefaultFont", 16, "bold"), height=1)
        self.notes.pack(anchor="w", padx=16, pady=(10, 0))

        # keys
        self.piano = tk.Canvas(root, height=170, bg=BG, highlightthickness=0)
        self.piano.pack(fill="x", padx=16, pady=6)
        self.piano.bind("<Configure>", lambda e: self.draw_piano())

        #buttons
        row = tk.Frame(root, bg=BG)
        row.pack(fill="x", padx=16, pady=6)
        self.btn_labels = {}
        for i, (bid, _) in enumerate(BUTTONS):
            name = BUTTON_NAMES[bid].replace("Button ", "Btn ").replace("Encoder", "Enc")
            lab = tk.Label(row, text=name, bg=CARD, fg=FG, width=11, pady=6)
            lab.grid(row=0, column=i, padx=(0, 6), sticky="ew")
            row.columnconfigure(i, weight=1)
            self.btn_labels[bid] = lab
        self.enc_label = tk.Label(root, text="", bg=BG, fg=DIM)
        self.enc_label.pack(anchor="w", padx=16)
        self.show_enc()

        #Serial monitor
        logbar = tk.Frame(root, bg=BG)
        logbar.pack(fill="x", padx=16, pady=(10, 0))
        tk.Label(logbar, text="EVENTS", bg=BG, fg=DIM, font=("TkDefaultFont", 9)).pack(side="left")
        tk.Button(logbar, text="Clear", bg=CARD, fg=FG, relief="flat", command=self.clear_log).pack(side="right")
        self.log = tk.Text(root, height=10, bg=CARD, fg=FG, relief="flat", state="disabled",
                           font=("TkFixedFont", 9), padx=8, pady=6)
        self.log.pack(fill="both", expand=True, padx=16, pady=(4, 16))

        root.after(30, self.poll)

    # functions
    def refresh_cards(self):
        s = self.state
        self.cards["OCT"].set(str(s["OCT"]))
        self.cards["VEL"].set(str(s["VEL"]))
        self.cards["CH"].set(str(s["CH"]))
        self.cards["TR"].set(f"{s['TR']:+d}")

    def show_enc(self):
        self.enc_label.config(text=f"Encoder 1: {self.enc[41]}      Encoder 2: {self.enc[42]}")

    def pad_note(self, pad):
        return max(0, min(127, (self.state["OCT"] + 1) * 12 + pad - 1 + self.state["TR"]))

    def draw_piano(self):
        c = self.piano
        c.delete("all")
        w, h = max(c.winfo_width(), 350), 170
        kw = w / 7
        white, black = [1, 3, 5, 6, 8, 10, 12], {2: 1, 4: 2, 7 + 0: 4, 9: 5, 11: 6}   # pad -> boundary index
        for i, pad in enumerate(white):
            on = pad in self.down
            c.create_rectangle(i * kw + 1, 0, (i + 1) * kw - 1, h, fill=ACCENT if on else WHITE_KEY, outline=BG)
            c.create_text(i * kw + kw / 2, h - 36, text=note_name(self.pad_note(pad)), fill="#222", font=("TkDefaultFont", 11, "bold"))
            c.create_text(i * kw + kw / 2, h - 16, text=f"pad {pad}", fill="#666", font=("TkDefaultFont", 8))
        for pad, edge in black.items():
            on = pad in self.down
            x = edge * kw
            c.create_rectangle(x - kw * 0.3, 0, x + kw * 0.3, h * 0.6, fill=ACCENT if on else BLACK_KEY, outline=BG)
            c.create_text(x, h * 0.6 - 24, text=NOTE_NAMES[(pad - 1) % 12], fill="#fff" if not on else "#222", font=("TkDefaultFont", 9, "bold"))
            c.create_text(x, h * 0.6 - 10, text=str(pad), fill="#999" if not on else "#222", font=("TkDefaultFont", 8))

    def add_log(self, text):
        self.log.config(state="normal")
        self.log.insert("end", f"{time.strftime('%H:%M:%S')}  {text}\n")
        if int(self.log.index("end-1c").split(".")[0]) > 300:
            self.log.delete("1.0", "50.0")
        self.log.see("end")
        self.log.config(state="disabled")

    def clear_log(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")

    def show_notes(self):
        self.notes.config(text="  ".join(note_name(n) for n in sorted(self.held)) or " ")

    # message handling
    def handle(self, kind, data):
        if kind == "port":
            self.port.config(text=data)
        elif kind == "status":
            text, color = {"connected": ("Connected", GOOD), "connecting": ("Plugged in - connecting...", ACCENT),
                           "unplugged": ("Not plugged in", BAD)}[data]
            self.status.config(text=text)
            self.dot.itemconfig(self.dot_id, fill=color)
            if data != "connected":
                self.held.clear(); self.down.clear(); self.show_notes(); self.draw_piano()
                for lab in self.btn_labels.values():
                    lab.config(bg=CARD, fg=FG)
            self.add_log(text)
        elif kind == "state":
            self.state.update(zip(("OCT", "VEL", "CH", "TR"), data))
            self.refresh_cards()
            self.draw_piano()
        elif kind == "input":
            eid, value = data
            if 1 <= eid <= 12:
                (self.down.add if value else self.down.discard)(eid)
                self.draw_piano()
            elif eid in self.btn_labels:
                self.btn_labels[eid].config(bg=ACCENT if value else CARD, fg="#222" if value else FG)
                self.add_log(f"{BUTTON_NAMES[eid]} {'pressed' if value else 'released'}")
            elif eid in self.enc:
                self.add_log(f"Encoder {eid - 40}: {value} ({value - self.enc[eid]:+d})")
                self.enc[eid] = value
                self.show_enc()
        elif kind == "note":
            note, vel = data
            if vel:
                self.held[note] = True
            else:
                self.held.pop(note, None)
            self.show_notes()
            self.add_log(f"Note {note_name(note)} " + (f"on  vel {vel}" if vel else "off"))
        elif kind == "log":
            self.add_log(data)

    def poll(self):
        try:
            while True:
                self.handle(*self.rx_q.get_nowait())
        except queue.Empty:
            pass
        self.root.after(30, self.poll)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", help="serial port, e.g. COM5 (default: auto-detect)")
    args = ap.parse_args()

    rx_q, tx_q = queue.Queue(), queue.Queue()
    threading.Thread(target=serial_thread, args=(args.port, rx_q, tx_q), daemon=True).start()
    root = tk.Tk()
    App(root, rx_q, tx_q)
    root.mainloop()


if __name__ == "__main__":
    main()