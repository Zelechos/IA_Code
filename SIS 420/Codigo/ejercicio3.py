import copy
from ej3Nodos import Nodo


def moverCuadradoAbajo(Nodo):
    aux = []
    aux = copy.deepcopy(Nodo)
    filas = 0
    for vectores in aux:
        for datos in range(len(vectores)):
            if (vectores[datos] == 1):
                # borrar los 2 espacios que se mueven
                aux[filas][datos] = 0
                aux[filas][datos + 1] = 0
                # agregar la parte faltante
                aux[filas + 2][datos] = 1
                aux[filas + 2][datos + 1] = 1
                return aux
        filas = filas + 1


def moverCuadradoIzquierda(Nodo):
    aux = []
    aux = copy.deepcopy(Nodo)
    filas = 0
    for vectores in aux:
        for datos in range(len(vectores)):
            if (vectores[datos] == 1):
                # borrar los 2 espacios que se mueven
                aux[filas][datos + 1] = 0
                aux[filas + 1][datos + 1] = 0
                # agregar la parte faltante
                aux[filas][datos - 1] = 1
                aux[filas + 1][datos - 1] = 1
                return aux
        filas = filas + 1


def moverCuadradoDerecha(Nodo):
    aux1 = []
    aux1 = copy.deepcopy(Nodo)
    filas = 0
    for vectores in aux1:
        for datos in range(len(vectores)):
            if (vectores[datos] == 1):
                # borrar los 2 espacios que se mueven
                aux1[filas][datos] = 0
                aux1[filas + 1][datos] = 0
                # agregar la parte faltante
                aux1[filas][datos + 2] = 1
                aux1[filas + 1][datos + 2] = 1
                return aux1
        filas = filas + 1


def Result(matrizJuego, matrizFinal):
    resuelto = False
    nodos_visitados = []
    nodos_frontera = []
    nodo_raiz = Nodo(matrizJuego)
    nodos_frontera.append(nodo_raiz)
    romperE = 0
    while (not resuelto) and len(nodos_frontera) != 0:
        nodo_actual = nodos_frontera.pop(0)
        nodos_visitados.append(nodo_actual)
        if nodo_actual.get_estado() == matrizFinal:
            resuelto = True
            return nodo_actual
        else:
            matriz = nodo_actual.get_estado()
            izquierda = 0
            derecha = 0
            abajo = 0
            filas = 0
            salirBucle = False
            for vectores in matriz:
                for datos in range(len(vectores)):
                    if ((vectores[datos] == 1) and (not salirBucle)):
                        izquierda = datos
                        derecha = datos + 1
                        abajo = filas + 1
                        salirBucle = True
                filas = filas + 1

            valorIzq = izquierda - 1
            hijo = moverCuadradoIzquierda(matriz)
            hijo_izquierda = Nodo(hijo)


            if valorIzq >= 0:
                if not hijo_izquierda.en_lista(nodos_visitados) and not hijo_izquierda.en_lista(
                        nodos_frontera) and romperE != 1:
                    romperE = 1
                    nodos_frontera.append(hijo_izquierda)

            valorAbajo = abajo + 1
            hijo = moverCuadradoAbajo(matriz)
            hijo_centro = Nodo(hijo)

            if valorAbajo < 7:
                if not hijo_centro.en_lista(nodos_visitados) and not hijo_centro.en_lista(
                        nodos_frontera) and romperE != 2:
                    romperE = 2
                    nodos_frontera.append(hijo_centro)

            valorDerecha = derecha + 1
            hijo = moverCuadradoDerecha(matriz)
            hijo_derecha = Nodo(hijo)

            if valorDerecha < 7:
                if not hijo_derecha.en_lista(nodos_visitados) and not hijo_derecha.en_lista(
                        nodos_frontera) and romperE != 3:
                    romperE = 3
                    nodos_frontera.append(hijo_derecha)

        nodo_actual.set_hijo([hijo_izquierda, hijo_centro, hijo_derecha])


if __name__ == "__main__":

    estado_inicial = [[0, 1, 1, 0, 0, 0, 0],
                      [0, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0]]

    solucion = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0],
                [0, 0, 0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]

    nodo_solucion = Result(estado_inicial, solucion)
    resultado = []
    nodo_actual = nodo_solucion
    while nodo_actual.get_padre() is not None:
        resultado.append(nodo_actual.get_estado())
        nodo_actual = nodo_actual.get_padre()
        # print(nodo_actual)

    resultado.append(estado_inicial)
    resultado.reverse()
    print(resultado)
