import cocotb

class ModbusScoreboard:
    """
    Reconfigurable scoreboard for Modbus RTU frames (IS4310-based VIP).
    """
    def __init__(self):
        self.expected = []
        self.received = []

    def add_expected(self, frame: list):
        self.expected.append(frame)
        cocotb.log.info(f"Scoreboard: Expected frame recorded: {frame}")

    def add_received(self, frame: list):
        self.received.append(frame)
        cocotb.log.info(f"Scoreboard: Received frame recorded: {frame}")

    def compare(self):
        if len(self.expected) != len(self.received):
            cocotb.log.error("Mismatch in number of expected and received frames.")
            return False

        for exp, rec in zip(self.expected, self.received):
            if isinstance(exp, bytes):
                exp = list(exp)
            if exp != rec:
                cocotb.log.error(f"Mismatch: Expected {exp} vs Received {rec}")
                return False

        return True

