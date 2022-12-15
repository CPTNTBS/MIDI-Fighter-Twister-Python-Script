# **MIDI-Fighter-Twister-Python-Script**
**An FL Studio Script for the MIDI Fighter Twister**

This script is designed to add more general functionality to the device.

**FEATURES**
**BASIC ENHANCEMENTS - WORKING**
- When an encoder is linked to a value, the RGB LED is visible and indicator brightness is maxed. Unlinked encoders' LEDs are off and indicator brightness dimmed and reset to 0 if modified.

**BI-DIRECTIONAL FEEDBACK - WORKING**
- By default, changing a parameter via the MIDI Fighter Twister will change it on FL Studio, but modifying that same parameter via the FL Studio window will desync the indicator on the MIDI Fighter Twister.
- Using this script, the above problem is fixed: editing a value linked to an encoder in FL Studio will also change the linked encoder's indicator on the physical device.
- This fix also adds new functionality to the device. For example, if a linked encoder's parameter is automated, then the indicators will light up accordingly during playback or jogging through audio.
- Most of this functionality only works for channel 0 (the white indicators).
- Physical feedback can appear choppy as the implementation runs through multiple linked controls in order to find the correct one. Until there is a way to select individual controlIDs on a MIDI device, this implementation seems best.

**SMART SWITCH BETWEEN PLUGINS/GENERATORS - SHOULD WORK**
- When a GENERATOR/EFFECT is FOCUSED in FL Studio, linked controls on the Twister are updated to those on the focused Generator/Effect.
- Useful for global links, where one encoder can have multiple links to multiple plugins.
- When Updating Midi Fighter Twister Indicators, last focused plugin is used.

**TO-DO**
- INCREMENTAL/DECREMENTAL ENCODERS
	- Some Encoder functionality broken in FL Studio for MIDI Fighter Twister.
	- The ENC 3FH/41H mode is a setting for any encoder on the device. 
	- With it, the encoder is suppose to send an incremental value of +1 or -1 to the linked control, rather than keeping track of the specific value.
	- Unfortuantely, using the ENC 3FH/41H mode in FL Studio will only send a static value of 65 or 63 to FL Studio. This script seeks to fix that.
		- When a value of 63 is given, linked control parameter should be reduced by 1.
		- When a value of 65 is given, linked control parameter should be increased by 1.
- (Maybe) Change Color Scheme of all RGBs to presets when focused on new effect/generator.
- Some projects can't load when this plugin is enabled by default. Disabling the script before loading the project and enabling it afterwards fixes this. Should probalby fix that.
- Other Features by request.
