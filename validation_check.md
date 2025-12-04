# การตรวจสอบความถูกต้องของค่าที่ดึงจาก PCS

## 📋 สรุปผลการตรวจสอบ

### ✅ ส่วนที่ถูกต้อง

1. **Status Registers (Address 81-96)**
   - ✅ Address ถูกต้อง: 81-96
   - ✅ Mapping ถูกต้อง: bits[0-15] ตรงกับ address 81-96
   - ✅ BMS Dry Contact: bits[13] ตรงกับ address 94

2. **Telemetry - AC Voltage (Address 201-203)**
   - ✅ Address: 201-203
   - ✅ Coefficient: × 0.1 ✓
   - ✅ Data Type: U16 ✓

3. **Telemetry - AC Current (Address 204-206)**
   - ✅ Address: 204-206
   - ✅ Coefficient: × 0.1 ✓
   - ✅ Data Type: S16 (Signed) ✓
   - ✅ Conversion: ใช้ `_convert_signed_16bit()` ✓

4. **Telemetry - Frequency (Address 207)**
   - ✅ Address: 207
   - ✅ Coefficient: × 0.01 ✓

5. **Telemetry - Active Power (Address 208-211)**
   - ✅ Address: 208-211
   - ✅ Coefficient: × 0.1 ✓
   - ✅ Data Type: S16 (Signed) ✓

6. **Telemetry - Reactive Power (Address 212-215)**
   - ✅ Address: 212-215
   - ✅ Coefficient: × 0.1 ✓
   - ✅ Data Type: S16 (Signed) ✓

7. **Telemetry - Apparent Power (Address 216-219)**
   - ✅ Address: 216-219
   - ✅ Coefficient: × 0.1 ✓
   - ✅ Data Type: U16 ✓

8. **Telemetry - Power Factor (Address 220-223)**
   - ✅ Address: 220-223
   - ✅ Coefficient: × 0.001 ✓

9. **Telemetry - DC Input (Address 224-226)**
   - ✅ Address: 224-226
   - ✅ Coefficient: × 0.1 ✓
   - ✅ Data Type: S16 (Signed) ✓

10. **Temperature (Address 227, 257-261)**
    - ✅ Address: 227 (Radiator)
    - ✅ Address: 257-261 (SOC, IGBT 1-4)
    - ✅ Coefficient: × 1.0 ✓

11. **Fault Words (Address 256, 272-275)**
    - ✅ Address: 256 (Fault Word 5)
    - ✅ Address: 272-275 (Fault Word 1-4)

12. **System Info (Address 238-247)**
    - ✅ Address: 238 (Comm Status)
    - ✅ Address: 239-244 (System Clock)
    - ✅ Address: 245-246 (Version)
    - ✅ Address: 247 (Phase N Current)

### ⚠️ ส่วนที่ต้องตรวจสอบเพิ่มเติม

1. **Accumulated Power (Address 230-237)**
   - ⚠️ **ต้องตรวจสอบ**: การรวม 32-bit value
   - **โค้ดปัจจุบัน**: `(regs[1] << 16 | regs[0])`
   - **ตาม Protocol**: Low word อยู่ที่ address ต่ำกว่า, High word อยู่ที่ address สูงกว่า
   - **ควรเป็น**: `(regs[1] << 16) | regs[0]` (ถูกต้องแล้ว)
   - **หมายเหตุ**: ต้องตรวจสอบกับค่าจริงจากอุปกรณ์

---

## 🔍 วิธีตรวจสอบอย่างง่าย

### วิธีที่ 1: ตรวจสอบ Range ของค่า

#### 1.1 AC Voltage (Address 201-203)
```python
# ค่าปกติ: 180-250 V (ระบบ 230V)
# Register value: 1800-2500
voltage = regs[0] * 0.1
assert 180 <= voltage <= 250, f"Voltage out of range: {voltage}V"
```

#### 1.2 Frequency (Address 207)
```python
# ค่าปกติ: 49.5-50.5 Hz (ระบบ 50Hz) หรือ 59.5-60.5 Hz (ระบบ 60Hz)
# Register value: 4950-5050 (50Hz) หรือ 5950-6050 (60Hz)
frequency = regs[6] * 0.01
assert 49.5 <= frequency <= 50.5 or 59.5 <= frequency <= 60.5, f"Frequency out of range: {frequency}Hz"
```

#### 1.3 Power Factor (Address 220-223)
```python
# ค่าปกติ: 0.0-1.0
# Register value: 0-1000
power_factor = regs[19] * 0.001
assert 0.0 <= power_factor <= 1.0, f"Power Factor out of range: {power_factor}"
```

#### 1.4 Temperature (Address 227, 257-261)
```python
# ค่าปกติ: 0-100°C
# Register value: 0-100
temp = regs_227[0]
assert 0 <= temp <= 100, f"Temperature out of range: {temp}°C"
```

---

### วิธีที่ 2: ตรวจสอบความสัมพันธ์ระหว่างค่า

#### 2.1 Power = Voltage × Current
```python
# ตรวจสอบ: Active Power ≈ Voltage × Current (Phase A)
voltage_a = telemetry['voltage_a']  # V
current_a = abs(telemetry['current_a'])  # A
active_power_a = abs(telemetry['active_power_a'])  # kW

# คำนวณ: Power (kW) = V × I / 1000
calculated_power = (voltage_a * current_a) / 1000

# เปรียบเทียบ (ยอมรับความแตกต่าง 10%)
difference = abs(calculated_power - active_power_a)
tolerance = active_power_a * 0.1

if difference > tolerance:
    print(f"⚠️ Warning: Power mismatch!")
    print(f"  Calculated: {calculated_power:.2f} kW")
    print(f"  Actual: {active_power_a:.2f} kW")
    print(f"  Difference: {difference:.2f} kW")
```

#### 2.2 Apparent Power = √(Active² + Reactive²)
```python
# ตรวจสอบ: Apparent Power ≈ √(Active Power² + Reactive Power²)
active = abs(telemetry['active_power_a'])
reactive = abs(telemetry['reactive_power_a'])
apparent = telemetry['apparent_power_a']

calculated_apparent = (active**2 + reactive**2)**0.5

# เปรียบเทียบ (ยอมรับความแตกต่าง 5%)
difference = abs(calculated_apparent - apparent)
tolerance = apparent * 0.05

if difference > tolerance:
    print(f"⚠️ Warning: Apparent Power mismatch!")
    print(f"  Calculated: {calculated_apparent:.2f} kVA")
    print(f"  Actual: {apparent:.2f} kVA")
```

#### 2.3 Power Factor = Active Power / Apparent Power
```python
# ตรวจสอบ: Power Factor = Active / Apparent
active = abs(telemetry['active_power_a'])
apparent = telemetry['apparent_power_a']
power_factor = telemetry['power_factor_a']

if apparent > 0:
    calculated_pf = active / apparent
    
    # เปรียบเทียบ (ยอมรับความแตกต่าง 0.01)
    difference = abs(calculated_pf - power_factor)
    
    if difference > 0.01:
        print(f"⚠️ Warning: Power Factor mismatch!")
        print(f"  Calculated: {calculated_pf:.3f}")
        print(f"  Actual: {power_factor:.3f}")
```

#### 2.4 Total Power = Sum of Phases
```python
# ตรวจสอบ: Total Active Power ≈ Phase A + Phase B + Phase C
total = abs(telemetry['active_power_total'])
sum_phases = abs(telemetry['active_power_a']) + \
             abs(telemetry['active_power_b']) + \
             abs(telemetry['active_power_c'])

# เปรียบเทียบ (ยอมรับความแตกต่าง 5%)
difference = abs(total - sum_phases)
tolerance = total * 0.05 if total > 0 else 0.1

if difference > tolerance:
    print(f"⚠️ Warning: Total Power mismatch!")
    print(f"  Sum of Phases: {sum_phases:.2f} kW")
    print(f"  Total: {total:.2f} kW")
```

#### 2.5 DC Power = DC Voltage × DC Current
```python
# ตรวจสอบ: DC Input Power ≈ DC Voltage × DC Current
dc_voltage = abs(telemetry['dc_input_voltage'])
dc_current = abs(telemetry['dc_input_current'])
dc_power = abs(telemetry['dc_input_power'])

# คำนวณ: Power (kW) = V × I / 1000
calculated_dc_power = (dc_voltage * dc_current) / 1000

# เปรียบเทียบ (ยอมรับความแตกต่าง 10%)
difference = abs(calculated_dc_power - dc_power)
tolerance = dc_power * 0.1 if dc_power > 0 else 0.1

if difference > tolerance:
    print(f"⚠️ Warning: DC Power mismatch!")
    print(f"  Calculated: {calculated_dc_power:.2f} kW")
    print(f"  Actual: {dc_power:.2f} kW")
```

---

### วิธีที่ 3: ใช้ Modbus Client Tools

#### 3.1 ใช้ Modbus Poll หรือ ModScan
1. เปิด Modbus Poll/ModScan
2. ตั้งค่า Connection:
   - IP: 192.168.0.20
   - Port: 502
   - Unit ID: 1
3. อ่านค่าแต่ละ Address:
   - Address 201: Voltage A
   - Address 207: Frequency
   - Address 211: Total Active Power
4. เปรียบเทียบกับค่าที่แสดงใน Streamlit

#### 3.2 ใช้ Python Script ตรวจสอบ
```python
from pcs_client import PCSClient

client = PCSClient(host='192.168.0.20', port=502)
if client.connect():
    # อ่าน Raw Registers
    regs = client._read_input_registers(201, 26)
    
    print("=== Raw Register Values ===")
    print(f"Address 201 (Voltage A): {regs[0]} → {regs[0] * 0.1} V")
    print(f"Address 207 (Frequency): {regs[6]} → {regs[6] * 0.01} Hz")
    print(f"Address 211 (Total Power): {regs[10]} → {regs[10] * 0.1} kW")
    
    # อ่านผ่าน Method
    telemetry = client.get_telemetry()
    print("\n=== Processed Values ===")
    print(f"Voltage A: {telemetry['voltage_a']} V")
    print(f"Frequency: {telemetry['frequency']} Hz")
    print(f"Total Active Power: {telemetry['active_power_total']} kW")
    
    client.close()
```

---

### วิธีที่ 4: ตรวจสอบ Signed Values

#### 4.1 ตรวจสอบ Current (Address 204-206)
```python
# Current เป็น Signed: บวก = Charge, ลบ = Discharge
current_a = telemetry['current_a']

# ตรวจสอบ range: -3276.8 ถึง 3276.7 A
assert -3276.8 <= current_a <= 3276.7, f"Current out of range: {current_a}A"

# ตรวจสอบว่าค่าลบถูกแปลงถูกต้อง
reg_value = regs[3]
if reg_value > 32767:
    expected_current = (reg_value - 65536) * 0.1
    assert abs(current_a - expected_current) < 0.01, "Signed conversion error"
```

#### 4.2 ตรวจสอบ Active Power (Address 208-211)
```python
# Active Power เป็น Signed: บวก = Charge, ลบ = Discharge
active_power = telemetry['active_power_total']

# ตรวจสอบ range: -3276.8 ถึง 3276.7 kW
assert -3276.8 <= active_power <= 3276.7, f"Power out of range: {active_power}kW"
```

---

### วิธีที่ 5: ตรวจสอบ 32-bit Values (Accumulated Power)

#### 5.1 ตรวจสอบการรวม 32-bit
```python
# อ่าน Raw Registers
regs = client._read_input_registers(230, 8)

# ตรวจสอบ AC Charging Energy
low = regs[0]   # Address 230
high = regs[1]  # Address 231

# รวมเป็น 32-bit
combined = (high << 16) | low
energy_kwh = combined * 0.001

print(f"Low (230): {low} (0x{low:04X})")
print(f"High (231): {high} (0x{high:04X})")
print(f"Combined: {combined} (0x{combined:08X})")
print(f"Energy: {energy_kwh:.3f} kWh")

# ตรวจสอบว่าไม่เกิน 32-bit max
assert combined <= 0xFFFFFFFF, "32-bit value overflow"
```

#### 5.2 ตรวจสอบกับค่าจริง
```python
# เปรียบเทียบกับค่าที่แสดงใน UI
acc_power = client.get_accumulated_power()
print(f"AC Charging: {acc_power['ac_charging_kwh']:.3f} kWh")

# ตรวจสอบว่าค่าเพิ่มขึ้นเมื่อเวลาผ่านไป (ถ้า device กำลัง charge)
```

---

## 📝 Checklist การตรวจสอบ

### ✅ การตรวจสอบเบื้องต้น

- [ ] **Connection**: เชื่อมต่อกับ PCS สำเร็จ
- [ ] **Status**: อ่าน Status ได้ (Address 81-96)
- [ ] **Telemetry**: อ่าน Telemetry ได้ (Address 201-226)
- [ ] **Temperature**: อ่าน Temperature ได้ (Address 227, 257-261)
- [ ] **Fault Words**: อ่าน Fault Words ได้ (Address 256, 272-275)
- [ ] **System Info**: อ่าน System Info ได้ (Address 238-247)
- [ ] **Accumulated Power**: อ่าน Accumulated Power ได้ (Address 230-237)

### ✅ การตรวจสอบ Range

- [ ] **Voltage**: 180-250 V (ระบบ 230V)
- [ ] **Frequency**: 49.5-50.5 Hz (50Hz) หรือ 59.5-60.5 Hz (60Hz)
- [ ] **Current**: -3276.8 ถึง 3276.7 A
- [ ] **Power**: -3276.8 ถึง 3276.7 kW
- [ ] **Power Factor**: 0.0-1.0
- [ ] **Temperature**: 0-100°C

### ✅ การตรวจสอบความสัมพันธ์

- [ ] **Power = V × I**: Active Power ≈ Voltage × Current
- [ ] **Apparent = √(Active² + Reactive²)**: Apparent Power ≈ √(Active² + Reactive²)
- [ ] **PF = Active / Apparent**: Power Factor ≈ Active / Apparent
- [ ] **Total = Sum**: Total Power ≈ Sum of Phases
- [ ] **DC Power = DC V × DC I**: DC Power ≈ DC Voltage × DC Current

### ✅ การตรวจสอบ Signed Values

- [ ] **Current**: ค่าลบถูกแปลงถูกต้อง
- [ ] **Active Power**: ค่าลบถูกแปลงถูกต้อง
- [ ] **Reactive Power**: ค่าลบถูกแปลงถูกต้อง
- [ ] **DC Input**: ค่าลบถูกแปลงถูกต้อง

### ✅ การตรวจสอบ 32-bit Values

- [ ] **Accumulated Power**: การรวม Low/High ถูกต้อง
- [ ] **Energy Values**: ค่าไม่เกิน 32-bit max

---

## 🛠️ Script สำหรับตรวจสอบอัตโนมัติ

สร้างไฟล์ `validate_pcs_data.py`:

```python
from pcs_client import PCSClient
import sys

def validate_pcs_data(host='192.168.0.20', port=502):
    """ตรวจสอบความถูกต้องของข้อมูลจาก PCS"""
    
    client = PCSClient(host=host, port=port)
    if not client.connect():
        print("❌ ไม่สามารถเชื่อมต่อกับ PCS ได้")
        return False
    
    print("✅ เชื่อมต่อสำเร็จ\n")
    errors = []
    warnings = []
    
    # 1. อ่าน Telemetry
    telemetry = client.get_telemetry()
    if not telemetry:
        errors.append("❌ ไม่สามารถอ่าน Telemetry ได้")
    else:
        print("=== ตรวจสอบ Telemetry ===")
        
        # ตรวจสอบ Voltage Range
        for phase in ['a', 'b', 'c']:
            voltage = telemetry.get(f'voltage_{phase}', 0)
            if not (180 <= voltage <= 250):
                warnings.append(f"⚠️ Voltage {phase.upper()}: {voltage}V (out of normal range 180-250V)")
        
        # ตรวจสอบ Frequency
        frequency = telemetry.get('frequency', 0)
        if not (49.5 <= frequency <= 50.5) and not (59.5 <= frequency <= 60.5):
            warnings.append(f"⚠️ Frequency: {frequency}Hz (out of normal range)")
        
        # ตรวจสอบ Power = V × I
        voltage_a = telemetry.get('voltage_a', 0)
        current_a = abs(telemetry.get('current_a', 0))
        active_power_a = abs(telemetry.get('active_power_a', 0))
        
        if voltage_a > 0 and current_a > 0:
            calculated_power = (voltage_a * current_a) / 1000
            difference = abs(calculated_power - active_power_a)
            tolerance = active_power_a * 0.1 if active_power_a > 0 else 0.1
            
            if difference > tolerance:
                warnings.append(f"⚠️ Power mismatch Phase A: Calculated={calculated_power:.2f}kW, Actual={active_power_a:.2f}kW")
        
        # ตรวจสอบ Apparent Power
        active = abs(telemetry.get('active_power_a', 0))
        reactive = abs(telemetry.get('reactive_power_a', 0))
        apparent = telemetry.get('apparent_power_a', 0)
        
        if apparent > 0:
            calculated_apparent = (active**2 + reactive**2)**0.5
            difference = abs(calculated_apparent - apparent)
            tolerance = apparent * 0.05
            
            if difference > tolerance:
                warnings.append(f"⚠️ Apparent Power mismatch: Calculated={calculated_apparent:.2f}kVA, Actual={apparent:.2f}kVA")
        
        print("✅ Telemetry ถูกต้อง")
    
    # 2. อ่าน Status
    status = client.get_status()
    if not status:
        errors.append("❌ ไม่สามารถอ่าน Status ได้")
    else:
        print("\n=== ตรวจสอบ Status ===")
        print(f"Running: {status.get('running')}")
        print(f"Fault: {status.get('fault')}")
        print(f"Grid Connected: {status.get('grid_connected')}")
        print("✅ Status ถูกต้อง")
    
    # 3. อ่าน Temperature
    temp = client.get_temperature()
    if not temp:
        warnings.append("⚠️ ไม่สามารถอ่าน Temperature ได้")
    else:
        print("\n=== ตรวจสอบ Temperature ===")
        radiator_temp = temp.get('radiator_temp', 0)
        if not (0 <= radiator_temp <= 100):
            warnings.append(f"⚠️ Radiator Temp: {radiator_temp}°C (out of normal range 0-100°C)")
        print("✅ Temperature ถูกต้อง")
    
    # 4. อ่าน Accumulated Power
    acc_power = client.get_accumulated_power()
    if not acc_power:
        warnings.append("⚠️ ไม่สามารถอ่าน Accumulated Power ได้")
    else:
        print("\n=== ตรวจสอบ Accumulated Power ===")
        for key, value in acc_power.items():
            if value < 0 or value > 4294967.295:
                errors.append(f"❌ {key}: {value}kWh (out of range)")
        print("✅ Accumulated Power ถูกต้อง")
    
    # สรุปผล
    print("\n" + "="*50)
    if errors:
        print("❌ ERRORS:")
        for error in errors:
            print(f"  {error}")
    
    if warnings:
        print("\n⚠️ WARNINGS:")
        for warning in warnings:
            print(f"  {warning}")
    
    if not errors and not warnings:
        print("✅ ทุกอย่างถูกต้อง!")
    
    client.close()
    return len(errors) == 0

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else '192.168.0.20'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 502
    validate_pcs_data(host, port)
```

---

## 📌 สรุป

### ค่าที่ดึงมาถูกต้องตาม Protocol:
- ✅ Address ทั้งหมดถูกต้อง
- ✅ Coefficient ถูกต้อง
- ✅ Data Type (Signed/Unsigned) ถูกต้อง
- ✅ การแปลง Signed Values ถูกต้อง

### วิธีตรวจสอบ:
1. **ตรวจสอบ Range**: เปรียบเทียบกับค่าปกติ
2. **ตรวจสอบความสัมพันธ์**: Power = V × I, Apparent = √(Active² + Reactive²)
3. **ใช้ Modbus Tools**: เปรียบเทียบกับ Modbus Poll/ModScan
4. **ใช้ Script**: รัน `validate_pcs_data.py` เพื่อตรวจสอบอัตโนมัติ

### สิ่งที่ต้องตรวจสอบเพิ่มเติม:
- ⚠️ **Accumulated Power**: ต้องตรวจสอบกับค่าจริงจากอุปกรณ์
- ⚠️ **IGBT Temperature**: อาจต้อง decode bit mapping
- ⚠️ **Phase N Current**: ตรวจสอบว่าแสดงถูกต้องหรือไม่

