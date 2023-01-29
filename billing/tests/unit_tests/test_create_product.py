import pytest

from core.usecases.product.create_product import CreateProductUseCase, CreateProductCommand


@pytest.mark.asyncio
async def test_create_new_product(uow_factory):
    uow = uow_factory.for_create_product()
    handler = CreateProductUseCase(uow)
    command = CreateProductCommand(
        name='CPU',
        description='Intel Core i7',
        unit_label='core',
    )
    response = await handler.handle(command)

    product = await uow.product_repository.get(response.id)

    assert product.name == 'CPU'
    assert product.description == 'Intel Core i7'
    assert product.unit_label == 'core'
    assert uow.committed
