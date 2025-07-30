from ..client import Client

class Chat:
    def __init__(self, instruction: str = None, think: bool = False, uncensored: bool = False):
        self.client = Client()
        self.instruction = instruction
        self.think = think
        self.uncensored = uncensored
        self.history = []

    def send_message(self, text: str, trying: int = 50):
        if self.instruction:
            self.history.append({"role": "system", "content": self.instruction})
        self.history.append({"role": "user", "content": text})
        for _ in range(trying):
            response = self.client.send_message(self.history, self.instruction, self.think, self.uncensored)
            if not response:
                continue
            else:
                self.history.append({"role": "assistant", "content": response})
                return response
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.history.clear()
