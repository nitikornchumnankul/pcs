import streamlit as st
import time
import pandas as pd
import os
import glob
from pcs_client import PCSClient, REMOTE_METERING_FIELDS, CONTROL_REGISTER_FIELDS

# Page Configuration
st.set_page_config(
    page_title="PCS Control Panel",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Session State
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'client' not in st.session_state:
    st.session_state.client = None
if 'connection_info' not in st.session_state:
    st.session_state.connection_info = None
if 'last_update' not in st.session_state:
    st.session_state.last_update = 0

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

# Sidebar - Connection Settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Data Source Selection
    data_source = st.radio("Data Source", ["Live Connection", "Log File Viewer"])
    
    if data_source == "Live Connection":
        st.subheader("🔌 Connection")
        host = st.text_input("Host IP", value="192.168.0.20")
        port = st.number_input("Port", value=502, step=1)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Connect", disabled=st.session_state.connected):
                connect_pcs(host, port)
        with col2:
            if st.button("Disconnect", disabled=not st.session_state.connected):
                disconnect_pcs()

        st.markdown("---")
        st.header("👁️ Read-only Mode")
        st.info("แดชบอร์ดนี้อ่านค่าจาก PCS อย่างเดียว (Function Code 0x02/0x03/0x04) ไม่มีคำสั่งสั่งงานหรือเขียนค่าใดๆ เพื่อความปลอดภัยของระบบ")
    
    else: # Log File Viewer
        st.subheader("📂 Log Files")
        log_files = glob.glob("pcs_log_*.csv")
        log_files.sort(reverse=True)
        
        if log_files:
            selected_log = st.selectbox("Select Log File", log_files)
        else:
            st.warning("No log files found.")
            selected_log = None

# Main Content
st.title("⚡ PCS Control Panel")

if data_source == "Live Connection":
    # Connection Status Banner
    if st.session_state.connected and st.session_state.connection_info:
        info = st.session_state.connection_info
        st.success(f"🟢 **เชื่อมต่ออยู่**: {info['host']}:{info['port']} | Unit ID: {info['unit_id']}")
    elif not st.session_state.connected:
        st.warning("🔴 **ยังไม่ได้เชื่อมต่อ** - กรุณาเชื่อมต่อผ่าน Sidebar")

    st.markdown("---")

    if st.session_state.connected:
        client = st.session_state.client
        status = client.get_status()
        telemetry = client.get_telemetry()
        temp = client.get_temperature()
        acc_power = client.get_accumulated_power()
        fault_words = client.get_fault_words()
        sys_info = client.get_system_info()
        control_data = client.get_control_registers()

        telemetry_meta = {field["key"]: field for field in REMOTE_METERING_FIELDS}
        control_meta = {field["key"]: field for field in CONTROL_REGISTER_FIELDS}
        control_value_maps = {
            "running_mode": {0: "None", 1: "Constant current charge", 2: "Constant voltage charge", 3: "Constant power charge"},
            "grid_setting": {0: "Grid-connected", 1: "VF grid-disconnected"},
            "grid_switch_mode": {0: "None", 1: "Manual", 2: "Automatic", 3: "Mix", 4: "Silence"},
        }

        def meta_label(key):
            meta = telemetry_meta.get(key)
            if not meta:
                return key
            return f"{meta['name']} [Addr {meta['address']}]"

        def format_value(key, value):
            meta = telemetry_meta.get(key)
            if meta is None or value is None:
                return "-"
            unit = meta.get("unit", "")
            unit_str = f" {unit}" if unit else ""
            coef = meta.get("coefficient", 1)
            if coef >= 1:
                precision = 0
            elif coef >= 0.1:
                precision = 1
            elif coef >= 0.01:
                precision = 2
            else:
                precision = 3
            return f"{value:.{precision}f}{unit_str}"

        def format_control_value(key, value):
            meta = control_meta.get(key)
            if meta is None or value is None:
                return "-"

            # Enumerated text
            if key in control_value_maps:
                label = control_value_maps[key].get(int(round(value)), "Unknown")
                return f"{int(round(value))} ({label})"

            unit = meta.get("unit", "")
            unit_str = f" {unit}" if unit else ""
            coef = meta.get("coefficient", 1)
            if coef >= 1:
                precision = 0
            elif coef >= 0.1:
                precision = 1
            elif coef >= 0.01:
                precision = 2
            else:
                precision = 3
            return f"{value:.{precision}f}{unit_str}"

        def control_table_rows():
            rows = []
            for field in CONTROL_REGISTER_FIELDS:
                value = control_data.get(field["key"]) if control_data else None
                rows.append(
                    {
                        "No.": field["no"],
                        "Modbus address": f"{field['address']:05d}",
                        "Name": field["name"],
                        "Permission": field["permission"],
                        "Data type": field["data_type"],
                        "Coefficient": field["coefficient"],
                        "Unit": field["unit"] or "/",
                        "Value": format_control_value(field["key"], value),
                        "Remarks": field["remarks"],
                    }
                )
            return rows


        tab_dashboard, tab_table, tab_reference = st.tabs(
            ["📊 Dashboard View", "📋 Table View", "📚 Address Reference"]
        )

        with tab_dashboard:
            # Refresh button
            col_refresh, col_auto = st.columns([1, 4])
            with col_refresh:
                if st.button("🔄 Refresh Data"):
                    st.rerun()
            with col_auto:
                auto_refresh = st.checkbox("Auto Refresh (5s)", value=False)
                if auto_refresh:
                    time.sleep(5)
                    st.rerun()

            # 1. Device Status
            st.subheader("📊 สถานะอุปกรณ์")
            st.caption(
                "Source: Discrete inputs 81-96 (1x) via Function Code 0x02 — Boolean bits (1=True, 0=False)"
            )
            if status:
                cols = st.columns(6)
                cols[0].metric("Running", "🟢 ON" if status.get("running") else "🔴 OFF")
                cols[1].metric("Fault", "🔴 YES" if status.get("fault") else "🟢 NO")
                cols[2].metric("Alarm", "🟡 YES" if status.get("alarm") else "🟢 NO")
                cols[3].metric("Grid", "🟢 Connected" if status.get("grid_connected") else "🔴 Disconnected")
                cols[4].metric("Standby", "🟡 YES" if status.get("standby") else "⚪ NO")
                cols[5].metric("Remote", "🟢 YES" if status.get("remote_control") else "⚪ NO")
                
                # Additional status info
                with st.expander("รายละเอียดสถานะเพิ่มเติม"):
                    st.write(f"**Shutdown**: {'YES' if status.get('shutdown') else 'NO'}")
                    st.write(f"**Emergency Stop**: {'ACTIVE' if status.get('emergency_stop_active') else 'INACTIVE'}")
                    st.write(f"**VF Grid Disconnected**: {'YES' if status.get('vf_grid_disconnected') else 'NO'}")
                    st.write(f"**Overload Derating**: {'YES' if status.get('overload_derating') else 'NO'}")
                    st.write(f"**BMS Dry Contact**: {'FAULT' if status.get('bms_dry_contact') else 'NORMAL'}")
            else:
                st.warning("⚠️ ไม่สามารถอ่านสถานะได้")

            st.markdown("---")

            # 2. AC Power & Frequency
            st.subheader("⚡ กำลังไฟฟ้า AC")
            st.caption(
                "Source: Input registers 208-223 (3x) via Function Code 0x04 — power registers ×0.1 kW/kVar, PF ×0.001, frequency ×0.01 Hz"
            )
            if telemetry:
                power_keys = ["active_power_total", "reactive_power_total", "apparent_power_total", "frequency"]
                power_cols = st.columns(len(power_keys))
                for col, key in zip(power_cols, power_keys):
                    col.metric(meta_label(key), format_value(key, telemetry.get(key)))
                
                # Power by Phase
                with st.expander("กำลังไฟฟ้าตาม Phase (Addr 208-223)"):
                    phase_rows = []
                    phase_groups = {
                        "Phase A": ["active_power_a", "reactive_power_a", "apparent_power_a", "power_factor_a"],
                        "Phase B": ["active_power_b", "reactive_power_b", "apparent_power_b", "power_factor_b"],
                        "Phase C": ["active_power_c", "reactive_power_c", "apparent_power_c", "power_factor_c"],
                    }
                    for phase_name, keys in phase_groups.items():
                        row = {"Phase": phase_name}
                        for k in keys:
                            row[meta_label(k)] = format_value(k, telemetry.get(k))
                        phase_rows.append(row)
                    st.dataframe(pd.DataFrame(phase_rows), width="stretch")
            else:
                st.warning("⚠️ ไม่สามารถอ่านข้อมูล Telemetry ได้")

            st.markdown("---")

            # 3. AC Voltage & Current
            st.subheader("🔌 แรงดันและกระแส AC")
            st.caption(
                "Source: Input registers 201-206 (3x, ×0.1 V/A signed for current) and system info 247 (Phase N current ×0.1 A)"
            )
            if telemetry:
                # Voltage (3 Phase + N)
                st.markdown("#### แรงดัน (V)")
                v_cols = st.columns(3)
                for col, key in zip(v_cols, ["voltage_a", "voltage_b", "voltage_c"]):
                    col.metric(meta_label(key), format_value(key, telemetry.get(key)))
                
                # Current (3 Phase + N)
                st.markdown("#### กระแส (A)")
                c_cols = st.columns(4)
                for col, key in zip(c_cols[:3], ["current_a", "current_b", "current_c"]):
                    col.metric(meta_label(key), format_value(key, telemetry.get(key)))
                
                # Phase N current from system info
                if sys_info:
                    phase_n_meta = {"name": "Phase N current effective value", "address": 247, "unit": "A", "coefficient": 0.1}
                    value = sys_info.get("current_n")
                    unit_str = f" {phase_n_meta['unit']}" if phase_n_meta.get("unit") else ""
                    c_cols[3].metric(
                        f"{phase_n_meta['name']} [Addr {phase_n_meta['address']} ×0.1]",
                        f"{value:.2f}{unit_str}" if value is not None else "-"
                    )

            st.markdown("---")

            # 4. DC Input
            st.subheader("🔋 ข้อมูล DC Input")
            st.caption(
                "Source: Input registers 224-226 (3x) via Function Code 0x04 — voltage/current ×0.1, power ×0.1 kW (signed)"
            )
            if telemetry:
                dc_cols = st.columns(3)
                for col, key in zip(dc_cols, ["dc_input_power", "dc_input_voltage", "dc_input_current"]):
                    col.metric(meta_label(key), format_value(key, telemetry.get(key)))

            st.markdown("---")

            # 5. Temperature
            st.subheader("🌡️ อุณหภูมิ")
            st.caption(
                "Source: Input registers 227 (Radiator, signed) and 257-261 (SOC + IGBT temps) — direct °C (×1)"
            )
            if temp:
                temp_cols = st.columns(3)
                temp_cols[0].metric("Radiator Temp", f"{temp.get('radiator_temp', 0):.1f} °C")
                temp_cols[1].metric("SOC Temp", f"{temp.get('soc_temp', 0):.1f} °C")
                
                with st.expander("IGBT Temperature (Addr 257-261)"):
                    igbt_rows = []
                    for idx in range(1, 5):
                        val = temp.get(f"igbt_temp_{idx}")
                        igbt_rows.append(
                            {
                                "Address": 256 + idx,
                                "Name": f"IGBT temperature 1",
                                "Value": f"{val:.1f} °C" if val is not None else "-",
                            }
                        )
                    st.dataframe(pd.DataFrame(igbt_rows), width="stretch")
            else:
                st.warning("⚠️ ไม่สามารถอ่านข้อมูลอุณหภูมิได้")

            st.markdown("---")

            # 6. Accumulated Power
            st.subheader("📈 พลังงานสะสม")
            st.caption(
                "Source: Input registers 230-237 (3x) — combine low/high words into 32-bit, multiply by 0.001 kWh"
            )
            if acc_power:
                acc_cols = st.columns(4)
                acc_cols[0].metric("AC Charging", f"{acc_power.get('ac_charging_kwh', 0):.3f} kWh")
                acc_cols[1].metric("AC Discharging", f"{acc_power.get('ac_discharging_kwh', 0):.3f} kWh")
                acc_cols[2].metric("DC Charging", f"{acc_power.get('dc_charging_kwh', 0):.3f} kWh")
                acc_cols[3].metric("DC Discharging", f"{acc_power.get('dc_discharging_kwh', 0):.3f} kWh")
            else:
                st.warning("⚠️ ไม่สามารถอ่านข้อมูลพลังงานสะสมได้")

            st.markdown("---")

            # 7. Fault Words
            st.subheader("⚠️ Fault Words")
            st.caption("Source: Input registers 256, 272-275 (3x) — raw 16-bit bitfields")
            if fault_words:
                fault_cols = st.columns(5)
                fault_cols[0].metric("Fault Word 1", f"0x{fault_words.get('fault_word_1', 0):04X}")
                fault_cols[1].metric("Fault Word 2", f"0x{fault_words.get('fault_word_2', 0):04X}")
                fault_cols[2].metric("Fault Word 3", f"0x{fault_words.get('fault_word_3', 0):04X}")
                fault_cols[3].metric("Fault Word 4", f"0x{fault_words.get('fault_word_4', 0):04X}")
                fault_cols[4].metric("Fault Word 5", f"0x{fault_words.get('fault_word_5', 0):04X}")
                
                # Check if any fault word is non-zero
                has_fault = any([
                    fault_words.get('fault_word_1', 0) != 0,
                    fault_words.get('fault_word_2', 0) != 0,
                    fault_words.get('fault_word_3', 0) != 0,
                    fault_words.get('fault_word_4', 0) != 0,
                    fault_words.get('fault_word_5', 0) != 0,
                ])
                
                if has_fault:
                    st.error("⚠️ พบ Fault Words ที่ไม่เป็นศูนย์ - กรุณาตรวจสอบ")
                else:
                    st.success("✅ ไม่พบ Fault")

            st.markdown("---")

            # 8. System Information
            st.subheader("ℹ️ ข้อมูลระบบ")
            st.caption(
                "Source: Input registers 238-247 (3x) — clock values direct ints, versions ×0.1"
            )
            if sys_info:
                sys_cols = st.columns(4)
                clock = sys_info.get('system_clock', {})
                sys_cols[0].metric("PCS program version [Addr 245 ×0.1]", f"{sys_info.get('pcs_version', 0):.1f}")
                sys_cols[1].metric("FPGA program version [Addr 246 ×1]", f"{sys_info.get('fpga_version', 0)}")
                sys_cols[2].metric("PCS communication status word [Addr 238]", f"{sys_info.get('communication_status', 0)}")
                
                if clock:
                    sys_cols[3].write(f"**System Clock**: {clock.get('year', 0)}/{clock.get('month', 0):02d}/{clock.get('day', 0):02d} {clock.get('hour', 0):02d}:{clock.get('minute', 0):02d}:{clock.get('second', 0):02d}")

            st.markdown("---")

            # 9. Control Registers Snapshot (Read-only)
            st.subheader("🧾 ค่า Setting (Holding Registers 301-340)")
            st.caption(
                "Source: Holding registers 301-340 (4x) via Function Code 0x03 — ดึงตารางเดียวกับในเอกสาร PCS.pdf มาแสดงแบบอ่านอย่างเดียว"
            )
            if control_data:
                ctrl_cols = st.columns(3)
                ctrl_cols[0].metric(
                    "Running mode [Addr 301]",
                    format_control_value("running_mode", control_data.get("running_mode"))
                )
                ctrl_cols[1].metric(
                    "Grid setting [Addr 306]",
                    format_control_value("grid_setting", control_data.get("grid_setting"))
                )
                ctrl_cols[2].metric(
                    "Switch mode [Addr 324]",
                    format_control_value("grid_switch_mode", control_data.get("grid_switch_mode"))
                )

                with st.expander("ดูรายละเอียด Holding Registers 301-340"):
                    st.dataframe(pd.DataFrame(control_table_rows()), width="stretch", height=500)
            else:
                st.warning("⚠️ ไม่สามารถอ่าน Holding Registers 301-340 ได้")

        with tab_table:
            st.subheader("📋 ตารางข้อมูลแบบละเอียด")
            combined_rows = []

            if telemetry:
                for meta in REMOTE_METERING_FIELDS:
                    value = telemetry.get(meta["key"])
                    combined_rows.append(
                        {
                            "Section": "Remote metering (Addr 201-226)",
                            "Modbus Address": str(meta["address"]),
                            "Name": meta["name"],
                            "Value": format_value(meta["key"], value),
                            "Data Type": meta["data_type"],
                            "Coefficient": meta["coefficient"],
                            "Unit": meta["unit"],
                        }
                    )

            if temp:
                temp_fields = [
                    {"address": 227, "name": "PCS radiator temperature", "value": f"{temp.get('radiator_temp', 0):.1f} °C", "data_type": "S16", "coefficient": 1, "unit": "°C"},
                    {"address": 257, "name": "SOC temperature", "value": f"{temp.get('soc_temp', 0):.1f} °C", "data_type": "U16", "coefficient": 1, "unit": "°C"},
                    {"address": 258, "name": "IGBT temperature 1", "value": f"{temp.get('igbt_temp_1', 0):.1f} °C", "data_type": "U16", "coefficient": 1, "unit": "°C"},
                    {"address": 259, "name": "IGBT temperature 2", "value": f"{temp.get('igbt_temp_2', 0):.1f} °C", "data_type": "U16", "coefficient": 1, "unit": "°C"},
                    {"address": 260, "name": "IGBT temperature 3", "value": f"{temp.get('igbt_temp_3', 0):.1f} °C", "data_type": "U16", "coefficient": 1, "unit": "°C"},
                    {"address": 261, "name": "IGBT temperature 4", "value": f"{temp.get('igbt_temp_4', 0):.1f} °C", "data_type": "U16", "coefficient": 1, "unit": "°C"},
                ]
                for field in temp_fields:
                    combined_rows.append(
                        {
                            "Section": "Temperature (Addr 227, 257-261)",
                            "Modbus Address": str(field["address"]),
                            "Name": field["name"],
                            "Value": field["value"],
                            "Data Type": field["data_type"],
                            "Coefficient": field["coefficient"],
                            "Unit": field["unit"],
                        }
                    )

            if sys_info:
                sys_fields = [
                    {"address": 245, "name": "PCS program version", "value": f"{sys_info.get('pcs_version', 0):.1f}", "data_type": "U16", "coefficient": 0.1, "unit": ""},
                    {"address": 246, "name": "FPGA program version", "value": f"{sys_info.get('fpga_version', 0)}", "data_type": "U16", "coefficient": 1, "unit": ""},
                    {"address": 247, "name": "Phase N current effective value", "value": f"{sys_info.get('current_n', 0):.2f} A", "data_type": "U16", "coefficient": 0.1, "unit": "A"},
                ]
                for field in sys_fields:
                    combined_rows.append(
                        {
                            "Section": "System info (Addr 245-247)",
                            "Modbus Address": str(field["address"]),
                            "Name": field["name"],
                            "Value": field["value"],
                            "Data Type": field["data_type"],
                            "Coefficient": field["coefficient"],
                            "Unit": field["unit"],
                        }
                    )

            if acc_power:
                energy_fields = [
                    {"address": "230/231", "name": "PCS AC accumulated charging power", "value": f"{acc_power.get('ac_charging_kwh', 0):.3f} kWh"},
                    {"address": "232/233", "name": "PCS AC accumulated discharging power", "value": f"{acc_power.get('ac_discharging_kwh', 0):.3f} kWh"},
                    {"address": "234/235", "name": "PCS DC accumulated charging power", "value": f"{acc_power.get('dc_charging_kwh', 0):.3f} kWh"},
                    {"address": "236/237", "name": "PCS DC accumulated discharging power", "value": f"{acc_power.get('dc_discharging_kwh', 0):.3f} kWh"},
                ]
                for field in energy_fields:
                    combined_rows.append(
                        {
                            "Section": "Accumulated energy (Addr 230-237)",
                            "Modbus Address": field["address"],
                            "Name": field["name"],
                            "Value": field["value"],
                            "Data Type": "U32",
                            "Coefficient": "Low/High ×0.001",
                            "Unit": "kWh",
                        }
                    )

            if control_data:
                for field in CONTROL_REGISTER_FIELDS:
                    value = control_data.get(field["key"])
                    combined_rows.append(
                        {
                            "Section": "Holding registers (Addr 301-340)",
                            "Modbus Address": f"{field['address']:05d}",
                            "Name": field["name"],
                            "Value": format_control_value(field["key"], value),
                            "Data Type": field["data_type"],
                            "Coefficient": field["coefficient"],
                            "Unit": field["unit"],
                        }
                    )

            if not combined_rows:
                st.info("ไม่พบข้อมูลสำหรับแสดงในรูปแบบตาราง")
            else:
                st.dataframe(pd.DataFrame(combined_rows), width="stretch", height=600)

            if control_data:
                st.markdown("### ตาราง Holding Registers 301-340 (อ้างอิง PCS.pdf)")
                st.dataframe(pd.DataFrame(control_table_rows()), width="stretch", height=520)

        with tab_reference:
            st.subheader("📚 Address Reference & Conversion Guide")
            st.markdown(
                "ตารางนี้ช่วยอธิบายว่าข้อมูลบน UI แต่ละจุดมาจาก Address ไหน, ใช้ Function Code อะไร และต้องคูณ/แปลงอย่างไร"
            )

            base_reference = [
                {
                    "Address/Range": "81-96",
                    "Type": "1x (Discrete Input)",
                    "Function Code": "0x02",
                    "Description": "สถานะ Shutdown/Standby/Running/Fault ฯลฯ",
                    "Conversion": "Bool (1=True, 0=False)",
                },
                {
                    "Address/Range": "227, 257-261",
                    "Type": "3x",
                    "Function Code": "0x04",
                    "Description": "Radiator, SOC, IGBT Temperatures",
                    "Conversion": "ค่า × 1 (°C), Radiator เป็น signed",
                },
                {
                    "Address/Range": "230-237",
                    "Type": "3x",
                    "Function Code": "0x04",
                    "Description": "พลังงานสะสม AC/DC (Low/High word)",
                    "Conversion": "(High<<16 | Low) × 0.001 = kWh",
                },
                {
                    "Address/Range": "238-247",
                    "Type": "3x",
                    "Function Code": "0x04",
                    "Description": "Comm counter, System Clock, Version, Phase N current",
                    "Conversion": "Clock = ตัวเลขตรง, Version ×0.1, Current ×0.1 A",
                },
                {
                    "Address/Range": "256, 272-275",
                    "Type": "3x",
                    "Function Code": "0x04",
                    "Description": "Fault Words 1-5",
                    "Conversion": "เป็น bitfield 16-bit (ตีความตามเอกสาร)",
                },
                {
                    "Address/Range": "301-304",
                    "Type": "4x (Holding)",
                    "Function Code": "0x03/0x06/0x10",
                    "Description": "Running Mode, Power setpoint ฯลฯ",
                    "Conversion": "Mode = ค่า integer, Power ×0.1 kW",
                },
                {
                    "Address/Range": "00001-00007",
                    "Type": "0x (Coil)",
                    "Function Code": "0x01/0x05",
                    "Description": "Fault reset, Start, Stop, Emergency stop ฯลฯ",
                    "Conversion": "1 = ON (0xFF00), 0 = OFF (0x0000)",
                },
            ]
            remote_reference = []
            for field in REMOTE_METERING_FIELDS:
                unit = f" {field['unit']}" if field.get("unit") else ""
                signed_text = "signed " if field.get("signed") else ""
                remote_reference.append(
                    {
                        "Address/Range": str(field["address"]),
                        "Type": "3x",
                        "Function Code": "0x04",
                        "Description": field["name"],
                        "Conversion": f"{signed_text}×{field['coefficient']}{unit}".strip(),
                    }
                )
            address_reference = [base_reference[0]] + remote_reference + base_reference[1:]

            ref_df = pd.DataFrame(address_reference)
            st.dataframe(ref_df, width="stretch")

            st.subheader("Holding Registers 301-340 (Function Code 0x03)")
            st.caption("ตารางนี้อ้างอิงเอกสาร PCS.pdf Section 4.4 ใช้สำหรับตรวจสอบค่า Setting ที่เราอ่านแบบ Read-only")
            st.dataframe(pd.DataFrame(control_table_rows()), width="stretch")

            st.subheader("รายละเอียดสถานะ 1x (Address 81-96)")
            status_details = [
                {"Address": "81", "Name": "Shutdown status", "Meaning": "1 = Shutdown"},
                {"Address": "82", "Name": "Standby status", "Meaning": "1 = Standby"},
                {"Address": "83", "Name": "Running status", "Meaning": "1 = Running"},
                {"Address": "84", "Name": "Total fault status", "Meaning": "1 = Fault"},
                {"Address": "85", "Name": "Total alarm status", "Meaning": "1 = Alarm"},
                {"Address": "86", "Name": "Remote/local status", "Meaning": "1 = Remote, 0 = Local"},
                {"Address": "87", "Name": "Emergency stop input", "Meaning": "1 = Emergency stop valid"},
                {"Address": "88", "Name": "Grid-connected status", "Meaning": "1 = Grid connected"},
                {"Address": "89", "Name": "VF grid-disconnected", "Meaning": "1 = VF mode active"},
                {"Address": "90", "Name": "Overload derating", "Meaning": "1 = Overload occurred"},
                {"Address": "91-93", "Name": "Reserve", "Meaning": "-"},
                {"Address": "94", "Name": "BMS dry contact input", "Meaning": "1 = Fault valid (PCS v641+)"},
                {"Address": "95-96", "Name": "Reserve", "Meaning": "-"},
            ]
            st.dataframe(pd.DataFrame(status_details), width="stretch")

            st.markdown(
                """
    **หมายเหตุการแปลงค่าที่เจอบ่อย**

    - หาก Register ระบุว่า *Signed* และมีสเกล 0.1 → คำนวณ:  
      `value = raw if raw <= 32767 else raw - 65536` แล้ว `value × 0.1`
    - Energy 32-bit (addr 230-237):  
      `actual = ((high << 16) | low) × 0.001`
    - Power Factor: `raw × 0.001`
    - Frequency: `raw × 0.01`

    อ้างอิงจากเอกสาร `Protocol for External ModBus Communication of PCS_V2.3`
    """
            )

else: # Log File Viewer Mode
    if selected_log:
        st.subheader(f"📂 Viewing Log: {selected_log}")
        
        try:
            df = pd.read_csv(selected_log)
            
            # Display Data Table
            with st.expander("📋 Raw Data Table", expanded=False):
                st.dataframe(df, width="stretch")
            
            # Charts
            st.markdown("### 📈 Trends")
            
            # Power Chart
            st.markdown("#### Power (kW)")
            if "Total Grid Power (kW)" in df.columns:
                st.line_chart(df, x="Time (min)", y=["Total Grid Power (kW)", "Discharge (kw)"])
            
            # Voltage Chart
            st.markdown("#### Voltage (V)")
            volt_cols = [c for c in df.columns if "Volt" in c]
            if volt_cols:
                st.line_chart(df, x="Time (min)", y=volt_cols)
                
            # Current Chart
            st.markdown("#### Current (A)")
            curr_cols = [c for c in df.columns if "Current" in c]
            if curr_cols:
                st.line_chart(df, x="Time (min)", y=curr_cols)
                
        except Exception as e:
            st.error(f"Error reading log file: {e}")
    else:
        st.info("Please select a log file from the sidebar.")
