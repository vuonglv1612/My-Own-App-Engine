import copy
from datetime import datetime
from typing import List

from attrs import define, field

from core.errors.prices import InvalidPriceTiersError, InvalidPriceTiersModeError
from utils.datetime import aware_now


def validate_tiers(instance, attribute, value):
    # if only one tier, value.up_to must be "inf"
    # if more than one tier, value.up_to must be an integer and the last tier must be "inf"
    # up_to must be in ascending order and must be unique
    # up_to must be greater than 0
    # raise InvalidPriceTiersError if any of the above is not true

    new_value = copy.deepcopy(value)
    for v in new_value:
        if v.up_to != "inf":
            v.up_to = int(v.up_to)
        else:
            v.up_to = float("inf")

    new_value.sort(key=lambda x: x.up_to)

    if len(new_value) == 0:
        raise InvalidPriceTiersError("At least one tier is required")
    if len(new_value) == 1:
        if new_value[0].up_to != float("inf"):
            raise InvalidPriceTiersError("If only one tier, tier.up_to must be 'inf'")
    else:
        if new_value[-1].up_to != float("inf"):
            raise InvalidPriceTiersError("If more than one tier, the last tier must be 'inf'")
        for i in range(len(new_value) - 1):
            if new_value[i].up_to == new_value[i + 1].up_to:
                raise InvalidPriceTiersError("up_to must be unique")
            if new_value[i].up_to <= 0:
                raise InvalidPriceTiersError("up_to must be greater than 0")


def validate_price_tier_mode(instance, attribute, value):
    if value not in ["graduated", "volume"]:
        raise InvalidPriceTiersModeError("tiers_mode must be 'graduated' or 'volume'")


@define(kw_only=True, slots=False)
class PriceTier:
    unit_amount: float = field(default=0.0)
    flat_amount: float = field(default=0.0)
    up_to: int | str = field(default="inf")


@define(kw_only=True, slots=False)
class PriceRecurring:
    interval: str = field(default="month")
    interval_count: int = field(default=1)
    aggregate_usage: str = field(default="sum")


@define(kw_only=True, slots=False)
class Price:
    id: str = field()
    product_id: str = field()
    recurring: PriceRecurring
    tiers: List[PriceTier] = field(validator=validate_tiers)
    created_at: datetime = field(factory=aware_now)
    active: bool = field(default=True)
    lookup_key: str = field(default=None)
    tiers_mode: str = field(default="graduated", validator=validate_price_tier_mode)

    def billing(self, quantity) -> int:
        if self.tiers_mode == "volume":
            for i in range(len(self.tiers)):
                if quantity <= float(self.tiers[i].up_to):
                    return quantity * self.tiers[i].unit_amount + self.tiers[i].flat_amount
        if self.tiers_mode == "graduated":
            price = 0
            for i in range(len(self.tiers)):
                up_to_prev = 0 if i == 0 else self.tiers[i-1].up_to
                if quantity <= float(self.tiers[i].up_to):
                    price += (quantity - up_to_prev) * self.tiers[i].unit_amount + self.tiers[i].flat_amount
                    break
                else:
                    price += (self.tiers[i].up_to - up_to_prev) * self.tiers[i].unit_amount + self.tiers[i].flat_amount
            return price

    def line_billing(self, quantity) -> int:
        if self.tiers_mode == "volume":
            for i in range(len(self.tiers)):
                if quantity <= float(self.tiers[i]["up_to"]):
                    return quantity * self.tiers[i]["unit_amount"] + self.tiers[i]["flat_amount"]
        if self.tiers_mode == "graduated":
            price = 0
            for i in range(len(self.tiers)):
                up_to_prev = 0 if i == 0 else self.tiers[i-1]["up_to"]
                if quantity <= float(self.tiers[i]["up_to"]):
                    price += (quantity - up_to_prev) * self.tiers[i]["unit_amount"] + self.tiers[i]["flat_amount"]
                    break
                else:
                    price += (self.tiers[i]["up_to"] - up_to_prev) * self.tiers[i]["unit_amount"] + self.tiers[i]["flat_amount"]
            return price
