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
if 'last_update' not in st.session_state:
    st.session_state.last_update = 0

def connect_pcs(host, port):
    client = PCSClient(host=host, port=port)
    if client.connect():
        st.session_state.connected = True
        st.session_state.client = client
        st.success(f"Connected to {host}:{port}")
    else:
        st.error(f"Failed to connect to {host}:{port}")

def disconnect_pcs():
    if st.session_state.client:
        st.session_state.client.close()
    st.session_state.connected = False
    st.session_state.client = None
    st.info("Disconnected")

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

if st.session_state.connected:
    client = st.session_state.client
    
    # Auto-refresh logic (simple loop for demo, or manual refresh)
    if st.button("Refresh Data"):
        st.rerun()

    # 1. Status Indicators
    st.subheader("Device Status")
    status = client.get_status()
    if status:
        cols = st.columns(4)
        cols[0].metric("Running", "ON" if status.get("running") else "OFF", delta_color="normal")
        cols[1].metric("Fault", "YES" if status.get("fault") else "NO", delta_color="inverse")
        cols[2].metric("Alarm", "YES" if status.get("alarm") else "NO", delta_color="inverse")
        cols[3].metric("Grid", "Connected" if status.get("grid_connected") else "Disconnected")
    else:
        st.warning("Could not read status")

    st.markdown("---")

    # 2. Telemetry Dashboard
    st.subheader("Telemetry")
    telemetry = client.get_telemetry()
    if telemetry:
        # Power & Frequency
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Active Power", f"{telemetry.get('active_power_total', 0):.1f} kW")
        col2.metric("Frequency", f"{telemetry.get('frequency', 0):.2f} Hz")
        
        # Voltage (3 Phase)
        st.markdown("#### Voltage (V)")
        v_cols = st.columns(3)
        v_cols[0].metric("Phase A", f"{telemetry.get('voltage_a', 0):.1f} V")
        v_cols[1].metric("Phase B", f"{telemetry.get('voltage_b', 0):.1f} V")
        v_cols[2].metric("Phase C", f"{telemetry.get('voltage_c', 0):.1f} V")

        # Current (3 Phase)
        st.markdown("#### Current (A)")
        c_cols = st.columns(3)
        c_cols[0].metric("Phase A", f"{telemetry.get('current_a', 0):.1f} A")
        c_cols[1].metric("Phase B", f"{telemetry.get('current_b', 0):.1f} A")
        c_cols[2].metric("Phase C", f"{telemetry.get('current_c', 0):.1f} A")
    else:
        st.warning("Could not read telemetry")

    st.markdown("---")

    # 3. Settings
    st.subheader("Settings")
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
