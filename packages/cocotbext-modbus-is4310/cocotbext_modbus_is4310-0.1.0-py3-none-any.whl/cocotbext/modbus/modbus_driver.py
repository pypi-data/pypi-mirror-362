import cocotb
from cocotb.triggers import Timer
from cocotbext.modbus.modbus_rtu import calculate_crc

class ModbusRTUDriver:
    """
    IS4310-based, reconfigurable Modbus RTU Driver.
    """
    def __init__(self, dut, config=None):
        self.dut = dut
        self.config = config or {}
        self.default_baud_delay = self.config.get('baud_delay', 10)

    async def send_frame(self, address: int = None, function_code: int = None, data_bytes: list = None, baud_delay: int = None):
        address = address if address is not None else self.config.get('address', 1)
        function_code = function_code if function_code is not None else self.config.get('function_code', 0x03)
        data_bytes = data_bytes if data_bytes is not None else self.config.get('data_bytes', [0x00, 0x02])
        baud_delay = baud_delay if baud_delay is not None else self.default_baud_delay

        frame = [address, function_code] + data_bytes
        crc = calculate_crc(bytes(frame))
        full_frame = frame + list(crc)

        self.dut.tx_enable.value = 1
        for byte in full_frame:
            self.dut.tx_data.value = byte
            await Timer(baud_delay, units="us")
        self.dut.tx_enable.value = 0

        cocotb.log.info(f"Driver sent frame: {full_frame}")

