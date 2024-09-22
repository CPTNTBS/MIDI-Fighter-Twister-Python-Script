# Get method for EventData (Debug)
def getEventIDDebug(track,slot,param):
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
	for channelNr in range(0, 5):
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
