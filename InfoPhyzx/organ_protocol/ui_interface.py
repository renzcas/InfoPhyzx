class UIInterface:
    """
    Contract for the InfoPhyzx cockpit organism.
    Defines how UI panels communicate with backend state.
    """

    def send_event(self, event: dict):
        """Send an event from UI → backend."""
        raise NotImplementedError

    def receive_state(self) -> dict:
        """Return the current system state for UI rendering."""
        raise NotImplementedError

    def stream_updates(self):
        """Provide a generator/stream of live updates."""
        raise NotImplementedError
