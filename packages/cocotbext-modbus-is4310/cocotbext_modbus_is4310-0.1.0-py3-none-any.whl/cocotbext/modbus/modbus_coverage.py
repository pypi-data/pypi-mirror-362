import cocotb

class ModbusCoverage:
    """
    Reconfigurable Modbus function code coverage tracker for IS4310-based VIP.
    """
    def __init__(self):
        self.coverage = {}

    def sample(self, frame: list):
        if len(frame) < 2:
            return
        func_code = frame[1]
        self.coverage[func_code] = self.coverage.get(func_code, 0) + 1
        cocotb.log.info(f"Coverage: Function Code 0x{func_code:02X} count = {self.coverage[func_code]}")

    def report(self) -> str:
        report_str = "=== Modbus Coverage Report ===\n"
        for code, count in self.coverage.items():
            report_str += f"Function Code 0x{code:02X}: {count} transaction(s)\n"
        cocotb.log.info(report_str)
        return report_str

