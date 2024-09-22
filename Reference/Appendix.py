"""
#----------------------------------------APPENDIX----------------------------------------#
FUNCTIONALITY IN USE:
	Switch Action Types Supported:
		- CC Toggle: Basically a button, turn on and turn off
		- CC Hold: Basically a button, hold to turn on, turns off on release
		- Reset Encoder Value: When Encoder Pressed, Value is reset to default value (50 with detent, 0 without)
			How It Works:
				1. On a Control Change message sent to Channel 1 (Encoder Press), a value of 127 (0x7F) is sent.
				2. While this message is active, the value of data2 in Channel 0 is set to 0.
				3. On Release of the button, Channel 1 reverts to a value of 0.
		- Shift Encoder Toggle: Basically two encoders in one, press the encoder to change between them.
			How It Works:
				1. Encoder is on Channel 0 by default (Control Changes sent via 0xB0.
				2. A Control Change message of 127 is sent to Channel 1 (So the midiID is 0xB1, data2 is 0x7F)
				3. This Changes the Encoder to Channel 4, where the secondary set of encoder values are (0xB4)
				4. Sending another control change message to Channel 1 will send an OFF signal (0x00) to the encoder, reverting back to Channel 0.
	Encoder MIDI Types Supported:
		- CC: Sends a CC value from 0-127 to DAW
		- ENC 3FH/41H: Sends continuous value w/o keeping track of value (by default this does not work in FL Studio).

USES:
	BI-DIRECTIONAL FEEDBACK - WORKING
		- Editing a value on MIDI Fighter Twister changes it on FL
		- Editing a value in FL changes it on the lined encoder
		- During playback, if automation is present on linked encoder, indicators will light up accordingly in RealTime
		- When Recording during playback, can overwrite indicator automation via overdubbing.
	ENDLESS ENCODERS
		- Endless Encoder functionality missing from Base MIDI Fighter Twister.
		- When a value of 63 is given, linked control is reduced by 1.
		- When a value of 65 is given, linked control is increased by 1.
	SMART SWITCH BETWEEN PLUGINS/GENERATORS
		- When a GENERATOR/EFFECT is FOCUSED (window clicked on) in FL Studio, Any Linked Controls on the Midi Fighter Twister are Updated to those on the focused Generator/Effect.
		- When Updating Midi Fighter Twister Indicators, last focused plugin is used.
		- MAYBE? Change Color Scheme of all RGBs to preset one when focused on new effect/generator
	OTHER ENHANCEMENTS - WORKING
		- When an encoder is linked to a value, the RGB LED is visible and Indicator Brightness is maxed. Unlinked encoders' LEDs are off and indicator brightness dimmed.

CHANNEL DATA:
	CHANNEL 0: INDICATOR AMOUNT (0 - 127)
	CHANNEL 1: RGB COLOR, ENDOCDER SHIFTER
		- 0 = OFF State, 127 = ON State, any value between is considered ON, but will have a different color based on MIDI Fighter Twister Manual, p. 4: https://drive.google.com/file/d/0B-QvIds_FsH3Z0ZLT041VnZfOTA/view?resourcekey=0-fgp-m9PFslsMcR3SD5bJZQ
		- A class of basic colors is present in the code
				Ex: SendMIDI(midi.MIDI_CONTROLCHANGE, 1, 15, COLOR.ORANGE) #Change Encoder 15 to Orange
	CHANNEL 2: LED ANIMATION
		Animation CC Values:
			- 0, 9, 48 = No Animation; Static
			- 1 - 8 = RGB Flash
			- 10 - 16 = RGB Pulse
			- 17 - 47 = RGB Brightness (17 = Off, 32 = Mid, 47 = Max)
			- 49 - 56 = Indicator Flash
			- 57 - 64 = Indicator Pulse
			- 65 - 95 = Indicator Brightness (65 = Off, 80 = Mid, 95 = Max)
			- 127 = Rainbow Cycle
	CHANNEL 3: BANK SELECT
	CHANNEL 4: SECONDARY (SHIFT) ENCODER INDICATOR AMOUNT (0 - 127)
	CHANNEL 5: 2ND LED ANIMATION
	CHANNEL 6: 2ND INDICATOR AMOUNT
	CHANNEL 8:

GENERAL INFORMATION:
	CONTROL CHANGE MESSAGES
		- 176 = B0 = Base Control Change Byte
		- B0 + Channel = any other channel
	SHIFT ENCODERS:
		- SHIFT CC TYPE = B0 (Base Channel), B4 (Shift Channel)
		- B1 = Default CC Channel that activates secondary channel
	HANDLING MIDI MESSAGES
		- When a MIDI message is not handled, it doesn't control anything in FL/is not told to do anything in FL by the script/There is some task that it needs to do before it can be considered 'handled.'
			- Using it will do the default ish that FL would make it do w/o the script.
			- Ex: Linking parameters to encoders, notes and their values, etc.
		- Only handle parts of the device (channels, CCs, etc) when there is something specific that you want the control to do (change to this color when this happens, send this data back to the device when this happens, etc.).
			- Some Channels and Settings (Channel 3, Reset Encoder Val) don't need to be handled b/c they more or less do things exclusively to the device itself and nothing to the DAW.
	SETTING TWO ANIMATIONS:
		- You can set two animataons via the secondary LED animation channel (2 & 5)
	DEVICE CC VALUES
		- CC Numbers on Device: 0-63 (64 different CCs)
			- Controls With Side button functionality: 0, 1, 2, 3, 8.
	PLUGINID COMPUTATION (EFFECT):
		- Base 10: (track << 6 + slot) << 16
		- Base 16: (track << 0x06 + slot) << 0x10
	EVENTID COMPUTATION:
		- Base 10: (((0x2000 + 0x40 * track) + slot) << 0x10) + 0x8000 + param
		- Base 16: (((8192 + 64 * track) + slot) << 16) + 32768 + param
	CONTROLID COMPUTATION:
		- Base 10: (8388608 + 65536 * channel) + ctrl
		- Base 16: (0x800000 + 0x10000 * channel) + ctrl
	FL TERM GLOSSARY:
		- eventData = input from the device
		- data1 = device cc
		- data2 = device cc amount
		- midiId = midi codes (see midi.py)
		- midiChan = midi channel
		- status = midiId + midiChan
	FL REFRESH FLAGS:
		- 0x20 = DAW Unload Component
		- 0x127 = DAW Load Component, Focus Plugin
		- 0x1000 = Plugin Parameter Change
		- 0x1200 = Linked Control Change
		- 0x4127 = New Plugin

TENTATIVE MIDI FIGHTER TWISTER BANK SETUP:
	BANK 1: Effects
		- Bottom Right: Dry/Wet Mix
	BANK 2: Generator
	BANK 3: Misc. FL
	BANK 4: Free
"""
"""
# 0 = 1st Encoder Indicator Amount
# 4 = 2nd Encoder Indicator Amount

# 1 = Encoder LED Status (On, Off, Color)

# 2 = Encoder LED Animations (Brightness, Gate, Pulse)
# 5 = Indicator Animations (Brightness, Gate, Pulse)


"""