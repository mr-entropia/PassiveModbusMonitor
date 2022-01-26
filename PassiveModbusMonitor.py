# Passive Modbus RTU monitor
# Programmed by Entropia
# Inspired by Dala's EV Repair

import serial
import struct
import datetime

def HexToStr(input):
    return hex(ord(input))[2:]

def IntIEEE754Decode(input):
    packed_v = struct.pack('>l', input)
    return struct.unpack('>f', packed_v)[0]

# Combine two hex strings to one 16-bit int
def Combine(input1, input2):
    temp = int(input1, base=16) << 8
    temp += int(input2, base=16)
    return temp

# Combine four hex strings to one 32-bit int
def Combine4(input1, input2, input3, input4):
    temp = int(input1, base=16) << 24
    temp += int(input2, base=16) << 16
    temp += int(input3, base=16) << 8
    temp += int(input4, base=16)
    return temp

def tsprint(input):
    timestamp = datetime.datetime.now()
    print("[" + timestamp + "] " + input)

# All the magic happens here
def CheckModbusFunction(rxbuffer, nextframe, quantity):
    # Uncomment for debugging
    #print("Len:", len(rxbuffer), "Nextframe:", nextframe, "Quantity:", quantity, "Byte:", rxbuffer[len(rxbuffer) - 1])

    try:
        if(nextframe == 0 and len(rxbuffer) == 8):
            # Listening for known master requests
            if(rxbuffer[1] == '1'):
                # Read Coils
                deviceID = rxbuffer[0]
                address = int(rxbuffer[2], base=16) << 8
                address += int(rxbuffer[3], base=16)
                quantity = int(rxbuffer[4], base=16) << 8
                quantity += int(rxbuffer[5], base=16)
                timestamp = datetime.datetime.now()
                print(timestamp, "Read coils for device ID ", deviceID, ", Start address =", address, "Quantity =", quantity)
                if(quantity < 8):
                    quantity = 1
                else:
                    if(quantity % 8 == 0):
                        quantity /= 8
                    else:
                        quantity /= 8
                        quantity += 1
                return (True, 1, int(quantity))
            elif(rxbuffer[1] == '2'):
                # Read Discrete Inputs
                deviceID = rxbuffer[0]
                address = int(rxbuffer[2], base=16) << 8
                address += int(rxbuffer[3], base=16)
                quantity = int(rxbuffer[4], base=16) << 8
                quantity += int(rxbuffer[5], base=16)
                timestamp = datetime.datetime.now()
                print(timestamp, "Read discrete inputs for device ID", deviceID, ", Start address =", address, "Quantity =", quantity)
                if(quantity < 8):
                    quantity = 1
                else:
                    if(quantity % 8 == 0):
                        quantity /= 8
                    else:
                        quantity /= 8
                        quantity += 1
                return (True, 2, int(quantity))
            elif(rxbuffer[1] == '3'):
                # Read Holding Register
                deviceID = rxbuffer[0]
                address = int(rxbuffer[2], base=16) << 8
                address += int(rxbuffer[3], base=16)
                quantity = int(rxbuffer[4], base=16) << 8
                quantity += int(rxbuffer[5], base=16)
                timestamp = datetime.datetime.now()
                print(timestamp, "Read holding register for device ID", deviceID, ", Start address =", address, "Quantity =", quantity)
                return (True, 3, quantity)
            elif(rxbuffer[1] == '4'):
                # Read Input Register
                deviceID = rxbuffer[0]
                address = Combine(rxbuffer[2], rxbuffer[3])
                quantity = Combine(rxbuffer[4], rxbuffer[5])
                timestamp = datetime.datetime.now()
                print(timestamp, "Read input register for device ID", deviceID, ", Start address =", address, "Quantity =", quantity)
                return (True, 4, quantity)
            else:
                return (False, nextframe, quantity)
        elif(nextframe == 1 and len(rxbuffer) == (5 + quantity)):
            # Expecting reply from device for function code 1
            timestamp = datetime.datetime.now()
            deviceID = rxbuffer[0]
            for x in range(0, quantity):
                data = rxbuffer[x + 3]
                print(timestamp, "Response", (x + 1), "from device ID", deviceID, ", data =", data)
            return (True, 0, 0)
        elif(nextframe == 2 and len(rxbuffer) == (5 + quantity)):
            # Expecting reply from device for function code 2
            timestamp = datetime.datetime.now()
            deviceID = rxbuffer[0]
            for x in range(0, quantity):
                data = rxbuffer[x + 3]
                print(timestamp, "Response", (x + 1), "from device ID", deviceID, ", data =", data)
            return (True, 0, 0)
        elif(nextframe == 3 and len(rxbuffer) == (5 + (quantity * 2))):
            # Expecting reply from device for function code 3
            deviceID = rxbuffer[0]
            timestamp = datetime.datetime.now()
            for x in range(0, quantity):
                data = Combine(rxbuffer[(x * 2) + 3], rxbuffer[(x * 2) + 4])
                print(timestamp, "Response", (x + 1), "from device ID", deviceID, ", data =", data)
            if(quantity == 2):
                print(timestamp, "Float:", IntIEEE754Decode(Combine4(rxbuffer[3], rxbuffer[4], rxbuffer[5], rxbuffer[6])))
            return (True, 0, 0)
        elif(nextframe == 4 and len(rxbuffer) == (5 + (quantity * 2))):
            # Expecting reply from device for function code 4
            deviceID = rxbuffer[0]
            timestamp = datetime.datetime.now()
            for x in range(0, quantity):
                data = Combine(rxbuffer[(x * 2) + 3], rxbuffer[(x * 2) + 4])
                print(timestamp, "Response", (x + 1), "from device ID", deviceID, ", data =", data)
            return (True, 0, 0)
        else:
            return (False, nextframe, quantity)
    except:
        return (False, nextframe, quantity)

# Open serial port
ser = serial.Serial('COM3', 9600)

# Set up variables for first time use
framefinished = False
rxbuffer = list()
nextframe = 0
quantity = 0

# This main loop receives requests and responses and decodes them
while True:

    # Blocking loop for receiving frames
    while not framefinished:
        rxbuffer.append(HexToStr(ser.read(1)))
        (framefinished, nextframe, quantity) = CheckModbusFunction(rxbuffer, nextframe, quantity)

    # Succesfully received one frame, clear variables for next frame
    rxbuffer = list()
    framefinished = False