from tipo import Tipo 
from dataclasses import dataclass

@dataclass
class Quarto:
    numero_quarto: int
    disponibilidade: bool
    capacidade: int
    tipo: 'Tipo'  