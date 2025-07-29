import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue

class ModbusRTUMonitor:
    """
    IS4310-based, reconfigurable Modbus RTU Monitor.
    """
    def __init__(self, dut, config=None):
        self.dut = dut
        self.config = config or {}
        self.received_frames = []

    async def capture_frame(self, expected_length: int = None, baud_delay: int = None):
        expected_length = expected_length if expected_length is not None else self.config.get('frame_length', 6)
        baud_delay = baud_delay if baud_delay is not None else self.config.get('baud_delay', 100)
        self.dut.rx_enable.value = 1
        frame = []

        # Wait for non-zero valid byte to start
        while True:
            val = self.dut.rx_data.value
            if isinstance(val, BinaryValue) and ('x' in str(val) or 'z' in str(val)):
                await Timer(baud_delay, units="us")
                continue
            try:
                byte_val = int(val)
                if byte_val != 0:
                    frame.append(byte_val)
                    break
            except:
                pass
            await Timer(baud_delay, units="us")

        # Continue capturing the rest
        while len(frame) < expected_length:
            await Timer(baud_delay, units="us")
            val = self.dut.rx_data.value
            try:
                byte_val = int(val)
                frame.append(byte_val)
            except:
                continue

        self.dut.rx_enable.value = 0
        self.received_frames.append(frame)
        cocotb.log.info(f"Monitor captured frame: {frame}")
        return frame

