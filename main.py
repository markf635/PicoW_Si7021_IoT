import rp2
import network
import ubinascii
from secrets import secrets
from machine import Pin, I2C
import utime
import si7021
from umqtt.simple import MQTTClient

ssid = secrets['ssid']
pw = secrets['pw']

rp2.country('US')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm = 0xa11140) #disable powersaving mode
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
wlan.connect(ssid, pw)

timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >- 3:
        break
    timeout -= 1
    print('waiting for connection...')
    utime.sleep(1)
    
# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    led = machine.Pin('LED', machine.Pin.OUT)
    for i in range(num_blinks):
        led.on()
        utime.sleep(.2)
        led.off()
        utime.sleep(.2)
    
# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth

wlan_status = wlan.status()
blink_onboard_led(wlan_status)
    
#Handle connection error
if wlan.status() != 3:
    raise RuntimeError('Wi-Fi connection failed')
else:
    print('Connected to ' + wlan.config('essid'))
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    print('mac = ' + mac)
    
#initialise I2C
i2c = machine.I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

temp_sensor = si7021.Si7021(i2c)
print('Identifier:          {value}'.format(value=temp_sensor.identifier))
print('Serial:              {value}'.format(value=temp_sensor.serial) + '\n')

def connectMQTT():
    client = MQTTClient(client_id=b"device_name", server=b"___cluster_url.hivemq.cloud___", port=0, user=b"___hivemq_MQTT_username___", password=b"___hivemq_MQTT_password___",
                        keepalive=7200, ssl=True, ssl_params={'server_hostname':'___cluster_url.hivemq.cloud___'}
                        )
    client.connect()
    return client

client = connectMQTT()

def publish(topic, value):
    print(topic)
    print(value)
    client.publish(topic, value)
    print("publish Done")
    
while True:
    #Read sensor data
    Celsius = '{value}'.format(value=temp_sensor.temperature)
    Humidity = '{value}'.format(value=temp_sensor.relative_humidity)
    Fahrenheit = '{value}'.format(value=si7021.convert_celcius_to_fahrenheit(temp_sensor.temperature))
    
    publish('picow/Celsius', Celsius)
    publish('picow/Fahrenheit', Fahrenheit)
    publish('picow/Humidity', Humidity)
    utime.sleep(5)
    
