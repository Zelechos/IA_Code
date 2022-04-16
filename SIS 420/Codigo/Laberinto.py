import math
from busquedas_02 import ProblemaBusqueda, aestrella

MAPA = """
##############################
#         #              #   #
# ####    ########       #   #
#  o #    #              #   #
#    ###     ####   ######   #
#         ####      #        #
#            #  #   #   #### #
#     ######    #       # x  #
#        #      #            #
##############################
"""
MAPA = [list(x) for x in MAPA.split("\n") if x]

COSTOS = {
    "arriba": 1.0,
    "abajo": 1.0,
    "izquierda": 1.0,
    "derecha": 1.0,
    "arriba izquierda": 1.4,
    "arriba derecha": 1.4,
    "abajo izquierda": 1.4,
    "abajo derecha": 1.4,
}


class JuegoLaberinto(ProblemaBusqueda):

    def __init__(self, tablero):
        self.tablero = tablero
        self.estado_objetivo = (0, 0)
        for y in range(len(self.tablero)):
            for x in range(len(self.tablero[y])):
                if self.tablero[y][x].lower() == "o":
                    self.estado_inicial = (x, y)
                elif self.tablero[y][x].lower() == "x":
                    self.estado_objetivo = (x, y)

        super(JuegoLaberinto, self).__init__(estado_inicial=self.estado_inicial)

    def acciones(self, estado):
        acciones = []
        for accion in list(COSTOS.keys()):
            nuevox, nuevoy = self.resultado(estado, accion)
            if self.tablero[nuevoy][nuevox] != "#":
                acciones.append(accion)
        return acciones

    def resultado(self, estado, accion):
        x, y = estado

        if accion.count("arriba"):
            y -= 1
        if accion.count("abajo"):
            y += 1
        if accion.count("izquierda"):
            x -= 1
        if accion.count("derecha"):
            x += 1

        estado_nuevo = (x, y)
        return estado_nuevo

    def es_objetivo(self, estado):
        return estado == self.estado_objetivo

    def costo(self, estado, accion, estado2):
        return COSTOS[accion]

    def heuristic(self, estado):
        x, y = estado
        gx, gy = self.estado_objetivo
        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)


def main():
    problema = JuegoLaberinto(MAPA)
    resultado = aestrella(problema, busqueda_en_grafo=True)
    camino = [x[1] for x in resultado.camino()]

    for y in range(len(MAPA)):
        for x in range(len(MAPA[y])):
            if (x, y) == problema.estado_inicial:
                print("o", end='')
            elif (x, y) == problema.estado_objetivo:
                print("x", end='')
            elif (x, y) in camino:
                print("·", end='')
            else:
                print(MAPA[y][x], end='')
        print()


if __name__ == "__main__":
    main()

