from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException, ConnectionException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Remote metering metadata (addresses 201-226) from PCS protocol Table 4.3
REMOTE_METERING_FIELDS = [
    {"address": 201, "key": "voltage_a", "name": "Phase A voltage of PCS port", "data_type": "U16", "coefficient": 0.1, "unit": "V", "signed": False},
    {"address": 202, "key": "voltage_b", "name": "Phase B voltage of PCS port", "data_type": "U16", "coefficient": 0.1, "unit": "V", "signed": False},
    {"address": 203, "key": "voltage_c", "name": "Phase C voltage of PCS port", "data_type": "U16", "coefficient": 0.1, "unit": "V", "signed": False},
    {"address": 204, "key": "current_a", "name": "Phase A current of PCS output", "data_type": "S16", "coefficient": 0.1, "unit": "A", "signed": True},
    {"address": 205, "key": "current_b", "name": "Phase B current of PCS output", "data_type": "S16", "coefficient": 0.1, "unit": "A", "signed": True},
    {"address": 206, "key": "current_c", "name": "Phase C current of PCS output", "data_type": "S16", "coefficient": 0.1, "unit": "A", "signed": True},
    {"address": 207, "key": "frequency", "name": "Grid frequency", "data_type": "U16", "coefficient": 0.01, "unit": "Hz", "signed": False},
    {"address": 208, "key": "active_power_a", "name": "Active power of phase A output of PCS", "data_type": "S16", "coefficient": 0.1, "unit": "kW", "signed": True},
    {"address": 209, "key": "active_power_b", "name": "Active power of phase B output of PCS", "data_type": "S16", "coefficient": 0.1, "unit": "kW", "signed": True},
    {"address": 210, "key": "active_power_c", "name": "Active power of phase C output of PCS", "data_type": "S16", "coefficient": 0.1, "unit": "kW", "signed": True},
    {"address": 211, "key": "active_power_total", "name": "Active power of total output of PCS", "data_type": "S16", "coefficient": 0.1, "unit": "kW", "signed": True},
    {"address": 212, "key": "reactive_power_a", "name": "Reactive power of phase A output of PCS", "data_type": "S16", "coefficient": 0.1, "unit": "kVar", "signed": True},
    {"address": 213, "key": "reactive_power_b", "name": "Reactive power of phase B output of PCS", "data_type": "S16", "coefficient": 0.1, "unit": "kVar", "signed": True},
    {"address": 214, "key": "reactive_power_c", "name": "Reactive power of phase C output of PCS", "data_type": "S16", "coefficient": 0.1, "unit": "kVar", "signed": True},
    {"address": 215, "key": "reactive_power_total", "name": "Reactive power of total output of PCS", "data_type": "S16", "coefficient": 0.1, "unit": "kVar", "signed": True},
    {"address": 216, "key": "apparent_power_a", "name": "Apparent power of phase A output of PCS", "data_type": "U16", "coefficient": 0.1, "unit": "kVA", "signed": False},
    {"address": 217, "key": "apparent_power_b", "name": "Apparent power of phase B output of PCS", "data_type": "U16", "coefficient": 0.1, "unit": "kVA", "signed": False},
    {"address": 218, "key": "apparent_power_c", "name": "Apparent power of phase C output of PCS", "data_type": "U16", "coefficient": 0.1, "unit": "kVA", "signed": False},
    {"address": 219, "key": "apparent_power_total", "name": "Apparent power of total output of PCS", "data_type": "U16", "coefficient": 0.1, "unit": "kVA", "signed": False},
    {"address": 220, "key": "power_factor_a", "name": "Phase A power factor of PCS output", "data_type": "U16", "coefficient": 0.001, "unit": "", "signed": False},
    {"address": 221, "key": "power_factor_b", "name": "Phase B power factor of PCS output", "data_type": "U16", "coefficient": 0.001, "unit": "", "signed": False},
    {"address": 222, "key": "power_factor_c", "name": "Phase C power factor of PCS output", "data_type": "U16", "coefficient": 0.001, "unit": "", "signed": False},
    {"address": 223, "key": "power_factor_total", "name": "Total power factor of PCS output", "data_type": "U16", "coefficient": 0.001, "unit": "", "signed": False},
    {"address": 224, "key": "dc_input_power", "name": "PCS input power", "data_type": "S16", "coefficient": 0.1, "unit": "kW", "signed": True},
    {"address": 225, "key": "dc_input_voltage", "name": "PCS input voltage", "data_type": "S16", "coefficient": 0.1, "unit": "V", "signed": True},
    {"address": 226, "key": "dc_input_current", "name": "PCS input current", "data_type": "S16", "coefficient": 0.1, "unit": "A", "signed": True},
]

CONTROL_REGISTER_FIELDS = [
    {"no": 1, "address": 301, "key": "running_mode", "name": "Selection of running mode", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "", "signed": False, "remarks": "0-None, 1-CC charge, 2-CV charge, 3-CP charge"},
    {"no": 2, "address": 302, "key": "cv_voltage", "name": "Voltage setting of constant voltage charging", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "V", "signed": False, "remarks": "Charge battery when higher than pack voltage"},
    {"no": 3, "address": 303, "key": "cc_current", "name": "Current setting of constant current charging", "permission": "Read-only", "data_type": "S16", "coefficient": 1, "unit": "A", "signed": True, "remarks": "Negative=discharge to grid, positive=charge from grid"},
    {"no": 4, "address": 304, "key": "cp_active_power", "name": "Expectation of constant power active power", "permission": "Read-only", "data_type": "S16", "coefficient": 0.1, "unit": "kW", "signed": True, "remarks": "Negative=discharge to grid, positive=charge"},
    {"no": 5, "address": 305, "key": "cp_reactive_power", "name": "Expectation of constant power reactive power", "permission": "Read-only", "data_type": "S16", "coefficient": 0.1, "unit": "kVar", "signed": True, "remarks": "Negative inductive, positive capacitive"},
    {"no": 6, "address": 306, "key": "grid_setting", "name": "Grid-connected / grid-disconnected settings", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "", "signed": False, "remarks": "0=Grid-connected, 1=VF grid-disconnected"},
    {"no": 7, "address": 307, "key": "vf_voltage_three_wire", "name": "Grid-disconnected output voltage (three-wire)", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "V", "signed": False, "remarks": "230 V by default"},
    {"no": 8, "address": 308, "key": "vf_frequency", "name": "Grid-disconnected output frequency", "permission": "Read-only", "data_type": "U16", "coefficient": 0.01, "unit": "Hz", "signed": False, "remarks": "5000 by default → 50.00 Hz"},
    {"no": 9, "address": 309, "key": "split_phase_power_a", "name": "Phase A active power (split-phase)", "permission": "Read-only", "data_type": "S16", "coefficient": 0.1, "unit": "kW", "signed": True, "remarks": "Negative=discharge, positive=charge"},
    {"no": 10, "address": 310, "key": "split_phase_power_b", "name": "Phase B active power (split-phase)", "permission": "Read-only", "data_type": "S16", "coefficient": 0.1, "unit": "kW", "signed": True, "remarks": "Negative=discharge, positive=charge"},
    {"no": 11, "address": 311, "key": "split_phase_power_c", "name": "Phase C active power (split-phase)", "permission": "Read-only", "data_type": "S16", "coefficient": 0.1, "unit": "kW", "signed": True, "remarks": "Negative=discharge, positive=charge"},
    {"no": 12, "address": 312, "key": "split_phase_reactive_a", "name": "Phase A reactive power (split-phase)", "permission": "Read-only", "data_type": "S16", "coefficient": 0.1, "unit": "kVar", "signed": True, "remarks": "Negative inductive, positive capacitive"},
    {"no": 13, "address": 313, "key": "split_phase_reactive_b", "name": "Phase B reactive power (split-phase)", "permission": "Read-only", "data_type": "S16", "coefficient": 0.1, "unit": "kVar", "signed": True, "remarks": "Negative inductive, positive capacitive"},
    {"no": 14, "address": 314, "key": "split_phase_reactive_c", "name": "Phase C reactive power (split-phase)", "permission": "Read-only", "data_type": "S16", "coefficient": 0.1, "unit": "kVar", "signed": True, "remarks": "Negative inductive, positive capacitive"},
    {"no": 15, "address": 315, "key": "vf_voltage_phase_a", "name": "Grid-disconnected output voltage split-phase A", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "V", "signed": False, "remarks": ""},
    {"no": 16, "address": 316, "key": "vf_voltage_phase_b", "name": "Grid-disconnected output voltage split-phase B", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "V", "signed": False, "remarks": ""},
    {"no": 17, "address": 317, "key": "vf_voltage_phase_c", "name": "Grid-disconnected output voltage split-phase C", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "V", "signed": False, "remarks": ""},
    {"no": 18, "address": 318, "key": "dc_droop_coeff", "name": "Microgrid DC voltage droop coefficient", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "V", "signed": False, "remarks": "Range 0-100 V"},
    {"no": 19, "address": 319, "key": "primary_fm_dead_zone", "name": "Primary FM frequency dead zone", "permission": "Read-only", "data_type": "U16", "coefficient": 0.01, "unit": "Hz", "signed": False, "remarks": "Dead zone ≥ 0.05 Hz"},
    {"no": 20, "address": 320, "key": "primary_fm_k_value", "name": "Primary FM K value", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "", "signed": False, "remarks": "Range 0-120"},
    {"no": 21, "address": 321, "key": "reserve_321", "name": "Reserve", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "", "signed": False, "remarks": ""},
    {"no": 22, "address": 322, "key": "reserve_322", "name": "Reserve", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "", "signed": False, "remarks": ""},
    {"no": 23, "address": 323, "key": "reserve_323", "name": "Reserve", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "", "signed": False, "remarks": ""},
    {"no": 24, "address": 324, "key": "grid_switch_mode", "name": "Grid-connected/disconnected switch running mode", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "", "signed": False, "remarks": "0-None,1-Manual,2-Automatic,3-Mix,4-Silence"},
    {"no": 25, "address": 325, "key": "reserve_325", "name": "Reserve", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "", "signed": False, "remarks": ""},
    {"no": 26, "address": 326, "key": "battery_charge_voltage", "name": "Battery/super capacitor allowable charging voltage", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "V", "signed": False, "remarks": ""},
    {"no": 27, "address": 327, "key": "battery_discharge_voltage", "name": "Battery/super capacitor allowable discharging voltage", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "V", "signed": False, "remarks": ""},
    {"no": 28, "address": 328, "key": "battery_charge_current", "name": "Battery/super capacitor allowable charging current", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "A", "signed": False, "remarks": ""},
    {"no": 29, "address": 329, "key": "battery_discharge_current", "name": "Battery/super capacitor allowable discharging current", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "A", "signed": False, "remarks": ""},
    {"no": 30, "address": 330, "key": "time_sync_second", "name": "Time synchronization - Second", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "s", "signed": False, "remarks": ""},
    {"no": 31, "address": 331, "key": "time_sync_minute", "name": "Time synchronization - Minute", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "min", "signed": False, "remarks": ""},
    {"no": 32, "address": 332, "key": "time_sync_hour", "name": "Time synchronization - Hour", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "h", "signed": False, "remarks": ""},
    {"no": 33, "address": 333, "key": "time_sync_day", "name": "Time synchronization - Day", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "day", "signed": False, "remarks": ""},
    {"no": 34, "address": 334, "key": "time_sync_month", "name": "Time synchronization - Month", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "month", "signed": False, "remarks": ""},
    {"no": 35, "address": 335, "key": "time_sync_year", "name": "Time synchronization - Year", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "year", "signed": False, "remarks": ""},
    {"no": 36, "address": 336, "key": "reserve_336", "name": "Reserve", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "", "signed": False, "remarks": ""},
    {"no": 37, "address": 337, "key": "reserve_337", "name": "Reserve", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "", "signed": False, "remarks": ""},
    {"no": 38, "address": 338, "key": "reserve_338", "name": "Reserve", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "", "signed": False, "remarks": ""},
    {"no": 39, "address": 339, "key": "reserve_339", "name": "Reserve", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "", "signed": False, "remarks": ""},
    {"no": 40, "address": 340, "key": "reserve_340", "name": "Reserve", "permission": "Read-only", "data_type": "U16", "coefficient": 1, "unit": "", "signed": False, "remarks": ""},
]

class PCSClient:
    def __init__(self, host='192.168.0.20', port=502, unit_id=1):
        self.host = host
        self.port = port
        self.unit_id = unit_id
        self.client = ModbusTcpClient(host, port=port)

    def connect(self):
        """Connect to the PCS."""
        try:
            if self.client.connect():
                logger.info(f"Connected to PCS at {self.host}:{self.port}")
                return True
            else:
                logger.error(f"Failed to connect to PCS at {self.host}:{self.port}")
                return False
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return False

    def close(self):
        """Close the connection."""
        self.client.close()
        logger.info("Connection closed")

    def _reset_connection(self):
        """Try to reset TCP connection when errors occur."""
        try:
            self.client.close()
        except Exception:
            pass
        self.client = ModbusTcpClient(self.host, port=self.port)
        if self.client.connect():
            logger.info("Reconnected to PCS after communication error")
        else:
            logger.error("Failed to reconnect to PCS")

    def _handle_comm_error(self, error, context):
        logger.error(f"Communication error during {context}: {error}")
        self._reset_connection()

    def _read_input_registers(self, address, count):
        """Helper to read input registers (3x)."""
        try:
            result = self.client.read_input_registers(address, count=count, device_id=self.unit_id)
            if result.isError():
                logger.error(f"Error reading input registers at {address}: {result}")
                return None
            return result.registers
        except (ModbusException, ConnectionException, OSError) as e:
            self._handle_comm_error(e, f"read_input_registers addr={address} count={count}")
            return None

    def _read_holding_registers(self, address, count):
        """Helper to read holding registers (4x)."""
        try:
            result = self.client.read_holding_registers(address, count=count, device_id=self.unit_id)
            if result.isError():
                logger.error(f"Error reading holding registers at {address}: {result}")
                return None
            return result.registers
        except (ModbusException, ConnectionException, OSError) as e:
            self._handle_comm_error(e, f"read_holding_registers addr={address} count={count}")
            return None

    def _read_discrete_inputs(self, address, count):
        """Helper to read discrete inputs (1x)."""
        try:
            result = self.client.read_discrete_inputs(address, count=count, device_id=self.unit_id)
            if result.isError():
                logger.error(f"Error reading discrete inputs at {address}: {result}")
                return None
            return result.bits[:count] # Return only requested bits
        except (ModbusException, ConnectionException, OSError) as e:
            self._handle_comm_error(e, f"read_discrete_inputs addr={address} count={count}")
            return None

    def _write_coil(self, address, value):
        """Helper to write a single coil (0x)."""
        try:
            result = self.client.write_coil(address, value, device_id=self.unit_id)
            if result.isError():
                logger.error(f"Error writing coil at {address}: {result}")
                return False
            return True
        except (ModbusException, ConnectionException, OSError) as e:
            self._handle_comm_error(e, f"write_coil addr={address}")
            return False

    def _write_register(self, address, value):
        """Helper to write a single holding register (4x)."""
        try:
            result = self.client.write_register(address, value, device_id=self.unit_id)
            if result.isError():
                logger.error(f"Error writing register at {address}: {result}")
                return False
            return True
        except (ModbusException, ConnectionException, OSError) as e:
            self._handle_comm_error(e, f"write_register addr={address}")
            return False

    def _convert_signed_16bit(self, value, coefficient=1.0):
        """Convert 16-bit unsigned to signed value."""
        if value > 32767:
            value = value - 65536
        return value * coefficient
    
    # --- Telemetry (Input Registers 3x) ---
    def get_telemetry(self):
        """Reads key telemetry data."""
        # Reading registers from 201 to 226 (26 registers) per protocol
        start_addr = 201
        count = len(REMOTE_METERING_FIELDS)
        regs = self._read_input_registers(start_addr, count)
        
        if not regs:
            return None

        data = {}
        for field in REMOTE_METERING_FIELDS:
            idx = field["address"] - start_addr
            raw_value = regs[idx]
            if field["signed"]:
                value = self._convert_signed_16bit(raw_value, field["coefficient"])
            else:
                value = raw_value * field["coefficient"]
            data[field["key"]] = value

        return data

    @staticmethod
    def get_remote_metering_metadata():
        """Expose remote metering metadata (addresses 201-226)."""
        return REMOTE_METERING_FIELDS

    @staticmethod
    def get_control_register_metadata():
        """Expose control/holding register metadata (addresses 301-340)."""
        return CONTROL_REGISTER_FIELDS
    
    def get_temperature(self):
        """Reads temperature data."""
        # Address 227: PCS radiator temperature
        # Address 257: SOC temperature
        # Address 258-261: IGBT temperature 1-4
        regs_227 = self._read_input_registers(227, 1)
        regs_257 = self._read_input_registers(257, 5)
        
        if not regs_227 or not regs_257:
            return None
        
        data = {
            "radiator_temp": self._convert_signed_16bit(regs_227[0], 1.0),
            "soc_temp": regs_257[0],
            "igbt_temp_1": regs_257[1],
            "igbt_temp_2": regs_257[2],
            "igbt_temp_3": regs_257[3],
            "igbt_temp_4": regs_257[4],
        }
        return data
    
    def get_fault_words(self):
        """Reads PCS fault words."""
        # Address 272-275: PCS fault word 1-4
        # Address 256: PCS fault word 5
        regs_256 = self._read_input_registers(256, 1)
        regs_272 = self._read_input_registers(272, 4)
        
        if not regs_256 or not regs_272:
            return None
        
        data = {
            "fault_word_1": regs_272[0],
            "fault_word_2": regs_272[1],
            "fault_word_3": regs_272[2],
            "fault_word_4": regs_272[3],
            "fault_word_5": regs_256[0],
        }
        return data
    
    def get_accumulated_power(self):
        """Reads accumulated power data."""
        # Address 230-237: Accumulated power (low/high 16 bits)
        regs = self._read_input_registers(230, 8)
        
        if not regs:
            return None
        
        # Combine low and high 16 bits to form 32-bit values
        data = {
            "ac_charging_kwh": (regs[1] << 16 | regs[0]) * 0.001,
            "ac_discharging_kwh": (regs[3] << 16 | regs[2]) * 0.001,
            "dc_charging_kwh": (regs[5] << 16 | regs[4]) * 0.001,
            "dc_discharging_kwh": (regs[7] << 16 | regs[6]) * 0.001,
        }
        return data
    
    def get_system_info(self):
        """Reads system information."""
        # Address 238: Communication status word
        # Address 239-244: System clock
        # Address 245-246: Program version
        # Address 247: Phase N current
        regs = self._read_input_registers(238, 10)
        
        if not regs:
            return None
        
        data = {
            "communication_status": regs[0],
            "system_clock": {
                "second": regs[1],
                "minute": regs[2],
                "hour": regs[3],
                "day": regs[4],
                "month": regs[5],
                "year": regs[6],
            },
            "pcs_version": regs[7] * 0.1,
            "fpga_version": regs[8],
            "current_n": regs[9] * 0.1,
        }
        return data

    def get_control_registers(self):
        """Reads holding registers 301-340 (configuration snapshot)."""
        start_addr = 301
        count = len(CONTROL_REGISTER_FIELDS)
        regs = self._read_holding_registers(start_addr, count)

        if not regs:
            return None

        data = {}
        for field in CONTROL_REGISTER_FIELDS:
            idx = field["address"] - start_addr
            raw_value = regs[idx]
            if field["signed"]:
                value = self._convert_signed_16bit(raw_value, field["coefficient"])
            else:
                value = raw_value * field["coefficient"]
            data[field["key"]] = value

        return data

    # --- Status (Discrete Inputs 1x) ---
    def get_status(self):
        """Reads device status."""
        # Reading 16 bits starting from 81
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

    # --- Controls (Coils 0x) ---
    def start_device(self):
        """Sends startup command (Address 2)."""
        logger.info("Sending START command...")
        return self._write_coil(2, True)

    def stop_device(self):
        """Sends shutdown command (Address 3)."""
        logger.info("Sending STOP command...")
        return self._write_coil(3, True)

    def reset_fault(self):
        """Sends fault reset command (Address 1)."""
        logger.info("Sending FAULT RESET command...")
        return self._write_coil(1, True)

    # --- Settings (Holding Registers 4x) ---
    def set_running_mode(self, mode):
        """
        Sets running mode (Address 301).
        0: None, 1: CC Charge, 2: CV Charge, 3: CP Charge
        """
        logger.info(f"Setting running mode to {mode}...")
        return self._write_register(301, mode)

    def set_constant_power(self, power_kw):
        """
        Sets constant power expectation (Address 304).
        Unit: 0.1 kW. Positive = Charge, Negative = Discharge.
        """
        val = int(power_kw * 10)
        # Handle negative values for 16-bit signed integer
        if val < 0:
            val += 65536
            
        logger.info(f"Setting constant power to {power_kw} kW (Register val: {val})...")
        return self._write_register(304, val)

if __name__ == "__main__":
    # Example usage
    client = PCSClient(host='192.168.0.20')
    if client.connect():
        # Read Telemetry
        telemetry = client.get_telemetry()
        if telemetry:
            print("Telemetry:", telemetry)
        
        # Read Status
        status = client.get_status()
        if status:
            print("Status:", status)
            
        # Example: Start device (Commented out for safety)
        # client.start_device()
        
        client.close()
