import pytest

from core.usecases.account.create_account import CreateAccountUseCase, CreateAccountCommand


@pytest.mark.asyncio
async def test_create_new_account(uow_factory):
    uow = uow_factory.for_create_account()
    handler = CreateAccountUseCase(uow)
    command = CreateAccountCommand(
        name='Test Account',
        address='Test Address',
        description='Test Description'
    )
    response = await handler.handle(command)

    account = await uow.account_repository.get(response.id)
    account_balance = await uow.account_balance_repository.get_by_account_id(response.id)

    assert account.name == 'Test Account'
    assert account.address == 'Test Address'
    assert account.description == 'Test Description'
    assert account_balance.amount == 0.0
    assert account_balance.transactions == []
    assert uow.committed
