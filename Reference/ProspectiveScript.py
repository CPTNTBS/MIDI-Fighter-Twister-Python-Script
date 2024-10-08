# name=Midi Fighter Twister

import math
import midi
import utils
import device
import plugins
import mixer
import ui
import time


"""
#----------------------------------------OVERRIDES----------------------------------------#
"""

# Hardcoded Encoder Data from MidiFighter Utility 
# Edit to fit the settings of your setup, make sure to include all 64 encoders or the script might break
shiftEncoderCtrl = {0,1,2,3,4,5,6,7,8,9,10,11,
					16,17,18,19,20,21,22,23,24,25,26,27}
toggleEncoderCtrl = {12,13,14,15,
					 28,29,30,31,
					 32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,
					 48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63}
# New implementation using sets/dictionaries to provide constant access time.
channelInitCtrl = {0: set(), 1: set(), 2: set(), 4: set(), 5: set()}
channelInitCtrlVal = {0: {}, 1: {}, 2: {}, 4: {}, 5: {}}

# This method turns off all of the lights on initialization of the script in FL.
def OnInit():
	for ctrlChange in range(64):
		SendMIDI(0xB0, 0, ctrlChange, 0)
		SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_OFF + 1)
		SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_OFF)

# Likewise, this method returns the MIDI Fighter Twister to its default configuration upon closing FL Studio
def OnDeInit():
	for ctrlChange in range(64):
		SendMIDI(0xB0, 0, ctrlChange, 0)
		SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_BRIGHT)
		SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_BRIGHT)

def OnMidiMsg(event):
	event.handled = False
	channel = event.midiChan
	if channel in channelInitCtrlVal and event.data1 in channelInitCtrlVal[channel]:
		channelInitCtrlVal[channel][event.data1] = event.data2
	#DebugChannelStates([1])
 
def OnRefresh(flag):
	print(flag)
	if flag == 32:
		if ui.getFocused(5) == 0:
			for ctrlChange in range(64):
				SendMIDI(0xB0, 0, ctrlChange, 0)		
				SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_OFF)
				SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_OFF + 1)

def OnIdle():
	UpdateEncoders(0)
	UpdateEncoders(4)

	UpdateIndicators(0)
	UpdateIndicators(1)
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
        eventID = getEventID(channel, ctrlChange)
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
                    #if ctrlChange in shiftEncoderCtrl:
                    #    SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_BRIGHT)
                    #    if getEventID(4, ctrlChange) == 0x7fffffff:
                    SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_BRIGHT)
                    #if getEventID(1, ctrlChange) == 0x7fffffff:
                        #SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_PULSE)
                    #else:
                    #    SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_BRIGHT)
                elif channel == 1:
                    #SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_BRIGHT)
                    #if ctrlChange in toggleEncoderCtrl:
                    #    if getEventID(0, ctrlChange) == 0x7fffffff:
                    #        SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_PULSE + 3)
                    #        time.sleep(5)
                    #        SendMIDI(0xB0, 0, ctrlChange, 0)
                    #SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_BRIGHT)
                    pass
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
	if channel == 1:
		for linkedCtrl in channelInitCtrlVal[channel]:
			newValue = 127 if device.getLinkedValue(getEventID(channel, linkedCtrl)) > 0 else 0
			if newValue != channelInitCtrlVal[channel][linkedCtrl]:
				channelInitCtrlVal[channel][linkedCtrl] = newValue
				SendMIDI(0xB0, channel, linkedCtrl, newValue)
	if channel in channelInitCtrlVal:
		for linkedCtrl in channelInitCtrlVal[channel]:
			eventID = getEventID(channel, linkedCtrl)
			possNewVal = round(127 * device.getLinkedValue(eventID))
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

# Get method for EventData (Debug)
def getEventID(track,slot,param):
	return (((0x2000 + 0x40 * track) + slot) << 0x10) + 0x8000 + param

# Get method for EventData (Utility)
def getEventID(channel,ctrlChange):
	return device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), channel, ctrlChange))


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

def DebugChannelStates(selected_channels=None):
    # If no specific channels are provided, default to all channels
    if selected_channels is None:
        selected_channels = channelInitCtrl.keys()
    
    for channel in selected_channels:
        if channel in channelInitCtrl:  # Ensure the channel exists
            print(f"Channel {channel}:")
            
            # Print the initialized control numbers
            controls = channelInitCtrl[channel]
            values = channelInitCtrlVal[channel]
            
            if controls:
                print("  Initialized Controls:")
                for ctrl in controls:
                    value = values.get(ctrl, "Not set")  # Default if not found
                    print(f"    Control {ctrl}: Value {value}")
            else:
                print("  No Initialized Controls.")
        else:
            print(f"  Channel {channel} does not exist.")
        
        print()  # Add a blank line for better readability

# Example usage:
DebugChannelStates([0, 1])  # Specify channels you want to print


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