# name=Midi Fighter Twister

import math

#import sys
#sys.path.insert(0, 'C:\Program Files\Image-Line\FL Studio 21\Shared\Python\Lib\midi.py')

import midi
import utils
import device
import plugins
import mixer
import ui


"""
#----------------------------------------OVERRIDES----------------------------------------#
"""

#channel0InitCtrl = []
#channel0InitCtrlVal = []
#channel4InitCtrl = []
#channel4InitCtrlVal = []
#channel1InitCtrl = []
#channel1InitCtrlVal = []

#New implementation of sets/dictionaries to provide constant access time.
channelInitCtrl = {0: set(), 1: set(), 4: set()}
channelInitCtrlVal = {0: {}, 1: {}, 4: {}}

# This method turns off all of the lights on initialization of the script in FL.
def OnInit():
	for ctrlChange in range(64):
		SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_OFF + 1)
		SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_OFF)
		SendMIDI(0xB0, 0, ctrlChange, 0)

# Likewise, this method returns the MIDI Fighter Twister to its default configuration upon closing FL Studio
def OnDeInit():
	for ctrlChange in range(64):
		SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_BRIGHT)
		SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_BRIGHT)
		SendMIDI(0xB0, 0, ctrlChange, 0)

#	print(str(device.getName() + ' is connected to Port '+ str(device.getPortNumber())))

	#InitializeEncoders()
#	UpdateEncoders(0)
#	print("Channel 0:")
#	print(channel0InitCtrl)
#	print(channel0InitCtrlVal)
#	UpdateEncoders(1)
#	print("Channel 1:")
#	print(channel1InitCtrl)
#	print(channel1InitCtrlVal)
#	UpdateEncoders(4)
#	print("Channel 4:")
#	print(channel4InitCtrl)
#	print(channel4InitCtrlVal)

#	print("----------------------------------------------")

def OnMidiMsg(event):
	event.handled = False
	channel = event.midiChan
	if channel in channelInitCtrlVal and event.data1 in channelInitCtrlVal[channel]:
		channelInitCtrlVal[channel][event.data1] = event.data2
	#if event.midiChan == 0:
	#	if event.data1 in channel0InitCtrl:
	#		channel0InitCtrlVal[channel0InitCtrl.index(event.data1)] = event.data2
	#elif event.midiChan == 1:
	#	if event.data1 in channel1InitCtrl:
#			channel1InitCtrlVal[channel1InitCtrl.index(event.data1)] = event.data2
#	elif event.midiChan == 4:
#		if event.data1 in channel4InitCtrl:
#			channel4InitCtrlVal[channel4InitCtrl.index(event.data1)] = event.data2

	#GetIDS(event)
	#UpdateEncoders(0)
	#print("Channel 0:")
	#print(channel0InitCtrl)
	#print(channel0InitCtrlVal)
	#UpdateEncoders(1)
	#print("Channel 1:")
	#print(channel1InitCtrl)
	#print(channel1InitCtrlVal)
	#UpdateEncoders(4)
	#print("Channel 4:")
	#print(channel4InitCtrl)
	#print(channel4InitCtrlVal)

def OnRefresh(flag):
	print(flag)
	if flag == 32:
		if ui.getFocused(5) == 0:
			for ctrlChange in range(64):
				SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_OFF + 1)
				SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_OFF)
				SendMIDI(0xB0, 0, ctrlChange, 0)		
#def OnDoFullRefresh():
#	device.fullRefresh();

#def OnProjectLoad(status):
#	if(status == 100):
#		device.fullRefresh();

def OnIdle():
	UpdateEncoders(0)
	UpdateEncoders(1)
	UpdateEncoders(4)

	UpdateIndicators(0)
	#UpdateIndicators(1)
	UpdateIndicators(4)

def OnRefresh(event):
	#print(hex(event))
	UpdateEncoders(0)
	UpdateEncoders(1)
	UpdateEncoders(4)
	if event == 0x127 or event == 0x10127:
	#UpdateEncoders()
		UpdateIndicators(0)
		UpdateIndicators(1)
		UpdateIndicators(4)
	#if event == 0x200:
	#	UpdateIndicators()

"""
#----------------------------------------HELPER METHODS----------------------------------------#
"""
# Streamlined Midi Messaage sending to Device
#	- command = CC Type (Control Change, Note On, Pitch Bend, etc)
#	- channel = (Apperantly, not so sure) the channel that the device handles output you want
#	- data1 = the individual controller (encoder, button, slider, led, etc) that you want to change (shift by 8).
#	- data2 = the value you want to send. (bit shift by 16).
def SendMIDI(command, channel, data1, data2):
	device.midiOutMsg((command | channel) + (data1 << 8) + (data2 << 16));

# This Method does a lot of things:
# 1. For any linked controls, it turns the RGB on and sets the indicator brightness to the max
# 2. For any unlinked controls, it turns the RGB off and dims the indicator brightness
# 3. Functionality for adding linked controls, removing linked controls, and replacing linked controls is present
def UpdateEncoders(channel):
    # Ensure the channel is valid
    if channel not in channelInitCtrl:
        return

    currentCtrlSet = channelInitCtrl[channel]
    updatedCtrlSet = set()

    for ctrlChange in range(64):
        eventID = device.findEventID(
            midi.EncodeRemoteControlID(device.getPortNumber(), channel, ctrlChange)
        )
        isLinked = eventID != 0x7fffffff
        wasInitialized = ctrlChange in currentCtrlSet

        if isLinked:
            updatedCtrlSet.add(ctrlChange)
            if not wasInitialized:
                # Newly linked control
                channelInitCtrlVal[channel][ctrlChange] = 0
                # Send MIDI messages to turn on lights
                if channel == 0:
                    SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_BRIGHT)
                    if device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), 1, ctrlChange)) == 0x7fffffff:
                        SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_SEMI)
                    else:
                        SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_BRIGHT)
                elif channel == 1:
                    SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_BRIGHT)
                elif channel == 4:
                    # Include any channel 4 specific behavior here
                    pass
        else:
            if wasInitialized:
                # Control was unlinked
                #index = channelInitCtrl[channel].index(ctrlChange)
                #channelInitCtrlVal[channel].pop(index)
                del channelInitCtrlVal[channel][ctrlChange]
                # Send MIDI messages to turn off lights
                if channel == 0:
                    SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_OFF + 1)
                    SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_OFF)
                    SendMIDI(0xB0, 0, ctrlChange, 0)
                elif channel == 1:
                    # Include any channel 1 specific behavior here
                    pass
                elif channel == 4:
                    # Include any channel 4 specific behavior here
                    pass

    # Update the initialized controls for the channel
    channelInitCtrl[channel] = updatedCtrlSet


# BiDirectional Feedback
def UpdateIndicators(channel):
	if channel in channelInitCtrlVal:
		for linkedCtrl in channelInitCtrlVal[channel]:
			possNewVal = round(127 * device.getLinkedValue(device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), 0, linkedCtrl))))
			if possNewVal != channelInitCtrlVal[channel][linkedCtrl]:
				channelInitCtrlVal[channel][linkedCtrl] = possNewVal
				SendMIDI(0xB0, channel, linkedCtrl, possNewVal)
#	if channel == 0:
#		for linkedCtrl in channel0InitCtrl:
#			possNewVal = round(127 * device.getLinkedValue(device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), 0, linkedCtrl))))
#			if possNewVal != channel0InitCtrlVal[channel0InitCtrl.index(linkedCtrl)]:
#				channel0InitCtrlVal[channel0InitCtrl.index(linkedCtrl)] = possNewVal
#				SendMIDI(0xB0, 0, linkedCtrl, possNewVal)
#	elif channel == 1:
#		for linkedCtrl in channel1InitCtrl:
#			possNewVal = round(127 * device.getLinkedValue(device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), 1, linkedCtrl))))
#			#print(possNewVal)
#			if possNewVal != channel1InitCtrlVal[channel1InitCtrl.index(linkedCtrl)]:
#				channel1InitCtrlVal[channel1InitCtrl.index(linkedCtrl)] = possNewVal
#				#SendMIDI(0xB0, 1, linkedCtrl, possNewVal)
#	elif channel == 4:
#		for linkedCtrl in channel4InitCtrl:
#			possNewVal = round(127 * device.getLinkedValue(device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), 4, linkedCtrl))))
#			if possNewVal != channel4InitCtrlVal[channel4InitCtrl.index(linkedCtrl)]:
#				channel4InitCtrlVal[channel4InitCtrl.index(linkedCtrl)] = possNewVal
#				SendMIDI(0xB0, 4, linkedCtrl, possNewVal)

# Endless Encoder Fix Status - TO DO
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

# Get method for EventData
def GetEventID(track,slot,param):
	return (((0x2000 + 0x40 * track) + slot) << 0x10) + 0x8000 + param

# Get method for Plugin Track
def GetFocusedPluginTrack():
	return math.floor((ui.getFocusedFormID() >> 16) / 64)

# Get method for Plugin Slot
def GetFocusedPluginSlot():
	return (ui.getFocusedFormID() >> 16) % 64

# Debugging method for checking focused plugins
def GetFocusedWindowInfo():
	trackNumber = GetFocusedPluginTrack()
	slotNumber = GetFocusedPluginSlot()
	print("Current Plugin: " + str(plugins.getPluginName(trackNumber, slotNumber)))
	if trackNumber == 0:
		print("Location: Master Track, Slot " + str(slotNumber + 1))
	else:
		print("Location: Track " + str(trackNumber) + ", Slot " + str(slotNumber + 1))

	print("Linkable Parameters:")
	for param in range(4240): #Every plugin (effects at least) carries 4240 plugins
		while plugins.getParamName(param, trackNumber, slotNumber) != "": #Unnamed Midi CC (ones w/ default MIDI CC#) are just blank strings
			print("     - " + plugins.getParamName(param, trackNumber, slotNumber))
	print("Plugin ID: " + str(hex(ui.getFocusedFormID())))
	print("----------------------------------------------")

# Debugging method for ControlID and EventId of current CC Value
def GetIDS(event):
	print("CC Value: " + str(event.data1))
	print("Control ID: " + str(hex(midi.EncodeRemoteControlID(device.getPortNumber(), event.midiChan, event.data1))))
	print("Event ID: " + str(hex(device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), event.midiChan, event.data1)))))

# Debugging method for Channel Data?
def PrintEncoderData(encoder):
	for channelNr in range(0, 4):
		ID = device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), channelNr, encoder), 0)
		print(device.getLinkedInfo(ID))
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
