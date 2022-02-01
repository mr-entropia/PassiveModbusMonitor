# PassiveModbusMonitor
Taps into existing Modbus RTU bus and passively decodes traffic.

## Supported function codes
* 0x01 Read Coils
* 0x02 Read Discrete Inputs
* 0x03 Read Holding Registers
* 0x04 Read Input Registers
* 0x05 Write Single Coil
* 0x06 Write Single Register
* 0x0F Write Multiple Coils
* 0x10 Write Multiple Registers

## Other features
* Automatically decodes a single-precision IEEE 754 float if read quantity for 0x03 is two

## Tested instruments
* Produal FLTA, wireless gateway for building automation
* Finder 7E64, single phase energy meter
* HK Instruments CDT2000, combination CO2/temperature/humidity transmitter
* proconX modpoll 3.10, Modbus master simulator
* Fronius Symo, a solar inverter

## Example output
In this example, we are decoding three different measurements from a Finder 7E64 energy meter: mains voltage, instantaneous current, mains frequency, instantaneous active power as well as power factor (cos phi)

```
2022-01-27 22:32:05.833741 Read holding register for device ID 1 , Start address = 4108 Quantity = 2
2022-01-27 22:32:05.865656  * Response 1 from device ID 1 , data = 17253
2022-01-27 22:32:05.865656  * Response 2 from device ID 1 , data = 36241
2022-01-27 22:32:05.865656    * Float: 229.55299377441406
2022-01-27 22:32:05.881613 Read holding register for device ID 1 , Start address = 4118 Quantity = 2
2022-01-27 22:32:05.897570  * Response 1 from device ID 1 , data = 16440
2022-01-27 22:32:05.897570  * Response 2 from device ID 1 , data = 50332
2022-01-27 22:32:05.897570    * Float: 2.88700008392334
2022-01-27 22:32:05.913528 Read holding register for device ID 1 , Start address = 4152 Quantity = 2
2022-01-27 22:32:05.945443  * Response 1 from device ID 1 , data = 16968
2022-01-27 22:32:05.945443  * Response 2 from device ID 1 , data = 0
2022-01-27 22:32:05.945443    * Float: 50.0
2022-01-27 22:32:05.961400 Read holding register for device ID 1 , Start address = 4134 Quantity = 2
2022-01-27 22:32:05.977357  * Response 1 from device ID 1 , data = 17421
2022-01-27 22:32:05.977357  * Response 2 from device ID 1 , data = 58950
2022-01-27 22:32:05.977357    * Float: 567.5980224609375
2022-01-27 22:32:05.993314 Read holding register for device ID 1 , Start address = 4126 Quantity = 2
2022-01-27 22:32:06.025229  * Response 1 from device ID 1 , data = 16218
2022-01-27 22:32:06.025229  * Response 2 from device ID 1 , data = 57672
2022-01-27 22:32:06.025229    * Float: 0.8550000190734863
```

## License
GPL 3.0
