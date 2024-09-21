def UpdateEncoders(channel):
	prevControlLinkIndex = -1
	currControlLink = -1

	if channel == 0:
		for ctrlChange in range(64):
			if device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), 0, ctrlChange)) == 0x7fffffff:
				if ctrlChange in channel0InitCtrl:
					prevControlLinkIndex = channel0InitCtrl.index(ctrlChange)
					SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_OFF + 1)
					SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_OFF)
					SendMIDI(0xB0, 0, ctrlChange, 0)
			else:
				if ctrlChange not in channel0InitCtrl:
					currControlLink = ctrlChange
					SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_BRIGHT)
					SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_BRIGHT)


					# Mix Functionality

					#if device.getLinkedParamName(device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), 0, ctrlChange))) == "Mix":

					#	SendMIDI(0xB0, 1, ctrlChange, Color.GREEN)

					#	SendMIDI(0xB0, 1, ctrlChange, 0)

					#print(device.getLinkedParamName(device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), 0, ctrlChange))))

		if prevControlLinkIndex != -1 or currControlLink != -1:
			if prevControlLinkIndex == -1 and currControlLink != -1: #Means you added a new linked control
				channel0InitCtrl.append(currControlLink)
				channel0InitCtrlVal.append(0)
			if prevControlLinkIndex != -1 and currControlLink == -1: #Means you removed a linked control value
				channel0InitCtrl.pop(prevControlLinkIndex)
				channel0InitCtrlVal.pop(prevControlLinkIndex)
			if prevControlLinkIndex != -1 and currControlLink != -1: #Means you replaced a linked control with a new one
				channel0InitCtrl[prevControlLinkIndex] = currControlLink
	elif channel == 1:
		for ctrlChange in range(64):
			if device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), 1, ctrlChange)) == 0x7fffffff:
				if ctrlChange in channel1InitCtrl:
					prevControlLinkIndex = channel1InitCtrl.index(ctrlChange)

				#SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_OFF + 7)

				#SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_OFF)

				#SendMIDI(0xB0, 1, ctrlChange, 0)

			else:
				if ctrlChange not in channel1InitCtrl:
					currControlLink = ctrlChange
					SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_BRIGHT)
				#if device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), 0, ctrlChange)) != 0x7fffffff or device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), 4, ctrlChange)) != 0x7fffffff:

					#SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_BRIGHT)

				#else

					#SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_OFF + 7)

		if prevControlLinkIndex != -1 or currControlLink != -1:
			if prevControlLinkIndex == -1 and currControlLink != -1: #Means you added a new linked control
				channel1InitCtrl.append(currControlLink)
				channel1InitCtrlVal.append(0)
			if prevControlLinkIndex != -1 and currControlLink == -1: #Means you removed a linked control value
				channel1InitCtrl.pop(prevControlLinkIndex)
				channel1InitCtrlVal.pop(prevControlLinkIndex)
			if prevControlLinkIndex != -1 and currControlLink != -1: #Means you replaced a linked control with a new one
				channel1InitCtrl[prevControlLinkIndex] = currControlLink
	elif channel == 4:
		for ctrlChange in range(64):
			if device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), 4, ctrlChange)) == 0x7fffffff:
				if ctrlChange in channel4InitCtrl:
					prevControlLinkIndex = channel4InitCtrl.index(ctrlChange)
				#SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_OFF + 7)

				#SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_OFF)

				#SendMIDI(0xB0, 4, ctrlChange, 0)
			else:
				if ctrlChange not in channel4InitCtrl:
					currControlLink = ctrlChange
				#SendMIDI(0xB0, 2, ctrlChange, Animation.RGB_BRIGHT)
				#SendMIDI(0xB0, 5, ctrlChange, Animation.INDICATOR_BRIGHT)
		if prevControlLinkIndex != -1 or currControlLink != -1:
			if prevControlLinkIndex == -1 and currControlLink != -1: #Means you added a new linked control
				channel4InitCtrl.append(currControlLink)
				channel4InitCtrlVal.append(0)
			if prevControlLinkIndex != -1 and currControlLink == -1: #Means you removed a linked control value
				channel4InitCtrl.pop(prevControlLinkIndex)
				channel4InitCtrlVal.pop(prevControlLinkIndex)
			if prevControlLinkIndex != -1 and currControlLink != -1: #Means you replaced a linked control with a new one
				channel4InitCtrl[prevControlLinkIndex] = currControlLink