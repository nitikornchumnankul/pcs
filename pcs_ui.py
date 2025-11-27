import streamlit as st
import time
import pandas as pd
from pcs_client import PCSClient

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

# Main Content
st.title("⚡ PCS Control Panel")

# Connection Status Banner
if st.session_state.connected and st.session_state.connection_info:
    info = st.session_state.connection_info
    st.success(f"🟢 **เชื่อมต่ออยู่**: {info['host']}:{info['port']} | Unit ID: {info['unit_id']}")
elif not st.session_state.connected:
    st.warning("🔴 **ยังไม่ได้เชื่อมต่อ** - กรุณาเชื่อมต่อผ่าน Sidebar")

st.markdown("---")

if st.session_state.connected:
    client = st.session_state.client
    
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
    status = client.get_status()
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
    telemetry = client.get_telemetry()
    if telemetry:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Active Power", f"{telemetry.get('active_power_total', 0):.2f} kW")
        col2.metric("Total Reactive Power", f"{telemetry.get('reactive_power_total', 0):.2f} kVar")
        col3.metric("Total Apparent Power", f"{telemetry.get('apparent_power_total', 0):.2f} kVA")
        col4.metric("Frequency", f"{telemetry.get('frequency', 0):.2f} Hz")
        
        # Power by Phase
        with st.expander("กำลังไฟฟ้าตาม Phase"):
            p_cols = st.columns(3)
            p_cols[0].markdown("**Phase A**")
            p_cols[0].write(f"Active: {telemetry.get('active_power_a', 0):.2f} kW")
            p_cols[0].write(f"Reactive: {telemetry.get('reactive_power_a', 0):.2f} kVar")
            p_cols[0].write(f"Apparent: {telemetry.get('apparent_power_a', 0):.2f} kVA")
            p_cols[0].write(f"PF: {telemetry.get('power_factor_a', 0):.3f}")
            
            p_cols[1].markdown("**Phase B**")
            p_cols[1].write(f"Active: {telemetry.get('active_power_b', 0):.2f} kW")
            p_cols[1].write(f"Reactive: {telemetry.get('reactive_power_b', 0):.2f} kVar")
            p_cols[1].write(f"Apparent: {telemetry.get('apparent_power_b', 0):.2f} kVA")
            p_cols[1].write(f"PF: {telemetry.get('power_factor_b', 0):.3f}")
            
            p_cols[2].markdown("**Phase C**")
            p_cols[2].write(f"Active: {telemetry.get('active_power_c', 0):.2f} kW")
            p_cols[2].write(f"Reactive: {telemetry.get('reactive_power_c', 0):.2f} kVar")
            p_cols[2].write(f"Apparent: {telemetry.get('apparent_power_c', 0):.2f} kVA")
            p_cols[2].write(f"PF: {telemetry.get('power_factor_c', 0):.3f}")
    else:
        st.warning("⚠️ ไม่สามารถอ่านข้อมูล Telemetry ได้")

    st.markdown("---")

    # 3. AC Voltage & Current
    st.subheader("🔌 แรงดันและกระแส AC")
    if telemetry:
        # Voltage (3 Phase + N)
        st.markdown("#### แรงดัน (V)")
        v_cols = st.columns(4)
        v_cols[0].metric("Phase A", f"{telemetry.get('voltage_a', 0):.1f} V")
        v_cols[1].metric("Phase B", f"{telemetry.get('voltage_b', 0):.1f} V")
        v_cols[2].metric("Phase C", f"{telemetry.get('voltage_c', 0):.1f} V")
        
        # Current (3 Phase + N)
        st.markdown("#### กระแส (A)")
        c_cols = st.columns(4)
        c_cols[0].metric("Phase A", f"{telemetry.get('current_a', 0):.2f} A")
        c_cols[1].metric("Phase B", f"{telemetry.get('current_b', 0):.2f} A")
        c_cols[2].metric("Phase C", f"{telemetry.get('current_c', 0):.2f} A")
        
        # Phase N current from system info
        sys_info = client.get_system_info()
        if sys_info:
            c_cols[3].metric("Phase N", f"{sys_info.get('current_n', 0):.2f} A")

    st.markdown("---")

    # 4. DC Input
    st.subheader("🔋 ข้อมูล DC Input")
    if telemetry:
        dc_cols = st.columns(3)
        dc_cols[0].metric("DC Input Power", f"{telemetry.get('dc_input_power', 0):.2f} kW")
        dc_cols[1].metric("DC Input Voltage", f"{telemetry.get('dc_input_voltage', 0):.1f} V")
        dc_cols[2].metric("DC Input Current", f"{telemetry.get('dc_input_current', 0):.2f} A")

    st.markdown("---")

    # 5. Temperature
    st.subheader("🌡️ อุณหภูมิ")
    temp = client.get_temperature()
    if temp:
        temp_cols = st.columns(3)
        temp_cols[0].metric("Radiator Temp", f"{temp.get('radiator_temp', 0):.1f} °C")
        temp_cols[1].metric("SOC Temp", f"{temp.get('soc_temp', 0):.1f} °C")
        
        with st.expander("IGBT Temperature"):
            igbt_cols = st.columns(4)
            igbt_cols[0].metric("IGBT 1", f"{temp.get('igbt_temp_1', 0):.1f} °C")
            igbt_cols[1].metric("IGBT 2", f"{temp.get('igbt_temp_2', 0):.1f} °C")
            igbt_cols[2].metric("IGBT 3", f"{temp.get('igbt_temp_3', 0):.1f} °C")
            igbt_cols[3].metric("IGBT 4", f"{temp.get('igbt_temp_4', 0):.1f} °C")
    else:
        st.warning("⚠️ ไม่สามารถอ่านข้อมูลอุณหภูมิได้")

    st.markdown("---")

    # 6. Accumulated Power
    st.subheader("📈 พลังงานสะสม")
    acc_power = client.get_accumulated_power()
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
    fault_words = client.get_fault_words()
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
    else:
        st.warning("⚠️ ไม่สามารถอ่าน Fault Words ได้")

    st.markdown("---")

    # 8. System Information
    st.subheader("ℹ️ ข้อมูลระบบ")
    sys_info = client.get_system_info()
    if sys_info:
        sys_cols = st.columns(4)
        clock = sys_info.get('system_clock', {})
        sys_cols[0].metric("PCS Version", f"{sys_info.get('pcs_version', 0):.1f}")
        sys_cols[1].metric("FPGA Version", f"{sys_info.get('fpga_version', 0)}")
        sys_cols[2].metric("Comm Status", f"{sys_info.get('communication_status', 0)}")
        
        if clock:
            sys_cols[3].write(f"**System Clock**: {clock.get('year', 0)}/{clock.get('month', 0):02d}/{clock.get('day', 0):02d} {clock.get('hour', 0):02d}:{clock.get('minute', 0):02d}:{clock.get('second', 0):02d}")

    st.markdown("---")

    # 9. Settings
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

else:
    st.info("Please connect to the PCS device using the sidebar.")
