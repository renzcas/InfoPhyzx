from organ_protocol.ui_interface import UIInterface

class UIWrapper(UIInterface):
    def __init__(self, ui_impl):
        self.ui = ui_impl

    def send_event(self, event: dict):
        return self.ui.send_event(event)

    def receive_state(self):
        return self.ui.receive_state()

    def stream_updates(self):
        return self.ui.stream_updates()
