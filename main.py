import socket
import machine
import network
light = 13
fan = 15
pir = 12
ip = network.WLAN(network.STA_IF).ifconfig()[0]
light_pin = machine.Pin(light,machine.Pin.OUT)
fan_pin = machine.Pin(fan, machine.Pin.OUT)
pir_pin = machine.Pin(pir, machine.Pin.IN)
adc = machine.ADC(0)
s = socket.socket()
s.bind((ip,7000))
s.listen(2)
flag = True
while flag:
    client, addr = s.accept()
    print(client,addr)
    data = client.recv(20)
    print(data)
    if(data==b'switch1_on'):
        light_pin.off()
    elif(data==b'switch1_off'):
        light_pin.on()
    elif(data==b'switch2_on'):
        fan_pin.off()
    elif(data==b'switch2_off'):
        fan_pin.on()
    elif(data==b'give_data'):
        pirvalue = str(pir_pin.value())
        gasvalue = str(adc.read())
        client.send((pirvalue+","+gasvalue).encode())
    elif(data==b'shutdown'):
        flag=False
    client.close()
