
class NotAllowed(Exception):
    # Exception Raised when an action is not permitted
    def __init__(self, message='Bed Already In Use'):
        self.message = message
        super().__init__(self.message)


class InvalidStaffStatus(Exception):
    def __init__(self, message='Staff Must Be a Doctor or a Head Doctor'):
        self.message = message
        super().__init__(self.message)


class DateError(Exception):
    def __init__(self, message='The Date you choose is incorrect'):
        self.message = message
        super().__init__(self.message)

