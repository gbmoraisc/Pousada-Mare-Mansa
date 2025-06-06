from dataclasses import dataclass

@dataclass
class Cliente:
    cpf: str
    nome: str
    email: str