# PCS UI Tutorial - คู่มืออธิบายโค้ด pcs_ui.py

## 📋 สารบัญ
1. [ภาพรวมโปรเจค](#ภาพรวมโปรเจค)
2. [โครงสร้างโค้ด](#โครงสร้างโค้ด)
3. [การ Import Libraries](#การ-import-libraries)
4. [Page Configuration](#page-configuration)
5. [Session State Management](#session-state-management)
6. [Functions](#functions)
7. [Sidebar UI](#sidebar-ui)
8. [Main Content Sections](#main-content-sections)
9. [วิธีคิดและแนวทางการออกแบบ](#วิธีคิดและแนวทางการออกแบบ)
10. [การใช้งาน](#การใช้งาน)

---

## ภาพรวมโปรเจค

**PCS Control Panel** เป็น Web Application ที่สร้างด้วย Streamlit เพื่อควบคุมและตรวจสอบสถานะของ PCS (Power Conversion System) ผ่าน Modbus TCP Protocol

### วัตถุประสงค์
- แสดงข้อมูลสถานะของ PCS แบบ Real-time
- ควบคุมการทำงานของ PCS (Start, Stop, Reset)
- ตั้งค่าพารามิเตอร์การทำงาน
- แสดงข้อมูล Telemetry ครบถ้วน

---

## โครงสร้างโค้ด

```
pcs_ui.py
├── Import Statements (บรรทัด 1-4)
├── Page Configuration (บรรทัด 6-12)
├── Session State Initialization (บรรทัด 14-22)
├── Functions (บรรทัด 24-52)
│   ├── connect_pcs()
│   └── disconnect_pcs()
├── Sidebar UI (บรรทัด 54-89)
│   ├── Connection Settings
│   └── Device Controls
└── Main Content (บรรทัด 91-311)
    ├── Connection Status Banner
    ├── Device Status
    ├── AC Power & Frequency
    ├── AC Voltage & Current
    ├── DC Input
    ├── Temperature
    ├── Accumulated Power
    ├── Fault Words
    ├── System Information
    └── Settings
```

---

## การ Import Libraries

```python
import streamlit as st
import time
import pandas as pd
from pcs_client import PCSClient
```

### อธิบายแต่ละ Library

#### 1. `streamlit as st`
- **หน้าที่**: Framework หลักสำหรับสร้าง Web UI
- **ใช้สำหรับ**: 
  - สร้าง UI components (buttons, text inputs, metrics)
  - จัดการ Session State
  - แสดงข้อมูลในรูปแบบต่างๆ

#### 2. `time`
- **หน้าที่**: จัดการเวลาและ delay
- **ใช้สำหรับ**: 
  - Auto refresh (delay 5 วินาที)
  - ควบคุม timing ของการอัพเดทข้อมูล

#### 3. `pandas as pd`
- **หน้าที่**: จัดการข้อมูลแบบ DataFrame
- **หมายเหตุ**: Import มาแต่ไม่ได้ใช้ในโค้ดปัจจุบัน (อาจใช้ในอนาคตสำหรับแสดงข้อมูลแบบตาราง)

#### 4. `from pcs_client import PCSClient`
- **หน้าที่**: Import class สำหรับเชื่อมต่อกับ PCS ผ่าน Modbus
- **ใช้สำหรับ**: 
  - สร้าง connection กับ PCS device
  - อ่านข้อมูล Telemetry
  - ส่งคำสั่งควบคุม

---

## Page Configuration

```python
st.set_page_config(
    page_title="PCS Control Panel",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
```

### พารามิเตอร์

| พารามิเตอร์ | ค่า | อธิบาย |
|------------|-----|--------|
| `page_title` | "PCS Control Panel" | ชื่อที่แสดงใน Browser Tab |
| `page_icon` | "⚡" | Icon ที่แสดงใน Browser Tab |
| `layout` | "wide" | ใช้ layout แบบกว้าง (เต็มหน้าจอ) |
| `initial_sidebar_state` | "expanded" | Sidebar แสดงตั้งแต่เริ่มต้น |

### วิธีคิด
- **layout="wide"**: ต้องการแสดงข้อมูลหลายคอลัมน์ จึงใช้ wide layout
- **initial_sidebar_state="expanded"**: ต้องการให้ผู้ใช้เห็น controls ตั้งแต่เริ่มต้น

---

## Session State Management

```python
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'client' not in st.session_state:
    st.session_state.client = None
if 'connection_info' not in st.session_state:
    st.session_state.connection_info = None
if 'last_update' not in st.session_state:
    st.session_state.last_update = 0
```

### อธิบาย Session State

**Session State** คือตัวแปรที่เก็บข้อมูลระหว่างการ refresh หน้าเว็บใน Streamlit

#### 1. `st.session_state.connected`
- **ประเภท**: Boolean
- **ค่าเริ่มต้น**: `False`
- **หน้าที่**: เก็บสถานะการเชื่อมต่อกับ PCS
- **ใช้เมื่อ**: ตรวจสอบว่ามีการเชื่อมต่ออยู่หรือไม่

#### 2. `st.session_state.client`
- **ประเภท**: `PCSClient` object หรือ `None`
- **ค่าเริ่มต้น**: `None`
- **หน้าที่**: เก็บ instance ของ PCSClient ที่เชื่อมต่ออยู่
- **ใช้เมื่อ**: เรียกใช้ methods เพื่ออ่านข้อมูลหรือส่งคำสั่ง

#### 3. `st.session_state.connection_info`
- **ประเภท**: Dictionary หรือ `None`
- **ค่าเริ่มต้น**: `None`
- **หน้าที่**: เก็บข้อมูลการเชื่อมต่อ (host, port, unit_id)
- **โครงสร้าง**:
  ```python
  {
      'host': '192.168.0.20',
      'port': 502,
      'unit_id': 1
  }
  ```

#### 4. `st.session_state.last_update`
- **ประเภท**: Integer (timestamp)
- **ค่าเริ่มต้น**: `0`
- **หน้าที่**: เก็บเวลาที่อัพเดทข้อมูลล่าสุด
- **หมายเหตุ**: ยังไม่ได้ใช้ในโค้ดปัจจุบัน (อาจใช้สำหรับ auto-refresh แบบ advanced)

### วิธีคิด
- **ตรวจสอบก่อนสร้าง**: ใช้ `if 'key' not in st.session_state` เพื่อป้องกันการ reset ค่าเมื่อ refresh
- **เก็บ Object**: เก็บ `client` object ใน session state เพื่อไม่ต้องสร้างใหม่ทุกครั้ง

---

## Functions

### 1. Function: `connect_pcs(host, port)`

```python
def connect_pcs(host, port):
    with st.spinner(f"กำลังเชื่อมต่อไปยัง {host}:{port}..."):
        client = PCSClient(host=host, port=port)
        if client.connect():
            st.session_state.connected = True
            st.session_state.client = client
            st.session_state.connection_info = {
                'host': host,
                'port': port,
                'unit_id': client.unit_id
            }
            st.success(f"✅ เชื่อมต่อสำเร็จ: {host}:{port} (Unit ID: {client.unit_id})")
        else:
            st.session_state.connected = False
            st.session_state.client = None
            st.session_state.connection_info = None
            st.error(f"❌ เชื่อมต่อไม่สำเร็จ: {host}:{port}\n\nกรุณาตรวจสอบ:\n- IP Address ถูกต้อง\n- Port ถูกต้อง (502)\n- อุปกรณ์ PCS เปิดอยู่\n- Network connection")
```

#### อธิบายทีละส่วน

##### Parameters
- `host` (str): IP Address ของ PCS device
- `port` (int): Port number (ปกติ 502 สำหรับ Modbus TCP)

##### Process Flow

1. **แสดง Loading Spinner**
   ```python
   with st.spinner(f"กำลังเชื่อมต่อไปยัง {host}:{port}..."):
   ```
   - แสดง spinner ขณะกำลังเชื่อมต่อ
   - `with` statement ทำให้ spinner หยุดอัตโนมัติเมื่อออกจาก block

2. **สร้าง PCSClient Instance**
   ```python
   client = PCSClient(host=host, port=port)
   ```
   - สร้าง object สำหรับเชื่อมต่อ Modbus

3. **ลองเชื่อมต่อ**
   ```python
   if client.connect():
   ```
   - เรียก method `connect()` ของ PCSClient
   - คืนค่า `True` ถ้าสำเร็จ, `False` ถ้าไม่สำเร็จ

4. **กรณีเชื่อมต่อสำเร็จ**
   ```python
   st.session_state.connected = True
   st.session_state.client = client
   st.session_state.connection_info = {...}
   st.success(...)
   ```
   - อัพเดท session state ทั้งหมด
   - แสดงข้อความสำเร็จ

5. **กรณีเชื่อมต่อไม่สำเร็จ**
   ```python
   st.session_state.connected = False
   st.session_state.client = None
   st.session_state.connection_info = None
   st.error(...)
   ```
   - Reset session state
   - แสดงข้อความ error พร้อมคำแนะนำ

#### วิธีคิด
- **Error Handling**: แสดงข้อความ error ที่เป็นประโยชน์
- **State Management**: อัพเดท state ทั้งหมดในที่เดียว
- **User Feedback**: ใช้ spinner และ success/error messages

---

### 2. Function: `disconnect_pcs()`

```python
def disconnect_pcs():
    if st.session_state.client:
        st.session_state.client.close()
    connection_info = st.session_state.connection_info
    st.session_state.connected = False
    st.session_state.client = None
    st.session_state.connection_info = None
    if connection_info:
        st.info(f"🔌 ตัดการเชื่อมต่อจาก {connection_info['host']}:{connection_info['port']}")
    else:
        st.info("🔌 ตัดการเชื่อมต่อแล้ว")
```

#### อธิบายทีละส่วน

##### Process Flow

1. **ปิด Connection (ถ้ามี)**
   ```python
   if st.session_state.client:
       st.session_state.client.close()
   ```
   - ตรวจสอบว่ามี client object หรือไม่
   - เรียก `close()` เพื่อปิด Modbus connection

2. **เก็บ Connection Info ก่อน Reset**
   ```python
   connection_info = st.session_state.connection_info
   ```
   - เก็บข้อมูลไว้ก่อน reset เพื่อใช้แสดงข้อความ

3. **Reset Session State**
   ```python
   st.session_state.connected = False
   st.session_state.client = None
   st.session_state.connection_info = None
   ```
   - Reset ทุก state เป็นค่าเริ่มต้น

4. **แสดงข้อความ**
   ```python
   if connection_info:
       st.info(f"🔌 ตัดการเชื่อมต่อจาก {connection_info['host']}:{connection_info['port']}")
   else:
       st.info("🔌 ตัดการเชื่อมต่อแล้ว")
   ```
   - แสดงข้อมูลการเชื่อมต่อที่ตัดออก (ถ้ามี)

#### วิธีคิด
- **Safe Disconnect**: ตรวจสอบว่ามี client ก่อนเรียก close()
- **User Feedback**: แสดงข้อมูลการตัดการเชื่อมต่อ

---

## Sidebar UI

### โครงสร้าง Sidebar

```python
with st.sidebar:
    # Connection Settings
    # Controls
```

### 1. Connection Settings Section

```python
st.header("🔌 Connection")
host = st.text_input("Host IP", value="192.168.0.20")
port = st.number_input("Port", value=502, step=1)

col1, col2 = st.columns(2)
with col1:
    if st.button("Connect", disabled=st.session_state.connected):
        connect_pcs(host, port)
with col2:
    if st.button("Disconnect", disabled=not st.session_state.connected):
        disconnect_pcs()
```

#### อธิบาย Components

##### `st.text_input("Host IP", value="192.168.0.20")`
- **หน้าที่**: สร้าง input field สำหรับ IP Address
- **ค่าเริ่มต้น**: "192.168.0.20" (ตาม PCS Protocol)
- **คืนค่า**: String (IP address)

##### `st.number_input("Port", value=502, step=1)`
- **หน้าที่**: สร้าง input field สำหรับ Port number
- **ค่าเริ่มต้น**: 502 (Modbus TCP default port)
- **step=1**: เพิ่ม/ลดทีละ 1

##### `st.columns(2)`
- **หน้าที่**: แบ่งพื้นที่เป็น 2 คอลัมน์
- **ใช้สำหรับ**: จัดวางปุ่ม Connect และ Disconnect ข้างกัน

##### `st.button("Connect", disabled=st.session_state.connected)`
- **disabled**: ปิดการใช้งานปุ่มเมื่อ `connected=True`
- **เหตุผล**: ป้องกันการเชื่อมต่อซ้ำ

##### `st.button("Disconnect", disabled=not st.session_state.connected)`
- **disabled**: ปิดการใช้งานปุ่มเมื่อ `connected=False`
- **เหตุผล**: ไม่สามารถตัดการเชื่อมต่อถ้ายังไม่ได้เชื่อมต่อ

#### วิธีคิด
- **Default Values**: ใช้ค่าตาม Protocol เพื่อความสะดวก
- **Button States**: ใช้ disabled เพื่อป้องกันการกระทำที่ไม่ถูกต้อง
- **Layout**: ใช้ columns เพื่อจัดวางปุ่มให้สวยงาม

---

### 2. Controls Section

```python
st.markdown("---")
st.header("⚙️ Controls")
if st.session_state.connected:
    if st.button("Start Device", type="primary"):
        if st.session_state.client.start_device():
            st.success("Start command sent")
        else:
            st.error("Failed to send start command")
    
    if st.button("Stop Device", type="secondary"):
        if st.session_state.client.stop_device():
            st.warning("Stop command sent")
        else:
            st.error("Failed to send stop command")

    if st.button("Reset Fault"):
        if st.session_state.client.reset_fault():
            st.info("Reset fault command sent")
        else:
            st.error("Failed to send reset command")
else:
    st.info("Connect to enable controls")
```

#### อธิบาย Components

##### Conditional Rendering
```python
if st.session_state.connected:
    # แสดง controls
else:
    st.info("Connect to enable controls")
```
- แสดง controls เฉพาะเมื่อเชื่อมต่อแล้ว
- แสดงข้อความแนะนำเมื่อยังไม่ได้เชื่อมต่อ

##### Button Types
- `type="primary"`: ปุ่ม Start (สีเขียว, สำคัญที่สุด)
- `type="secondary"`: ปุ่ม Stop (สีเทา)
- ไม่ระบุ type: ปุ่ม Reset Fault (default)

##### Command Execution
```python
if st.session_state.client.start_device():
    st.success("Start command sent")
else:
    st.error("Failed to send start command")
```
- เรียก method จาก PCSClient
- แสดงผลลัพธ์ตาม success/error

#### วิธีคิด
- **Safety**: แสดง controls เฉพาะเมื่อเชื่อมต่อแล้ว
- **Visual Hierarchy**: ใช้ button types เพื่อแสดงความสำคัญ
- **Feedback**: แสดงผลลัพธ์ทันทีหลังกดปุ่ม

---

## Main Content Sections

### 1. Connection Status Banner

```python
if st.session_state.connected and st.session_state.connection_info:
    info = st.session_state.connection_info
    st.success(f"🟢 **เชื่อมต่ออยู่**: {info['host']}:{info['port']} | Unit ID: {info['unit_id']}")
elif not st.session_state.connected:
    st.warning("🔴 **ยังไม่ได้เชื่อมต่อ** - กรุณาเชื่อมต่อผ่าน Sidebar")
```

#### อธิบาย
- **แสดงที่ด้านบน**: ให้เห็นสถานะทันที
- **ใช้ Emoji**: 🟢 = เชื่อมต่อ, 🔴 = ไม่ได้เชื่อมต่อ
- **แสดงข้อมูล**: IP, Port, Unit ID

---

### 2. Refresh Controls

```python
col_refresh, col_auto = st.columns([1, 4])
with col_refresh:
    if st.button("🔄 Refresh Data"):
        st.rerun()
with col_auto:
    auto_refresh = st.checkbox("Auto Refresh (5s)", value=False)
    if auto_refresh:
        time.sleep(5)
        st.rerun()
```

#### อธิบาย

##### `st.columns([1, 4])`
- แบ่งพื้นที่เป็น 2 คอลัมน์ (อัตราส่วน 1:4)
- คอลัมน์แรก: ปุ่ม Refresh
- คอลัมน์สอง: Checkbox Auto Refresh

##### `st.rerun()`
- รัน script ใหม่ทั้งหมด
- ทำให้ข้อมูลอัพเดท

##### Auto Refresh Logic
```python
if auto_refresh:
    time.sleep(5)
    st.rerun()
```
- **ปัญหา**: `time.sleep(5)` จะบล็อก UI
- **วิธีแก้ที่ดีกว่า**: ใช้ `st.rerun()` กับ timer หรือใช้ `st.empty()` กับ loop

#### วิธีคิด
- **Manual Refresh**: ให้ผู้ใช้ควบคุมได้
- **Auto Refresh**: สะดวกสำหรับ monitoring
- **Note**: Implementation ปัจจุบันมีข้อจำกัด (ควรใช้ threading หรือ async)

---

### 3. Device Status Section

```python
st.subheader("📊 สถานะอุปกรณ์")
status = client.get_status()
if status:
    cols = st.columns(6)
    cols[0].metric("Running", "🟢 ON" if status.get("running") else "🔴 OFF")
    cols[1].metric("Fault", "🔴 YES" if status.get("fault") else "🟢 NO")
    # ... อื่นๆ
```

#### อธิบาย

##### `client.get_status()`
- เรียก method จาก PCSClient
- อ่าน Discrete Inputs (Address 81-96)
- คืนค่า Dictionary ของสถานะ

##### `st.columns(6)`
- แบ่งเป็น 6 คอลัมน์
- แสดงสถานะหลัก 6 อย่าง

##### `st.metric()`
- แสดงค่าแบบ metric card
- รองรับ emoji และ formatting

##### Conditional Display
```python
"🟢 ON" if status.get("running") else "🔴 OFF"
```
- ใช้ ternary operator
- แสดง emoji ตามสถานะ

##### Expander
```python
with st.expander("รายละเอียดสถานะเพิ่มเติม"):
    st.write(...)
```
- ซ่อนรายละเอียดเพิ่มเติม
- คลิกเพื่อขยาย

#### วิธีคิด
- **Visual Indicators**: ใช้ emoji และสีเพื่อให้เห็นชัด
- **Information Hierarchy**: แสดงข้อมูลสำคัญก่อน, รายละเอียดใน expander
- **Error Handling**: ตรวจสอบ `if status:` ก่อนแสดง

---

### 4. AC Power & Frequency Section

```python
st.subheader("⚡ กำลังไฟฟ้า AC")
telemetry = client.get_telemetry()
if telemetry:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Active Power", f"{telemetry.get('active_power_total', 0):.2f} kW")
    # ...
```

#### อธิบาย

##### `client.get_telemetry()`
- อ่าน Input Registers (Address 201-226)
- คืนค่า Dictionary ของ telemetry data

##### String Formatting
```python
f"{telemetry.get('active_power_total', 0):.2f} kW"
```
- `.get('key', 0)`: ใช้ค่า default ถ้าไม่มี key
- `:.2f`: แสดงทศนิยม 2 ตำแหน่ง

##### Expander for Details
```python
with st.expander("กำลังไฟฟ้าตาม Phase"):
    p_cols = st.columns(3)
    # แสดงข้อมูลแต่ละ Phase
```
- ซ่อนรายละเอียดแต่ละ Phase
- ใช้ columns เพื่อจัดเรียง

#### วิธีคิด
- **Summary First**: แสดงสรุปก่อน (Total)
- **Details in Expander**: รายละเอียดแต่ละ Phase อยู่ใน expander
- **Consistent Formatting**: ใช้ format เดียวกันทั้งหน้า

---

### 5. AC Voltage & Current Section

```python
st.subheader("🔌 แรงดันและกระแส AC")
if telemetry:
    st.markdown("#### แรงดัน (V)")
    v_cols = st.columns(4)
    v_cols[0].metric("Phase A", f"{telemetry.get('voltage_a', 0):.1f} V")
    # ...
```

#### อธิบาย

##### `st.markdown("#### แรงดัน (V)")`
- ใช้ Markdown สำหรับหัวข้อย่อย
- `####` = Heading level 4

##### 4 Columns Layout
- Phase A, B, C, N
- แสดงแรงดันและกระแสแยกกัน

##### Getting Phase N Current
```python
sys_info = client.get_system_info()
if sys_info:
    c_cols[3].metric("Phase N", f"{sys_info.get('current_n', 0):.2f} A")
```
- Phase N current อยู่ใน system info
- ต้องเรียก `get_system_info()` แยก

#### วิธีคิด
- **Grouping**: แยกแรงดันและกระแสเป็น section ย่อย
- **Consistency**: ใช้ layout เดียวกัน (4 columns)

---

### 6. DC Input Section

```python
st.subheader("🔋 ข้อมูล DC Input")
if telemetry:
    dc_cols = st.columns(3)
    dc_cols[0].metric("DC Input Power", f"{telemetry.get('dc_input_power', 0):.2f} kW")
    # ...
```

#### อธิบาย
- แสดงข้อมูล DC Input จาก telemetry
- 3 คอลัมน์: Power, Voltage, Current
- ใช้ข้อมูลจาก `get_telemetry()` เดียวกัน

---

### 7. Temperature Section

```python
st.subheader("🌡️ อุณหภูมิ")
temp = client.get_temperature()
if temp:
    temp_cols = st.columns(3)
    temp_cols[0].metric("Radiator Temp", f"{temp.get('radiator_temp', 0):.1f} °C")
    # ...
    
    with st.expander("IGBT Temperature"):
        igbt_cols = st.columns(4)
        # แสดง IGBT 1-4
```

#### อธิบาย

##### `client.get_temperature()`
- อ่าน Input Registers (Address 227, 257-261)
- คืนค่า Dictionary ของอุณหภูมิ

##### IGBT Temperature in Expander
- แสดง IGBT 1-4 ใน expander
- 4 columns layout

#### วิธีคิด
- **Main Temperatures**: Radiator และ SOC แสดงหลัก
- **IGBT Details**: อยู่ใน expander (ข้อมูลรอง)

---

### 8. Accumulated Power Section

```python
st.subheader("📈 พลังงานสะสม")
acc_power = client.get_accumulated_power()
if acc_power:
    acc_cols = st.columns(4)
    acc_cols[0].metric("AC Charging", f"{acc_power.get('ac_charging_kwh', 0):.3f} kWh")
    # ...
```

#### อธิบาย

##### `client.get_accumulated_power()`
- อ่าน Input Registers (Address 230-237)
- รวม Low และ High 16 bits เป็น 32-bit value
- คืนค่า Dictionary ของพลังงานสะสม

##### Formatting
- `.3f`: แสดงทศนิยม 3 ตำแหน่ง (kWh มักมีค่ามาก)

---

### 9. Fault Words Section

```python
st.subheader("⚠️ Fault Words")
fault_words = client.get_fault_words()
if fault_words:
    fault_cols = st.columns(5)
    fault_cols[0].metric("Fault Word 1", f"0x{fault_words.get('fault_word_1', 0):04X}")
    # ...
    
    has_fault = any([
        fault_words.get('fault_word_1', 0) != 0,
        # ...
    ])
    
    if has_fault:
        st.error("⚠️ พบ Fault Words ที่ไม่เป็นศูนย์ - กรุณาตรวจสอบ")
    else:
        st.success("✅ ไม่พบ Fault")
```

#### อธิบาย

##### Hexadecimal Formatting
```python
f"0x{fault_words.get('fault_word_1', 0):04X}"
```
- `0x`: Prefix สำหรับ hex
- `04X`: แสดง 4 หลัก, ตัวพิมพ์ใหญ่, เติม 0 ด้านหน้า

##### Fault Detection
```python
has_fault = any([...])
```
- ใช้ `any()` เพื่อตรวจสอบว่ามี fault word ใดไม่เป็น 0
- `any()` คืนค่า `True` ถ้ามีอย่างน้อย 1 ค่าเป็น `True`

##### Conditional Message
- แสดง error ถ้ามี fault
- แสดง success ถ้าไม่มี fault

#### วิธีคิด
- **Visual Alert**: ใช้ `st.error()` เพื่อดึงความสนใจ
- **Automatic Detection**: ตรวจสอบอัตโนมัติ ไม่ต้องอ่าน hex เอง

---

### 10. System Information Section

```python
st.subheader("ℹ️ ข้อมูลระบบ")
sys_info = client.get_system_info()
if sys_info:
    sys_cols = st.columns(4)
    clock = sys_info.get('system_clock', {})
    sys_cols[0].metric("PCS Version", f"{sys_info.get('pcs_version', 0):.1f}")
    # ...
    
    if clock:
        sys_cols[3].write(f"**System Clock**: {clock.get('year', 0)}/{clock.get('month', 0):02d}/...")
```

#### อธิบาย

##### `client.get_system_info()`
- อ่าน Input Registers (Address 238-247)
- รวมข้อมูล version, clock, communication status

##### Date Formatting
```python
f"{clock.get('year', 0)}/{clock.get('month', 0):02d}/{clock.get('day', 0):02d}"
```
- `02d`: แสดง 2 หลัก, เติม 0 ด้านหน้า (เช่น 01, 02, 03)

##### `st.write()` vs `st.metric()`
- `st.write()`: สำหรับข้อความยาว
- `st.metric()`: สำหรับตัวเลขเดี่ยว

---

### 11. Settings Section

```python
st.subheader("⚙️ การตั้งค่า")
with st.form("settings_form"):
    c1, c2 = st.columns(2)
    with c1:
        mode = st.selectbox("Running Mode", 
            options=[0, 1, 2, 3], 
            format_func=lambda x: {0: "None", 1: "CC Charge", 2: "CV Charge", 3: "CP Charge"}.get(x, str(x))
        )
    with c2:
        power_setpoint = st.number_input("Constant Power (kW)", value=0.0, step=0.1)
    
    if st.form_submit_button("Apply Settings"):
        if client.set_running_mode(mode):
            st.success(f"Mode set to {mode}")
        else:
            st.error("Failed to set mode")
        
        if client.set_constant_power(power_setpoint):
            st.success(f"Power set to {power_setpoint} kW")
        else:
            st.error("Failed to set power")
```

#### อธิบาย

##### `st.form()`
- จัดกลุ่ม inputs และ submit button
- ป้องกันการ submit อัตโนมัติเมื่อเปลี่ยนค่า
- ต้องกด "Apply Settings" เท่านั้น

##### `st.selectbox()` with `format_func`
```python
format_func=lambda x: {0: "None", 1: "CC Charge", 2: "CV Charge", 3: "CP Charge"}.get(x, str(x))
```
- `format_func`: แปลงค่าก่อนแสดง
- แสดงชื่อแทนตัวเลข
- ค่าที่ส่งไปยังเป็นตัวเลข (0, 1, 2, 3)

##### `st.number_input()`
- Input สำหรับตัวเลข
- `step=0.1`: เพิ่ม/ลดทีละ 0.1

##### `st.form_submit_button()`
- ปุ่ม submit เฉพาะใน form
- เมื่อกดจะรันโค้ดใน block

##### Command Execution
```python
if client.set_running_mode(mode):
    st.success(...)
else:
    st.error(...)
```
- เรียก method จาก PCSClient
- แสดงผลลัพธ์ทันที

#### วิธีคิด
- **Form Grouping**: ใช้ form เพื่อป้องกันการ submit โดยไม่ตั้งใจ
- **User-Friendly Labels**: แสดงชื่อแทนตัวเลข
- **Immediate Feedback**: แสดงผลลัพธ์ทันที

---

## วิธีคิดและแนวทางการออกแบบ

### 1. Architecture Pattern

#### Separation of Concerns
- **UI Layer** (`pcs_ui.py`): จัดการ UI และ user interaction
- **Business Logic Layer** (`pcs_client.py`): จัดการ Modbus communication

#### State Management
- ใช้ Streamlit Session State เพื่อเก็บ state ระหว่าง refresh
- แยก state เป็นส่วนๆ (connected, client, connection_info)

### 2. User Experience (UX)

#### Visual Hierarchy
- ใช้ emoji เพื่อแยกประเภทข้อมูล
- ใช้สี (success, error, warning) เพื่อแสดงสถานะ
- จัดเรียงข้อมูลสำคัญไว้ด้านบน

#### Information Architecture
- **Summary First**: แสดงสรุปก่อน (Total values)
- **Details in Expander**: รายละเอียดอยู่ใน expander
- **Grouping**: จัดกลุ่มข้อมูลที่เกี่ยวข้องกัน

#### Feedback
- แสดง loading spinner เมื่อกำลังเชื่อมต่อ
- แสดง success/error messages ทันทีหลัง action
- แสดงสถานะการเชื่อมต่อที่ด้านบน

### 3. Error Handling

#### Defensive Programming
```python
if status:
    # แสดงข้อมูล
else:
    st.warning("⚠️ ไม่สามารถอ่านสถานะได้")
```
- ตรวจสอบว่ามีข้อมูลก่อนแสดง
- แสดง warning ถ้าไม่มีข้อมูล

#### User-Friendly Error Messages
```python
st.error(f"❌ เชื่อมต่อไม่สำเร็จ: {host}:{port}\n\nกรุณาตรวจสอบ:\n- IP Address ถูกต้อง\n- ...")
```
- แสดงข้อความที่เข้าใจง่าย
- ให้คำแนะนำในการแก้ไข

### 4. Code Organization

#### Logical Sections
- แบ่งโค้ดเป็น sections ตามหน้าที่
- ใช้ comments เพื่อแยก sections

#### Reusability
- สร้าง functions สำหรับ actions ที่ใช้ซ้ำ
- ใช้ helper methods จาก PCSClient

### 5. Performance Considerations

#### Lazy Loading
- อ่านข้อมูลเฉพาะเมื่อเชื่อมต่อแล้ว
- แสดงข้อมูลเฉพาะเมื่อมี

#### Caching (Potential)
- ยังไม่ได้ implement
- สามารถใช้ `@st.cache_data` สำหรับข้อมูลที่ไม่เปลี่ยนบ่อย

### 6. Maintainability

#### Readable Code
- ใช้ชื่อตัวแปรที่สื่อความหมาย
- ใช้ comments อธิบาย logic ที่ซับซ้อน

#### Consistent Formatting
- ใช้ format เดียวกันทั้งหน้า
- ใช้ emoji และ icons อย่างสม่ำเสมอ

---

## การใช้งาน

### 1. การรันโปรแกรม

```bash
streamlit run pcs/pcs_ui.py
```

### 2. ขั้นตอนการใช้งาน

1. **เปิด Browser** ไปที่ `http://localhost:8501`
2. **ตั้งค่า Connection**:
   - ใส่ IP Address (default: 192.168.0.20)
   - ใส่ Port (default: 502)
   - กดปุ่ม "Connect"
3. **ตรวจสอบสถานะ**:
   - ดู Connection Status Banner
   - ตรวจสอบว่าแสดง "🟢 เชื่อมต่ออยู่"
4. **ดูข้อมูล**:
   - ข้อมูลจะแสดงอัตโนมัติเมื่อเชื่อมต่อ
   - กด "🔄 Refresh Data" เพื่ออัพเดท
   - เปิด "Auto Refresh" สำหรับ auto update
5. **ควบคุมอุปกรณ์**:
   - ใช้ปุ่มใน Sidebar (Start, Stop, Reset)
   - ตั้งค่าในส่วน Settings
6. **ตัดการเชื่อมต่อ**:
   - กดปุ่ม "Disconnect" ใน Sidebar

### 3. Troubleshooting

#### ไม่สามารถเชื่อมต่อได้
- ตรวจสอบ IP Address และ Port
- ตรวจสอบว่า PCS device เปิดอยู่
- ตรวจสอบ Network connection
- ตรวจสอบ Firewall settings

#### ข้อมูลไม่แสดง
- ตรวจสอบว่าเชื่อมต่อสำเร็จ
- กด "Refresh Data"
- ตรวจสอบ Logs ใน Console

#### Auto Refresh ไม่ทำงาน
- Implementation ปัจจุบันมีข้อจำกัด
- ใช้ Manual Refresh แทน
- หรือรอการอัพเดทในอนาคต

---

## สรุป

### จุดเด่นของโค้ด
1. **โครงสร้างชัดเจน**: แบ่ง sections ตามหน้าที่
2. **User-Friendly**: ใช้ emoji, colors, และ clear messages
3. **Error Handling**: ตรวจสอบและแสดง error อย่างเหมาะสม
4. **Maintainable**: โค้ดอ่านง่าย, มี comments

### จุดที่ควรปรับปรุง
1. **Auto Refresh**: ควรใช้ threading หรือ async
2. **Caching**: เพิ่ม caching สำหรับข้อมูลที่ไม่เปลี่ยนบ่อย
3. **Validation**: เพิ่ม validation สำหรับ user inputs
4. **Logging**: เพิ่ม logging สำหรับ debugging

### แนวทางการพัฒนาต่อ
1. เพิ่ม Data Visualization (charts, graphs)
2. เพิ่ม Data Export (CSV, Excel)
3. เพิ่ม Alarm/Notification system
4. เพิ่ม User Authentication
5. เพิ่ม Multi-device support

---

**สร้างโดย**: AI Assistant  
**วันที่**: 2025  
**เวอร์ชัน**: 1.0

