#!/usr/bin/python
#This is a example for Zelda ocarina of time. Based on it you can make your own script for your games

#       Copyright 2011 Alvaro Garcia <maxpowel@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


import cwiid
import serial
import struct
import pprint

from time import sleep


#Init arduino and wait for 2 seconds until serial in arduino is initializated
ser = serial.Serial('/dev/ttyACM1', 115200)
sleep(2)
cosa = True

#Connect to wiimote
w = cwiid.Wiimote()
#Turn on led 1
w.led = 1

w.rpt_mode = cwiid.RPT_STATUS | cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_MOTIONPLUS | cwiid.RPT_NUNCHUK | cwiid.RPT_EXT


attack_state = 0 #Used for ocarina of time

#Infinite loop, sure you can do anything better ;)
while( cosa ):
	
	#2 bytes for buttons and 2 bytes for stick
	byte1 = 0
	byte2 = 0
	stickX = 0
	stickY = 0
	
	###First Byte
	#B Button
	if w.state['buttons'] == 8:
		#print 'A'
		byte1 = byte1 | 0x80
		
	#A Button (Attack in ocarina of time): shaking wiimote or pressing button 4 (B in wiimote)
	if w.state['acc'][2] <= 110 and attack_state == 0:
		attack_state = 1;
	elif (w.state['acc'][2] > 140 and attack_state == 1) or w.state['buttons'] == 4:
		attack_state = 0
		#print "B"
		byte1 = byte1 | 0x40
		
	#Z Button
	if "nunchuk" in w.state:
		if w.state['nunchuk']['buttons'] == 1:
			#print 'Z'
			byte1 = byte1 | 0x20
		
		stickX = w.state['nunchuk']['stick'][0]
		if ((stickX >= 140 and stickX <= 150) or stickX == 0):
			stickX = 0
		else:
			stickX = stickX - 145
		
		
		stickY = w.state['nunchuk']['stick'][1];
		if ((stickY>= 125 and stickY <= 135) or stickY == 0):
			stickY = 0
		else:
			stickY = stickY - 130
		
	
	#Start Button
	if w.state['buttons'] == 128:
		#print 'Start'
		byte1 = byte1 | 0x10
		
	
	#Add the pad here. It is not used in ocarina of time
	
	
	### Second byte
	# Two first bits are 0
	
	# L Butto is not used in ocarina of time :P
	
	#R Button (shield)
	if (w.state['acc'][0] < 100 and w.state['acc'][2] < 130 and w.state['acc'][2] > 110) or w.state['nunchuk']['buttons'] == 2:
		#print 'R'
		byte2 = byte2 | 0x10
		
	#C-up Button
	if w.state['buttons'] == 2048:
		#print 'R'
		byte2 = byte2 | 0x08
	
	
	#C-down Button
	if w.state['buttons'] == 1024:
		#print 'R'
		byte2 = byte2 | 0x04
		
	#C-left Button
	if w.state['buttons'] ==256:
		##print 'R'
		byte2 = byte2 | 0x02
		
	#C-right Button
	if w.state['buttons'] == 512:
		#print 'R'
		byte2 = byte2 | 0x01
	
	
	#Send data: Last two bytes are sent from arduino (and are read in this app) because for an misterious reason, arduino does not read 4 bytes right
	ser.write(struct.pack('B', byte1));
	ser.write(struct.pack('B', byte2));
	ser.write(struct.pack('b', stickX));
	ser.read(1)
	ser.write(struct.pack('b', stickY));
	ser.read(1)
	

	
