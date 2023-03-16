import uuid

from attrs import define, field


@define(kw_only=True, slots=False)
class Environment:
    id: str = field(factory=lambda: str(uuid.uuid4().hex))
    app_id: str = field()
    name: str = field()
    value: str = field()

    app: 'App' = field(init=False, default=None)
