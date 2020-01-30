from random import choice
from typing import NoReturn, Iterable, Any, Tuple, List, Generator
from types import FunctionType
from os import system as sy
from itertools import cycle
from functools import reduce

from src.tools import MinhaLista


grade = """
\x1b[38;5;6m―――――――――――――――
| {} | {} | {} |
―――――――――――――――
| {} | {} | {} |
―――――――――――――――
| {} | {} | {} |
―――――――――――――――\x1b[0m
"""

grade = grade.replace('{}', '{}\x1b[38;5;6m')


def usuario(lista: List[int], texto: str = False) -> int:
    """ Função que, enquanto jogando, pede uma entrada para o jogador. """
    return int(pegar_entrada('1 a 9: ', lista, texto))


def maquina(lista: List[int], *_) -> int:
    """ Função que emula a máquina jogando. """
    return int(choice(lista))


def inverter(item: Any, lista: Iterable[Any]) -> Any:
    """ Função que pega o outro item dentro de uma lista. """
    return next(filter(lambda x: x != item, lista))


def alternar_adversarios(partida: FunctionType) -> FunctionType:
    """ Decorador que alterna os adversários entre as partidas. """
    def pegar_argumentos(adversario) -> FunctionType:
        jogador = 'usuário' if choice([0, 1]) == 0 else adversario
        partida(adversario, jogador)
        pergunta = 'deseja jogar novamente? (s/n): '
        while pegar_entrada(pergunta, 'sn') == 's':
            jogador = inverter(jogador, ['usuário', adversario])
            partida(adversario, jogador)
    return pegar_argumentos


@alternar_adversarios
def partida(adversario: str, jogador: str) -> NoReturn:
    """ Função que executa uma partida do jogo da velha. """
    lista = MinhaLista(' ' * 9)
    simbolos = {'usuário': '❌', adversario: '⭕'}  # ✖ ◽ ◻
    funcoes = {'usuário': usuario, 'usuário2': usuario, 'máquina': maquina}
    venc = vencedor(simbolos, lista)
    while not venc:
        print(grade.format(*numerar(lista)))
        jogador = inverter(jogador, ['usuário', adversario])
        print(f"jogador: {jogador}, simbolo: {simbolos[jogador]}")
        funcao = funcoes[jogador]
        numero = funcao(lista.vazios(), grade.format(*numerar(lista)))
        lista[numero - 1] = simbolos[jogador]
        sy('clear')
        venc = vencedor(simbolos, lista)
    print(f"{venc} venceu!" if venc != 'empate' else f"{venc}!")


def numerar(lista: List[str]) -> List[str]:
    """ Função que transforma todos os espaços em números com cor cinza. """
    forma = '\x1b[38;5;245m {}\x1b[0m'
    temp = enumerate(lista, 1)
    temp = map(lambda x: forma.format(x[0]) if x[1] == ' ' else x[1], temp)
    return list(temp)


def chunk(lista: Iterable, numero: int) -> list:
    """ Função que recorta uma lista em partes. """
    return [lista[x: x + numero] for x in range(0, len(lista), numero)]


def verificar_1(lista: List[List[str]]) -> Tuple[str, bool]:
    """ Função auxiliar à função vencedor. """
    temp = filter(lambda x: len(list(set(x))) == 1 and x[0] != ' ', lista)
    temp = next(temp, False)
    return temp[0] if temp else temp


def verificar_2(lista: List[List[str]]) -> Tuple[str, bool]:
    """ Função auxiliar à função vencedor. """
    a, b, c = lista
    temp = [a[0], b[1], c[2]]
    temp2 = [a[2], b[1], c[0]]
    temp =  verificar_1([temp, temp2])
    return temp


def verificar_empate(lista: List[str]) -> bool:
    """ Função pra verificar se ouve empate. """
    return all(map(lambda x: x != ' ', lista))


def vencedor(usuarios_simbolos: dict, lista: List[str]) -> Tuple[str, bool]:
    """ Função que verifica se algum competidor ganhou e o retorna. """
    simbolos_usuarios = {y: x for x, y in usuarios_simbolos.items()}
    lista_recortada = chunk(lista, 3)
    resultado = verificar_1(lista_recortada)
    lista_recortada = list(zip(*lista_recortada))
    resultado2 = verificar_1(lista_recortada)
    resultado3 = verificar_2(lista_recortada)
    temp = [resultado, resultado2, resultado3]
    empate = 'empate' if verificar_empate(lista) else False
    temp = next(filter(lambda x: x, temp), empate)
    return simbolos_usuarios.get(temp, temp)


def pegar_entrada(texto: str, itens: Iterable[str], texto2: str = False) -> str:
    """ Pega a entrada do usuário até ele responder uma entrada adequada. """
    resposta = input(texto).lower()
    sy('clear')
    while resposta not in itens:
        print('\nResposta errada. por favor, insira uma resposta aceitável.\n')
        if texto2:
            print(texto2)
        resposta = input(texto).lower()
        sy('clear')
    return resposta


def main() -> NoReturn:
    """ Função principal. """
    print('Aviso: o primeiro usuário a jogar será escolhido aleatoriamente.\n')
    print('deseja jogar contra a máquina ou um adiversário humano?')
    resposta = pegar_entrada('máquina = 0, adversário = 1. -> ', '01')
    adversario = 'máquina' if resposta == '0' else 'usuário2'
    partida(adversario)


# TODO: uma partida, melhor de 3, melhor de 5.
# todas devem ter a opção de jogar novamente.
