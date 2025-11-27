from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

    def _read_input_registers(self, address, count):
        """Helper to read input registers (3x)."""
        try:
            result = self.client.read_input_registers(address, count=count, device_id=self.unit_id)
            if result.isError():
                logger.error(f"Error reading input registers at {address}: {result}")
                return None
            return result.registers
        except ModbusException as e:
            logger.error(f"Modbus exception reading input registers: {e}")
            return None

    def _read_discrete_inputs(self, address, count):
        """Helper to read discrete inputs (1x)."""
        try:
            result = self.client.read_discrete_inputs(address, count=count, device_id=self.unit_id)
            if result.isError():
                logger.error(f"Error reading discrete inputs at {address}: {result}")
                return None
            return result.bits[:count] # Return only requested bits
        except ModbusException as e:
            logger.error(f"Modbus exception reading discrete inputs: {e}")
            return None

    def _write_coil(self, address, value):
        """Helper to write a single coil (0x)."""
        try:
            result = self.client.write_coil(address, value, device_id=self.unit_id)
            if result.isError():
                logger.error(f"Error writing coil at {address}: {result}")
                return False
            return True
        except ModbusException as e:
            logger.error(f"Modbus exception writing coil: {e}")
            return False

    def _write_register(self, address, value):
        """Helper to write a single holding register (4x)."""
        try:
            result = self.client.write_register(address, value, device_id=self.unit_id)
            if result.isError():
                logger.error(f"Error writing register at {address}: {result}")
                return False
            return True
        except ModbusException as e:
            logger.error(f"Modbus exception writing register: {e}")
            return False

    def _convert_signed_16bit(self, value, coefficient=1.0):
        """Convert 16-bit unsigned to signed value."""
        if value > 32767:
            value = value - 65536
        return value * coefficient
    
    # --- Telemetry (Input Registers 3x) ---
    def get_telemetry(self):
        """Reads key telemetry data."""
        # Reading registers from 201 to 226 (26 registers)
        count = 26 
        start_addr = 201
        regs = self._read_input_registers(start_addr, count)
        
        if not regs:
            return None

        data = {
            # AC Voltage (0.1 V)
            "voltage_a": regs[0] * 0.1,
            "voltage_b": regs[1] * 0.1,
            "voltage_c": regs[2] * 0.1,
            
            # AC Current (0.1 A, Signed)
            "current_a": self._convert_signed_16bit(regs[3], 0.1),
            "current_b": self._convert_signed_16bit(regs[4], 0.1),
            "current_c": self._convert_signed_16bit(regs[5], 0.1),
            
            # Frequency (0.01 Hz)
            "frequency": regs[6] * 0.01,
            
            # Active Power (0.1 kW, Signed)
            "active_power_a": self._convert_signed_16bit(regs[7], 0.1),
            "active_power_b": self._convert_signed_16bit(regs[8], 0.1),
            "active_power_c": self._convert_signed_16bit(regs[9], 0.1),
            "active_power_total": self._convert_signed_16bit(regs[10], 0.1),
            
            # Reactive Power (0.1 kVar, Signed)
            "reactive_power_a": self._convert_signed_16bit(regs[11], 0.1),
            "reactive_power_b": self._convert_signed_16bit(regs[12], 0.1),
            "reactive_power_c": self._convert_signed_16bit(regs[13], 0.1),
            "reactive_power_total": self._convert_signed_16bit(regs[14], 0.1),
            
            # Apparent Power (0.1 kVA)
            "apparent_power_a": regs[15] * 0.1,
            "apparent_power_b": regs[16] * 0.1,
            "apparent_power_c": regs[17] * 0.1,
            "apparent_power_total": regs[18] * 0.1,
            
            # Power Factor (0.001)
            "power_factor_a": regs[19] * 0.001,
            "power_factor_b": regs[20] * 0.001,
            "power_factor_c": regs[21] * 0.001,
            "power_factor_total": regs[22] * 0.001,
            
            # DC Input (0.1 kW/V/A, Signed)
            "dc_input_power": self._convert_signed_16bit(regs[23], 0.1),
            "dc_input_voltage": self._convert_signed_16bit(regs[24], 0.1),
            "dc_input_current": self._convert_signed_16bit(regs[25], 0.1),
        }

        return data
    
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
