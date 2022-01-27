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
        if(nextframe == 0 and len(rxbuffer) == 7):
            # Listening for known master requests (0x0F and 0x10)
            if(rxbuffer[1] == 'f'):
                # Write Multiple Coils
                deviceID = rxbuffer[0]
                address = int(rxbuffer[2], base=16) << 8
                address += int(rxbuffer[3], base=16)
                quantity = int(rxbuffer[4], base=16) << 8
                quantity += int(rxbuffer[5], base=16)
                timestamp = datetime.datetime.now()
                print(timestamp, "Write multiple coils for device ID ", deviceID, ", Start address =", address, "Quantity =", quantity)
                if(quantity < 8):
                    quantity = 1
                else:
                    if(quantity % 8 == 0):
                        quantity /= 8
                    else:
                        quantity /= 8
                        quantity += 1
                return (True, 15, int(quantity))
            elif(rxbuffer[1] == '10'):
                # Write Multiple Registers
                deviceID = rxbuffer[0]
                address = int(rxbuffer[2], base=16) << 8
                address += int(rxbuffer[3], base=16)
                quantity = int(rxbuffer[4], base=16) << 8
                quantity += int(rxbuffer[5], base=16)
                timestamp = datetime.datetime.now()
                print(timestamp, "Write multiple registers for device ID ", deviceID, ", Start address =", address, "Quantity =", quantity)
                quantity *= 2
                return (True, 16, int(quantity))
            else:
                return (False, nextframe, quantity)
        elif(nextframe == 0 and len(rxbuffer) == 8):
            # Listening for known master requests (0x01 thru 0x06)
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
            elif(rxbuffer[1] == '5'):
                # Write Single Coil
                deviceID = rxbuffer[0]
                address = Combine(rxbuffer[2], rxbuffer[3])
                quantity = Combine(rxbuffer[4], rxbuffer[5])
                timestamp = datetime.datetime.now()
                print(timestamp, "Write single coil for device ID", deviceID, ", Start address =", address, "Quantity =", quantity)
                return (True, 5, quantity)
            elif(rxbuffer[1] == '6'):
                # Write Single Register
                deviceID = rxbuffer[0]
                address = Combine(rxbuffer[2], rxbuffer[3])
                quantity = Combine(rxbuffer[4], rxbuffer[5])
                timestamp = datetime.datetime.now()
                print(timestamp, "Write single register for device ID", deviceID, ", Start address =", address, "Quantity =", quantity)
                return (True, 6, quantity)
            else:
                return (False, nextframe, quantity)

        elif(nextframe == 1 and len(rxbuffer) == 5):
            # Exception for function code 1 (0x01)
            if(rxbuffer[1] == '81'):
                timestamp = datetime.datetime.now()
                if(rxbuffer[2] == '2'):
                    print(timestamp, " * Illegal Data Address exception")
                else:
                    print(timestamp, " * Exception! Code:", rxbuffer[2])
                return (True, 0, 0)
            else:
                return (False, nextframe, quantity)
        elif(nextframe == 1 and len(rxbuffer) == (5 + quantity)):
            # Expecting reply from device for function code 1 (0x01)
            timestamp = datetime.datetime.now()
            deviceID = rxbuffer[0]
            for x in range(0, quantity):
                data = rxbuffer[x + 3]
                print(timestamp, " * Response", (x + 1), "from device ID", deviceID, ", data =", data)
            return (True, 0, 0)

        elif(nextframe == 2 and len(rxbuffer) == 5):
            # Exception for function code 2 (0x02)
            if(rxbuffer[1] == '82'):
                timestamp = datetime.datetime.now()
                if(rxbuffer[2] == '2'):
                    print(timestamp, " * Illegal Data Address exception")
                else:
                    print(timestamp, " * Exception! Code:", rxbuffer[2])
                return (True, 0, 0)
            else:
                return (False, nextframe, quantity)
        elif(nextframe == 2 and len(rxbuffer) == (5 + quantity)):
            # Expecting reply from device for function code 2 (0x02)
            timestamp = datetime.datetime.now()
            deviceID = rxbuffer[0]
            for x in range(0, quantity):
                data = rxbuffer[x + 3]
                print(timestamp, " * Response", (x + 1), "from device ID", deviceID, ", data =", data)
            return (True, 0, 0)

        elif(nextframe == 3 and len(rxbuffer) == 5):
            # Exception for function code 3 (0x03)
            if(rxbuffer[1] == '83'):
                timestamp = datetime.datetime.now()
                if(rxbuffer[2] == '2'):
                    print(timestamp, " * Illegal Data Address exception")
                else:
                    print(timestamp, " * Exception! Code:", rxbuffer[2])
                return (True, 0, 0)
            else:
                return (False, nextframe, quantity)
        elif(nextframe == 3 and len(rxbuffer) == (5 + (quantity * 2))):
            # Expecting reply from device for function code 3 (0x03)
            deviceID = rxbuffer[0]
            timestamp = datetime.datetime.now()
            for x in range(0, quantity):
                data = Combine(rxbuffer[(x * 2) + 3], rxbuffer[(x * 2) + 4])
                print(timestamp, " * Response", (x + 1), "from device ID", deviceID, ", data =", data)
            if(quantity == 2):
                print(timestamp, "   * Float:", IntIEEE754Decode(Combine4(rxbuffer[3], rxbuffer[4], rxbuffer[5], rxbuffer[6])))
            return (True, 0, 0)

        elif(nextframe == 4 and len(rxbuffer) == 5):
            # Exception for function code 4 (0x04)
            if(rxbuffer[1] == '84'):
                timestamp = datetime.datetime.now()
                if(rxbuffer[2] == '2'):
                    print(timestamp, " * Illegal Data Address exception")
                else:
                    print(timestamp, " * Exception! Code:", rxbuffer[2])
                return (True, 0, 0)
            else:
                return (False, nextframe, quantity)
        elif(nextframe == 4 and len(rxbuffer) == (5 + (quantity * 2))):
            # Expecting reply from device for function code 4 (0x04)
            deviceID = rxbuffer[0]
            timestamp = datetime.datetime.now()
            for x in range(0, quantity):
                data = Combine(rxbuffer[(x * 2) + 3], rxbuffer[(x * 2) + 4])
                print(timestamp, " * Response", (x + 1), "from device ID", deviceID, ", data =", data)
            return (True, 0, 0)

        elif(nextframe == 5 and len(rxbuffer) == 5):
            # Exception for function code 5 (0x05)
            if(rxbuffer[1] == '85'):
                timestamp = datetime.datetime.now()
                if(rxbuffer[2] == '2'):
                    print(timestamp, " * Illegal Data Address exception")
                else:
                    print(timestamp, " * Exception! Code:", rxbuffer[2])
                return (True, 0, 0)
            else:
                return (False, nextframe, quantity)
        elif(nextframe == 5 and len(rxbuffer) == 8):
            # Expecting reply from device for function code 5 (0x05)
            deviceID = rxbuffer[0]
            address = Combine(rxbuffer[2], rxbuffer[3])
            data = Combine(rxbuffer[4], rxbuffer[5])
            timestamp = datetime.datetime.now()
            print(timestamp, " * Response from device ID", deviceID, " Address", address, "is now", data)

        elif(nextframe == 6 and len(rxbuffer) == 5):
            # Exception for function code 6 (0x06)
            if(rxbuffer[1] == '86'):
                timestamp = datetime.datetime.now()
                if(rxbuffer[2] == '2'):
                    print(timestamp, " * Illegal Data Address exception")
                else:
                    print(timestamp, " * Exception! Code:", rxbuffer[2])
                return (True, 0, 0)
            else:
                return (False, nextframe, quantity)
        elif(nextframe == 6 and len(rxbuffer) == 8):
            # Expecting reply from device for function code 6 (0x06)
            deviceID = rxbuffer[0]
            address = Combine(rxbuffer[2], rxbuffer[3])
            data = Combine(rxbuffer[4], rxbuffer[5])
            timestamp = datetime.datetime.now()
            print(timestamp, " * Response from device ID", deviceID, " Address", address, "is now", data)

        elif(nextframe == 15 and len(rxbuffer) == (quantity + 7)):
            # Exception for function code 15 (0x0F)
            if(rxbuffer[quantity + 3] == '8f'):
                timestamp = datetime.datetime.now()
                if(rxbuffer[quantity + 4] == '2'):
                    print(timestamp, " * Illegal Data Address exception")
                else:
                    print(timestamp, " * Exception! Code:", rxbuffer[quantity + 4])
                return (True, 0, 0)
            else:
                return (False, nextframe, quantity)
        elif(nextframe == 15 and len(rxbuffer) == (quantity + 3 + 7)):
            # Output values are still being sent, also expecting device reply for function code 15 (0x0F)
            deviceID = rxbuffer[quantity + 3]
            address = Combine(rxbuffer[quantity + 4], rxbuffer[quantity + 5])
            timestamp = datetime.datetime.now()
            for x in range (0, quantity):
                print(timestamp, " * Write command", x, ":", rxbuffer[x])
            return (True, 0, 0)

        elif(nextframe == 16 and len(rxbuffer) == (quantity + 7)):
            # Exception for function code 16 (0x10)
            if(rxbuffer[quantity + 3] == '90'):
                timestamp = datetime.datetime.now()
                if(rxbuffer[quantity + 4] == '2'):
                    print(timestamp, " * Illegal Data Address exception")
                else:
                    print(timestamp, " * Exception! Code:", rxbuffer[quantity + 4])
                return (True, 0, 0)
            else:
                return (False, nextframe, quantity)
        elif(nextframe == 16 and len(rxbuffer) == (quantity + 3 + 7)):
            # Output values are still being sent, also expecting device reply for function code 16 (0x10)
            deviceID = rxbuffer[quantity + 3]
            address = Combine(rxbuffer[quantity + 4], rxbuffer[quantity + 5])
            timestamp = datetime.datetime.now()
            for x in range (0, quantity):
                print(timestamp, " * Write command", x, ":", rxbuffer[x])
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