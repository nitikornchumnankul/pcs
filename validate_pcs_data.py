"""
Script สำหรับตรวจสอบความถูกต้องของข้อมูลจาก PCS
Usage: python validate_pcs_data.py [host] [port]
"""
from pcs_client import PCSClient
import sys

def validate_pcs_data(host='192.168.0.20', port=502):
    """ตรวจสอบความถูกต้องของข้อมูลจาก PCS"""
    
    print("="*60)
    print("PCS Data Validation Script")
    print("="*60)
    
    client = PCSClient(host=host, port=port)
    if not client.connect():
        print("❌ ไม่สามารถเชื่อมต่อกับ PCS ได้")
        print(f"   Host: {host}, Port: {port}")
        return False
    
    print(f"✅ เชื่อมต่อสำเร็จ: {host}:{port}\n")
    errors = []
    warnings = []
    
    # 1. อ่าน Telemetry
    print("="*60)
    print("1. ตรวจสอบ Telemetry (Address 201-226)")
    print("="*60)
    telemetry = client.get_telemetry()
    if not telemetry:
        errors.append("❌ ไม่สามารถอ่าน Telemetry ได้")
        print("❌ ไม่สามารถอ่าน Telemetry ได้")
    else:
        print("✅ อ่าน Telemetry สำเร็จ\n")
        
        # ตรวจสอบ Voltage Range
        print("📊 AC Voltage:")
        for phase in ['a', 'b', 'c']:
            voltage = telemetry.get(f'voltage_{phase}', 0)
            if 180 <= voltage <= 250:
                print(f"  ✅ Phase {phase.upper()}: {voltage:.1f} V (ปกติ)")
            else:
                msg = f"⚠️ Phase {phase.upper()}: {voltage:.1f} V (นอกช่วงปกติ 180-250V)"
                warnings.append(msg)
                print(f"  {msg}")
        
        # ตรวจสอบ Frequency
        print("\n📊 Frequency:")
        frequency = telemetry.get('frequency', 0)
        if 49.5 <= frequency <= 50.5:
            print(f"  ✅ Frequency: {frequency:.2f} Hz (ระบบ 50Hz)")
        elif 59.5 <= frequency <= 60.5:
            print(f"  ✅ Frequency: {frequency:.2f} Hz (ระบบ 60Hz)")
        else:
            msg = f"⚠️ Frequency: {frequency:.2f} Hz (นอกช่วงปกติ)"
            warnings.append(msg)
            print(f"  {msg}")
        
        # ตรวจสอบ Power = V × I
        print("\n📊 Power Calculation (Phase A):")
        voltage_a = telemetry.get('voltage_a', 0)
        current_a = abs(telemetry.get('current_a', 0))
        active_power_a = abs(telemetry.get('active_power_a', 0))
        
        if voltage_a > 0 and current_a > 0:
            calculated_power = (voltage_a * current_a) / 1000
            difference = abs(calculated_power - active_power_a)
            tolerance = active_power_a * 0.15 if active_power_a > 0 else 0.1
            
            print(f"  Voltage A: {voltage_a:.1f} V")
            print(f"  Current A: {current_a:.2f} A")
            print(f"  Calculated Power: {calculated_power:.2f} kW")
            print(f"  Actual Power: {active_power_a:.2f} kW")
            print(f"  Difference: {difference:.2f} kW")
            
            if difference <= tolerance:
                print(f"  ✅ Power calculation ถูกต้อง (tolerance: {tolerance:.2f} kW)")
            else:
                msg = f"⚠️ Power mismatch: Difference {difference:.2f}kW > Tolerance {tolerance:.2f}kW"
                warnings.append(msg)
                print(f"  {msg}")
        
        # ตรวจสอบ Apparent Power
        print("\n📊 Apparent Power Calculation (Phase A):")
        active = abs(telemetry.get('active_power_a', 0))
        reactive = abs(telemetry.get('reactive_power_a', 0))
        apparent = telemetry.get('apparent_power_a', 0)
        
        if apparent > 0:
            calculated_apparent = (active**2 + reactive**2)**0.5
            difference = abs(calculated_apparent - apparent)
            tolerance = apparent * 0.1
            
            print(f"  Active Power: {active:.2f} kW")
            print(f"  Reactive Power: {reactive:.2f} kVar")
            print(f"  Calculated Apparent: {calculated_apparent:.2f} kVA")
            print(f"  Actual Apparent: {apparent:.2f} kVA")
            print(f"  Difference: {difference:.2f} kVA")
            
            if difference <= tolerance:
                print(f"  ✅ Apparent Power calculation ถูกต้อง (tolerance: {tolerance:.2f} kVA)")
            else:
                msg = f"⚠️ Apparent Power mismatch: Difference {difference:.2f}kVA > Tolerance {tolerance:.2f}kVA"
                warnings.append(msg)
                print(f"  {msg}")
        
        # ตรวจสอบ Total Power = Sum of Phases
        print("\n📊 Total Power = Sum of Phases:")
        total = abs(telemetry.get('active_power_total', 0))
        sum_phases = abs(telemetry.get('active_power_a', 0)) + \
                     abs(telemetry.get('active_power_b', 0)) + \
                     abs(telemetry.get('active_power_c', 0))
        
        difference = abs(total - sum_phases)
        tolerance = total * 0.1 if total > 0 else 0.1
        
        print(f"  Sum of Phases: {sum_phases:.2f} kW")
        print(f"  Total Power: {total:.2f} kW")
        print(f"  Difference: {difference:.2f} kW")
        
        if difference <= tolerance:
            print(f"  ✅ Total Power ถูกต้อง (tolerance: {tolerance:.2f} kW)")
        else:
            msg = f"⚠️ Total Power mismatch: Difference {difference:.2f}kW > Tolerance {tolerance:.2f}kW"
            warnings.append(msg)
            print(f"  {msg}")
        
        # ตรวจสอบ DC Power
        print("\n📊 DC Input Power Calculation:")
        dc_voltage = abs(telemetry.get('dc_input_voltage', 0))
        dc_current = abs(telemetry.get('dc_input_current', 0))
        dc_power = abs(telemetry.get('dc_input_power', 0))
        
        if dc_voltage > 0 and dc_current > 0:
            calculated_dc_power = (dc_voltage * dc_current) / 1000
            difference = abs(calculated_dc_power - dc_power)
            tolerance = dc_power * 0.15 if dc_power > 0 else 0.1
            
            print(f"  DC Voltage: {dc_voltage:.1f} V")
            print(f"  DC Current: {dc_current:.2f} A")
            print(f"  Calculated Power: {calculated_dc_power:.2f} kW")
            print(f"  Actual Power: {dc_power:.2f} kW")
            print(f"  Difference: {difference:.2f} kW")
            
            if difference <= tolerance:
                print(f"  ✅ DC Power calculation ถูกต้อง (tolerance: {tolerance:.2f} kW)")
            else:
                msg = f"⚠️ DC Power mismatch: Difference {difference:.2f}kW > Tolerance {tolerance:.2f}kW"
                warnings.append(msg)
                print(f"  {msg}")
    
    # 2. อ่าน Status
    print("\n" + "="*60)
    print("2. ตรวจสอบ Status (Address 81-96)")
    print("="*60)
    status = client.get_status()
    if not status:
        errors.append("❌ ไม่สามารถอ่าน Status ได้")
        print("❌ ไม่สามารถอ่าน Status ได้")
    else:
        print("✅ อ่าน Status สำเร็จ\n")
        print("📊 Device Status:")
        print(f"  Running: {'🟢 ON' if status.get('running') else '🔴 OFF'}")
        print(f"  Fault: {'🔴 YES' if status.get('fault') else '🟢 NO'}")
        print(f"  Alarm: {'🟡 YES' if status.get('alarm') else '🟢 NO'}")
        print(f"  Grid Connected: {'🟢 YES' if status.get('grid_connected') else '🔴 NO'}")
        print(f"  Standby: {'🟡 YES' if status.get('standby') else '⚪ NO'}")
        print(f"  Remote Control: {'🟢 YES' if status.get('remote_control') else '⚪ NO'}")
    
    # 3. อ่าน Temperature
    print("\n" + "="*60)
    print("3. ตรวจสอบ Temperature (Address 227, 257-261)")
    print("="*60)
    temp = client.get_temperature()
    if not temp:
        warnings.append("⚠️ ไม่สามารถอ่าน Temperature ได้")
        print("⚠️ ไม่สามารถอ่าน Temperature ได้")
    else:
        print("✅ อ่าน Temperature สำเร็จ\n")
        print("📊 Temperature:")
        radiator_temp = temp.get('radiator_temp', 0)
        if 0 <= radiator_temp <= 100:
            print(f"  ✅ Radiator Temp: {radiator_temp:.1f}°C (ปกติ)")
        else:
            msg = f"⚠️ Radiator Temp: {radiator_temp:.1f}°C (นอกช่วงปกติ 0-100°C)"
            warnings.append(msg)
            print(f"  {msg}")
        
        soc_temp = temp.get('soc_temp', 0)
        print(f"  SOC Temp: {soc_temp:.1f}°C")
        
        for i in range(1, 5):
            igbt_temp = temp.get(f'igbt_temp_{i}', 0)
            print(f"  IGBT {i} Temp: {igbt_temp:.1f}°C")
    
    # 4. อ่าน Accumulated Power
    print("\n" + "="*60)
    print("4. ตรวจสอบ Accumulated Power (Address 230-237)")
    print("="*60)
    acc_power = client.get_accumulated_power()
    if not acc_power:
        warnings.append("⚠️ ไม่สามารถอ่าน Accumulated Power ได้")
        print("⚠️ ไม่สามารถอ่าน Accumulated Power ได้")
    else:
        print("✅ อ่าน Accumulated Power สำเร็จ\n")
        print("📊 Accumulated Energy:")
        for key, value in acc_power.items():
            if 0 <= value <= 4294967.295:
                print(f"  ✅ {key}: {value:.3f} kWh")
            else:
                msg = f"❌ {key}: {value:.3f} kWh (นอกช่วง 0-4294967.295 kWh)"
                errors.append(msg)
                print(f"  {msg}")
    
    # 5. อ่าน Fault Words
    print("\n" + "="*60)
    print("5. ตรวจสอบ Fault Words (Address 256, 272-275)")
    print("="*60)
    fault_words = client.get_fault_words()
    if not fault_words:
        warnings.append("⚠️ ไม่สามารถอ่าน Fault Words ได้")
        print("⚠️ ไม่สามารถอ่าน Fault Words ได้")
    else:
        print("✅ อ่าน Fault Words สำเร็จ\n")
        print("📊 Fault Words:")
        has_fault = False
        for i in range(1, 6):
            fault_value = fault_words.get(f'fault_word_{i}', 0)
            if fault_value == 0:
                print(f"  ✅ Fault Word {i}: 0x{fault_value:04X} (ไม่มี Fault)")
            else:
                print(f"  ⚠️ Fault Word {i}: 0x{fault_value:04X} (มี Fault)")
                has_fault = True
        
        if has_fault:
            warnings.append("⚠️ พบ Fault Words ที่ไม่เป็นศูนย์")
    
    # 6. อ่าน System Info
    print("\n" + "="*60)
    print("6. ตรวจสอบ System Information (Address 238-247)")
    print("="*60)
    sys_info = client.get_system_info()
    if not sys_info:
        warnings.append("⚠️ ไม่สามารถอ่าน System Info ได้")
        print("⚠️ ไม่สามารถอ่าน System Info ได้")
    else:
        print("✅ อ่าน System Info สำเร็จ\n")
        print("📊 System Information:")
        pcs_version = sys_info.get('pcs_version', 0)
        fpga_version = sys_info.get('fpga_version', 0)
        print(f"  PCS Version: {pcs_version:.1f}")
        print(f"  FPGA Version: {fpga_version}")
        
        clock = sys_info.get('system_clock', {})
        if clock:
            clock_str = f"{clock.get('year', 0)}/{clock.get('month', 0):02d}/{clock.get('day', 0):02d} {clock.get('hour', 0):02d}:{clock.get('minute', 0):02d}:{clock.get('second', 0):02d}"
            print(f"  System Clock: {clock_str}")
        
        current_n = sys_info.get('current_n', 0)
        print(f"  Phase N Current: {current_n:.2f} A")
    
    # สรุปผล
    print("\n" + "="*60)
    print("สรุปผลการตรวจสอบ")
    print("="*60)
    
    if errors:
        print("\n❌ ERRORS (ต้องแก้ไข):")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
    
    if warnings:
        print("\n⚠️ WARNINGS (ควรตรวจสอบ):")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")
    
    if not errors and not warnings:
        print("\n✅ ทุกอย่างถูกต้อง! ไม่พบปัญหา")
    
    print("\n" + "="*60)
    
    client.close()
    return len(errors) == 0

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else '192.168.0.20'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 502
    
    try:
        success = validate_pcs_data(host, port)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ ถูกยกเลิกโดยผู้ใช้")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

