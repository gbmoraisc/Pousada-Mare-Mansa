from datetime import date
from quarto import Quarto
from cliente import Cliente
from dataclasses import dataclass

@dataclass

class Agendamento:
    id:int
    data_entrada:date
    data_saida:date
    cliente:'Cliente'
    quarto:'Quarto'