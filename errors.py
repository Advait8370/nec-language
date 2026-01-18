class NECError(Exception):
    def __init__(self, message, line):
        super().__init__(f"[NEC Error] Line {line}: {message}")
        self.line = line
