# name=Midi Fighter Twister

import midi
import device
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

lastUpdateTime = time.time()

#UNLINKED_CONTROL_ID = 0x7fffffff # Old value, works in older versions of FL Studio
UNLINKED_CONTROL_ID = -0x1 # New value for unlinked controls, works in FL Studio 25 and later
REFRESH_FLAGS = [0x127, 0x10127]
FL_FOCUSED_FLAG = 32

# New implementation using sets/dictionaries to provide constant access time.
channelInitCtrl = {0: set(), 1: set(), 2: set(), 4: set(), 5: set()}
channelInitCtrlVal = {0: {}, 1: {}, 2: {}, 4: {}, 5: {}}

# This method turns off all of the lights on initialization of the script in FL.
def OnInit():
	for ctrlChange in range(64):
		SendMIDI(midi.MIDI_CONTROLCHANGE, 0, ctrlChange, 0)
		SendMIDI(midi.MIDI_CONTROLCHANGE, 5, ctrlChange, Animation.INDICATOR_OFF + 1)
		SendMIDI(midi.MIDI_CONTROLCHANGE, 2, ctrlChange, Animation.RGB_OFF)
	print("Midi Fighter Twister Initialized")

# Likewise, this method returns the MIDI Fighter Twister to its default configuration upon closing FL Studio
#def OnDeInit():
#	for ctrlChange in range(64):
#		SendMIDI(midi.MIDI_CONTROLCHANGE, 0, ctrlChange, 0)
#		SendMIDI(midi.MIDI_CONTROLCHANGE, 5, ctrlChange, Animation.INDICATOR_BRIGHT)
#		SendMIDI(midi.MIDI_CONTROLCHANGE, 2, ctrlChange, Animation.RGB_BRIGHT)

# Alternate implementation: on deinitialization, turn everything off. good for darker rooms/when you dont want the lights to be on.
def OnDeInit():
	for ctrlChange in range(64):
		SendMIDI(midi.MIDI_CONTROLCHANGE, 0, ctrlChange, 0)
		SendMIDI(midi.MIDI_CONTROLCHANGE, 5, ctrlChange, Animation.INDICATOR_OFF)
		SendMIDI(midi.MIDI_CONTROLCHANGE, 2, ctrlChange, Animation.RGB_OFF)


def OnMidiMsg(event):
	event.handled = False
	channel = event.midiChan
	if channel in channelInitCtrlVal and event.data1 in channelInitCtrlVal[channel]:
		channelInitCtrlVal[channel][event.data1] = event.data2
	print(f"Channel: {channel}, Ctrl: {event.data1}, Value: {event.data2}")
 
 
def OnIdle():
	global lastUpdateTime
	currentTime = time.time()
	if currentTime - lastUpdateTime > 0.025:
		UpdateEncoders(0)
		UpdateEncoders(4)

		UpdateIndicators(0)
		UpdateIndicators(1)
		UpdateIndicators(4)

		lastUpdateTime = currentTime

def OnRefresh(flag):
	UpdateEncoders(0)
	UpdateEncoders(1)
	UpdateEncoders(4)
	if flag in REFRESH_FLAGS:
		UpdateIndicators(0)
		UpdateIndicators(4)
	if flag == FL_FOCUSED_FLAG:
		if ui.getFocused(5) == 0:
			for ctrlChange in range(64):
				SendMIDI(midi.MIDI_CONTROLCHANGE, 0, ctrlChange, 0)		
				SendMIDI(midi.MIDI_CONTROLCHANGE, 4, ctrlChange, 0)		
				SendMIDI(midi.MIDI_CONTROLCHANGE, 2, ctrlChange, Animation.RGB_OFF)
				SendMIDI(midi.MIDI_CONTROLCHANGE, 5, ctrlChange, Animation.INDICATOR_OFF + 1)
"""
#----------------------------------------HELPER METHODS----------------------------------------#
"""
# Streamlined Midi Messaage sending to Device
#	- command = CC Type (Control Change, Note On, Pitch Bend, etc)
#	- channel = (Apperantly, not so sure) the channel that the device handles output you want
#	- data1 = the individual controller (encoder, button, slider, led, etc) that you want to change (shift by 8).
#	- data2 = the value you want to send. (bit shift by 16).
def SendMIDI(command, channel, data1, data2):
	status = command | channel
	message = status + (data1 << 8) + (data2 << 16)
	device.midiOutMsg(message);

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
        isLinked = eventID != UNLINKED_CONTROL_ID
        wasInitialized = ctrlChange in currentCtrlSet

        if isLinked:
            updatedCtrlSet.add(ctrlChange)
            if not wasInitialized:
                # Newly linked control
                channelInitCtrlVal[channel][ctrlChange] = 0
                # Send MIDI messages to turn on lights
                if channel == 0 or channel == 4:
                    SendMIDI(midi.MIDI_CONTROLCHANGE, 5, ctrlChange, Animation.INDICATOR_BRIGHT)
                    SendMIDI(midi.MIDI_CONTROLCHANGE, 2, ctrlChange, Animation.RGB_BRIGHT)
                #elif channel == 1:
                	# TO DO
        else:
            if wasInitialized:
                # Control was unlinked
                del channelInitCtrlVal[channel][ctrlChange]
                # Send MIDI messages to turn off lights
                if channel == 0 or channel == 4:
                    SendMIDI(midi.MIDI_CONTROLCHANGE, 5, ctrlChange, Animation.INDICATOR_OFF + 1)
                    SendMIDI(midi.MIDI_CONTROLCHANGE, 2, ctrlChange, Animation.RGB_OFF)
                    SendMIDI(midi.MIDI_CONTROLCHANGE, channel, ctrlChange, 0)
                #elif channel == 1:
                    # TO DO

    # Update the initialized controls for the channel
    channelInitCtrl[channel] = updatedCtrlSet

# BiDirectional Feedback
def UpdateIndicators(channel):
    if channel not in channelInitCtrlVal:
        return

    for linkedCtrl in channelInitCtrlVal[channel]:
        eventID = getEventID(channel, linkedCtrl)
        linkedValue = device.getLinkedValue(eventID)

        if channel == 1:
            newValue = 127 if linkedValue > 0 else 0
        else:
            newValue = round(127 * linkedValue)

        if newValue != channelInitCtrlVal[channel][linkedCtrl]:
            channelInitCtrlVal[channel][linkedCtrl] = newValue
            SendMIDI(midi.MIDI_CONTROLCHANGE, channel, linkedCtrl, newValue)

# Endless Encoder Fix
#	- Made for ENC 3FH/41H mode.
#		- When a value of 65 is given, the encoder sends a midi value of
#			newValue = currentValue + 1
#		- When a value of 63 is given, the encoder sends a midi value of
#			newValue = currentValue - 1
def EndlessEncoder(currentValue, encVal):
    if encVal == 65:
        return min(currentValue + 1, 127)
    elif encVal == 63:
        return max(currentValue - 1, 0)
    else:
        return currentValue

# Get method for EventData (Utility)
def getEventID(channel,ctrlChange):
	return device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), channel, ctrlChange))

"""
#----------------------------------------CLASSES----------------------------------------#
"""
	
class EncoderStatus:
	ON = 127
	OFF = 0

class Color:
	SAPPHIRE = 1
	BLUE = 8
	AZURE = 16
	CYAN = 24
	MINT = 40
	GREEN = 51
	APPLE = 61
	YELLOW = 65
	GOLD = 70
	ORANGE = 74
	AMBER = 79
	RED = 83
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