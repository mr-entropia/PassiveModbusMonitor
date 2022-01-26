# PassiveModbusMonitor
Taps into existing Modbus RTU bus and passively decodes traffic

## Supported function codes
* Decode 0x01 Read Coils
* Decode 0x02 Read Discrete Inputs
* Decode 0x03 Read Holding Registers
* Decode 0x04 Read Input Registers

## Other features
* Automatically decodes a single-precision IEEE 754 float if read quantity for 0x03 is two

## Tested instruments
* Produal FLTA, wireless gateway for building automation
* Finder 7E64, single phase energy meter
* HK Instruments CDT2000, combination CO2/temperature/humidity transmitter

## Example output
In this example, we are decoding three different measurements from a Finder 7E64 energy meter: mains voltage, instantaneous current, mains frequency and finally instantaneous active power

```
2022-01-26 21:12:17.785499 Read holding register for device ID 1 , Start address = 4108 Quantity = 2
2022-01-26 21:12:17.817414 Response 1 from device ID 1 , data = 17258
2022-01-26 21:12:17.817414 Response 2 from device ID 1 , data = 12648
2022-01-26 21:12:17.817414 Float: 234.1929931640625
2022-01-26 21:12:17.833371 Read holding register for device ID 1 , Start address = 4118 Quantity = 2
2022-01-26 21:12:17.849834 Response 1 from device ID 1 , data = 16434
2022-01-26 21:12:17.849834 Response 2 from device ID 1 , data = 45089
2022-01-26 21:12:17.849834 Float: 2.7920000553131104
2022-01-26 21:12:17.865790 Read holding register for device ID 1 , Start address = 4152 Quantity = 2
2022-01-26 21:12:17.897705 Response 1 from device ID 1 , data = 16968
2022-01-26 21:12:17.897705 Response 2 from device ID 1 , data = 0
2022-01-26 21:12:17.897705 Float: 50.0
2022-01-26 21:12:17.913662 Read holding register for device ID 1 , Start address = 4134 Quantity = 2
2022-01-26 21:12:17.945577 Response 1 from device ID 1 , data = 17420
2022-01-26 21:12:17.945577 Response 2 from device ID 1 , data = 60457
2022-01-26 21:12:17.945577 Float: 563.6900024414062
```
