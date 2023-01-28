from core.usecases.account.create_account import CreateAccountUseCase, CreateAccountCommand


def test_create_new_account(uow_factory):
    uow = uow_factory.for_create_account()
    with uow:
        handler = CreateAccountUseCase(uow.account_repository, uow.account_balance_repository)
        command = CreateAccountCommand(
            name='Test Account',
            address='Test Address',
            description='Test Description'
        )
        response = handler.handle(command)
        uow.commit()

    account = uow.account_repository.get(response.id)
    account_balance = uow.account_balance_repository.get(account.id)

    assert account.name == 'Test Account'
    assert account.address == 'Test Address'
    assert account.description == 'Test Description'
    assert account_balance.amount == 0.0
    assert account_balance.transactions == []
