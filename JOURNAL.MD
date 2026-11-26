---
title: "Axiom MIDI"
github: "https://github.com/PieSquared/Axiom-Midi/tree/main"
description: "Advanced MIDI keyboard powered by an esp 32. it has 2 knobs, a 6 key sound pad, and a 0.96inch screen. It has 12 keys to form one octave and each key has an LED on it. I am building it because I wanted to challenge myself with a bigger project"
created_at: "2026-11-21"
total_time: "20h 36m"
---

\---

title: "Axiom MIDI"

github: ""

description: "Advanced MIDI keyboard powered by an esp 32. it has 2 knobs, a 6 key sound pad, and a 0.96inch screen. It has 12 keys to form one octave"

created\_at: "2026-11-21"

total\_time: "20h 36m"

\---



\# November 21, 2026: Planning the parts



\# November 20.2026:Planning the PCB



\## What I did today



I lowk forgot to make the project so I’m doing it rn



I wanted to make something cool so I checked the guides and saw a midi keyboard. It looked too simple for me so I decided to upgrade it. I thought of the name right now and randomly thought of Axiom, I thought the name has a ring to it and sounded professional but I might change it. Anyway, I looked at the tutorial and it recommended me two microcontrollers but they did not have many touch capable IOs on them so I looked at a few others. The one I chose was a ESP32-S3. I was choosing between doing it the easy way, which was using a dev kit and sticking some pin connectors in the board, but that made the board way to big. So I decided to do the hard way which was sticking on only the micro controller and somehow routing everything. This was not as hard as I thought it would be because I looked at how the dev kit worked and kind of copied it from there. This makes it have a small form factor and maybe I could add more stuff, which led me to what methods of input I wanted. In the tutorial there are Rotary encoders and I realized I should probably use one because of switching octaves on the piano. I also wanted a sound board so I decided to use a few keyboard switches, I did not want to use the keycaps in the tutorial so decided to just use those thin keycaps you see in office computers. I also wanted another knob for stuff like volume and switching pitches stuff ect. And because there are buttons inside the knob I could program it to do switching. I decided not to get a slider because it wqs expensive according to the guide. I also had a little LCD laying around so I decided to use it for showing stuff like the octave you were on. I realized we needed some way to change the sound board sounds so I think I am going to make a software for it. so that was it for planning the project. This def took the longest because I was trying to choose between what to use and looking at every possible design while staying within my budget. Not using a dev kit might give me the chance to increase my project tier so I might be able to get PCBA because soldering on a controller is straight impossible, and I might be able to add some size to the pcb snd make it over 10cm which I probably need to. I shut off my pc and forgot to take screenshots so I’m going to attach photos of how I figured out what I should get. I found stuff from Aliexpress and JLCPCB because they have a parts list for PCBA







\# Tomorrow



Tomorrow I’m going to start making the schematic and maybe the PCB. I also need to think of the layout and design



\*\*Total time spent: 6h \*\*



!\[](https://fabricate.hackclub-assets.com/d1cfe81ee1c26f31f389f96d70684e678a0d6f047ec1da76c95c870af651b42a/image-jpeg/IMG\_6471.jpeg)



\*\*Total time spent: 36m\*\*



\# November 22, 2026: Making Design and schematicing



\# November 22, 2026: Making Design and Schematicing



\## Today



HELLO, today I made my Very cool design and made like half my schematic. For my design I decided to make my board 100x150 which isnt 100x100 but you will understand why in a bit. I wanted this to be a 2 Handed keyboard so I did not want to hold back so I increased it just a bit (Size might change). But doesnt this have a risk of exceeding my budget, well yes and no. My budget should be 50 dollars but because I am not using a devboard it should be complex enough to increase it to 125 which is way over what i need (or should be). Anyway I wanted it to be colorful so i added side LEDs so when a key is pressed it lights it up so its cool. I also found these cool transparent keys on aliexpress so I might use thoese. I designed a simple logo on the Bottom right middle, Its just AXIOM without the horizontal line in the A. After I finished the design I started making the schematic. I got all my footprints, models, and symbols from easyeda and turned them into Kicad with the EasyEDA2KiCad tool, and started connnecting everything. It was tricky at first because I did not know how to use a bare controller but I just looked online for some tutorials and got it (My symbol for the microcontroller looks confusing but it just says what each of the pins can be used for lol). I didnt finish adding the LEDs because idk how they work but i promise i will tomorrow and start making the PCB.



\# Tomorrow?



Start making the PCB



\*\*Total time spent: 4.5 hours\*\* - obv excluding video tutorials





!\[](https://fabricate.hackclub-assets.com/3da83c91b3dcd7970234512774f7fe64bd89f829ef3bd1f39fe054e60393072a/image-png/image.png)



!\[](https://fabricate.hackclub-assets.com/04336359e4ae4a0d342849fda7935b8a92dd1b7891827d6c36f3fc5fb522b090/image-jpeg/IMG\_6474.jpeg)



\*\*Total time spent: 4h 30m\*\*



\# November 23, 2026: Finish Schematic and Placing parts on PCB



\# November 23, 2026



\## Today



Today was pretty busy, I finished up the schematic and added some LEDs, I found good ones on JLCPCB, instead of mouting them on the side I figured I just cut holes thorugh because the LED I am using side emitting ones. This part itself was pretty simple because I just copied and pasted a bunch of parts. When I got to the PCB part i realized how much I had to do. I wanted to keep it compact but there were alot of tiny parts, tomorrow i might move tiny parts like the capacitors to the back because theres like nothing there. The via routes might be a little messy as u can see in the screenshot but I am going to just take advantage of the B.Cu layer so it will be fine I think. Im thinking wether I should add mouting holes to it to keep it still, but i might make it so The PCB just goes in the case and the cover snaps so I might remove them from the PCB. The PCB overall looks pretty nice I think, I might add some more art if there is space, I just added the Hack Club logo and my logo to keep it simple right now in case I gotta move something. Im a little worred on the screen part, if It is too short I might just use jumper cables to put it where I want it to on the case so.



\## Tomorrow



Route PCB and hope for the best Ig



\*\*Total time spent: 5 hours\*\*



!\[](https://fabricate.hackclub-assets.com/c94811a0007942ed343173405d733a6cb723b93b8f94982624a56bbd40ec36c7/image-png/image.png)

!\[](https://fabricate.hackclub-assets.com/950b5f582a84066ae38cd3db9357b1c1d619fcd7b63bb5f8e8e2a2f033c7ab8f/image-png/image.png)

!\[](https://fabricate.hackclub-assets.com/7a0b0ff6cdea21fcfba322b6cebc3845149195f46ce283c4f9de8b5fcaaf0b11/image-png/image.png)



\*\*Total time spent: 5h\*\*



\# November 23, 2026: Finding Models and Routing PCB



\# November 24,2026



\## Today



Today I just found models for my PCB and started routing it, I am having quite a hard time with the routing because I have little space and there is a lot of things to route, I might move some stuff around or add more area to the PCB so it is easier to work with but I am kind of worried about the price of things. I have PCBA prices to worry about, AliExpress orders and case orders. But I also moved some small parts like capacitors and resistors to the back layer. I think this will be right below the 125 mark, hopefully lower. Anyway for routing the PCB, I found switching a lot between B.Cu and F.Cu to make it a lot easier, the KiCad path finding thing is also pretty helpful for this but it can be a bit laggy, I had my client crash a couple times but I always have it saved. This project might be my hardest one but most put together one I would say, the routing job is kind of bad and might add a bit of latency because of the corners but i will fix that after I am done the hard parts of it.



\## Tomorrow



Finish PCB and work on FW or the case



\*\*Total time spent: 4h\*\*



!\[](https://fabricate.hackclub-assets.com/162aafa93af9d9ff5c354d134f00fa81e533e610fbfe44208012a30f32950fc2/image-png/image.png)



!\[](https://fabricate.hackclub-assets.com/8653582691f19ba2c9bed52e5dec44c09a1a2b4bafe6408fd241e965e940743a/image-png/image.png)

!\[](https://fabricate.hackclub-assets.com/fe49af8e12056d8fccabaa6e86cabbd898b2f0aac9f9689066d72f58952e12a2/image-png/image.png)



\*\*Total time spent: 4h\*\*



\# November 24, 2026: Routed PCB and Finished Firmware/Client



\# November 24,2026: Routed PCB and Finished Firmware/Client



\## Today



Today I basically just finished routing and made the firmware. Along side the firmware I made a client and I plan to make features like changing what the Buttons do and what it looks like. But for now I just added the basic stuff like showing the keys. In the firmware, I added a calibration thing and tests so I can make sure all the parts are working correctly. There is nothing really to explain here but I had to route power and gnd which was annoying because it was busy everywhere, I fixed all the errors and warnings except silk screen but thats about it because i have a test to study for.



\## Tomorrow



Make case



\*\*Total Time spent: 3h\*\*

!\[](https://fabricate.hackclub-assets.com/25fb794e1caea3a36daf8480817beed9e77c57b975e747b25c28ddf1e24696ef/image-png/image.png)



!\[](https://fabricate.hackclub-assets.com/878cad55e9e44d2c8a3bf375b0f16122274a284d7a4933b09f44082a8e509eb7/image-png/image.png)



!\[](https://fabricate.hackclub-assets.com/2b50cfd2e5678829bb5693b5ef5b109e1aaac6ba7c50c6a016a25d38f8c935c1/image-png/image.png)



!\[](https://fabricate.hackclub-assets.com/628888ef76efcc7b48f85fb957fb66c61889034b968aa5548bb363770fa25acb/image-png/image.png)



\*\*Total time spent: 3h\*\*



\# November 25, 2026: Made the Case



\# November 25, 2026: Made the case



\## Today



I did not do much today, I made a very nice case that's easy to assemble, If i knew more of the measurements I could have probably made it better but I am pretty happy with how it looks. I wanted to make it look like the professional midi keyboards people have so I added some rounded corners and my logo thingy on it. I haven't decided if I am going to print it with acrylic or get it from print legion but I probably will need to do it from printing legion because it is expensive. After this journal I am going to set up the GitHub and submit my project to fabricate so hopefully it gets accepted.



\*\*Total time spent: 3.5h\*\*



!\[](https://fabricate.hackclub-assets.com/3c4a77dcb81ff44a55d83b1aa27ad544391c05a146456e9c4329e1bbe7b32f67/image-png/image.png)



\*\*Total time spent: 3h 30m\*\*

# November 21, 2026: Planning the parts
<!-- fabricate:entry 3558 -->

## November 20.2026:Planning the PCB

## What I did today

I lowk forgot to make the project so I’m doing it rn

I wanted to make something cool so I checked the guides and saw a midi keyboard. It looked too simple for me so I decided to upgrade it. I thought of the name right now and randomly thought of Axiom, I thought the name has a ring to it and sounded professional but I might change it. Anyway, I looked at the tutorial and it recommended me two microcontrollers but they did not have many touch capable IOs on them so I looked at a few others. The one I chose was a ESP32-S3. I was choosing between doing it the easy way, which was using a dev kit and sticking some pin connectors in the board, but that made the board way to big. So I decided to do the hard way which was sticking on only the micro controller and somehow routing everything. This was not as hard as I thought it would be because I looked at how the dev kit worked and kind of copied it from there. This makes it have a small form factor and maybe I could add more stuff, which led me to what methods of input I wanted. In the tutorial there are Rotary encoders and I realized I should probably use one because of switching octaves on the piano. I also wanted a sound board so I decided to use a few keyboard switches, I did not want to use the keycaps in the tutorial so decided to just use those thin keycaps you see in office computers. I also wanted another knob for stuff like volume and switching pitches stuff ect. And because there are buttons inside the knob I could program it to do switching. I decided not to get a slider because it wqs expensive according to the guide. I also had a little LCD laying around so I decided to use it for showing stuff like the octave you were on. I realized we needed some way to change the sound board sounds so I think I am going to make a software for it. so that was it for planning the project. This def took the longest because I was trying to choose between what to use and looking at every possible design while staying within my budget. Not using a dev kit might give me the chance to increase my project tier so I might be able to get PCBA because soldering on a controller is straight impossible, and I might be able to add some size to the pcb snd make it over 10cm which I probably need to. I shut off my pc and forgot to take screenshots so I’m going to attach photos of how I figured out what I should get. I found stuff from Aliexpress and JLCPCB because they have a parts list for PCBA



## Tomorrow

Tomorrow I’m going to start making the schematic and maybe the PCB. I also need to think of the layout and design


![](https://fabricate.hackclub-assets.com/d1cfe81ee1c26f31f389f96d70684e678a0d6f047ec1da76c95c870af651b42a/image-jpeg/IMG_6471.jpeg)

**Total time spent: 36m**

# November 22, 2026: Making Design and schematicing
<!-- fabricate:entry 3685 -->

## November 22, 2026: Making Design and Schematicing

## Today

HELLO, today I made my Very cool design and made like half my schematic. For my design I decided to make my board 100x150 which isnt 100x100 but you will understand why in a bit. I wanted this to be a 2 Handed keyboard so I did not want to hold back so I increased it just a bit (Size might change). But doesnt this have a risk of exceeding my budget, well yes and no. My budget should be 50 dollars but because I am not using a devboard it should be complex enough to increase it to 125 which is way over what i need (or should be). Anyway I wanted it to be colorful so i added side LEDs so when a key is pressed it lights it up so its cool. I also found these cool transparent keys on aliexpress so I might use thoese. I designed a simple logo on the Bottom right middle, Its just AXIOM without the horizontal line in the A. After I finished the design I started making the schematic. I got all my footprints, models, and symbols from easyeda and turned them into Kicad with the EasyEDA2KiCad tool, and started connnecting everything. It was tricky at first because I did not know how to use a bare controller but I just looked online for some tutorials and got it (My symbol for the microcontroller looks confusing but it just says what each of the pins can be used for lol). I didnt finish adding the LEDs because idk how they work but i promise i will tomorrow and start making the PCB.

## Tomorrow?

Start making the PCB

**Total time spent: 4.5 hours** - obv excluding video tutorials


![](https://fabricate.hackclub-assets.com/3da83c91b3dcd7970234512774f7fe64bd89f829ef3bd1f39fe054e60393072a/image-png/image.png)

![](https://fabricate.hackclub-assets.com/04336359e4ae4a0d342849fda7935b8a92dd1b7891827d6c36f3fc5fb522b090/image-jpeg/IMG_6474.jpeg)

**Total time spent: 4h 30m**

# November 23, 2026: Finish Schematic and Placing parts on PCB
<!-- fabricate:entry 3752 -->

## November 23, 2026

## Today

Today was pretty busy, I finished up the schematic and added some LEDs, I found good ones on JLCPCB, instead of mouting them on the side I figured I just cut holes thorugh because the LED I am using side emitting ones. This part itself was pretty simple because I just copied and pasted a bunch of parts. When I got to the PCB part i realized how much I had to do. I wanted to keep it compact but there were alot of tiny parts, tomorrow i might move tiny parts like the capacitors to the back because theres like nothing there. The via routes might be a little messy as u can see in the screenshot but I am going to just take advantage of the B.Cu layer so it will be fine I think. Im thinking wether I should add mouting holes to it to keep it still, but i might make it so The PCB just goes in the case and the cover snaps so I might remove them from the PCB. The PCB overall looks pretty nice I think, I might add some more art if there is space, I just added the Hack Club logo and my logo to keep it simple right now in case I gotta move something. Im a little worred on the screen part, if It is too short I might just use jumper cables to put it where I want it to on the case so.

## Tomorrow

Route PCB and hope for the best Ig


![](https://fabricate.hackclub-assets.com/c94811a0007942ed343173405d733a6cb723b93b8f94982624a56bbd40ec36c7/image-png/image.png)
![](https://fabricate.hackclub-assets.com/950b5f582a84066ae38cd3db9357b1c1d619fcd7b63bb5f8e8e2a2f033c7ab8f/image-png/image.png)
![](https://fabricate.hackclub-assets.com/7a0b0ff6cdea21fcfba322b6cebc3845149195f46ce283c4f9de8b5fcaaf0b11/image-png/image.png)

**Total time spent: 5h**

# November 23, 2026 (entry 2): Finding Models and Routing PCB
<!-- fabricate:entry 3816 -->

## November 24,2026

## Today

Today I just found models for my PCB and started routing it, I am having quite a hard time with the routing because I have little space and there is a lot of things to route, I might move some stuff around or add more area to the PCB so it is easier to work with but I am kind of worried about the price of things. I have PCBA prices to worry about, AliExpress orders and case orders. But I also moved some small parts like capacitors and resistors to the back layer. I think this will be right below the 125 mark, hopefully lower. Anyway for routing the PCB, I found switching a lot between B.Cu and F.Cu to make it a lot easier, the KiCad path finding thing is also pretty helpful for this but it can be a bit laggy, I had my client crash a couple times but I always have it saved. This project might be my hardest one but most put together one I would say, the routing job is kind of bad and might add a bit of latency because of the corners but i will fix that after I am done the hard parts of it.

## Tomorrow

Finish PCB and work on FW or the case


![](https://fabricate.hackclub-assets.com/162aafa93af9d9ff5c354d134f00fa81e533e610fbfe44208012a30f32950fc2/image-png/image.png)

![](https://fabricate.hackclub-assets.com/8653582691f19ba2c9bed52e5dec44c09a1a2b4bafe6408fd241e965e940743a/image-png/image.png)
![](https://fabricate.hackclub-assets.com/fe49af8e12056d8fccabaa6e86cabbd898b2f0aac9f9689066d72f58952e12a2/image-png/image.png)

**Total time spent: 4h**

# November 24, 2026: Routed PCB and Finished Firmware/Client
<!-- fabricate:entry 3868 -->

## November 24,2026: Routed PCB and Finished Firmware/Client

## Today

Today I basically just finished routing and made the firmware. Along side the firmware I made a client and I plan to make features like changing what the Buttons do and what it looks like. But for now I just added the basic stuff like showing the keys. In the firmware, I added a calibration thing and tests so I can make sure all the parts are working correctly. There is nothing really to explain here but I had to route power and gnd which was annoying because it was busy everywhere, I fixed all the errors and warnings except silk screen but thats about it because i have a test to study for.

## Tomorrow

Make case

![](https://fabricate.hackclub-assets.com/25fb794e1caea3a36daf8480817beed9e77c57b975e747b25c28ddf1e24696ef/image-png/image.png)

![](https://fabricate.hackclub-assets.com/878cad55e9e44d2c8a3bf375b0f16122274a284d7a4933b09f44082a8e509eb7/image-png/image.png)

![](https://fabricate.hackclub-assets.com/2b50cfd2e5678829bb5693b5ef5b109e1aaac6ba7c50c6a016a25d38f8c935c1/image-png/image.png)

![](https://fabricate.hackclub-assets.com/628888ef76efcc7b48f85fb957fb66c61889034b968aa5548bb363770fa25acb/image-png/image.png)

**Total time spent: 3h**

# November 25, 2026: Made the Case
<!-- fabricate:entry 3923 -->

## November 25, 2026: Made the case

## Today

I did not do much today, I made a very nice case that's easy to assemble, If i knew more of the measurements I could have probably made it better but I am pretty happy with how it looks. I wanted to make it look like the professional midi keyboards people have so I added some rounded corners and my logo thingy on it. I haven't decided if I am going to print it with acrylic or get it from print legion but I probably will need to do it from printing legion because it is expensive. After this journal I am going to set up the GitHub and submit my project to fabricate so hopefully it gets accepted.


![](https://fabricate.hackclub-assets.com/3c4a77dcb81ff44a55d83b1aa27ad544391c05a146456e9c4329e1bbe7b32f67/image-png/image.png)

**Total time spent: 3h 30m**
