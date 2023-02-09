import uuid
from datetime import datetime
from typing import List

from attrs import define, field

from utils.datetime import aware_now


@define(kw_only=True, slots=False)
class Transaction:
    id: str = field(factory=lambda: str(uuid.uuid4().hex))
    created_at: datetime = field(factory=aware_now)
    account_id: str = field()
    amount: float = field()
    transaction_type: str = field()
    description: str = field(default=None)


@define(kw_only=True, slots=False)
class AccountBalance:
    id: str = field(factory=lambda: str(uuid.uuid4().hex))
    created_at: datetime = field(factory=aware_now)
    amount: float = field(default=0.0)
    account_id: str = field()
    transactions: List[Transaction] = field(factory=list)
    version_number: int = field(default=1)

    def charge(amount):
        # tao transaction
        pass

    def topup(amount):
        pass


@define(kw_only=True, slots=False)
class Account:
    id: str = field(factory=lambda: str(uuid.uuid4().hex))
    created_at: datetime = field(factory=aware_now)
    deleted_at: datetime = field(default=None)
    name: str = field(default=None)
    address: str = field(default=None)
    description: str = field(default=None)
    email: str = field(default=None)
    phone: str = field(default=None)
    version_number: int = field(default=1)

    # def update_info(self, **kwargs):
    #     for k, v in kwargs.items():
    #         if hasattr(self, k):
    #             setattr(self, k, v)
    #     self.version_number += 1
