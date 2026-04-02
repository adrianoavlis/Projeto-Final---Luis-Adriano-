class DomainException(Exception):
    pass

class EntidadeNaoEncontradaException(DomainException):
    def __init__(self, entidade: str, id: object) -> None:
        super().__init__(f"{entidade} com id={id!r} não encontrado.")

class ValidacaoException(DomainException):
    def __init__(self, erros: list[str]) -> None:
        self.erros = erros
        super().__init__("; ".join(erros))

class PeriodoInvalidoException(DomainException):
    pass
