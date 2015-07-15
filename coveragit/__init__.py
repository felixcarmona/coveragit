class ContextualizedException(Exception):
    def __init__(self, message='', context=None, previous_exception=None):
        self.message = message
        self._context = context
        self._previous_exception = previous_exception

    def get_context(self):
        return self._context

    def get_previous_exception(self):
        return self._previous_exception
