#include <Adafruit_NeoPixel.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// --Pins--
const int ledPin = 13;
const int numLeds = 12;

const int buttonPins[8] = {14, 21, 38, 47, 48, 45, 39, 42};
const int buttonIds[8] = {21, 22, 23, 24, 25, 26, 31, 32};

const int enc1A = 15;
const int enc1B = 16;
const int enc2A = 40;
const int enc2B = 41;

const int touchPins[12] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};

// OLED
const int oledSDA = 18;
const int oledSCL = 17;
const int oledAddr = 0x3C;
Adafruit_SSD1306 display(128, 64, &Wire, -1);
bool oledOk = false;

const int ledBrightness = 40;
const float touchSensitivity = 1.15;
const unsigned long clientTimeoutMs = 3000;

// --Variables--
Adafruit_NeoPixel strip(numLeds, ledPin, NEO_GRB + NEO_KHZ800);

int lastButtonState[8];
int lastEnc1A;
int lastEnc2A;
int enc1Count = 0;
int enc2Count = 0;

long touchBaseline[12];
bool touched[12];
int sounding[12];

int octave = 4;
int velocity = 100;
int channel = 1;
int transposeSemis = 0;

bool clientConnected = false;
bool screenDirty = true;
unsigned long lastClientMs = 0;
unsigned long lastReadyMs = 0;
unsigned long lastBlinkMs = 0;
bool blinkOn = true;
String rxLine;

const char* noteNames[12] = {"C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"};

//--Screen--
void drawMainScreen() {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);

  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print("EZMIDI");
  display.setCursor(80, 0);
  display.print("CH ");
  display.print(channel);

  display.setTextSize(2);
  display.setCursor(0, 11);
  display.print("OCT ");
  display.print(octave);
  display.setCursor(76, 11);
  display.print("V");
  display.print(velocity);

  display.setTextSize(1);
  display.setCursor(0, 31);
  display.print("Transpose ");
  if (transposeSemis > 0) display.print("+");
  display.print(transposeSemis);
  display.print(" st");

  display.drawLine(0, 42, 127, 42, SSD1306_WHITE);

// only 5 held notes for now till I figure out power draw
  String held = "";
  int count = 0;
  for (int i = 0; i < 12; i++) {
    if (touched[i]) {
      if (count < 5) {
        if (count > 0) held += " ";
        held += noteNames[sounding[i] % 12];
        held += String(sounding[i] / 12 - 1);
      }
      count++;
    }
  }
  if (count > 5) held += " +" + String(count - 5);

  display.setCursor(0, 47);
  if (count == 0) display.print("Play something...");
  else display.print(held);

  display.display();
}

void drawWaitingScreen() {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(2);
  display.setCursor(0, 0);
  display.println("EZMIDI");
  if (blinkOn) {
    display.setTextSize(1);
    display.setCursor(0, 28);
    display.println("Connecting to");
    display.setCursor(0, 42);
    display.println("client...");
  }
  display.display();
}

// client linker
void sendEvent(int id, long value) {
  if (!clientConnected) return;
  Serial.print("EV:");
  Serial.print(id);
  Serial.print(":");
  Serial.println(value);
}

void sendNote(int note, int vel) {
  if (!clientConnected) return;
  Serial.print("NT:");
  Serial.print(note);
  Serial.print(":");
  Serial.println(vel);
}

void sendState() {
  if (!clientConnected) return;
  Serial.print("ST:");
  Serial.print(octave);
  Serial.print(":");
  Serial.print(velocity);
  Serial.print(":");
  Serial.print(channel);
  Serial.print(":");
  Serial.println(transposeSemis);
}

void stateChanged() {
  screenDirty = true;
  sendState();
}

void setClientConnected(bool state) {
  if (state == clientConnected) return;
  clientConnected = state;
  if (state) sendState();
  screenDirty = true;
}

// Client commands
void handleCommand(String cmd) {
  if (!cmd.startsWith("SET:")) return;
  int p = cmd.indexOf(':', 4);
  if (p < 0) return;
  String key = cmd.substring(4, p);
  int val = cmd.substring(p + 1).toInt();

  if (key == "OCT") octave = constrain(val, 0, 8);
  else if (key == "VEL") velocity = constrain(val, 1, 127);
  else if (key == "CH") channel = constrain(val, 1, 16);
  else if (key == "TR") transposeSemis = constrain(val, -12, 12);
  else return;
  stateChanged();
}

void handleSerialIn() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      rxLine.trim();
      if (rxLine == "EZMIDI:HELLO" || rxLine == "EZMIDI:PING") {
        lastClientMs = millis();
        setClientConnected(true);
        Serial.println("EZMIDI:OK");
      } else if (clientConnected) {
        lastClientMs = millis();
        handleCommand(rxLine);
      }
      rxLine = "";
    } else if (c != '\r' && rxLine.length() < 40) {
      rxLine += c;
    }
  }
}

void updateScreen() {
  unsigned long now = millis();

  if (clientConnected && now - lastClientMs > clientTimeoutMs) {
    setClientConnected(false);
  }

  if (!clientConnected) {

    if (now - lastReadyMs >= 1000) {
      lastReadyMs = now;
      Serial.println("EZMIDI:READY");
    }

    if (now - lastBlinkMs >= 500) {
      lastBlinkMs = now;
      blinkOn = !blinkOn;
      screenDirty = true;
    }
  }

  if (screenDirty && oledOk) {
    screenDirty = false;
    if (clientConnected) drawMainScreen();
    else drawWaitingScreen();
  }
}

//--Inputs--
void onButton(int i) {
  if (i == 0) transposeSemis = constrain(transposeSemis - 1, -12, 12);
  else if (i == 1) transposeSemis = constrain(transposeSemis + 1, -12, 12);
  else if (i == 2) channel = constrain(channel - 1, 1, 16);
  else if (i == 3) channel = constrain(channel + 1, 1, 16);
  else if (i == 6) octave = 4;
  else if (i == 7) velocity = 100;
  else return;
  stateChanged();
}

void onEncoder(int which, int dir) {
  if (which == 1) octave = constrain(octave + dir, 0, 8);
  else velocity = constrain(velocity + dir * 5, 1, 127);
  stateChanged();
}

void onPad(int i, bool isTouched) {
  if (isTouched) {
    sounding[i] = constrain((octave + 1) * 12 + i + transposeSemis, 0, 127);
    sendNote(sounding[i], velocity);
  } else {
    sendNote(sounding[i], 0);
  }
  screenDirty = true;
}

void setup() {
  Serial.begin(115200);
  Serial.setTxTimeoutMs(0);
  delay(1000);

//Turn on the screen
  Wire.begin(oledSDA, oledSCL);
  Wire.setClock(400000);
  oledOk = display.begin(SSD1306_SWITCHCAPVCC, oledAddr);
  if (oledOk) {
    display.clearDisplay();
    display.setTextColor(SSD1306_WHITE);
    display.setTextSize(2);
    display.setCursor(0, 0);
    display.println("EZMIDI");
    display.setTextSize(1);
    display.setCursor(0, 28);
    display.println("Booting...");
    display.setCursor(0, 42);
    display.println("Do not touch!");
    display.display();
  }

  // Buttons
  for (int i = 0; i < 8; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
    lastButtonState[i] = HIGH;
  }

  // Encoders
  pinMode(enc1A, INPUT_PULLUP);
  pinMode(enc1B, INPUT_PULLUP);
  pinMode(enc2A, INPUT_PULLUP);
  pinMode(enc2B, INPUT_PULLUP);
  lastEnc1A = digitalRead(enc1A);
  lastEnc2A = digitalRead(enc2A);

  // Start tests
  strip.begin();
  strip.setBrightness(ledBrightness);
  for (int i = 0; i < numLeds; i++) {
    strip.setPixelColor(i, strip.Color(0, 0, 255));
    strip.show();
    delay(50);
  }
  delay(200);
  strip.clear();
  strip.show();

  // Calibrate
  for (int i = 0; i < 12; i++) {
    long total = 0;
    for (int n = 0; n < 16; n++) {
      total = total + touchRead(touchPins[i]);
      delay(5);
    }
    touchBaseline[i] = total / 16;
    touched[i] = false;
    sounding[i] = 0;
  }
}

void loop() {
  handleSerialIn();
  updateScreen();

  // Buttons
  for (int i = 0; i < 8; i++) {
    int state = digitalRead(buttonPins[i]);
    if (state != lastButtonState[i]) {
      lastButtonState[i] = state;
      sendEvent(buttonIds[i], state == LOW ? 1 : 0);
      if (state == LOW) onButton(i);
      delay(10);
    }
  }

  // Encoder 1
  int a1 = digitalRead(enc1A);
  if (a1 != lastEnc1A && a1 == LOW) {
    int dir = (digitalRead(enc1B) == HIGH) ? 1 : -1;
    enc1Count += dir;
    sendEvent(41, enc1Count);
    onEncoder(1, dir);
  }
  lastEnc1A = a1;

  // Encoder 2
  int a2 = digitalRead(enc2A);
  if (a2 != lastEnc2A && a2 == LOW) {
    int dir = (digitalRead(enc2B) == HIGH) ? 1 : -1;
    enc2Count += dir;
    sendEvent(42, enc2Count);
    onEncoder(2, dir);
  }
  lastEnc2A = a2;

  // Touch pads
  bool ledsChanged = false;
  for (int i = 0; i < 12; i++) {
    long reading = touchRead(touchPins[i]);
    bool isTouched = (reading > touchBaseline[i] * touchSensitivity);
    if (isTouched != touched[i]) {
      touched[i] = isTouched;
      sendEvent(i + 1, isTouched ? 1 : 0);
      onPad(i, isTouched);
      strip.setPixelColor(i, isTouched ? strip.Color(255, 255, 255) : 0);
      ledsChanged = true;
    }
  }
  if (ledsChanged) {
    strip.show();
  }

  delay(2);
}