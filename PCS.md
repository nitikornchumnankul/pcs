Protocol for External ModBus Communication of


PCS_V2.3

### **Q/YB**

## **Beijing IN-POWER Electric Co., Ltd.**

# **Protocol for External ModBus** **Communication of PCS**

#### Controlled state: **Document No.:** **Document version:** **Number of revisions:**

|Col1|Approved by|Reviewed by|Prepared by|
|---|---|---|---|
|**Signature:**|||**Peng Yu**|
|**Date:**|||**2023.06.13**|



Published on December 21, 2022 Implemented on December 21, 2022

### **Published by Beijing IN-POWER Electric Co., Ltd.**


P 1/17


Protocol for External ModBus Communication of


PCS_V2.3


















|Description|of Document Configuration|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
|**Document**<br>**name**|Protocol for External ModBus Communication of PCS|Protocol for External ModBus Communication of PCS|Protocol for External ModBus Communication of PCS|Protocol for External ModBus Communication of PCS|Protocol for External ModBus Communication of PCS|Protocol for External ModBus Communication of PCS|
|**Scope of**<br>**application**|||||||
|**Creation**|**Prepared by:**|Peng Yu|**Date:**|2021.11.20|**Version No.:**|V1.0|
|**Creation**|Newly created.|Newly created.|Newly created.|Newly created.|Newly created.|Newly created.|
|**Revision**|**Prepared by:**|Peng Yu|**Date:**|2021.12.20|**Version No.:**|V1.1|
|**Revision**|1.<br>Revised to add split-phase active and reactive power settings.|1.<br>Revised to add split-phase active and reactive power settings.|1.<br>Revised to add split-phase active and reactive power settings.|1.<br>Revised to add split-phase active and reactive power settings.|1.<br>Revised to add split-phase active and reactive power settings.|1.<br>Revised to add split-phase active and reactive power settings.|
|**Revision**|**Prepared by:**|Peng Yu|**Date:**|2022.1.19|**Version No.:**|V1.2|
|**Revision**|1.<br>Revised the protocol of CMS to BMS communication data.<br>2.<br>Modified the definition of fault word, and added PCS and DCDC communication fault, EMS<br>communication fault and dry contact input fault.<br>3.<br>Added the rules for offset address under multi-module parallel connection.<br>4.<br>Added the description that DCDC system is not included.|1.<br>Revised the protocol of CMS to BMS communication data.<br>2.<br>Modified the definition of fault word, and added PCS and DCDC communication fault, EMS<br>communication fault and dry contact input fault.<br>3.<br>Added the rules for offset address under multi-module parallel connection.<br>4.<br>Added the description that DCDC system is not included.|1.<br>Revised the protocol of CMS to BMS communication data.<br>2.<br>Modified the definition of fault word, and added PCS and DCDC communication fault, EMS<br>communication fault and dry contact input fault.<br>3.<br>Added the rules for offset address under multi-module parallel connection.<br>4.<br>Added the description that DCDC system is not included.|1.<br>Revised the protocol of CMS to BMS communication data.<br>2.<br>Modified the definition of fault word, and added PCS and DCDC communication fault, EMS<br>communication fault and dry contact input fault.<br>3.<br>Added the rules for offset address under multi-module parallel connection.<br>4.<br>Added the description that DCDC system is not included.|1.<br>Revised the protocol of CMS to BMS communication data.<br>2.<br>Modified the definition of fault word, and added PCS and DCDC communication fault, EMS<br>communication fault and dry contact input fault.<br>3.<br>Added the rules for offset address under multi-module parallel connection.<br>4.<br>Added the description that DCDC system is not included.|1.<br>Revised the protocol of CMS to BMS communication data.<br>2.<br>Modified the definition of fault word, and added PCS and DCDC communication fault, EMS<br>communication fault and dry contact input fault.<br>3.<br>Added the rules for offset address under multi-module parallel connection.<br>4.<br>Added the description that DCDC system is not included.|
|**Revision**|**Prepared by:**|Peng Yu|**Date:**|2022.1.25|**Version No.:**|V1.3|
|**Revision**|1.<br>Added the upper computer to display the above fault code for query.<br>2.<br>Added the EMS communication fault as well as DC fuse and emergency stop input fault.|1.<br>Added the upper computer to display the above fault code for query.<br>2.<br>Added the EMS communication fault as well as DC fuse and emergency stop input fault.|1.<br>Added the upper computer to display the above fault code for query.<br>2.<br>Added the EMS communication fault as well as DC fuse and emergency stop input fault.|1.<br>Added the upper computer to display the above fault code for query.<br>2.<br>Added the EMS communication fault as well as DC fuse and emergency stop input fault.|1.<br>Added the upper computer to display the above fault code for query.<br>2.<br>Added the EMS communication fault as well as DC fuse and emergency stop input fault.|1.<br>Added the upper computer to display the above fault code for query.<br>2.<br>Added the EMS communication fault as well as DC fuse and emergency stop input fault.|
|**Revision**|**Prepared by:**|Peng Yu|**Date:**|2022.2.20|**Version No.:**|V1.4|
|**Revision**|1.<br>Deleted the description of the temporarily unsupported RS485 from the hardware part of the<br>protocol.|1.<br>Deleted the description of the temporarily unsupported RS485 from the hardware part of the<br>protocol.|1.<br>Deleted the description of the temporarily unsupported RS485 from the hardware part of the<br>protocol.|1.<br>Deleted the description of the temporarily unsupported RS485 from the hardware part of the<br>protocol.|1.<br>Deleted the description of the temporarily unsupported RS485 from the hardware part of the<br>protocol.|1.<br>Deleted the description of the temporarily unsupported RS485 from the hardware part of the<br>protocol.|
|**Revision**|**Prepared by:**|Peng Yu|**Date:**|2022.9.16|**Version No.:**|V1.6|
|**Revision**|1.<br>RS485 is supported.|1.<br>RS485 is supported.|1.<br>RS485 is supported.|1.<br>RS485 is supported.|1.<br>RS485 is supported.|1.<br>RS485 is supported.|
|**Revision**|**Prepared by:**|Peng Yu|**Date:**|2022.9.30|**Version No.:**|V1.7|
|**Revision**|1.<br>Modified the DCDC fault wordparsing to fault code determination.|1.<br>Modified the DCDC fault wordparsing to fault code determination.|1.<br>Modified the DCDC fault wordparsing to fault code determination.|1.<br>Modified the DCDC fault wordparsing to fault code determination.|1.<br>Modified the DCDC fault wordparsing to fault code determination.|1.<br>Modified the DCDC fault wordparsing to fault code determination.|
|**Revision**|**Prepared by:**|Peng Yu|**Date:**|2022.12.18|**Version No.:**|V1.8|
|**Revision**|1.<br>Added one PCS fault word 5, address 256, and addedphase N current display.|1.<br>Added one PCS fault word 5, address 256, and addedphase N current display.|1.<br>Added one PCS fault word 5, address 256, and addedphase N current display.|1.<br>Added one PCS fault word 5, address 256, and addedphase N current display.|1.<br>Added one PCS fault word 5, address 256, and addedphase N current display.|1.<br>Added one PCS fault word 5, address 256, and addedphase N current display.|
|**Revision**|**Prepared by:**|Peng Yu|**Date:**|2022.12.21|**Version No.:**|V1.9|
|**Revision**|1.<br>Added BMS dry contact fault valid status to remote signaling address 94, corresponding to<br>PCS version 641.0 or above.|1.<br>Added BMS dry contact fault valid status to remote signaling address 94, corresponding to<br>PCS version 641.0 or above.|1.<br>Added BMS dry contact fault valid status to remote signaling address 94, corresponding to<br>PCS version 641.0 or above.|1.<br>Added BMS dry contact fault valid status to remote signaling address 94, corresponding to<br>PCS version 641.0 or above.|1.<br>Added BMS dry contact fault valid status to remote signaling address 94, corresponding to<br>PCS version 641.0 or above.|1.<br>Added BMS dry contact fault valid status to remote signaling address 94, corresponding to<br>PCS version 641.0 or above.|
|**Revision**|**Prepared by:**|Peng Yu|**Date:**|2023.1.3|**Version No.:**|V2.0|
|**Revision**|1.<br>Added primary FM parameter address 319 frequency dead zone, address 320 active power<br>FM coefficient K.|1.<br>Added primary FM parameter address 319 frequency dead zone, address 320 active power<br>FM coefficient K.|1.<br>Added primary FM parameter address 319 frequency dead zone, address 320 active power<br>FM coefficient K.|1.<br>Added primary FM parameter address 319 frequency dead zone, address 320 active power<br>FM coefficient K.|1.<br>Added primary FM parameter address 319 frequency dead zone, address 320 active power<br>FM coefficient K.|1.<br>Added primary FM parameter address 319 frequency dead zone, address 320 active power<br>FM coefficient K.|
|**Revision**|**Prepared by:**|Peng Yu|**Date:**|2023.6.13|**Version No.:**|V2.2|
|**Revision**|1.<br>Redefined the function of addresses 280-295. Supported read-only and read-write.|1.<br>Redefined the function of addresses 280-295. Supported read-only and read-write.|1.<br>Redefined the function of addresses 280-295. Supported read-only and read-write.|1.<br>Redefined the function of addresses 280-295. Supported read-only and read-write.|1.<br>Redefined the function of addresses 280-295. Supported read-only and read-write.|1.<br>Redefined the function of addresses 280-295. Supported read-only and read-write.|
|**Revision**|**Prepared by:**|Peng Yu|**Date:**|2023.9.1|**Version No.:**|V2.3|
|**Revision**|1.<br>Modified the network port speed as 100M full duplex.<br>2.<br>Added temperature display to addresses 257-261.<br>3.<br>Added DC component overrun to fault word 3.<br>4.<br>Modified communication use cases.|1.<br>Modified the network port speed as 100M full duplex.<br>2.<br>Added temperature display to addresses 257-261.<br>3.<br>Added DC component overrun to fault word 3.<br>4.<br>Modified communication use cases.|1.<br>Modified the network port speed as 100M full duplex.<br>2.<br>Added temperature display to addresses 257-261.<br>3.<br>Added DC component overrun to fault word 3.<br>4.<br>Modified communication use cases.|1.<br>Modified the network port speed as 100M full duplex.<br>2.<br>Added temperature display to addresses 257-261.<br>3.<br>Added DC component overrun to fault word 3.<br>4.<br>Modified communication use cases.|1.<br>Modified the network port speed as 100M full duplex.<br>2.<br>Added temperature display to addresses 257-261.<br>3.<br>Added DC component overrun to fault word 3.<br>4.<br>Modified communication use cases.|1.<br>Modified the network port speed as 100M full duplex.<br>2.<br>Added temperature display to addresses 257-261.<br>3.<br>Added DC component overrun to fault word 3.<br>4.<br>Modified communication use cases.|



P 2/17


Protocol for External ModBus Communication of


PCS_V2.3


**I.** **Overview**


This protocol is applicable to the communication between the energy storage system of PCS and the

background monitoring system. It can read the running information and fault status of the inverter in

real time, and control the running of the system.


**II.** **Physical Interface**


1. Ethernet


Transmission mode: ModBus Tcp


Network card type: 100M full duplex


Maximum frame length: 263 bytes


Maximum slave response time: 20ms


Minimum master polling interval: 5ms


IP address: 192.168.0.20


Port No.: 502


Check mode: Hardware check


Modbus station address: 1 by default


2. RS485


Transmission mode: ModBus RTU


Baud rate: 4800, 9600, 19200, etc. may be set; 9600 by default


Check bit: No check;


Data bit: 8 bits;


Stop bit: 1 bit;


Frame interval: Not less than 3.5 bytes of time;


Intra-frame character interval: Not more than 1.5 bytes of time;


Maximum frame length: 100 bytes;


Maximum slave response time: 150 bytes of time;


Minimum master polling interval: 100 bytes of time;


Check type: CRC16 check, generator polynomial, with the low byte before the high byte;


Modbus station address: 1 by default.


**III.** **Protocol Description**


P 3/17


Protocol for External ModBus Communication of


PCS_V2.3


Based on the different medium imported on the DC side of PCS, the definition of the register address

is different. When DCDC is connected on the DC side of PCS, the labelled address in *(1) is valid.

When the energy storage device connected to the PCS system is a battery, *(2) is valid. When the

connected energy storage device is a super capacitor or others, *(2) is invalid, and it needs to be

communicated separately.


Based on the different mode of import on the DC side of PCS, the definition of the register address

is different. When the number of PCS modules connected to the energy storage system is greater than

or equal to 2, if the DC side of PCS is connected in parallel, the definition of the register address

remains unchanged. If the DC side is a separate system, the access address of N#PCS (N>=2) is

+1000 offset from the access address of 1#PCS.


**3.1** **Data type**


**Table 1: Data Type**

|Datatype|Explanation|
|---|---|
|Signed integer_16|16-bit character, 2 complement|
|Signed integer_32|32-bit word, two consecutive Modbus addresses are used for<br>transmission. The low word is located at the Modbus low address.|
|Unsigned integer_16|16-bit word|
|Unsigned integer_32|32-bit word, two consecutive Modbus addresses are used for<br>transmission. The low word is located at the Modbus low address.|
|Singleprecision floating point|32-bit word, IEEE-754 floating point format|



The data transmission sequence is in big-endian mode, with the high byte before the low byte.


For example: For U16 data 0x0102, the transmission sequence is 01, 02.


**3.2** **Function code**


**Table 2: Function Code**

|Functioncode|Function|Correspondingaddresstype|
|---|---|---|
|0x01|Read slave coil register, bit operation|0x|
|0x02|Read discrete input register, bit operation|1x|
|0x03|Read<br>multiple<br>holding<br>registers,<br>byte<br>operation|4x|
|0x04|Read multiple input registers, byte operation|3x|
|0x05|Write coil register, bit operation|0x|
|0x06|Write single holding register, byte operation|4x|
|0x10|Write<br>multiple<br>holding<br>registers,<br>byte<br>operation|4x|



**IV.** **Address Information**


**4.1** **Definition of remote control variable address (address type 0x)**


(1) Write single coil: (take ModBus-Tcp format as an example)


0xFF00 request output is ON, and 0x000 request output is OFF


P 4/17


Protocol for External ModBus Communication of


PCS_V2.3


Request: MBAP function code Output address H Output address L Output value H Output value L

(12 bytes in total)


Response: MBAP function code Output address H Output address L Output value H Output value L

(12 bytes in total)


For example: Set the coil with the address as 0x0002 in the slave station to ON: 00 01 00 00 00 06

01 05 00 02 FF 00


Response: Write successfully-00 01 00 00 00 06 01 05 00 03 FF 00











|No<br>.|Modbus<br>address|Name|Permission|Datatype|Coefficient|Unit|Remarks|
|---|---|---|---|---|---|---|---|
|1|00001|Fault reset|Read-write|Bool|1|1|1-Reset|
|2|00002|Device startup|Read-write|Bool|1|1|1-Startup|
|3|00003|Device shutdown|Read-write|Bool|1|1|1-Shutdown|
|4|00004|Remote<br>emergency stop|Read-write|Bool|1|1|1-Emergency stop|
|5|00005|Accumulated<br>charging power<br>reset to zero|Read-write|Bool|1|1|1-Reset to zero|
|6|00006|Accumulated<br>discharging<br>power reset to<br>zero|Read-write|Bool|1|1|1-Reset to zero|
|7|00007|Remote/local<br>settings|Read-write|Bool|1|1|1-Remote; 0-Local|
|8|00008|Reserve|Read-write|Bool|1|1||
|9|00009|Reserve|Read-write|Bool|1|1||
|10|00010|Reserve|Read-write|Bool|1|1||
|11|00011|Reserve|Read-write|Bool|1|1||
|12|00012|Reserve|Read-write|Bool|1|1||
|13|00013|Reserve|Read-write|Bool|1|1||
|14|00014|Reserve|Read-write|Bool|1|1||
|15|00015|Reserve|Read-write|Bool|1|1||
|16|00016|Reserve|Read-write|Bool|1|1||


**4.2** **Definition of remote signaling data address (address type 1x)**


(1) Read the input status of continuous discrete quantities from the slave station (take ModBus-Tcp

format as an example)


Request: MBAP function code Start address H Start address L Number H Number L (12 bytes in total)


Response: MBAP function code Data length Data (length: 9+ceil (number/8))


Read 16 inputs of discrete quantities starting from address 81 00 01 00 00 00 06 01 02 00 51 00 10


Response: 00 01 00 00 00 06 01 02 02 81 00


The data length is 0x02 bytes, and the data is 0x81 00, which means that the device address 81 and

device address 88 are ON, the device is in the grid-connected shutdown status, and the rest are OFF.


P 5/17


Protocol for External ModBus Communication of


PCS_V2.3


It is recommended to read 16 consecutive statuses starting from address 81.

















|No<br>.|Modbus<br>address|Name|Permission|Datatype|Coefficient|Unit|Remarks|
|---|---|---|---|---|---|---|---|
|1|00081|Shutdown status|Read-only|Bool|1|1|1-Shutdown|
|2|00082|Standby status|Read-only|Bool|1|1|1-Standby|
|3|00083|Running status|Read-only|Bool|1|1|1-Running|
|4|00084|Total fault status|Read-only|Bool|1|1|1-Fault|
|5|00085|Total alarm status|Read-only|Bool|1|1|1-Alarm|
|6|00086|Remote/local<br>status|Read-only|Bool|1|1|1-Remote; 0-Local|
|7|00087|Emergency stop<br>input status|Read-only|Bool|1|1|1-Emergency stop<br>valid|
|8|00088|Grid-connected<br>status|Read-only|Bool|1|1|1-Grid-connected|
|9|00089|VF grid-<br>disconnected<br>status|Read-only|Bool|1|1|1-VF grid-<br>disconnected|
|10|00090|Overload derating|Read-only|Bool|1|1|1-Overload occurred|
|11|00091|Reserve|Read-only|Bool|1|1||
|12|00092|Reserve|Read-only|Bool|1|1||
|13|00093|Reserve|Read-only|Bool|1|1||
|14|00094|BMS dry contact<br>input|Read-only|Bool|1|1|1-Fault valid|
|15|00095|Reserve|Read-only|Bool|1|1||
|16|00096|Reserve|Read-only|Bool|1|1||


**4.3** **Definition of remote metering data address (address type 3x)**


(1) Read the analog quantity information and fault word of device running from the slave station.

(take ModBus-Tcp format as an example)


Request: MBAP function code Start address H Start address L Number of registers H Number of

registers L (12 bytes in total)


Response: MBAP function code Data length Register data (length: 9 + number of registers × 2)


For example: Read the data of the register of which the start address is 201 and the number is 0x0003:


00 01 00 00 00 06 01 04 00 C9 00 03


Response: The data length is 0x06, and the phase A voltage of port is 223.0V, phase B 223.0V, phase

C 223.0V


00 01 00 00 00 0D 01 04 06 08 B6 08 B6 08 B6












|No<br>.|Modbus<br>address|Name|Permission|Data<br>type|Coefficient|Unit|Remarks|
|---|---|---|---|---|---|---|---|
|1|00201|Phase A voltage of PCS<br>port|Read-only|U16|0.1|V||
|2|00202|Phase B voltage of PCS<br>port|Read-only|U16|0.1|V||



P 6/17


Protocol for External ModBus Communication of


PCS_V2.3







|3|00203|PhaseCvoltageofPCS<br>port|Read -only|U16|01<br>.|V|Col8|
|---|---|---|---|---|---|---|---|
|4|00204|Phase A current of PCS<br>output|Read-only|S16|0.1|A||
|5|00205|Phase B current of PCS<br>output|Read-only|S16|0.1|A||
|6|00206|Phase C current of PCS<br>output|Read-only|S16|0.1|A||
|7|00207|Grid frequency|Read-only|U16|0.01|Hz||
|8|00208|Active power of phase A<br>output of PCS|Read-only|S16|0.1|kW||
|9|00209|Active power of phase B<br>output of PCS|Read-only|S16|0.1|kW||
|10|00210|Active power of phase C<br>output of PCS|Read-only|S16|0.1|kW||
|11|00211|Active power of total<br>output of PCS|Read-only|S16|0.1|kW||
|12|00212|Reactive power of phase<br>A output of PCS|Read-only|S16|0.1|kVar||
|13|00213|Reactive power of phase<br>B output of PCS|Read-only|S16|0.1|kVar||
|14|00214|Reactive power of phase<br>C output of PCS|Read-only|S16|0.1|kVar||
|15|00215|Reactive power of total<br>output of PCS|Read-only|S16|0.1|kVar||
|16|00216|Apparent power of phase<br>A output of PCS|Read-only|U16|0.1|kVA||
|17|00217|Apparent power of phase<br>B output of PCS|Read-only|U16|0.1|kVA||
|18|00218|Apparent power of phase<br>C output of PCS|Read-only|U16|0.1|kVA||
|19|00219|Apparent power of total<br>output of PCS|Read-only|U16|0.1|kVA||
|20|00220|Phase A power factor of<br>PCS output|Read-only|U16|0.001|||
|21|00221|Phase B power factor of<br>PCS output|Read-only|U16|0.001|||
|22|00222|Phase C power factor of<br>PCS output|Read-only|U16|0.001|||
|23|00223|Total power factor of<br>PCS output|Read-only|U16|0.001|||
|24|00224|PCS input power|Read-only|S16|0.1|kW|PCS DC input<br>power|
|25|00225|PCS input voltage|Read-only|S16|0.1|V|PCS DC input<br>voltage|
|26|00226|PCS input current|Read-only|S16|0.1|A|PCS DC input<br>current|


P 7/17


Protocol for External ModBus Communication of


PCS_V2.3















|27|00227|PCSradiatortemperature|Read -only|S16|1|℃|IGBTmaximum<br>temperature|
|---|---|---|---|---|---|---|---|
|28|00228|Reserve|Read-only|S16|1|||
|29|00229|Reserve|Read-only|S16|1|||
|30|00230|PCS AC accumulated<br>charging power low 16<br>bits|Read-only|U16|0.001|kWh||
|31|00231|PCS AC accumulated<br>charging power high 16<br>bits|Read-only|U16|0.001|kWh||
|32|00232|PCS AC accumulated<br>discharging power low<br>16 bits|Read-only|U16|0.001|kWh||
|33|00233|PCS AC accumulated<br>discharging power high<br>16 bits|Read-only|U16|0.001|kWh||
|34|00234|PCS DC accumulated<br>charging power low 16<br>bits|Read-only|U16|0.001|kWh||
|35|00235|PCS DC accumulated<br>charging power high 16<br>bits|Read-only|U16|0.001|kWh||
|36|00236|PCS DC accumulated<br>discharging power low<br>16 bits|Read-only|U16|0.001|kWh||
|37|00237|PCS DC accumulated<br>discharging power high<br>16 bits|Read-only|U16|0.001|kWh||
|38|00238|PCS communication<br>status word|Read-only|U16|1||Auto-increased by 1<br>every second|
|39|00239|System clock-Second|Read-only|U16|1|||
|40|00240|System clock-Minute|Read-only|U16|1|||
|41|00241|System clock-Hour|Read-only|U16|1|||
|42|00242|System clock-Day|Read-only|U16|1|||
|43|00243|System clock-Month|Read-only|U16|1|||
|44|00244|System clock-Year|Read-only|U16|1|||
|45|00245|PCSprogram version|Read-only|U16|0.1|||
|46|00246|FPGAprogram version|Read-only|U16|1|||
|47|00247|Phase N current effective<br>value|Read-only|U16|0.1|A||
|48|00248|PCS status query code 1|Read-only|U16|1||For running history<br>queries|
|49|00249|PCS status query code 2|Read-only|U16|1||For running history<br>queries|
|50|00250|PCS status query code 3|Read-only|U16|1||For running history<br>queries|
|51|00251|PCS statusquery code 4|Read-only|U16|1||For running history|


P 8/17


Protocol for External ModBus Communication of


PCS_V2.3













|Col1|Col2|Col3|Col4|Col5|Col6|Col7|queries|
|---|---|---|---|---|---|---|---|
|52|00252|PCS status query code 5|Read-only|U16|1||For running history<br>queries|
|53|00253|PCS status query code 6|Read-only|U16|1||For running history<br>queries|
|54|00254|PCS status query code 7|Read-only|U16|1||For running history<br>queries|
|55|00255|PCS status query code 8|Read-only|U16|1||For running history<br>queries|
|56|00256|PCS fault word 5|Read-only|U16|1|||
|57|00257|**SOC temperature**|Read-only|U16|1||Temperature<br>difference from<br>ambient temperature<br>is roughly 40°C|
|58|00258|IGBT temperature 1|Read-only|U16|1||The 8 high bits and<br>8 low bits are a set<br>of temperature<br>values respectively|
|59|00259|IGBT temperature 2|Read-only|U16|1||As above|
|60|00260|IGBT temperature 3|Read-only|U16|1||As above|
|61|00261|IGBT temperature 4|Read-only|U16|1||As above|
|62|00262|Reserve|Read-only|U16|1|||
|63|00263|DCDC input voltage|Read-only|S16|0.1|V|*(1)|
|64|00264|DCDC output voltage|Read-only|S16|0.1|V|*(1)|
|65|00265|DCDC input current|Read-only|S16|0.1|A|*(1)|
|66|00266|DCDC output current|Read-only|S16|0.1|A|*(1)|
|67|00267|DCDC inputpower|Read-only|S16|0.1|kW|*(1)|
|68|00268|DCDC radiator<br>temperature|Read-only|S16|1||*(1)|
|69|00269|Reserve|Read-only|S16|1||*(1)|
|70|00270|Reserve|Read-only|S16|1||*(1)|
|71|00271|DCDCprogram version|U16|0.1|||*(1)|
|72|00272|PCS fault word 1|Read-only|U16|1|||
|73|00273|PCS fault word 2|Read-only|U16|1|||
|74|00274|PCS fault word 3|Read-only|U16|1|||
|75|00275|PCS fault word 4|Read-only|U16|1|||
|76|00276|DCDC fault word 1|Read-only|U16|1||*(1)|
|77|00277|DCDC fault word 2|Read-only|U16|1||*(1)|
|78|00278|DCDC fault word 3|Read-only|U16|1||*(1)|
|79|00279|DCDC fault word 4|Read-only|U16|1||*(1)|
|80|00280|BMS/CMS work<br>instructions|**Read-**<br>**write**|U16|1||0x1111 charging<br>disabled<br>0x2222 discharging<br>disabled<br>0x5555 standby<br>0xaaaa fault|


P 9/17


Protocol for External ModBus Communication of


PCS_V2.3











































|Col1|Col2|Col3|Col4|Col5|Col6|Col7|0xbbbbnormal<br>0xccccalarm|
|---|---|---|---|---|---|---|---|
|81|00281|BMS/CMS allowable<br>charging current|**Read-**<br>**write**|U16|0.1|A|*(2)|
|82|00282|BMS/CMS allowable<br>discharging current|**Read-**<br>**write**|U16|0.1|A|*(2)|
|83|00283|BMS/CMS SOC|**Read-**<br>**write**|U16|0.1|%|*(2)|
|84|00284|BMS/CMS chargeable<br>power|**Read-**<br>**write**|U16|0.1|kWh|*(2)|
|85|00285|BMS/CMS dischargeable<br>power|**Read-**<br>**write**|U16|0.1|kWh|*(2)|
|86|00286|BMS/CMS total voltage|**Read-**<br>**write**|U16|0.1|V|*(2)|
|87|00287|BMS/CMS total current|**Read-**<br>**write**|S16|0.1|A|*(2)|
|88|00288|BMS/CMS single highest<br>SOC|**Read-**<br>**write**|U16|0.1|%|*(2)|
|89|00289|BMS/CMS single lowest<br>SOC|**Read-**<br>**write**|U16|0.1|%|*(2)|
|90|00290|BMS/CMS single highest<br>voltage|**Read-**<br>**write**|U16|0.1|V|*(2)|
|91|00291|BMS/CMS single lowest<br>voltage|**Read-**<br>**write**|U16|0.1|V|*(2)|
|92|00292|BMS/CMS single highest<br>temperature|**Read-**<br>**write**|U16|0.1|℃|*(2)|
|93|00293|BMS/CMS single lowest<br>temperature|**Read-**<br>**write**|S16|0.1|℃|*(2)|
|94|00294|BMS/CMS allowable<br>charging power|**Read-**<br>**write**|U16|0.1|kW|*(2)|
|95|00295|BMS/CMS allowable<br>discharging power|**Read-**<br>**write**|U16|0.1|kW|*(2)|
|96|00296|Reserve|Read-only|U16|1||*(2)|
|97|00297|Reserve|Read-only|U16|1||*(2)|
|98|00298|Reserve|Read-only|U16|1||*(2)|
|99|00299|Reserve|Read-only|U16|1||*(2)|
|100|00300|Reserve|Read-only|U16|1||*(2)|


**Note: Addresses 280-295 are used as read-only addresses when the PCS and BMS have an**

**independent communication link, and function code 04 applies. They are used as read-write**

**addresses when the PCS and BMS do not have an independent communication link and EMS**

**and BMS integrated controllers are applied, and function codes 0x03, 0x06, and 0x10 apply.**


**4.4** **Definition of remote regulating data address (address type 4x)**


(1) Read the content of continuous blocks of holding registers from the remote device:


Request: MBAP function code Start address H Start address L Number of registers H Number of


P 10/17


Protocol for External ModBus Communication of


PCS_V2.3


registers L (12 bytes in total)


Response: MBAP function code Data length Register data (length: 9 + number of registers × 2)


For example: The start address is 301, and the number of registers is 0x0003:


00 01 00 00 00 06 01 03 01 2D 00 03


Response: The data length is 0x06, the running mode of address 301 is set to 3, constant power mode,

and the rest are 0x00


00 01 00 00 00 09 01 03 06 00 03 00 00 00 00


(2) Write a holding register in a remote device:


Request: MBAP function code Register address H Register address L Register value H Register value

L (12 bytes in total)


Response: MBAP function code Register address H Register address L Register value H Register

value L (12 bytes in total)


For example: Write data 0x0003 to the register with the address as 301: 00 01 00 00 00 06 01 06 01

2D 00 03


Response: Write successfully: 00 01 00 00 00 06 01 06 01 2D 00 03


(3) Write continuous register blocks in a remote device:


Request: MBAP function code Start address H Start address L Number of registers H Number of

registers L Byte length Register value (13 + number of registers × 2)


Response: MBAP function code Start address H Start address L Number of registers H Number of

registers L (12 bytes in total)


For example: Write data to the register of which the start address is 301 and the number is 0x0003,

the data length is 0x06, write constant power, constant voltage 750V, constant current -50A. The data

is 0x0003, 0x02EE, 0xFFCE: 00 01 00 00 00 09 01 10 01 2D 00 03 06 00 03 02 EE FF CE


Response: Write successfully 00 01 00 00 00 06 01 10 01 2D 00 03













|No<br>.|Modbus<br>address|Name|Permi<br>ssion|Datatype|Coeff<br>icient|Unit|Remarks|
|---|---|---|---|---|---|---|---|
|1|00301|Selection of running<br>mode|Read-<br>write|U16|1|/|3 by default<br>0-None;<br>1- Constant<br>current<br>charging;<br>2- Constant<br>voltage<br>charging;<br>3- Constant<br>power<br>charging;|
|2|00302|Voltage setting value of<br>constant voltage<br>charging|Read-<br>write|U16|1|V|Charge<br>the<br>battery<br>when it is higher than<br>the<br>current<br>battery<br>voltage, and discharge|


P 11/17








Protocol for External ModBus Communication of


PCS_V2.3















































|Col1|Col2|Col3|Col4|Col5|Col6|Col7|the battery when it is<br>lower than the current<br>batteryvoltage|
|---|---|---|---|---|---|---|---|
|3|00303|Current setting value of<br>constant current charging|Read-<br>write|S16|1|A|Negative<br>means<br>discharging to the grid,<br>and positive means<br>charging from the grid.<br>0 by default|
|4|00304|Expectation of constant<br>power active power<br>(three-phase three-wire<br>system)|Read-<br>write|S16|0.1|kW|Negative<br>means<br>discharging to the grid,<br>and positive means<br>charging from the grid.|
|5|00305|Expectation of constant<br>power reactive power<br>(three-phase three-wire<br>system)|Read-<br>write|S16|0.1|kVar|Negative<br>inductive<br>reactive power and<br>positive<br>capacitive<br>reactive power|
|6|00306|Grid-connected and grid-<br>disconnected settings|Read-<br>write|U16|1|/|Grid-connected<br>by<br>default<br>Grid-connected mode;<br>VF grid-disconnected<br>mode;|
|7|00307|Grid-disconnected output<br>voltage given<br>(three-phase three-wire<br>system)|Read-<br>write|U16|1|V|230 by default|
|8|00308|Grid-disconnected output<br>frequency given|Read-<br>write|U16|0.01|Hz|5000 by default|
|9|00309|Phase A active power of<br>split-phase control<br>(three-phase four-wire<br>system)|Read-<br>write|S16|0.1|kW|Negative<br>means<br>discharging to the grid,<br>and positive means<br>charging from the grid.|
|10|00310|Phase B active power of<br>split-phase control<br>(three-phase four-wire<br>system)|Read-<br>write|S16|0.1|kW|Negative<br>means<br>discharging to the grid,<br>and positive means<br>charging from the grid.|
|11|00311|Phase C active power of<br>split-phase control<br>(three-phase four-wire<br>system)|Read-<br>write|S16|0.1|kW|Negative<br>means<br>discharging to the grid,<br>and positive means<br>charging from the grid.|
|12|00312|Phase A reactive power<br>of split-phase control<br>(three-phase four-wire<br>system)|Read-<br>write|S16|0.1|kVar|Negative inductive and<br>positive<br>capacitive<br>reactive power|
|13|00313|Phase B reactive power<br>of split-phase control<br>(three-phase four-wire<br>system)|Read-<br>write|S16|0.1|kVar|Negative inductive and<br>positive<br>capacitive<br>reactive power|
|14|00314|Phase C reactivepower|Read-|S16|0.1|kVar|Negative inductive and|


P 12/17


Protocol for External ModBus Communication of


PCS_V2.3








































|Col1|Col2|of split -phase control<br>(three-phase four-wire<br>system)|write|Col5|Col6|Col7|positive capacitive<br>reactivepower|
|---|---|---|---|---|---|---|---|
|15|00315|Grid-disconnected output<br>voltage split-phase given<br>A<br>(three-phase four-wire<br>system)|Read-<br>write|U16|1|V||
|16|00316|Grid-disconnected output<br>voltage split-phase given<br>B<br>(three-phase four-wire<br>system)|Read-<br>write|U16|1|V||
|17|00317|Grid-disconnected output<br>voltage split-phase given<br>C<br>(three-phase four-wire<br>system)|Read-<br>write|U16|1|V||
|18|00318|Microgrid DC voltage<br>droop coefficient|Read-<br>write|U16|1|V|0-100V|
|19|00319|Primary FM frequency<br>dead zone|Read-<br>write|U16|0.01|Hz|Dead zone >=0.05Hz|
|20|00320|Primary FM K value|Read-<br>write|U16|1|/|Range 0-120|
|21|00321|Reserve|Read-<br>write|U16|1|/||
|22|00322|Reserve|Read-<br>write|U16|1|/||
|23|00323|Reserve|Read-<br>write|U16|1|/||
|24|00324|Grid-connected and grid-<br>disconnected switch<br>running mode|Read-<br>write|U16|1|/|0- None<br>1- Manual<br>2- Automatic<br>3- Mix<br>4- Silence|
|25|00325|Reserve|Read-<br>write|U16|1|/||
|26|00326|Battery/super capacitor<br>allowable charging<br>voltage|Read-<br>write|U16|1|V||
|27|00327|Battery/super capacitor<br>allowable discharging<br>voltage|Read-<br>write|U16|1|V||
|28|00328|Battery/super capacitor<br>allowable charging<br>current|Read-<br>write|U16|1|A||
|29|00329|Battery/super capacitor|Read-|U16|1|A||



P 13/17


Protocol for External ModBus Communication of


PCS_V2.3












|Col1|Col2|allowabledischarging<br>current|write|Col5|Col6|Col7|Col8|
|---|---|---|---|---|---|---|---|
|30|00330|Time synchronization-<br>Second|Read-<br>write|U16|1|||
|31|00331|Time synchronization-<br>Minute|Read-<br>write|U16|1|||
|32|00332|Time synchronization-<br>Hour|Read-<br>write|U16|1|||
|33|00333|Time synchronization-<br>Day|Read-<br>write|U16|1|||
|34|00334|Time synchronization-<br>Month|Read-<br>write|U16|1|||
|35|00335|Time synchronization-<br>Year|Read-<br>write|U16|1|||
|36|00336|Reserve|Read-<br>write|U16|1|/||
|37|00337|Reserve|Read-<br>write|U16|1|/||
|38|00338|Reserve|Read-<br>write|U16|1|/||
|39|00339|Reserve|Read-<br>write|U16|1|/||
|40|00340|Reserve|Read-<br>write|U16|1|/||




|V. Appendix|Col2|Col3|
|---|---|---|
|PCS fault word 1|PCS fault word 1|PCS fault word 1|
|FPGA hardware fault-Phase A hardware overcurrent|1-Fault; 0-Normal|Bit0 setting|
|FPGA hardware fault-Phase B hardware overcurrent|1-Fault; 0-Normal|Bit1 setting|
|FPGA hardware fault-Phase C hardware overcurrent|1-Fault; 0-Normal|Bit2 setting|
|FPGA hardware fault-Phase N hardware overcurrent|1-Fault; 0-Normal|Bit3 setting|
|FPGA hardware fault-Reserve|1-Fault; 0-Normal|Bit4 setting|
|FPGA hardware fault-Reserve|1-Fault; 0-Normal|Bit5 setting|
|FPGA hardware fault-Unit DC voltage fault|1-Fault; 0-Normal|Bit6 setting|
|FPGA hardware fault-Reserve|1-Fault; 0-Normal|Bit7 setting|
|FPGA hardware fault-Reserve|1-Fault; 0-Normal|Bit8 setting|
|FPGA<br>hardware<br>fault-Switching<br>power<br>supply<br>undervoltage|1-Fault; 0-Normal|Bit9 setting|
|FPGA software fault-Phase A IGBT fault|1-Fault; 0-Normal|Bit10 setting|
|FPGA hardware fault-Phase B IGBT fault|1-Fault; 0-Normal|Bit11 setting|
|FPGA hardware fault-Phase C IGBT fault|1-Fault; 0-Normal|Bit12 setting|
|FPGA hardware fault-Phase N IGBT fault|1-Fault; 0-Normal|Bit13 setting|
|FPGA hardware fault-Overtemperature fault|1-Fault; 0-Normal|Bit14 setting|
|FPGA hardware fault-Reserve|1-Fault; 0-Normal|Bit15 setting|



P 14/17


Protocol for External ModBus Communication of


PCS_V2.3

|PCSfaultword2|Col2|Col3|
|---|---|---|
|ARM software fault-Phase A output overcurrent|1-Fault; 0-Normal|Bit0 setting|
|ARM software fault-Phase A outputquick-break|1-Fault; 0-Normal|Bit1 setting|
|ARM software fault-Phase B output overcurrent|1-Fault; 0-Normal|Bit2 setting|
|ARM software fault-Phase B outputquick-break|1-Fault; 0-Normal|Bit3 setting|
|ARM software fault-Phase C output overcurrent|1-Fault; 0-Normal|Bit4 setting|
|ARM software fault-Phase C outputquick-break|1-Fault; 0-Normal|Bit5 setting|
|ARM software fault-Phase N outputquick-break|1-Fault; 0-Normal|Bit6 setting|
|ARM software fault-Phase N outputquick-break|1-Fault; 0-Normal|Bit7 setting|
|ARM software fault-AC overvoltage|1-Fault; 0-Normal|Bit8 setting|
|ARM software fault-AC undervoltage|1-Fault; 0-Normal|Bit9 setting|
|ARM software fault-AC overfrequency|1-Fault; 0-Normal|Bit10 setting|
|ARM software fault-AC underfrequency|1-Fault; 0-Normal|Bit11 setting|
|ARM software fault-Voltage THDU overrun|1-Fault; 0-Normal|Bit12 setting|
|ARM software fault-Systemphase loss|1-Fault; 0-Normal|Bit13 setting|
|ARM software fault-Systemphase sequence error|1-Fault; 0-Normal|Bit14 setting|
|ARM software fault-DCpolarity reversed|1-Fault; 0-Normal|Bit15 setting|


|PCSfaultword3|Col2|Col3|
|---|---|---|
|ARM software fault-DC busbar software overvoltage|1-Fault; 0-Normal|Bit0 setting|
|ARM software fault-DC busbar software undervoltage|1-Fault; 0-Normal|Bit1 setting|
|ARM software fault-System overfrequency|1-Fault; 0-Normal|Bit2 setting|
|ARM software fault-System underfrequency|1-Fault; 0-Normal|Bit3 setting|
|ARM software fault-DC charging overcurrent|1-Fault; 0-Normal|Bit4 setting|
|ARM software fault-DC discharging overcurrent|1-Fault; 0-Normal|Bit5 setting|
|ARM software fault-Islanding protection|1-Fault; 0-Normal|Bit6 setting|
|ARM software fault-DC component overrun|1-Fault; 0-Normal|Bit7 setting|
|ARM software fault-AC main contact closing fault|1-Fault; 0-Normal|Bit8 setting|
|ARM software fault-AC main contact opening fault|1-Fault; 0-Normal|Bit9 setting|
|ARM software fault-AC soft start closing fault|1-Fault; 0-Normal|Bit10 setting|
|ARM software fault-AC soft start opening fault|1-Fault; 0-Normal|Bit11 setting|
|ARM software fault-DC main contact closing fault|1-Fault; 0-Normal|Bit12 setting|
|ARM software fault-DC main contact opening fault|1-Fault; 0-Normal|Bit13 setting|
|ARM software fault-DC soft start closing fault|1-Fault; 0-Normal|Bit14 setting|
|ARM software fault-DC soft start closing fault|1-Fault; 0-Normal|Bit15 setting|


|PCSfaultword4|Col2|Col3|
|---|---|---|
|ARM software fault-Ferroelectricparameter storage error|1-Fault; 0-Normal|Bit0 setting|
|ARM software fault-DC soft start failure|1-Fault; 0-Normal|Bit1 setting|
|ARM software fault-Reserve|1-Fault; 0-Normal|Bit2 setting|
|ARM software fault-Reserve|1-Fault; 0-Normal|Bit3 setting|
|ARM software fault-Starting conditions not met|1-Fault; 0-Normal|Bit4 setting|
|ARM software fault-Switch fault during running|1-Fault; 0-Normal|Bit5 setting|



P 15/17


Protocol for External ModBus Communication of


PCS_V2.3

|ARM software fault -Inverter startup timeout|1 -Fault; 0 -Normal|Bit6setting|
|---|---|---|
|ARM software fault-Parameter issuance setting error|1-Fault; 0-Normal|Bit7 setting|
|ARM software fault-BMS communication fault|1-Fault; 0-Normal|Bit8 setting|
|ARM software fault-BMS temperature abnormality|1-Fault; 0-Normal|Bit9 setting|
|ARM software fault-BMS trip|1-Fault; 0-Normal|Bit10 setting|
|ARM software fault-BMS battery alarm|1-Fault; 0-Normal|Bit11 setting|
|ARM software fault-DCDC communication fault|1-Fault; 0-Normal|Bit12 setting|
|ARM software fault-EMS communication fault|1-Fault; 0-Normal|Bit13 setting|
|ARM software fault-Emergency stop or fuse fault|1-Fault; 0-Normal|Bit14 setting|
|ARM software fault-PCS fiber-optic communication fault|1-Fault; 0-Normal|Bit15 setting|


|PCSfaultword5|Col2|Col3|
|---|---|---|
|ARM software fault-Reserve|1-Fault; 0-Normal|Bit0 setting|
|ARM software fault-Battery software overvoltage|1-Fault; 0-Normal|Bit1 setting|
|ARM software fault-Battery software undervoltage|1-Fault; 0-Normal|Bit2 setting|
|ARM software fault-Busbar unbalance abnormality|1-Fault; 0-Normal|Bit3 setting|
|ARM software fault-Busbar semi-DC overvoltage|1-Fault; 0-Normal|Bit4 setting|
|ARM software fault-DCDC startup timeout|1-Fault; 0-Normal|Bit5 setting|
|ARM software fault-Reserve|1-Fault; 0-Normal|Bit6 setting|
|ARM software fault-AC leakage currentprotection|1-Fault; 0-Normal|Bit7 setting|
|ARM software fault-Reserve|1-Fault; 0-Normal|Bit8 setting|
|ARM software fault-Reserve|1-Fault; 0-Normal|Bit9 setting|
|ARM software fault-Reserve|1-Fault; 0-Normal|Bit10 setting|
|ARM software fault-Reserve|1-Fault; 0-Normal|Bit11 setting|
|ARM software fault-Reserve|1-Fault; 0-Normal|Bit12 setting|
|ARM software fault-Reserve|1-Fault; 0-Normal|Bit13 setting|
|ARM software fault-Reserve|1-Fault; 0-Normal|Bit14 setting|
|ARM software fault-Reserve|1-Fault; 0-Normal|Bit15 setting|



DCDC Fault Word Parsing:


0: No fault


1: Reserve


2: Output overcurrent protection (hardware)


3: Communication fault


4: Overcurrent protection (hardware)


5: Reserve


6: Battery side overvoltage


7: Output overvoltage fault (hardware)


P 16/17


8: Output overvoltage protection (software)


9: Output undervoltage fault (software)


10: Fan fault


11: Input overvoltage fault (software)


12: Input overcurrent (software)


13: Input overcurrent (software)


14: Radiator overheat


15: Unit 1 overcurrent fault (hardware)


16: Unit 2 overcurrent fault (hardware)


17: Unit 3 overcurrent fault (hardware)


18: Unit 4 overcurrent fault (hardware)


19: Unit 5 overcurrent fault (hardware)


20: Unit 6 overcurrent fault (hardware)


21: EEPORM read/write fault (ERR21)


22: Unit 1VCE protection (hardware)


23: Unit 2VCE protection (hardware)


24: Unit 3VCE protection (hardware)


25: Unit 4VCE protection (hardware)


26: Unit 5VCE protection (hardware)


27: Unit 6VCE protection (hardware)



Protocol for External ModBus Communication of


PCS_V2.3


P 17/17


