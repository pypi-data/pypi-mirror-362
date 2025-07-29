import cocotb
from cocotbext.modbus.modbus_rtu import calculate_crc

class ModbusErrorChecker:
    def check_errors(self, frame: list):
        """Validate the integrity of a received Modbus frame."""
        if len(frame) < 3:  # Ensure frame length is valid
            cocotb.log.error("ERROR: Frame too short to validate CRC.")
            return False
        data, received_crc = frame[:-2], frame[-2:]  # Separate payload and CRC
        expected_crc = list(calculate_crc(bytes(data)))  # Compute expected CRC
        if received_crc != expected_crc:  # Compare CRC values
            cocotb.log.error(f"CRC ERROR: Expected {expected_crc}, Received {received_crc}")
            return False
        cocotb.log.info("CRC Validation PASSED.")  # Log success
        return True

