import csv
import time
import argparse
import random
import os
from datetime import datetime
from pcs_client import PCSClient

class PCSLogger:
    def __init__(self, host='192.168.0.20', port=502, interval=60, mock=False):
        self.host = host
        self.port = port
        self.interval = interval
        self.mock = mock
        self.client = PCSClient(host, port)
        self.start_time = time.time()
        self.filename = f"pcs_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Define CSV headers based on the user's image
        self.headers = [
            "Time (min)", 
            "Discharge (kw)", 
            "Power (W) L1", "Power (W) L2", "Power (W) L3",
            "Total Grid Power (kW)", 
            "Remark",
            "Power factor L1", "Power factor L2", "Power factor L3",
            "Volt L1", "Volt L2", "Volt L3",
            "Current (I) L1", "Current (I) L2", "Current (I) L3"
        ]
        
        self._init_csv()

    def _init_csv(self):
        """Initialize the CSV file with headers."""
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Create a structured header as per image (simplified for CSV)
            # The image has merged cells, but for CSV we'll just use flat headers
            writer.writerow(self.headers)
        print(f"Logging to {self.filename}")

    def _get_mock_data(self):
        """Generate random mock data for testing."""
        return {
            "voltage_a": 220.0 + random.uniform(-5, 5),
            "voltage_b": 220.0 + random.uniform(-5, 5),
            "voltage_c": 220.0 + random.uniform(-5, 5),
            "current_a": random.uniform(0, 10),
            "current_b": random.uniform(0, 10),
            "current_c": random.uniform(0, 10),
            "active_power_a": random.uniform(0, 2),
            "active_power_b": random.uniform(0, 2),
            "active_power_c": random.uniform(0, 2),
            "active_power_total": random.uniform(0, 6),
            "power_factor_a": 0.99,
            "power_factor_b": 0.99,
            "power_factor_c": 0.99,
        }

    def log_data(self):
        """Fetch data and write to CSV."""
        try:
            if self.mock:
                telemetry = self._get_mock_data()
            else:
                if not self.client.connect():
                    print("Failed to connect to PCS. Retrying...")
                    return

                telemetry = self.client.get_telemetry()
                self.client.close()

            if not telemetry:
                print("No telemetry data received.")
                return

            # Calculate elapsed time in minutes
            elapsed_min = int((time.time() - self.start_time) / 60)

            # Process data
            # Discharge (kw): Derived from active_power_total. 
            # Assumption: If negative (discharging), use abs value. If positive, 0.
            # However, image shows both Discharge and Total Grid Power as positive.
            # Let's assume Discharge is just a placeholder or specific logic.
            # For now, I'll use logic: if active_power_total < 0, discharge = abs(val), else 0.
            total_power = telemetry.get("active_power_total", 0)
            discharge_kw = abs(total_power) if total_power < 0 else 0
            
            # Power (W)
            power_a_w = telemetry.get("active_power_a", 0) * 1000
            power_b_w = telemetry.get("active_power_b", 0) * 1000
            power_c_w = telemetry.get("active_power_c", 0) * 1000

            row = [
                elapsed_min,
                discharge_kw,
                f"{power_a_w:.1f}", f"{power_b_w:.1f}", f"{power_c_w:.1f}",
                f"{total_power:.3f}",
                "", # Remark - manual entry or logic needed? Leaving empty for now.
                f"{telemetry.get('power_factor_a', 0):.3f}",
                f"{telemetry.get('power_factor_b', 0):.3f}",
                f"{telemetry.get('power_factor_c', 0):.3f}",
                f"{telemetry.get('voltage_a', 0):.1f}",
                f"{telemetry.get('voltage_b', 0):.1f}",
                f"{telemetry.get('voltage_c', 0):.1f}",
                f"{telemetry.get('current_a', 0):.3f}",
                f"{telemetry.get('current_b', 0):.3f}",
                f"{telemetry.get('current_c', 0):.3f}",
            ]

            with open(self.filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(row)
            
            print(f"Logged data at {elapsed_min} min: Total Power {total_power} kW")

        except Exception as e:
            print(f"Error logging data: {e}")

    def run(self):
        print(f"Starting PCS Logger (Interval: {self.interval}s, Mock: {self.mock})")
        try:
            while True:
                self.log_data()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\nLogging stopped by user.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PCS Data Logger")
    parser.add_argument("--host", default="192.168.0.20", help="PCS IP address")
    parser.add_argument("--port", type=int, default=502, help="Modbus port")
    parser.add_argument("--interval", type=int, default=60, help="Logging interval in seconds")
    parser.add_argument("--mock", action="store_true", help="Use mock data for testing")
    
    args = parser.parse_args()
    
    logger = PCSLogger(host=args.host, port=args.port, interval=args.interval, mock=args.mock)
    logger.run()
