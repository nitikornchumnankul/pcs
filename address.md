## A. Status Registers (Discrete Inputs - Address Type 1x)

### ข้อมูลทั่วไป
- **Function Code**: 0x02 (Read discrete input register)
- **Data Type**: Boolean (1 bit)
- **Read-Only**: Yes
- **Starting Address**: 81
- **Total Registers**: 16 (Address 81-96)

### ตารางรายละเอียด

| Modbus Address | Name                        | Data Type | Read/Write | Description                                    | Value Meaning                    |
|----------------|----------------------------|-----------|------------|-----------------------------------------------|----------------------------------|
| **00081**      | Shutdown status            | Bool      | Read-only  | สถานะการปิดเครื่อง                              | 1 = Shutdown, 0 = Not Shutdown  |
| **00082**      | Standby status             | Bool      | Read-only  | สถานะ Standby (พร้อมใช้งาน)                      | 1 = Standby, 0 = Not Standby   |
| **00083**      | Running status             | Bool      | Read-only  | สถานะการทำงาน                                   | 1 = Running, 0 = Not Running    |
| **00084**      | Total fault status         | Bool      | Read-only  | สถานะ Fault รวมทั้งหมด                          | 1 = Fault, 0 = No Fault         |
| **00085**      | Total alarm status         | Bool      | Read-only  | สถานะ Alarm รวมทั้งหมด                          | 1 = Alarm, 0 = No Alarm         |
| **00086**      | Remote/local status        | Bool      | Read-only  | สถานะการควบคุม (Remote/Local)                    | 1 = Remote, 0 = Local           |
| **00087**      | Emergency stop input status| Bool      | Read-only  | สถานะ Emergency Stop                            | 1 = Emergency Stop Active, 0 = Inactive |
| **00088**      | Grid-connected status      | Bool      | Read-only  | สถานะการเชื่อมต่อกับ Grid                         | 1 = Grid-connected, 0 = Disconnected |
| **00089**      | VF grid-disconnected status| Bool      | Read-only  | สถานะ VF (Voltage/Frequency) Grid Disconnected | 1 = VF Grid-disconnected, 0 = Connected |
| **00090**      | Overload derating          | Bool      | Read-only  | สถานะ Overload Derating                         | 1 = Overload Occurred, 0 = Normal |
| **00091**      | Reserve                    | Bool      | Read-only  | สำรอง                                           | —                                |
| **00092**      | Reserve                    | Bool      | Read-only  | สำรอง                                           | —                                |
| **00093**      | Reserve                    | Bool      | Read-only  | สำรอง                                           | —                                |
| **00094**      | BMS dry contact input      | Bool      | Read-only  | สถานะ BMS Dry Contact (PCS v641.0+)            | 1 = Fault Valid, 0 = Normal     |
| **00095**      | Reserve                    | Bool      | Read-only  | สำรอง                                           | —                                |
| **00096**      | Reserve                    | Bool      | Read-only  | สำรอง                                           | —                                |

### วิธีอ่านข้อมูล

#### Python Code Example
```python
# อ่าน 16 discrete inputs เริ่มจาก address 81
bits = client.read_discrete_inputs(address=81, count=16, device_id=1)

# แปลงเป็น dictionary
status = {
    "shutdown": bits[0],              # Address 81
    "standby": bits[1],               # Address 82
    "running": bits[2],               # Address 83
    "fault": bits[3],                 # Address 84
    "alarm": bits[4],                 # Address 85
    "remote_control": bits[5],         # Address 86
    "emergency_stop_active": bits[6], # Address 87
    "grid_connected": bits[7],        # Address 88
    "vf_grid_disconnected": bits[8],  # Address 89
    "overload_derating": bits[9],     # Address 90
    "reserve_91": bits[10],           # Address 91
    "reserve_92": bits[11],           # Address 92
    "reserve_93": bits[12],           # Address 93
    "bms_dry_contact": bits[13],      # Address 94
    "reserve_95": bits[14],           # Address 95
    "reserve_96": bits[15],           # Address 96
}
```

#### Modbus TCP Request Example
```
Request: 00 01 00 00 00 06 01 02 00 51 00 10
- Transaction ID: 00 01
- Protocol ID: 00 00
- Length: 00 06
- Unit ID: 01
- Function Code: 02 (Read Discrete Inputs)
- Starting Address: 00 51 (81 decimal)
- Quantity: 00 10 (16 decimal)
```

### สถานะที่สำคัญ

#### 1. Running Status (Address 83)
- **1 (True)**: อุปกรณ์กำลังทำงาน
- **0 (False)**: อุปกรณ์ไม่ทำงาน (อาจอยู่ในสถานะ Shutdown, Standby, หรือ Fault)

#### 2. Fault Status (Address 84)
- **1 (True)**: มี Fault เกิดขึ้น - ต้องตรวจสอบ Fault Words (Address 272-275, 256)
- **0 (False)**: ไม่มี Fault

#### 3. Alarm Status (Address 85)
- **1 (True)**: มี Alarm เกิดขึ้น
- **0 (False)**: ไม่มี Alarm

#### 4. Grid-Connected Status (Address 88)
- **1 (True)**: เชื่อมต่อกับ Grid แล้ว
- **0 (False)**: ไม่ได้เชื่อมต่อกับ Grid (อาจอยู่ใน VF mode)

### หมายเหตุ
- **Address 94**: BMS Dry Contact ใช้ได้เฉพาะ PCS version 641.0 หรือสูงกว่า
- **Reserve Addresses**: Address 91-93, 95-96 เป็น reserved สำหรับอนาคต
- **การอ่าน**: แนะนำให้อ่าน 16 bits พร้อมกัน (Address 81-96) เพื่อประสิทธิภาพที่ดี

### การใช้งานในโค้ด

#### ใน pcs_client.py
```python
def get_status(self):
    """Reads device status."""
    bits = self._read_discrete_inputs(81, 16)
    if not bits:
        return None
        
    status = {
        "shutdown": bits[0],
        "standby": bits[1],
        "running": bits[2],
        "fault": bits[3],
        "alarm": bits[4],
        "remote_control": bits[5],
        "emergency_stop_active": bits[6],
        "grid_connected": bits[7],
        "vf_grid_disconnected": bits[8],
        "overload_derating": bits[9],
        "bms_dry_contact": bits[13] if len(bits) > 13 else False,
    }
    return status
```

#### ใน pcs_ui.py
```python
status = client.get_status()
if status:
    if status.get("running"):
        st.success("🟢 Device is Running")
    if status.get("fault"):
        st.error("🔴 Fault Detected!")
    if status.get("grid_connected"):
        st.info("🟢 Grid Connected")
```

## B. PCS AC Voltage (Input Registers - Address Type 3x)

### ข้อมูลทั่วไป
- **Function Code**: 0x04 (Read input registers)
- **Data Type**: Unsigned 16-bit Integer (U16)
- **Coefficient**: × 0.1
- **Unit**: Volt (V)
- **Read-Only**: Yes
- **Starting Address**: 201
- **Total Registers**: 3 (Address 201-203)

### ตารางรายละเอียด

| Modbus Address | Name                        | Data Type | Coefficient | Unit | Read/Write | Description                    |
|----------------|----------------------------|-----------|-------------|------|------------|--------------------------------|
| **00201**      | Phase A voltage of PCS port | U16       | × 0.1       | V    | Read-only  | แรงดัน Phase A ที่ PCS port      |
| **00202**      | Phase B voltage of PCS port | U16       | × 0.1       | V    | Read-only  | แรงดัน Phase B ที่ PCS port      |
| **00203**      | Phase C voltage of PCS port | U16       | × 0.1       | V    | Read-only  | แรงดัน Phase C ที่ PCS port      |

### วิธีอ่านข้อมูล

#### Python Code Example
```python
# อ่าน 3 registers เริ่มจาก address 201
regs = client.read_input_registers(address=201, count=3, device_id=1)

# แปลงค่า (คูณด้วย 0.1)
voltage_a = regs[0] * 0.1  # Address 201
voltage_b = regs[1] * 0.1  # Address 202
voltage_c = regs[2] * 0.1  # Address 203

# ตัวอย่าง: ถ้า register value = 2300, แรงดันจริง = 230.0 V
```

### หมายเหตุ
- **ค่าปกติ**: แรงดัน 3-phase ระบบ 230V จะมีค่า register ประมาณ 2300 (230.0 V)
- **Range**: 0 - 6553.5 V (U16 max = 65535, × 0.1)

---

## C. PCS AC Current (Input Registers - Address Type 3x)

### ข้อมูลทั่วไป
- **Function Code**: 0x04 (Read input registers)
- **Data Type**: Signed 16-bit Integer (S16)
- **Coefficient**: × 0.1
- **Unit**: Ampere (A)
- **Read-Only**: Yes
- **Starting Address**: 204
- **Total Registers**: 3 (Address 204-206)

### ตารางรายละเอียด

| Modbus Address | Name            | Data Type | Coefficient | Unit | Read/Write | Description                    | Value Range        |
|----------------|----------------|-----------|-------------|------|------------|--------------------------------|-------------------|
| **00204**      | Phase A current | S16       | × 0.1       | A    | Read-only  | กระแส Phase A ที่ PCS output    | -3276.8 ถึง 3276.7 A |
| **00205**      | Phase B current | S16       | × 0.1       | A    | Read-only  | กระแส Phase B ที่ PCS output    | -3276.8 ถึง 3276.7 A |
| **00206**      | Phase C current | S16       | × 0.1       | A    | Read-only  | กระแส Phase C ที่ PCS output    | -3276.8 ถึง 3276.7 A |

### วิธีอ่านข้อมูล

#### Python Code Example
```python
# อ่าน 3 registers เริ่มจาก address 204
regs = client.read_input_registers(address=204, count=3, device_id=1)

# แปลงค่า signed 16-bit (คูณด้วย 0.1)
def convert_signed_16bit(value, coefficient=0.1):
    if value > 32767:
        value = value - 65536
    return value * coefficient

current_a = convert_signed_16bit(regs[0])  # Address 204
current_b = convert_signed_16bit(regs[1])  # Address 205
current_c = convert_signed_16bit(regs[2])  # Address 206

# ตัวอย่าง: 
# - ถ้า register = 1000, กระแส = 100.0 A (Charge)
# - ถ้า register = 65535, กระแส = -0.1 A (Discharge)
```

### หมายเหตุ
- **Signed Value**: ค่าบวก = Charge (ชาร์จ), ค่าลบ = Discharge (คายประจุ)
- **การแปลง Signed**: ต้องตรวจสอบว่าค่า > 32767 แล้วลบ 65536

---

## D. Frequency (Input Registers - Address Type 3x)

### ข้อมูลทั่วไป
- **Function Code**: 0x04 (Read input registers)
- **Data Type**: Unsigned 16-bit Integer (U16)
- **Coefficient**: × 0.01
- **Unit**: Hertz (Hz)
- **Read-Only**: Yes
- **Address**: 207

### ตารางรายละเอียด

| Modbus Address | Name           | Data Type | Coefficient | Unit | Read/Write | Description              | Normal Range    |
|----------------|----------------|-----------|-------------|------|------------|--------------------------|-----------------|
| **00207**      | Grid frequency | U16       | × 0.01      | Hz   | Read-only  | ความถี่ของ Grid            | 50.00 Hz (50Hz system) หรือ 60.00 Hz (60Hz system) |

### วิธีอ่านข้อมูล

#### Python Code Example
```python
# อ่าน 1 register ที่ address 207
regs = client.read_input_registers(address=207, count=1, device_id=1)

# แปลงค่า (คูณด้วย 0.01)
frequency = regs[0] * 0.01  # Address 207

# ตัวอย่าง: ถ้า register value = 5000, ความถี่ = 50.00 Hz
```

### หมายเหตุ
- **ค่าปกติ**: 50.00 Hz (ระบบ 50Hz) หรือ 60.00 Hz (ระบบ 60Hz)
- **Range**: 0 - 655.35 Hz

---

## E. Active Power (Input Registers - Address Type 3x)

### ข้อมูลทั่วไป
- **Function Code**: 0x04 (Read input registers)
- **Data Type**: Signed 16-bit Integer (S16)
- **Coefficient**: × 0.1
- **Unit**: Kilowatt (kW)
- **Read-Only**: Yes
- **Starting Address**: 208
- **Total Registers**: 4 (Address 208-211)

### ตารางรายละเอียด

| Modbus Address | Name                 | Data Type | Coefficient | Unit | Read/Write | Description                    | Value Meaning              |
|----------------|---------------------|-----------|-------------|------|------------|--------------------------------|----------------------------|
| **00208**      | Active power phase A | S16       | × 0.1       | kW   | Read-only  | กำลังไฟฟ้าจริง Phase A          | บวก = Charge, ลบ = Discharge |
| **00209**      | Active power phase B | S16       | × 0.1       | kW   | Read-only  | กำลังไฟฟ้าจริง Phase B          | บวก = Charge, ลบ = Discharge |
| **00210**      | Active power phase C | S16       | × 0.1       | kW   | Read-only  | กำลังไฟฟ้าจริง Phase C          | บวก = Charge, ลบ = Discharge |
| **00211**      | Total active power   | S16       | × 0.1       | kW   | Read-only  | กำลังไฟฟ้าจริงรวมทั้งหมด (3 Phase) | บวก = Charge, ลบ = Discharge |

### วิธีอ่านข้อมูล

#### Python Code Example
```python
# อ่าน 4 registers เริ่มจาก address 208
regs = client.read_input_registers(address=208, count=4, device_id=1)

# แปลงค่า signed 16-bit
def convert_signed_16bit(value, coefficient=0.1):
    if value > 32767:
        value = value - 65536
    return value * coefficient

active_power_a = convert_signed_16bit(regs[0])  # Address 208
active_power_b = convert_signed_16bit(regs[1])  # Address 209
active_power_c = convert_signed_16bit(regs[2])  # Address 210
active_power_total = convert_signed_16bit(regs[3])  # Address 211

# ตัวอย่าง:
# - register = 5000 → 500.0 kW (Charge)
# - register = 65535 → -0.1 kW (Discharge)
```

### หมายเหตุ
- **Signed Value**: ค่าบวก = Charge (ชาร์จเข้า Grid), ค่าลบ = Discharge (คายประจุจาก Grid)
- **Total Power**: Address 211 = Phase A + Phase B + Phase C

---

## F. Reactive Power (Input Registers - Address Type 3x)

### ข้อมูลทั่วไป
- **Function Code**: 0x04 (Read input registers)
- **Data Type**: Signed 16-bit Integer (S16)
- **Coefficient**: × 0.1
- **Unit**: Kilovolt-Ampere Reactive (kVar)
- **Read-Only**: Yes
- **Starting Address**: 212
- **Total Registers**: 4 (Address 212-215)

### ตารางรายละเอียด

| Modbus Address | Name                   | Data Type | Coefficient | Unit | Read/Write | Description                    | Value Meaning                    |
|----------------|------------------------|-----------|-------------|------|------------|--------------------------------|----------------------------------|
| **00212**      | Reactive power phase A | S16       | × 0.1       | kVar | Read-only  | กำลังไฟฟ้ารีแอคทีฟ Phase A       | บวก = Capacitive, ลบ = Inductive |
| **00213**      | Reactive power phase B | S16       | × 0.1       | kVar | Read-only  | กำลังไฟฟ้ารีแอคทีฟ Phase B       | บวก = Capacitive, ลบ = Inductive |
| **00214**      | Reactive power phase C | S16       | × 0.1       | kVar | Read-only  | กำลังไฟฟ้ารีแอคทีฟ Phase C       | บวก = Capacitive, ลบ = Inductive |
| **00215**      | Total reactive power   | S16       | × 0.1       | kVar | Read-only  | กำลังไฟฟ้ารีแอคทีฟรวมทั้งหมด      | บวก = Capacitive, ลบ = Inductive |

### วิธีอ่านข้อมูล

#### Python Code Example
```python
# อ่าน 4 registers เริ่มจาก address 212
regs = client.read_input_registers(address=212, count=4, device_id=1)

# แปลงค่า signed 16-bit
reactive_power_a = convert_signed_16bit(regs[0])  # Address 212
reactive_power_b = convert_signed_16bit(regs[1])  # Address 213
reactive_power_c = convert_signed_16bit(regs[2])  # Address 214
reactive_power_total = convert_signed_16bit(regs[3])  # Address 215
```

### หมายเหตุ
- **Signed Value**: 
  - ค่าบวก = Capacitive reactive power (ให้ capacitive power)
  - ค่าลบ = Inductive reactive power (ให้ inductive power)

---

## G. Apparent Power (Input Registers - Address Type 3x)

### ข้อมูลทั่วไป
- **Function Code**: 0x04 (Read input registers)
- **Data Type**: Unsigned 16-bit Integer (U16)
- **Coefficient**: × 0.1
- **Unit**: Kilovolt-Ampere (kVA)
- **Read-Only**: Yes
- **Starting Address**: 216
- **Total Registers**: 4 (Address 216-219)

### ตารางรายละเอียด

| Modbus Address | Name                   | Data Type | Coefficient | Unit | Read/Write | Description                    | Formula                    |
|----------------|------------------------|-----------|-------------|------|------------|--------------------------------|----------------------------|
| **00216**      | Apparent power phase A | U16       | × 0.1       | kVA  | Read-only  | กำลังไฟฟ้าปรากฏ Phase A          | √(Active² + Reactive²)    |
| **00217**      | Apparent power phase B | U16       | × 0.1       | kVA  | Read-only  | กำลังไฟฟ้าปรากฏ Phase B          | √(Active² + Reactive²)    |
| **00218**      | Apparent power phase C | U16       | × 0.1       | kVA  | Read-only  | กำลังไฟฟ้าปรากฏ Phase C          | √(Active² + Reactive²)    |
| **00219**      | Total apparent power   | U16       | × 0.1       | kVA  | Read-only  | กำลังไฟฟ้าปรากฏรวมทั้งหมด        | √(Total Active² + Total Reactive²) |

### วิธีอ่านข้อมูล

#### Python Code Example
```python
# อ่าน 4 registers เริ่มจาก address 216
regs = client.read_input_registers(address=216, count=4, device_id=1)

# แปลงค่า (คูณด้วย 0.1)
apparent_power_a = regs[0] * 0.1  # Address 216
apparent_power_b = regs[1] * 0.1  # Address 217
apparent_power_c = regs[2] * 0.1  # Address 218
apparent_power_total = regs[3] * 0.1  # Address 219
```

### หมายเหตุ
- **Unsigned Value**: ค่าเป็นบวกเสมอ (กำลังไฟฟ้าปรากฏไม่มีทิศทาง)
- **Relationship**: Apparent Power = √(Active Power² + Reactive Power²)

---

## H. Power Factor (Input Registers - Address Type 3x)

### ข้อมูลทั่วไป
- **Function Code**: 0x04 (Read input registers)
- **Data Type**: Unsigned 16-bit Integer (U16)
- **Coefficient**: × 0.001
- **Unit**: None (dimensionless)
- **Read-Only**: Yes
- **Starting Address**: 220
- **Total Registers**: 4 (Address 220-223)

### ตารางรายละเอียด

| Modbus Address | Name                 | Data Type | Coefficient | Unit | Read/Write | Description                    | Normal Range    |
|----------------|---------------------|-----------|-------------|------|------------|--------------------------------|-----------------|
| **00220**      | Phase A power factor | U16       | × 0.001     | —    | Read-only  | Power Factor Phase A            | 0.000 ถึง 1.000 (หรือ -1.000 ถึง 1.000) |
| **00221**      | Phase B power factor | U16       | × 0.001     | —    | Read-only  | Power Factor Phase B            | 0.000 ถึง 1.000 |
| **00222**      | Phase C power factor | U16       | × 0.001     | —    | Read-only  | Power Factor Phase C            | 0.000 ถึง 1.000 |
| **00223**      | Total power factor   | U16       | × 0.001     | —    | Read-only  | Power Factor รวมทั้งหมด          | 0.000 ถึง 1.000 |

### วิธีอ่านข้อมูล

#### Python Code Example
```python
# อ่าน 4 registers เริ่มจาก address 220
regs = client.read_input_registers(address=220, count=4, device_id=1)

# แปลงค่า (คูณด้วย 0.001)
power_factor_a = regs[0] * 0.001  # Address 220
power_factor_b = regs[1] * 0.001  # Address 221
power_factor_c = regs[2] * 0.001  # Address 222
power_factor_total = regs[3] * 0.001  # Address 223

# ตัวอย่าง: ถ้า register value = 950, Power Factor = 0.950
```

### หมายเหตุ
- **ค่าปกติ**: 0.8 - 1.0 (ยิ่งใกล้ 1.0 ยิ่งดี)
- **Range**: 0.000 - 0.655 (U16 max = 65535, × 0.001)
- **Formula**: Power Factor = Active Power / Apparent Power

---

## I. PCS DC Input (Input Registers - Address Type 3x)

### ข้อมูลทั่วไป
- **Function Code**: 0x04 (Read input registers)
- **Data Type**: Signed 16-bit Integer (S16) สำหรับ Power และ Current, Unsigned/Signed สำหรับ Voltage
- **Coefficient**: × 0.1
- **Read-Only**: Yes
- **Starting Address**: 224
- **Total Registers**: 3 (Address 224-226)
- **Source**: จาก PV (Photovoltaic) หรือ Battery

### ตารางรายละเอียด

| Modbus Address | Name              | Data Type | Coefficient | Unit | Read/Write | Description                    | Value Meaning              |
|----------------|-------------------|-----------|-------------|------|------------|--------------------------------|----------------------------|
| **00224**      | PCS input power   | S16       | × 0.1       | kW   | Read-only  | กำลังไฟฟ้า DC Input              | บวก = Charge, ลบ = Discharge |
| **00225**      | PCS input voltage | S16       | × 0.1       | V    | Read-only  | แรงดัน DC Input                 | ค่าบวกเสมอ                  |
| **00226**      | PCS input current | S16       | × 0.1       | A    | Read-only  | กระแส DC Input                  | บวก = Charge, ลบ = Discharge |

### วิธีอ่านข้อมูล

#### Python Code Example
```python
# อ่าน 3 registers เริ่มจาก address 224
regs = client.read_input_registers(address=224, count=3, device_id=1)

# แปลงค่า signed 16-bit
dc_input_power = convert_signed_16bit(regs[0])  # Address 224
dc_input_voltage = convert_signed_16bit(regs[1])  # Address 225
dc_input_current = convert_signed_16bit(regs[2])  # Address 226

# ตัวอย่าง:
# - DC Voltage: register = 8000 → 800.0 V
# - DC Current: register = 1000 → 100.0 A (Charge)
# - DC Power: register = 80000 → 8000.0 kW (แต่ต้องตรวจสอบ range)
```

### หมายเหตุ
- **DC Input**: ข้อมูลจากด้าน DC ของ PCS (จาก PV หรือ Battery)
- **Power Calculation**: Power = Voltage × Current
- **Signed Values**: Power และ Current มีทิศทาง (Charge/Discharge)

---

## J. Temperature (Input Registers - Address Type 3x)

### ข้อมูลทั่วไป
- **Function Code**: 0x04 (Read input registers)
- **Data Type**: Signed 16-bit Integer (S16) สำหรับ Radiator, Unsigned 16-bit (U16) สำหรับ IGBT และ SOC
- **Coefficient**: × 1.0
- **Unit**: Celsius (°C)
- **Read-Only**: Yes
- **Addresses**: 227, 257-261

### ตารางรายละเอียด

| Modbus Address | Name                     | Data Type | Coefficient | Unit | Read/Write | Description                    | Remarks                      |
|----------------|--------------------------|-----------|-------------|------|------------|--------------------------------|------------------------------|
| **00227**      | PCS radiator temperature | S16       | × 1.0       | °C   | Read-only  | อุณหภูมิ Radiator (IGBT max temp) | IGBT อุณหภูมิสูงสุด            |
| **00257**      | SOC temperature          | U16       | × 1.0       | °C   | Read-only  | อุณหภูมิ SOC                    | ~40°C offset จาก ambient temp |
| **00258**      | IGBT temperature 1       | U16       | × 1.0       | °C   | Read-only  | อุณหภูมิ IGBT 1                 | High/low bit mapping         |
| **00259**      | IGBT temperature 2       | U16       | × 1.0       | °C   | Read-only  | อุณหภูมิ IGBT 2                 | —                            |
| **00260**      | IGBT temperature 3       | U16       | × 1.0       | °C   | Read-only  | อุณหภูมิ IGBT 3                 | —                            |
| **00261**      | IGBT temperature 4       | U16       | × 1.0       | °C   | Read-only  | อุณหภูมิ IGBT 4                 | —                            |

### วิธีอ่านข้อมูล

#### Python Code Example
```python
# อ่าน Radiator temperature (Address 227)
radiator_regs = client.read_input_registers(address=227, count=1, device_id=1)
radiator_temp = convert_signed_16bit(radiator_regs[0], 1.0)  # Address 227

# อ่าน SOC และ IGBT temperatures (Address 257-261)
temp_regs = client.read_input_registers(address=257, count=5, device_id=1)
soc_temp = temp_regs[0]  # Address 257
igbt_temp_1 = temp_regs[1]  # Address 258
igbt_temp_2 = temp_regs[2]  # Address 259
igbt_temp_3 = temp_regs[3]  # Address 260
igbt_temp_4 = temp_regs[4]  # Address 261

# ตัวอย่าง:
# - Radiator: register = 65 → 65°C
# - SOC: register = 25 → 25°C (จริงๆ อาจเป็น 25 + 40 = 65°C จาก ambient)
# - IGBT: register = 70 → 70°C
```

### หมายเหตุ
- **Radiator Temperature**: แสดงอุณหภูมิสูงสุดของ IGBT
- **SOC Temperature**: มี offset ประมาณ 40°C จาก ambient temperature
- **IGBT Temperature**: 8 high bits และ 8 low bits เป็นชุดอุณหภูมิ (อาจต้อง decode)
- **Normal Range**: 0-100°C (ควรตรวจสอบ spec ของอุปกรณ์)

---

## K. AC/DC Energy Counters (Input Registers - Address Type 3x)

### ข้อมูลทั่วไป
- **Function Code**: 0x04 (Read input registers)
- **Data Type**: Unsigned 32-bit Integer (U32) - ใช้ 2 registers (Low + High 16-bit)
- **Coefficient**: × 0.001
- **Unit**: Kilowatt-hour (kWh)
- **Read-Only**: Yes
- **Addresses**: 230-237 (4 คู่: Low/High)

### ตารางรายละเอียด

| Modbus Address (Low) | Modbus Address (High) | Name                                    | Data Type | Coefficient | Unit | Read/Write | Description                    |
|----------------------|----------------------|-----------------------------------------|-----------|-------------|------|------------|--------------------------------|
| **00230**            | **00231**            | PCS AC accumulated charging energy      | U32       | × 0.001     | kWh  | Read-only  | พลังงานสะสม AC การชาร์จ          |
| **00232**            | **00233**            | PCS AC accumulated discharging energy   | U32       | × 0.001     | kWh  | Read-only  | พลังงานสะสม AC การคายประจุ        |
| **00234**            | **00235**            | PCS DC accumulated charging energy      | U32       | × 0.001     | kWh  | Read-only  | พลังงานสะสม DC การชาร์จ          |
| **00236**            | **00237**            | PCS DC accumulated discharging energy   | U32       | × 0.001     | kWh  | Read-only  | พลังงานสะสม DC การคายประจุ        |

### วิธีอ่านข้อมูล

#### Python Code Example
```python
# อ่าน 8 registers เริ่มจาก address 230
regs = client.read_input_registers(address=230, count=8, device_id=1)

# รวม Low และ High 16-bit เป็น 32-bit value
def combine_32bit(low, high):
    """รวม Low และ High 16-bit เป็น 32-bit unsigned integer"""
    return (high << 16) | low

# แปลงค่า (คูณด้วย 0.001)
ac_charging_kwh = combine_32bit(regs[0], regs[1]) * 0.001  # Address 230/231
ac_discharging_kwh = combine_32bit(regs[2], regs[3]) * 0.001  # Address 232/233
dc_charging_kwh = combine_32bit(regs[4], regs[5]) * 0.001  # Address 234/235
dc_discharging_kwh = combine_32bit(regs[6], regs[7]) * 0.001  # Address 236/237

# ตัวอย่าง:
# - Low (230) = 0x1234, High (231) = 0x0001
# - Combined = (1 << 16) | 0x1234 = 0x11234 = 70196 decimal
# - Energy = 70196 × 0.001 = 70.196 kWh
```

### หมายเหตุ
- **32-bit Value**: ต้องอ่าน 2 registers และรวมกัน (Low word อยู่ที่ address ต่ำกว่า)
- **Big-Endian**: High byte อยู่ก่อน Low byte
- **Range**: 0 - 4,294,967.295 kWh (U32 max × 0.001)
- **Reset**: สามารถ reset ได้ผ่าน Coil Address 5 (AC charging) และ 6 (AC discharging)

---

## L. System Clock (Input Registers - Address Type 3x)

### ข้อมูลทั่วไป
- **Function Code**: 0x04 (Read input registers)
- **Data Type**: Unsigned 16-bit Integer (U16)
- **Coefficient**: × 1.0
- **Read-Only**: Yes
- **Starting Address**: 239
- **Total Registers**: 6 (Address 239-244)

### ตารางรายละเอียด

| Modbus Address | Name   | Data Type | Coefficient | Unit | Read/Write | Description                    | Range        |
|----------------|--------|-----------|-------------|------|------------|--------------------------------|--------------|
| **00239**      | Second | U16       | × 1.0       | —    | Read-only  | วินาที (System Clock)            | 0-59         |
| **00240**      | Minute | U16       | × 1.0       | —    | Read-only  | นาที (System Clock)              | 0-59         |
| **00241**      | Hour   | U16       | × 1.0       | —    | Read-only  | ชั่วโมง (System Clock)            | 0-23         |
| **00242**      | Day    | U16       | × 1.0       | —    | Read-only  | วัน (System Clock)               | 1-31         |
| **00243**      | Month  | U16       | × 1.0       | —    | Read-only  | เดือน (System Clock)              | 1-12         |
| **00244**      | Year   | U16       | × 1.0       | —    | Read-only  | ปี (System Clock)                 | 2000-2099 (หรือ 0-99 + 2000) |

### วิธีอ่านข้อมูล

#### Python Code Example
```python
# อ่าน 6 registers เริ่มจาก address 239
regs = client.read_input_registers(address=239, count=6, device_id=1)

# แปลงค่า
system_clock = {
    "second": regs[0],  # Address 239
    "minute": regs[1],  # Address 240
    "hour": regs[2],    # Address 241
    "day": regs[3],     # Address 242
    "month": regs[4],   # Address 243
    "year": regs[5]     # Address 244 (อาจเป็น 2-digit: 23 = 2023)
}

# Format เป็น string
clock_str = f"{system_clock['year']}/{system_clock['month']:02d}/{system_clock['day']:02d} {system_clock['hour']:02d}:{system_clock['minute']:02d}:{system_clock['second']:02d}"
```

### หมายเหตุ
- **Year Format**: อาจเป็น 2-digit (23 = 2023) หรือ 4-digit ขึ้นอยู่กับ firmware
- **Synchronization**: สามารถตั้งค่าได้ผ่าน Holding Registers 330-335

---

## M. Program Version (Input Registers - Address Type 3x)

### ข้อมูลทั่วไป
- **Function Code**: 0x04 (Read input registers)
- **Data Type**: Unsigned 16-bit Integer (U16)
- **Coefficient**: × 0.1 สำหรับ PCS, × 1.0 สำหรับ FPGA และ DCDC
- **Read-Only**: Yes
- **Addresses**: 245, 246, 271

### ตารางรายละเอียด

| Modbus Address | Name                 | Data Type | Coefficient | Unit | Read/Write | Description                    | Example Value    |
|----------------|----------------------|-----------|-------------|------|------------|--------------------------------|------------------|
| **00245**      | PCS program version  | U16       | × 0.1       | —    | Read-only  | เวอร์ชันโปรแกรม PCS              | 641.0 (register = 6410) |
| **00246**      | FPGA program version | U16       | × 1.0       | —    | Read-only  | เวอร์ชันโปรแกรม FPGA             | 123 (register = 123) |
| **00271**      | DCDC program version | U16       | × 0.1       | —    | Read-only  | เวอร์ชันโปรแกรม DCDC (ถ้ามี)      | 100.0 (register = 1000) |

### วิธีอ่านข้อมูล

#### Python Code Example
```python
# อ่าน PCS และ FPGA version (Address 245-246)
version_regs = client.read_input_registers(address=245, count=2, device_id=1)
pcs_version = version_regs[0] * 0.1  # Address 245
fpga_version = version_regs[1]  # Address 246

# อ่าน DCDC version (Address 271) - ถ้ามี DCDC
dcdc_version_regs = client.read_input_registers(address=271, count=1, device_id=1)
dcdc_version = dcdc_version_regs[0] * 0.1  # Address 271

# ตัวอย่าง:
# - PCS: register = 6410 → version = 641.0
# - FPGA: register = 123 → version = 123
# - DCDC: register = 1000 → version = 100.0
```

### หมายเหตุ
- **PCS Version**: ใช้ coefficient × 0.1 (เช่น 641.0)
- **FPGA Version**: ใช้ coefficient × 1.0 (integer)
- **DCDC Version**: ใช้ coefficient × 0.1 (ถ้ามี DCDC module)
- **Version Check**: ใช้ตรวจสอบว่า firmware ตรงกับที่ต้องการหรือไม่



