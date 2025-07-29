from agora_logging import logger

class LastValueCallbacks:
    """
    Provide ability to trigger callbacks.
    """
    def __init__(self, value) -> None:
        self.last_value = value
        self.callbacks = []

    def append(self, callback):
        """
        Appends callback to list of callbacks to be processed when value changes.
        """
        self.callbacks.append(callback)

    def remove(self, callback):
        """
        Removes callback from list of callbacks to be processed when value changes.
        """
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def update(self, value):
        """
        If new value != last value, the callbacks are called.
        """
        if value != self.last_value:
            for callback in self.callbacks:
                if callback != None:
                    try:
                        callback(value)
                    except:
                        logger.error(f"Callback '{callback}' failed with '{value}'")
        self.last_value = value
