# **MIDI-Fighter-Twister-Python-Script**
**An FL Studio Script for the MIDI Fighter Twister**

### **FEATURES**
**BASIC ENHANCEMENTS - WORKING**
- When an encoder is linked to a value, the RGB LED is visible and Indicator Brightness is maxed. Unlinked encoders' LEDs are off and indicator brightness dimmed.

**BI-DIRECTIONAL FEEDBACK - WORKING**
- By default, editing a value on the MIDI Fighter Twister changes it on FL Studio only
- Now, editing a value linked to an encoder in FL changes it on the linked encoder.
- During playback, if automation is present on a linked encoder, indicators will light up accordingly in realiime
- When Recording during playback, can overwrite indicator automation via overdubbing.
- Currently only works for channel 0 (indicators).
- Physical feedback can appear choppy as the implementation runs through multiple linked controls in order to find the correct one.

**SMART SWITCH BETWEEN PLUGINS/GENERATORS - SHOULD WORK, UNTESTED**
- When a GENERATOR/EFFECT is FOCUSED (window clicked on) in FL Studio, linked controls on the Twister are updated to those on the focused Generator/Effect.
- Useful for global links, where one encoder has multiple links to multiple plugins.
- When Updating Midi Fighter Twister Indicators, last focused plugin is used.
- MAYBE? Change Color Scheme of all RGBs to preset one when focused on new effect/generator

**INCREMENTAL/DECREMENTAL ENCODERS - TO-DO**
- Some Encoder functionality broken in FL Studio for MIDI Fighter Twister.
- The ENC 3FH/41H mode is a setting for any encoder on the device. 
- With it, the encoder is suppose to send an incremental value of +1 or -1 to the linked control, rather than keeping track of the specific value.
- Unfortuantely, using the ENC 3FH/41H mode in FL Studio will only send a static value of 65 or 63 to FL Studio. This script seeks to fix that.
	- When a value of 63 is given, linked control parameter should be reduced by 1.
	- When a value of 65 is given, linked control parameter should be increased by 1.
