# PassiveModbusMonitor
Taps into existing Modbus RTU bus and passively decodes traffic

## Supported function codes
* Decode 0x01 Read Coils
* Decode 0x02 Read Discrete Inputs
* Decode 0x03 Read Holding Registers
* Decode 0x04 Read Input Registers

## Other features
* Automatically decodes a single-precision IEEE 754 float if read is quantity is two