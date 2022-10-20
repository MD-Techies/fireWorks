import network
import socket
import time
import machine 
from machine import Pin
 
# Various variables for GPIO pins on board & LED
led = machine.Pin("LED", machine.Pin.OUT)
p5  = machine.Pin(5, Pin.OUT)
p15 = machine.Pin(15, Pin.OUT)

# SSID and Password to wifi
ssid = 'PICO'
password = '123456789'


# HTML page to be served to user
html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
    <style> 
        * {
        margin: 0;
        padding: 0;
        }
        body {background-color: black;}
        header {
            color: red;
            border: 12px orangered solid;
            text-align: center;
            text-decoration: double;
        }
        p {
            color: red;
            text-align: center;
            width: 50%;
            margin: 25px auto;
        }
        strong {
            text-transform: capitalize;
        }
        .flexbox {
            display: flex;
            flex-direction: column;

        }
        .ULButtons {
            padding: 10px;
            width: fit-content;
            height: fit-content;
            margin: 10px auto;
            border: 3px orangered solid;
            display: inline-block;
        }
        .b1 {
            padding: 5px;
            margin: 10px;
            font-size: larger;
            width: 100px;
            height: 25px;
            border: 2px orangered solid;
            border-radius: 5px;
            text-align: center;
            box-shadow: 2px 5px 10px inset orange;
        }
        

    </style>
</head>
<body>
<header>
    <h1>
        Controlled Chaos FireWorks Display
    </h1>
</header>
<div class="flexbox">
    <div class="ULButtons">
        <div class="b1"><a href="/launcher1">Launcher 1</a></div>
        <div class="b1"><a href="/launcher2">Launcher 2</a></div>
        <div class="b1"><a href="/launchALL">Launch ALL</a></div>
    </div>
</div>
<div>
    <p>As the creator of this device I love watching fireworks explode.  What I do not like is almost <strong> blowing my fingers OFF </strong> which is why we now have the Fireworks display before you. Connect via the devices wifi load your morters stand back and launch.</p>
</div>


</body>
</html>
"""

# Functions to open GPIO ports 
def sparkP15OneSecond():
    p15.value(1)
    time.sleep(1)
    p15.value(0)
    return

def sparkP5OneSecond():
    p5.value(1)
    time.sleep(1)
    p5.value(0)
    return

def sparkALL():
    p5.value(1)
    p15.value(1)
    time.sleep(1)
    p5.value(0)
    p15.value(0)

def ledLightOneSecond():
    led.value(1)
    time.sleep(1)
    led.value(0)
    return


# Activating Wifi Station 
wlan = network.WLAN(network.AP_IF)
wlan.config(essid=ssid, password=password) 
wlan.active(True)
print(wlan.ifconfig()[0])
 
# Open socket listen for any request ('0.0.0.0' == listen from any IP)  #[0]IP  [-1]Port#
addres = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
 
# Create Socket object
s = socket.socket()

# Bind addres to socket
s.bind(addres)

# Listening for connections
s.listen(1)
 


 

while True:
    try:
        # Socket object.accept returns a tuple
        cl, addr = s.accept()
        # cl (client) is a new socket object

        request = cl.recv(1024)
        request = str(request)
        
        
        # returns index where '/launcher' begins === 6
        launcher1 = request.find('/launcher1')
        launcher2 = request.find('/launcher2')
        launchALL = request.find('/launchALL')
        

        if launcher1 == 6:
            led.value(1)
            sparkP5OneSecond()
            led.value(0)
            
        if launcher2 == 6:
            led.value(1)
            sparkP15OneSecond()
            led.value(0)
            
        if launchALL == 6:
            led.value(1)
            sparkALL()
            led.value(0)
            
        
        
        
        # send a response to user who connected / Send our static HTML page
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(html)
        cl.close()
 
    except OSError as e:
        cl.close()
        print('connection closed')

