class DataCleaningError(Exception):
    def __init__(self, message):    # it is one of the constructorand public scope
        self.message = message
        super().__init__(self.message)