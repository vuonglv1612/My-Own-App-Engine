class InsufficientBalanceError(Exception):
    def __init__(self, project_id: str, amount: int):
        self.project_id = project_id
        self.amount = amount
        super().__init__(f"Project {project_id} has insufficient balance for charge of {amount}")
