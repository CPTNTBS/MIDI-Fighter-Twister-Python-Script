# name=Midi Fighter Twister

import math
import midi
import device
import plugins
import mixer
import ui

"""
#----------------------------------------OVERRIDES----------------------------------------#
"""

def OnInit():
	print(str(device.getName() + ' is connected to Port '+ str(device.getPortNumber())))
	InitializedLEDs()
	print("----------------------------------------------")

		#	SendMIDI()
		#print(device.getLinkedInfo(0x800000 + ctrlChange))
		#if device.getLinkedInfo(0x800000 + ctrlChange) == -1:
			#SendMIDI(midi.MIDI_CONTROLCHANGE, 2, ctrlChange, 17)
			#SendMIDI(midi.MIDI_CONTROLCHANGE, 2, ctrlChange, 65)

# Called when something changed that the script might want to respond to.
#def OnRefresh(HW_Dirty_RemoteLinkValues):
#	if Flags & midi.HW_Dirty_RemoteLinks:
#		# Update the on your devices shown links into a dictionary
#	if Flags & midi.HW_Dirty_RemoteLinkValues: (if you are running the current beta)
#		# Update displays by looping throug the dictionary

# Use when looking for modification to midi device
def OnMidiMsg(event):
	#event.handled = False
	#print(plugins.isValid(1,2))
	#print(plugins.getPluginName(1,1))#slot index (track effect slot) = 1, index (track) = 1
	#print(ui.getFocusedPluginName()) #plugin index = 6
	#print("Plugin Location: " + str(hex(ui.getFocusedFormID() >> 16)))
	#print("Plugin Location: " + str(ui.getFocusedFormID() >> 16))
	#to get:
	#slotindex: focusedformid mod 64
	#tracknumber: focusedformid / 64
	#print("Plugin Param Count: " + str(plugins.getPluginName(ui.getFocusedFormID())))
	#print(plugins.getPluginName(1,1,0))
	#print(plugins.getParamCount(1,1))
	#print(plugins.getParamName(8,1,1))
	#print(plugins.getParamValue(8,1,1))
	#PrintOutControllerDeats(event)
	#print(ui.getFocusedPluginName())
	
	#if event.midiId != midi.MIDI_CONTROLCHANGE + 1:
		#Set event.handled to false to modify what happens if it is activated
	#if event.status == 0xB0 or event.status == 0xB4:
	#	OnRefresh
	print("CC Value: " + str(event.data1))
	#print(device.isAssigned())
	print("Control ID: " + str(hex(midi.EncodeRemoteControlID(device.getPortNumber(), event.midiChan, event.data1))))
	print("Event ID: " + str(hex(device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), event.midiChan, event.data1)))))
	#print(device.getLinkedValue(midi.EncodeRemoteControlID(device.getPortNumber(), event.midiChan, event.data1)))

	#if event.data1 == 15:
	#SendMIDI(midi.MIDI_CONTROLCHANGE, 2, event.data1, event.data2)
		#SendMIDI(midi.MIDI_CONTROLCHANGE, 2, event.data1, event.data2)
	#GetChannel(event)
	#if(event.status)
	#PrintEncoderData(event.data1)
	#event.handled = True

#def LightUp():

#def UpdatePluginVals(event):
#	for plugin in range(9):
#		if plugins.isValid

def OnRefresh(HW_Dirty_RemoteLinkValues):
	GetFocusedWindowInfo()

"""
#----------------------------------------HELPER METHODS----------------------------------------#
"""
#	Streamlined Midi Messaage sending to Device
#		- command = CC Type (Control Change, Note On, Pitch Bend, etc)
#		- channel = (Apperantly, not so sure) the channel that the device handles output you want
#		- data1 = the individual controller (encoder, button, slider, led, etc) that you want to change (shift by 8).
#		- data2 = the value you want to send. (bit shift by 16).
def SendMIDI(command, channel, data1, data2):
	device.midiOutMsg((command | channel) + (data1 << 8) + (data2 << 16));

#Unlinked encoders have the LED turned off and Indicator Brightness Dimmed.
def InitializedLEDs():
	for ctrlChange in range(64):
		print("Control #" + str(ctrlChange) + ": " + str(hex(device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), 0, ctrlChange)))))
		if device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), 0, ctrlChange)) == 0x7fffffff:
			SendMIDI(0xB0, 2, ctrlChange, 17)
			SendMIDI(0xB0, 2, ctrlChange, 77)
		else:
			SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_BRIGHT)
			SendMIDI(0xB0, 2, ctrlChange, Animation.INDICATOR_BRIGHT)

#Endless Encoder Fix
#	- Made for ENC 3FH/41H mode.
#		- When a value of 65 is given, the encoder sends a midi value of
#			newValue = currentValue + 1
#		- When a value of 63 is given, the encoder sends a midi value of
#			newValue = currentValue - 1
def EndlessEncoder(encVal):
	if encVal == 65:
		print('MixVal + 1')
	elif encVal == 63:
		print('MixVal - 1')

#Get method for EventData
def getEventID(track,slot,param):
	return (((0x2000 + 0x40 * track) + slot) << 0x10) + 0x8000 + param


#Debugging method for checking focused plugins
def GetFocusedWindowInfo():
	trackNumber = math.floor((ui.getFocusedFormID() >> 16) / 64)
	slotNumber = (ui.getFocusedFormID() >> 16) % 64
	print("Current Plugin: " + str(plugins.getPluginName(trackNumber, slotNumber)))
	if trackNumber == 0:
		print("Location: Master Track, Slot " + str(slotNumber + 1))
	else:
		print("Location: Track " + str(trackNumber) + ", Slot " + str(slotNumber + 1))

	print("Linkable Parameters:")
	for param in range(4240): #Every plugin (effects at least) carries 4240 plugins
		if plugins.getParamName(param, trackNumber, slotNumber) != "": #Unnamed Midi CC (ones w/ default MIDI CC#) are just blank strings
			print("     - " + plugins.getParamName(param, trackNumber, slotNumber))
		else:
			break
	print("Plugin ID: " + str(hex(ui.getFocusedFormID())))
	print("----------------------------------------------")

def GetChannel(encoder):
	print(encoder.progNum)

def PrintEncoderData(encoder):
	for channelNr in range(0, 4):
		ID = device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), channelNr, encoder), 0)
		print(device.getLinkedInfo(ID))

	#print("Encoder " + str(encoder.data1) + ":")
	#print("Channel 0 Value: ")
	#print("Channel 1 Value: ")
	#print("Channel 2 Value: ")
	#print("Channel 3 Value: ")
	#print("Channel 4 Value: ")

#def ShiftControl(control):
#	if control.midiId == midi.MIDI_CONTROLCHANGE + 1
			
#Debugging method for checking controller event data
def PrintOutControllerDeats(event):
	#print('Modified Event is Handled: ' + str(bool(event.handled)))
	#print('Modified Event Timestamp: ' + str(event.timestamp))
	#print('Modified Event Status: ' + str(event.status))
	if event.midiId == 0xB0:
		print("Modified Event Type: Control Change")
	elif event.midiId == 0x90:
		print("Modified Event Type: Note On")
	else:
		print("Modified Event Function: " + str(event.midiId))
	print("Modified Event Data1 (Controller): " + str(event.data1))
	print("Modified Event Data2 (Value): " + str(event.data2))
	print("Modified Event Port: " + str(event.port))
	print("Modified Event Channel: " + str(event.midiChan))
	print("Modified Event ChannelEX: " + str(event.midiChanEx))
	print("----------------------------------------------")

"""
#----------------------------------------CLASSES----------------------------------------#
"""
	
class EncoderStatus:
	ON = 127;
	OFF = 0;

class Color:
	SAPPHIRE = 1
	BLUE = 8
	AZURE = 16
	CYAN = 24
	MINT = 40#32
	GREEN = 51#40
	APPLE = 61#48
	YELLOW = 65#56
	GOLD = 70#64
	ORANGE = 74
	AMBER = 79#80
	RED = 83#88
	FUCSHIA = 90
	MAGENTA = 98
	ORCHID = 109
	VIOLET = 113

class Animation:
	NONE = 0;
	RGB_GATE = 1
	RGB_PULSE = 10
	RGB_OFF = 17
	RGB_SEMI = 32
	RGB_BRIGHT = 47
	INDICATOR_GATE = 49
	INDICATOR_PULSE = 57
	INDICATOR_OFF = 65
	INDICATOR_SEMI = 80
	INDICATOR_BRIGHT = 95
	RAINBOW = 127

class EncoderTypeFlag:
	CC_TOGGLE = 0
	CC_HOLD = 1
	RESET_VALUE = 2
	SHIFT_TOGGLE = 3
	SHIFT_HOLD = 4

class Encoder:
	channel0Value = 0;
	channel1Value = Color.VIOLET;
	channel2Value = 0;
	channel4Value = 0;
	
	'''	def SetDefaults():
		SendMIDI(0xB0, 0, data1, Encoder.channel0Value):
		SendMIDI(0xB0, 1, data1, Encoder.channel1Value):
		SendMIDI(0xB0, 2, data1, Encoder.channel2Value):
		SendMIDI(0xB0, 4, data1, Encoder.channel4Value):
	'''

	def SetCh0Value(newValue):
		Encoder.channel0Value = newValue;

	def SetCh1Value(newValue):
		Encoder.channel1Value = newValue;

	def SetCh2Value(newValue):
		Encoder.channel2Value = newValue;

	def SetCh4Value(newValue):
		Encoder.channel4Value = newValue;

	def GetCh0Value():
		return Encoder.channel0Value;

	def GetCh1Value():
		return Encoder.channel1Value;

	def GetCh2Value():
		return Encoder.channel2Value;

	def GetCh4Value():
		return Encoder.channel4Value;
	
	#def UpdateCh1():

class EncoderBank:
	channel3DefaultBank = 0;

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
	BI-DIRECTIONAL FEEDBACK
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
	OTHER ENHANCEMENTS
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
	CHANNEL 5: LED ANIMATION (AGAIN?)
	CHANNEL 6: INDICATOR AMOUNT (AGAIN?)
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
	DEVICE CC VALUES
		- CC Numbers on Device: 0-63 (64 different CCs)
			- Controls With Side button functionality: 0, 1, 2, 3, 8.
	PLUGINID COMPUTATION (EFFECT):
		- Base 10: (track << 6 + slot) << 16
		- Base 16: (track << 0x06 + slot) << 0x10
	EVENTID COMPUTATION:
		- Base 10: (((0x2000 + 0x40 * track) + slot) << 0x10) + 0x8000 + param
		- Base 16: (((8192 + 64 * track) + slot) << 16) + 32768 + param
	FL TERM GLOSSARY:
		eventData = input from the device
		data1 = device cc
		data2 = device cc amount
		midiId = midi codes (see midi.py)
		midiChan = midi channel
		status = midiId + midiChan

TENTATIVE MIDI FIGHTER TWISTER BANK SETUP:
	BANK 1: Effects
		- Bottom Right: Dry/Wet Mix
	BANK 2: Generator
	BANK 3: Misc. FL
	BANK 4: Free
"""
