from datetime import datetime, timezone

from attrs import define, field

from src.core.errors import InsufficientBalanceError


@define
class BalanceAdjustment:
    id: str
    amount: int
    note: str
    created_at: datetime = field(default=None)
    deleted_at: datetime = field(init=False, default=None)


@define
class Project:
    id: str
    name: str
    balance: int = field(init=False, default=0)
    balance_adjustments: list[BalanceAdjustment] = field(init=False, default=[])
    created_at: datetime = field(default=None)
    deleted_at: datetime = field(init=False, default=None)
    version_number: int = field(init=False, default=0)

    def _generate_balance_adjustment_id(self):
        return f"{self.id}-{len(self.balance_adjustments) + 1}"

    @classmethod
    def create(cls, project_id: str, project_name: str, created_at: datetime):
        return cls(id=project_id, name=project_name, created_at=created_at)

    def top_up(self, amount: int, note: str):
        self.balance += amount
        balance_adjustment_id = self._generate_balance_adjustment_id()
        balance_adjustment = BalanceAdjustment(
            id=balance_adjustment_id,
            amount=amount,
            note=note,
            created_at=datetime.now(tz=timezone.utc),
        )
        self.balance_adjustments.append(balance_adjustment)
        self.version_number += 1
        return balance_adjustment

    def charge(self, amount: int, note: str):
        if self.balance < amount:
            raise InsufficientBalanceError(project_id=self.id, amount=amount)
        self.balance -= amount
        balance_adjustment_id = self._generate_balance_adjustment_id()
        balance_adjustment = BalanceAdjustment(
            id=balance_adjustment_id,
            amount=-amount,
            note=note,
            created_at=datetime.now(tz=timezone.utc),
        )
        self.balance_adjustments.append(balance_adjustment)
        self.version_number += 1
        return balance_adjustment
