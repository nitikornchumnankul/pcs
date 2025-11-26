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
            result = self.client.read_input_registers(address, count, slave=self.unit_id)
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
            result = self.client.read_discrete_inputs(address, count, slave=self.unit_id)
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
            result = self.client.write_coil(address, value, slave=self.unit_id)
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
            result = self.client.write_register(address, value, slave=self.unit_id)
            if result.isError():
                logger.error(f"Error writing register at {address}: {result}")
                return False
            return True
        except ModbusException as e:
            logger.error(f"Modbus exception writing register: {e}")
            return False

    # --- Telemetry (Input Registers 3x) ---
    def get_telemetry(self):
        """Reads key telemetry data."""
        # Reading a block of registers from 201 to 226 (26 registers)
        # Adjust count based on what you need. 
        # 201-203: Voltage A, B, C (0.1 V)
        # 204-206: Current A, B, C (0.1 A)
        # 207: Frequency (0.01 Hz)
        # 208-210: Active Power A, B, C (0.1 kW)
        # 211: Total Active Power (0.1 kW)
        
        count = 26 
        start_addr = 201
        regs = self._read_input_registers(start_addr, count)
        
        if not regs:
            return None

        data = {
            "voltage_a": regs[0] * 0.1,
            "voltage_b": regs[1] * 0.1,
            "voltage_c": regs[2] * 0.1,
            "current_a": regs[3] * 0.1, # Signed
            "current_b": regs[4] * 0.1, # Signed
            "current_c": regs[5] * 0.1, # Signed
            "frequency": regs[6] * 0.01,
            "active_power_total": regs[10] * 0.1, # Signed
            # ... add more as needed
        }
        
        # Handle signed values (16-bit)
        for key in ["current_a", "current_b", "current_c", "active_power_total"]:
            if data[key] > 3276.7: # roughly half of 65535 * 0.1
                 data[key] -= 6553.6 # subtract 65536 * 0.1

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
            # ...
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
