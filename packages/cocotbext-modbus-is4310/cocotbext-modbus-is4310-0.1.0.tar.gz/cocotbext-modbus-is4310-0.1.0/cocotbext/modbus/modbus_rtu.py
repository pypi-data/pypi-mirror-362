def calculate_crc(data: bytes) -> bytes:
    """
    Compute the Modbus RTU CRC16 checksum for the given data.
    """
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc.to_bytes(2, byteorder='little')

# Provide an alias so both names work.
compute_crc = calculate_crc

def build_modbus_frame(addr: int, func: int, data: list[int]) -> bytes:
    """
    Construct a complete Modbus RTU frame with address, function code, data, and CRC.
    All fields are parameterized for reconfigurable VIP.
    """
    payload = bytes([addr, func] + data)
    crc = calculate_crc(payload)
    return payload + crc

