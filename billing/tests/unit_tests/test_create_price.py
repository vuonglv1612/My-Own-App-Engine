import pytest

from core.errors.prices import InvalidPriceTiersError, InvalidPriceTiersModeError
from core.models.prices import PriceRecurring, PriceTier
from core.usecases.price.create_price import CreatePriceCommand, CreatePriceUseCase


@pytest.mark.asyncio
async def test_create_price(uow_factory):
    unit_of_work = uow_factory.new()
    command = CreatePriceCommand(
        product_id="product_id_1",
        recurring=PriceRecurring(interval="month", interval_count=1, aggregate_usage="sum"),
        tiers=[PriceTier(unit_amount=1000.0, flat_amount=0.0, up_to=10),
               PriceTier(unit_amount=900.0, flat_amount=0.0, up_to="inf")],
        tiers_mode="graduated",
    )
    handler = CreatePriceUseCase(unit_of_work)
    response = await handler.execute(command)

    assert response.product_id == "product_id_1"
    assert response.recurring == PriceRecurring(interval="month", interval_count=1, aggregate_usage="sum")
    assert response.tiers == [PriceTier(unit_amount=1000.0, flat_amount=0.0, up_to=10),
                              PriceTier(unit_amount=900.0, flat_amount=0.0, up_to="inf")]
    assert response.tiers_mode == "graduated"
    assert unit_of_work.committed


@pytest.mark.asyncio
async def test_create_price_with_invalid_tiers(uow_factory):
    unit_of_work = uow_factory.new()
    command = CreatePriceCommand(
        product_id="product_id_1",
        recurring=PriceRecurring(interval="month", interval_count=1, aggregate_usage="sum"),
        tiers=[PriceTier(unit_amount=1000.0, flat_amount=0.0, up_to=10),
               PriceTier(unit_amount=900.0, flat_amount=0.0, up_to=5)],
        tiers_mode="graduated",
    )
    handler = CreatePriceUseCase(unit_of_work)

    with pytest.raises(InvalidPriceTiersError):
        await handler.execute(command)

    assert not unit_of_work.committed


@pytest.mark.asyncio
async def test_create_price_with_invalid_tiers_duplicate_up_to(uow_factory):
    unit_of_work = uow_factory.new()
    command = CreatePriceCommand(
        product_id="product_id_1",
        recurring=PriceRecurring(interval="month", interval_count=1, aggregate_usage="sum"),
        tiers=[PriceTier(unit_amount=1000.0, flat_amount=0.0, up_to=10),
               PriceTier(unit_amount=900.0, flat_amount=0.0, up_to=10),
               PriceTier(unit_amount=800.0, flat_amount=0.0, up_to="inf")],
        tiers_mode="graduated",
    )
    handler = CreatePriceUseCase(unit_of_work)

    with pytest.raises(InvalidPriceTiersError):
        await handler.execute(command)

    assert not unit_of_work.committed


@pytest.mark.asyncio
async def test_create_price_with_one_tier_but_not_inf(uow_factory):
    unit_of_work = uow_factory.new()
    command = CreatePriceCommand(
        product_id="product_id_1",
        recurring=PriceRecurring(interval="month", interval_count=1, aggregate_usage="sum"),
        tiers=[PriceTier(unit_amount=1000.0, flat_amount=0.0, up_to=10)],
        tiers_mode="graduated",
    )
    handler = CreatePriceUseCase(unit_of_work)

    with pytest.raises(InvalidPriceTiersError):
        await handler.execute(command)

    assert not unit_of_work.committed


@pytest.mark.asyncio
async def test_create_price_with_missing_tiers(uow_factory):
    unit_of_work = uow_factory.new()
    command = CreatePriceCommand(
        product_id="product_id_1",
        recurring=PriceRecurring(interval="month", interval_count=1, aggregate_usage="sum"),
        tiers=[],
        tiers_mode="graduated",
    )
    handler = CreatePriceUseCase(unit_of_work)

    with pytest.raises(InvalidPriceTiersError):
        await handler.execute(command)

    assert not unit_of_work.committed


@pytest.mark.asyncio
async def test_create_price_with_invalid_tiers_up_to_less_than_zero(uow_factory):
    unit_of_work = uow_factory.new()
    command = CreatePriceCommand(
        product_id="product_id_1",
        recurring=PriceRecurring(interval="month", interval_count=1, aggregate_usage="sum"),
        tiers=[PriceTier(unit_amount=1000.0, flat_amount=0.0, up_to=-1),
               PriceTier(unit_amount=900.0, flat_amount=0.0, up_to="inf")],
        tiers_mode="graduated",
    )
    handler = CreatePriceUseCase(unit_of_work)

    with pytest.raises(InvalidPriceTiersError):
        await handler.execute(command)

    assert not unit_of_work.committed


@pytest.mark.asyncio
async def test_create_price_with_invalid_tiers_mode(uow_factory):
    unit_of_work = uow_factory.new()
    command = CreatePriceCommand(
        product_id="product_id_1",
        recurring=PriceRecurring(interval="month", interval_count=1, aggregate_usage="sum"),
        tiers=[PriceTier(unit_amount=1000.0, flat_amount=0.0, up_to=10),
               PriceTier(unit_amount=900.0, flat_amount=0.0, up_to="inf")],
        tiers_mode="invalid",
    )
    handler = CreatePriceUseCase(unit_of_work)

    with pytest.raises(InvalidPriceTiersModeError):
        await handler.execute(command)

    assert not unit_of_work.committed
