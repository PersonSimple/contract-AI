class ContractNotFoundException(Exception):
    def __init__(self, message="Contract not found"):
        self.message = message
        super().__init__(self.message)


class TaskNotFoundException(Exception):
    def __init__(self, message="Task not found"):
        self.message = message
        super().__init__(self.message)


class BudgetExceededException(Exception):
    def __init__(self, message="Contract budget limit exceeded"):
        self.message = message
        super().__init__(self.message)


class InvalidHoursException(Exception):
    def __init__(self, message="Hours must be positive"):
        self.message = message
        super().__init__(self.message)