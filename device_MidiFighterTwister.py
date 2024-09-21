# name=Midi Fighter Twister

import math
import midi
import utils
import device
import plugins
import mixer
import ui


"""
#----------------------------------------OVERRIDES----------------------------------------#
"""

# New implementation using sets/dictionaries to provide constant access time.
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

def OnMidiMsg(event):
	event.handled = False
	channel = event.midiChan
	if channel in channelInitCtrlVal and event.data1 in channelInitCtrlVal[channel]:
		channelInitCtrlVal[channel][event.data1] = event.data2

def OnRefresh(flag):
	print(flag)
	if flag == 32:
		if ui.getFocused(5) == 0:
			for ctrlChange in range(64):
				SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_OFF + 1)
				SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_OFF)
				SendMIDI(0xB0, 0, ctrlChange, 0)		

def OnIdle():
	UpdateEncoders(0)
	UpdateEncoders(1)
	UpdateEncoders(4)

	UpdateIndicators(0)
	UpdateIndicators(4)

def OnRefresh(event):
	UpdateEncoders(0)
	UpdateEncoders(1)
	UpdateEncoders(4)
	if event == 0x127 or event == 0x10127:
		UpdateIndicators(0)
		UpdateIndicators(4)

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
                    SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_BRIGHT)
                    #if device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), 1, ctrlChange)) == 0x7fffffff:
                    #    SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_SEMI)
                    #else:
                    #    SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_BRIGHT)
                elif channel == 1:
                    SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_BRIGHT)
                elif channel == 4:
                    # Include any channel 4 specific behavior here
                    pass
        else:
            if wasInitialized:
                # Control was unlinked
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