from datetime import datetime, timezone
from dataclasses import dataclass, field


@dataclass
class BaseEntity:
    id: int | None = field(default=None)
    criado_em: datetime | None = field(default=None)
    atualizado_em: datetime | None = field(default=None)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        if self.id is None or other.id is None:
            return self is other
        return self.id == other.id

    def __hash__(self) -> int:
        if self.id is None:
            return hash(id(self))
        return hash((type(self), self.id))
