#### { SETUP } ####


### VERSION DETAILS ###
#######################
### Version 0.7 : Intellifest writes a string with the graphic filename.  This version is the first to start to read a string instead of a number.
### 		  Starting with VALID, the goal of this version is to read that string and display the Valid screen.
#######################
### Version 0.8 : This version will add a delay after a message screen is displayed before displaying the ready screen again.
#######################
###



### Import Supporting Libraries

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import HX8357driver as LCD
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import time
import cPickle
import os



### Configures and Initializes Screen SPI connection

DC = 'P9_18'
RST = 'P9_27'
SPI_PORT = 1

SPI_DEVICE = 1
screen1 = LCD.HX8357(rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=23000000), dc=DC)

SPI_DEVICE = 0
screen2 = LCD.HX8357(rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=23000000), dc=DC)

screen1.begin()
screen2.begin()



### Global Variables

typeface = './fonts/coolvetica.ttf'
h1 = 90
h2 = 60
h3 = 45
h4 = 29
h5 = 25

font = ImageFont.truetype(typeface, 28) ## Sets Font



### Defines Images for Screen
logo_scr = './graphics/logo_scr.png' 
network_scr = './graphics/network_scr.png'
ready_scr = './graphics/ready_scr.png'
idle_scr = './graphics/idle_scr.png'
graphicidle_scr = './graphics/graphicidle_scr.png'
valid_scr = './graphics/valid_scr.png'
transactionincorrect_scr = './graphics/transactionincorrect_scr.png'
wrongway_scr = './graphics/wrongway_scr.png'
wrongday_scr = './graphics/wrongday_scr.png'
noaccesszone_scr = './graphics/noaccesszone_scr.png'
noaccessdevice_scr = './graphics/noaccessdevice_scr.png'
noaccessaddon_scr = './graphics/noaccessaddon_scr.png'
outofaddons_scr = './graphics/outofaddons_scr.png'
validnotregistered_scr = './graphics/validnotregistered_scr.png'
notregistered_scr = './graphics/notregistered_scr.png'
shuttingdown_scr = './graphics/shuttingdown_scr.png'
ticketnotfound_scr = './graphics/ticketnotfound.png'
error_scr = './graphics/wristbanderror.png'


screen = [	logo_scr,		#0
		network_scr,		#1
		ready_scr,		#2
		valid_scr,		#3
		transactionincorrect_scr,#4
		wrongway_scr,		#5
		wrongday_scr,		#6
		noaccesszone_scr,	#7
		noaccessdevice_scr,	#8
		noaccessaddon_scr,	#9
		outofaddons_scr,	#10
		validnotregistered_scr,	#11
		notregistered_scr,	#12
		shuttingdown_scr,	#13
		idle_scr,		#14
		graphicidle_scr,	#15
		ticketnotfound_scr,	#16
		error_scr		#17
	]



### Define Colors

black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
lt_green = (53,188,56)
silver = (192,192,192)
white = (255,255,255)



### Configure FIFO Pipe To Get Commands From PHP

rfPath = "/tmp/antenna-reader-screen.fifo"

controlleridPath = "/tmp/antenna-reader-screen/controllerid"
ipaddressPath = "/tmp/antenna-reader-screen/ipaddress"
pingtimePath = "/tmp/antenna-reader-screen/pingtime"
accesspoint1Path = "/tmp/antenna-reader-screen/accesspoint1"
accesspoint2Path = "/tmp/antenna-reader-screen/accesspoint2"
accesspoint3Path = "/tmp/antenna-reader-screen/accesspoint3"
uptimePath = "/tmp/antenna-reader-screen/uptime"


try:
	os.mkfifo(rfPath)

except OSError:
	pass



### Define Functions

def clear_screen():
	screen2.clear(black)
	screen2.display()

clear_screen()

print''
print''
print '     >>> GEN7 SCREEN SESSION INITIATED : Version 0.6'
print '       - Listening to FIFO Pipe'
print''

def idle_scr(): ####
        image = Image.open('./graphics/graphicidle_scr.png')
        image = image.rotate(180)
        screen1.display(image)

	

#### { MAIN } ####

image = Image.open('./graphics/frontscreen_arrow.png')
image = image.rotate(180)
screen2.display(image)

image = Image.open ('./graphics/ready_scr.png')
image = image.rotate(180)
screen1.display(image)

lastcommand = 'none'
ignoreindex = 0

valid = 'valid'
error = 'invalid'

lastlength = 1

while True:

	rp = open(rfPath, 'r')
	command_string = rp.read()
	
	#print command_string

	commands = command_string.split("\n")

	length = len(commands)
	length = length - 2	
	
        #print 'Length=',length
	#print 'commands[1]=',commands[length]

	rp.close() ### ### ###
	
	if length != lastlength:
		imagepath = './graphics/'
		scr_to_display = imagepath + commands[length]
		index = int(commands[length])

		#image = Image.open(scr_to_display)

		image = Image.open(screen[index])
        	image = image.rotate(180)
        	screen1.display(image)

		if index == 3:
			delay = 1
		else:
			delay = .5

		time.sleep(delay)

        	image = Image.open(ready_scr)
        	image = image.rotate(180)
        	screen1.display(image)

	lastlength = length


	
print ''
print '    >>> GEN7 SCREEN SESSION TERMINATED'
print ''
print ''

