from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class YearMonth:
    year: int
    month: int

    def __post_init__(self) -> None:
        if not (1 <= self.month <= 12):
            raise ValueError(f"Mês inválido: {self.month}")
        if self.year < 1900:
            raise ValueError(f"Ano inválido: {self.year}")

    @classmethod
    def from_string(cls, value: str) -> "YearMonth":
        """Parseia formatos: MM/YYYY, YYYY-MM, MMyyyy (6 dígitos)."""
        value = value.strip()
        if len(value) == 6 and value.isdigit():
            mm, yyyy = int(value[:2]), int(value[2:])
            if 1 <= mm <= 12:
                return cls(yyyy, mm)
            return cls(int(value[:4]), int(value[4:]))
        for fmt, parser in [
            ("/", lambda p: cls(int(p[1]), int(p[0]))),
            ("-", lambda p: cls(int(p[0]), int(p[1]))),
        ]:
            if fmt in value:
                parts = value.split(fmt)
                if len(parts) == 2:
                    try:
                        return parser(parts)
                    except (ValueError, IndexError):
                        pass
        raise ValueError(f"Formato de YearMonth inválido: {value!r}")

    def to_iso(self) -> str:
        return f"{self.year:04d}-{self.month:02d}"

    def to_display(self) -> str:
        return f"{self.month:02d}/{self.year:04d}"

    def __str__(self) -> str:
        return self.to_display()
