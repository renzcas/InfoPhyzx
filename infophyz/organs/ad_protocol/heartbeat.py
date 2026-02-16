import time

class Heartbeat:
    def __init__(self, orchestrator, interval=0.1):
        self.orchestrator = orchestrator
        self.interval = interval

    def start(self):
        while True:
            self.orchestrator.step()
            time.sleep(self.interval)
