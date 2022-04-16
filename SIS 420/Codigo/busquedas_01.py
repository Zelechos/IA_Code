from collections import defaultdict
import collections
import collections.abc
import math
import random
import sys
import bisect
from operator import itemgetter

infinito = float('inf')

class Queue:
    """Queue es una clase/interface abstrac. Hay tres tipos:
        Stack(): Primero en entrar ultimo en salir.
        FIFOQueue(): Primero en entrar primero en salir.
        PriorityQueue(order, f): columnaa ordenada de acuerdo a un criterio (por defecto el menor es el primero).
    Cada tipo soporta los siguientes metodos y funciones:
        q.append(item)  -- agrega un item en la columnaa
        q.extend(items) -- equivalente a: for item in items: q.append(item)
        q.pop()         -- devuelve el elemento de la cima desde la columnaa
        len(q)          -- numbero de elementos en q (tambien q.__len())
        item in q       -- q contiene el elemento item?
    Nota isinstance(Stack(), Queue) es falso, porque se implementa las pilas como listas.
    as lists. Si Python alguna vez obtiene interfaces, Queue será una interfaz."""

    def __init__(self):
        raise NotImplementedError

    def extend(self, items):
        for item in items:
            self.append(item)


def Stack():
    """Devuelve una lista vacia, adecuada como una columnaa primero en entrar, ultimo en salir."""
    return []


class FIFOQueue(Queue):
    """Cola primero en entrar primero en salir."""

    def __init__(self, maxlen=None, items=[]):
        self.queue = collections.deque(items, maxlen)

    def append(self, item):
        if not self.queue.maxlen or len(self.queue) < self.queue.maxlen:
            self.queue.append(item)
        else:
            raise Exception('FIFOQueue is full')

    def extend(self, items):
        if not self.queue.maxlen or len(self.queue) + len(items) <= self.queue.maxlen:
            self.queue.extend(items)
        else:
            raise Exception('FIFOQueue max length exceeded')

    def pop(self):
        if len(self.queue) > 0:
            return self.queue.popleft()
        else:
            raise Exception('FIFOQueue is empty')

    def __len__(self):
        return len(self.queue)

    def __contains__(self, item):
        return item in self.queue


class PriorityQueue(Queue):

    """Cola donde el minimo (o maximo) elemento (que ha sido determinado por f y ordenado) es el primero que se devuelve.
    Si el orden es min, el elemento con minimo f(x) es devuelto primero; si el orden es ma, entonces se devuelve el elemento
    con maximo f(x). Tambien admite busquedas tipo diq."""

    def __init__(self, order=min, f=lambda x: x):
        self.A = []
        self.order = order
        self.f = f

    def append(self, item):
        bisect.insort(self.A, (self.f(item), item))

    def __len__(self):
        return len(self.A)

    def pop(self):
        if self.order == min:
            return self.A.pop(0)[1]
        else:
            return self.A.pop()[1]

    def __contains__(self, item):
        return any(item == pair[1] for pair in self.A)

    def __getitem__(self, key):
        for _, item in self.A:
            if item == key:
                return item

    def __delitem__(self, key):
        for i, (value, item) in enumerate(self.A):
            if item == key:
                self.A.pop(i)
# ______________________________________________________________________________

def memoize(fn, slot = None, maxsize=32):
    """Memoize fn:
    hace que recuerde el valor calculado para cualquier lista de argumentos.
    Si se especifica el espacio, almacenar el resultado en ese espacio del primer argumento.
    Si la ranura es falsa, use lru_cache para almacenar en caché los valores.."""
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return fn(*args)

    return memoized_fn

def is_in(elt, seq):
    """Similar a (elt in seq), pero compara con 'is', not '=='."""
    return any(x is elt for x in seq)

class Problema(object):

    """Clase abstrata para formalizacion del problema. Se debe crear una subclase de esta e implementar
    los metodos acciones y resultadoado, y posiblemente __init__, estado_objetivo_prueba y costo_camino. Luego se
    crearan instancias de la subclase y se resolvera con ello varias funciones de busqueda.
    
    La clase abstracta para un problema formal. Debería subclasificar esto e 
    implementar los métodos acciones y resultados, y posiblemente __init__, estado_objetivo_test y camino_cost. 
    Luego creará instancias de su subclase y las resolverá con las diversas funciones de búsqueda
    """

    def __init__(self, estado_inicial, estado_objetivo = None):
        """El constructor espcifica el estado estado_inicial y posible estado estado_objetivo, si hay un solo estado_objetivo.
        El constructor de la subclase puede agregar otros argumentos."""
        self.estado_inicial = estado_inicial
        self.estado_objetivo = estado_objetivo

    def acciones(self, estado):
        #"""Devuelve las acciones que pueden ser ejecutadas en un estado. 
        #El resultado normalmente es una lista, por lo que hay que considerar entregarlas 
        #una a la vez en un iterador, en lugar de construirlas todas a la vez."""
        pass

    def resultado(self, estado, accion):
        """Devuelve el estado que resulta de ejecutar la acción dada en el estado dado. 
        La accion debe ser una de self.acciones (estado)."""
        pass

    def es_objetivo(self, estado):
        """Devuelve True si el estado es un estado_objetivo. El método predeterminado compara el estado con self.estado_objetivo 
        o verifica el estado en self.estado_objetivo si es una lista, como se especifica en el constructor. 
        Se debe anular este método si no es suficiente verificar con un solo self.estado_objetivo."""
        if isinstance(self.estado_objetivo, list):
            return is_in(estado, self.estado_objetivo)
        else:
            return estado == self.estado_objetivo

    def costo(self, estado, accion, state2):
        '''Devuelve el costo de aplicar una accion de un estado1 a estado2.
        El valor retornado es un numero (entero o punto flotante).
        por defecto la funcion retorna 1. '''
        return 1

    def costo_camino(self, c, estado1, accion, estado2):
        """Devuelva el costo de una ruta de solución que llega al estado2 desde el estado1 a través de accion, 
        asumiendo que el costo c llega al estado1. Si el problema es tal que la ruta no importa, 
        esta función solo analizará el estado2. Si la ruta importa, considerará c y quizás estado1 y accion. 
        El método predeterminado cuesta 1 por cada paso en la ruta."""
        return c + 1

    def valor(self, estado):
        """Para problemas de optimización, cada estado tiene un valor. 
        Varios algoritmos intentan maximizar este valor."""
        pass

    def h(self, estado):
    #    '''Devuelve una estimacion del costo sobrante para encontrar la solucion a partir de un estado'''
        return 0


class Grafo:
    """Un grafo conecta nodos (vértices) a traves de aristas(enlaces). 
    Cada arista también puede tener una longitud asociada. 
    La llamada al constructor es algo como: g = Grafo({'A': {'B': 1, 'C': 2})
    esto contruye un grafo con 3 nodos, A, B, y C, 
    con una arista de longitud igual a 1 de A a B, y una arista de longitud igual a 2 de A a C.
    Esto se puede establecer tambien de esta forma: g = Grafo({'A': {'B': 1, 'C': 2}, dirigido=False)
    Esto define un grafo no dirigido, por lo que si se agregan enlaces inversos, el grafo permanece sin dirigir;
    Si se desea agregar aristas de lo hace con g.connect('B', 'C', 3), entonces la arista inversa es tambien agregada.
    Se puede utilizar g.nodes() para obtener una lista de los nodos, g.get('A') para obtener un dict del enlace saliente de A,
    y g.get('A', 'B') para obtener la longitud de la arista desde A a B.  
    'Lengths', puede ser cualquier objeto, y los nodos pueden ser cualquier objeto hashable."""

    def __init__(self, graph_dict=None, dirigido=True):
        self.graph_dict = graph_dict or {}
        self.dirigido = dirigido
        if not dirigido:
            self.hacer_no_dirigido()

    def hacer_no_dirigido(self):
        """Hace un digrafo en un grafo no dirigido agregando aristas simetricas."""
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.connect1(b, a, dist)

    def connect(self, A, B, distancia=1):
        """Agrega una arista de A a B, dada una distancia,
        y tambien agrega la arista inversa si el grafo es no dirigido."""
        self.connect1(A, B, distancia)
        if not self.dirigido:
            self.connect1(B, A, distancia)

    def connect1(self, A, B, distancia):
        """Agrega una arista de A a B, dada una distancia, en una sola direccion."""
        self.graph_dict.setdefault(A, {})[B] = distancia

    def get(self, a, b=None):
        """Devuelve la distancia de una arista o un dict de entrada {node: distancia}.
        .get(a,b) devuelve la distancia o None;
        .get(a) devuelve un dict de entrada {node: distancia}, posibilidad {}."""
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    def nodes(self):
        """Devuelve un listado de los nodos en el grafico."""
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)


def UndirectedGraph(graph_dict=None):
    """Construye un grafo donde cada arista (incluidos los futuros) van en ambos direcciones."""
    return Grafo(graph_dict = graph_dict, dirigido=False)

class ProblemaGrafo(Problema):

    """Problema de busqueda de un nodo a otro nodo."""

    def __init__(self, estado_inicial, estado_objetivo, grafo):
        Problema.__init__(self, estado_inicial, estado_objetivo)
        self.grafo = grafo

    def acciones(self, A):
        """Las acciones en un nodo grafo son solo sus vecinas."""
        return list(self.grafo.get(A).keys())

    def result(self, estado, accion):
        """El resultado de ir a un vecino es solo ese vecino."""
        return accion

    def costo_camino(self, costo_actual, A, accion, B):
        return costo_actual + (self.grafo.get(A, B) or infinito)

    def encontrar_limite_minimo(self):
        """Encuentra el valor minimo de las aristas."""
        m = infinito
        for d in self.grafo.graph_dict.values():
            local_min = min(d.values())
            m = min(m, local_min)

        return m

    def h(self, node):
        """la funcion h es la distancia en linea recta de un nodo al nodo objetivo."""
        locs = getattr(self.grafo, 'locations', None)
        if locs:
            if type(node) is str:
                return int(distancia(locs[node], locs[self.estado_objetivo]))

            return int(distancia(locs[node.estado], locs[self.estado_objetivo]))
        else:
            return infinito

# ______________________________________________________________________________


class Nodo:

    """Un nodo en un árbol de búsqueda. Contiene un puntero al padre (el nodo del que es sucesor) y al estado real de este nodo. 
    Se debe tomar en cuenta que si se llega a un estado por dos caminos, entonces hay dos nodos con el mismo estado. 
    También incluye la accion que nos llevó a ese estado, y el total de costo_camino(también conocido como g) para llegar al nodo. 
    Otras funciones pueden agregar un valor f y h. No se necesita crear una subclase de esta clase."""

    def __init__(self, estado, padre = None, accion = None, costo_camino = 0):
        """Crea un nodo en un árbol de búsqueda a partir de un padre y una acción."""
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.costo_camino = costo_camino
        self.profundidad = 0
        if padre:
            self.profundidad = padre.profundidad + 1

    def __repr__(self):
        return "<Nodo {}>".format(self.estado)

    def __lt__(self, nodo):
        return self.estado < nodo.estado

    def expandir(self, problema):
        """Lista los nodos accesibles en un paso a partir de este nodo."""
        return [self.nodo_hijo(problema, accion)
                for accion in problema.acciones(self.estado)]

    def nodo_hijo(self, problema, accion):
        estado_siguiente = problema.resultado(self.estado, accion)
        nodo_siguiente = Nodo(estado_siguiente, self, accion,
                    problema.costo_camino(self.costo_camino, self.estado, accion, estado_siguiente))
        return nodo_siguiente
        
        siguiente = problema.resultado(self.estado, accion)
        return Nodo(siguiente, self, accion, problema.costo_camino(self.costo_camino, self.estado, accion, siguiente))

    def solucion(self):
        """Devuelce una secuencia de acciones para ir del nodo raiz al nodo actual."""
        return [nodo.accion for nodo in self.camino()[1:]]

    def camino(self):
        """Devuelve una lista de nodos que conforma el camino desde el nodo raiz al nodo actual."""
        nodo, camino_retorno = self, []
        while nodo:
            camino_retorno.append(nodo)
            nodo = nodo.padre
        return list(reversed(camino_retorno))

    #Para las busquedas primero en anchura y aestrella se requiere una cola de nodos sin duplicados,
    #por lo que tratamos los nodos con el mismo estado como iguales. 
    #[Problema: esto puede no ser lo que quieres en otros contextos.]"""

    def __eq__(self, otro):
        return isinstance(otro, Nodo) and self.estado == otro.estado

    def __hash__(self):
        return hash(self.estado)
# ______________________________________________________________________________

def busqueda_arbol(problema, frontera):
    """Busca entre los sucesores de un problema para encontrar un estado_objetivo. 
    El argumento frontera debe ser una columnaa vacía. 
    No hay que preocuparse por los caminos repetidos hacia un estado."""

    frontera.append(Nodo(problema.estado_inicial))
    while frontera:
        nodo = frontera.pop()
        if problema.es_objetivo(nodo.estado):
            return nodo
        frontera.extend(nodo.expandir(problema))
    return None


def busqueda_grafo(problema, frontera):
    """Busca entre los sucesores de un problema para encontrar un estado_objetivo.
    El argumento frontera debería ser una columnaa vacía.
    Si dos caminos alcanzan un estado, solo usa el primero."""
    frontera.append(Nodo(problema.estado_inicial))
    explorados = set()
    while frontera:
        nodo = frontera.pop()
        if problema.es_objetivo(nodo.estado):
            return nodo
        explorados.add(nodo.estado)
        frontera.extend(hijo for hijo in nodo.expandir(problema)
                        if hijo.estado not in explorados and
                        hijo not in frontera)
    return None

def busqueda_arbol_primero_anchura(problema):
    """Busca primero los nodos menos profundos en el árbol de búsqueda."""
    return busqueda_arbol(problema, FIFOQueue())

def busqueda_arbol_primero_profundidad(problema):
    """Busca primero los nodos más profundos en el árbol de búsqueda."""
    return busqueda_arbol(problema, Stack())

def busqueda_grafo_primero_profundidad(problema):
    """Busca primero los nodos más profundos en el grafo de búsqueda."""
    return busqueda_grafo(problema, Stack())

def busqueda_primero_anchura(problema):
    nodo = Nodo(problema.estado_inicial)
    if problema.es_objetivo(nodo.estado):
        return nodo
    frontera = FIFOQueue()
    frontera.append(nodo)
    explorados = set()
    while frontera:
        nodo = frontera.pop()
        explorados.add(nodo.estado)
        for hijo in nodo.expandir(problema):
            if hijo.estado not in explorados and hijo not in frontera:
                if problema.es_objetivo(hijo.estado):
                    return hijo
                frontera.append(hijo)
    return None

def busqueda_costo_uniforme(problema):
    return busqueda_grafo_primero_mejor(problema, lambda nodo: nodo.costo_camino)

def busqueda_profundidad_limitada(problema, limite=50):
    def recursivo_bpl(nodo, problema, limite):
        if problema.es_objetivo(nodo.estado):
            return nodo
        elif limite == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for hijo in nodo.expandir(problema):
                resultado = recursivo_bpl(hijo, problema, limite - 1)
                if resultado == 'cutoff':
                    cutoff_occurred = True
                elif resultado is not None:
                    return resultado
            return 'cutoff' if cutoff_occurred else None

    # cuerpo de busqueda en profundidad limitada:
    return recursivo_bpl(Nodo(problema.estado_inicial), problema, limite)


def busqueda_profundidad_iterativa(problema):
    for profundidad in range(sys.maxsize):
        resultado = busqueda_profundidad_limitada(problema, profundidad)
        if resultado != 'cutoff':
            return resultado

def busqueda_bidireccional(problema):
    e = problema.encontrar_limite_minimo()
    gF, gB = {problema.estado_inicial : 0}, {problema.estado_objetivo : 0}
    openF, openB = [problema.estado_inicial], [problema.estado_objetivo]
    closedF, closedB = [], []
    U = infinito


    def extend(U, open_dir, open_otro, g_dir, g_otro, closed_dir):
        """Amplia la busqueda en una direccion dada"""
        n = find_key(C, open_dir, g_dir)

        open_dir.remove(n)
        closed_dir.append(n)

        for c in problema.acciones(n):
            if c in open_dir or c in closed_dir:
                if g_dir[c] <= problema.costo_camino(g_dir[n], n, None, c):
                    continue

                open_dir.remove(c)

            g_dir[c] = problema.costo_camino(g_dir[n], n, None, c)
            open_dir.append(c)

            if c in open_otro:
                U = min(U, g_dir[c] + g_otro[c])

        return U, open_dir, closed_dir, g_dir


    def find_min(open_dir, g):
        """Encuentra la prioridad minima, valores g y f valors en open_dir"""
        m, m_f = infinito, infinito
        for n in open_dir:
            f = g[n] + problema.h(n)
            pr = max(f, 2*g[n])
            m = min(m, pr)
            m_f = min(m_f, f)

        return m, m_f, min(g.valors())


    def find_key(pr_min, open_dir, g):
        """Encuentra el valor de la en open_dir con un valor igual a pr_min y un valor minimo de g."""
        m = infinito
        estado = -1
        for n in open_dir:
            pr = max(g[n] + problema.h(n), 2*g[n])
            if pr == pr_min:
                if g[n] < m:
                    m = g[n]
                    estado = n

        return estado


    while openF and openB:
        pr_min_f, f_min_f, g_min_f = find_min(openF, gF)
        pr_min_b, f_min_b, g_min_b = find_min(openB, gB)
        C = min(pr_min_f, pr_min_b)

        if U <= max(C, f_min_f, f_min_b, g_min_f + g_min_b + e):
            return U

        if C == pr_min_f:
            # Ampliar hacia adelante
            U, openF, closedF, gF = extend(U, openF, openB, gF, gB, closedF)
        else:
            # Ampliar hacia atraz
            U, openB, closedB, gB = extend(U, openB, openF, gB, gF, closedB)

    return infinito

def busqueda_grafo_primero_mejor(problema, f):
    """Busca los nodos con las puntuaciones f más bajas primero. 
    Se especifica la función f (nodo) que desea minimizar; por ejemplo, 
    si f es una estimación heurística del estado_objetivo, entonces tenemos la mejor búsqueda codiciosa; 
    si f es nodo.profundidad, entonces tenemos una búsqueda de amplitud."""
    f = memoize(f, 'f')
    nodo = Nodo(problema.estado_inicial)
    if problema.es_objetivo(nodo.estado):
        return nodo
    frontera = PriorityQueue(min, f)
    frontera.append(nodo)
    explorados = set()
    while frontera:
        nodo = frontera.pop()
        if problema.es_objetivo(nodo.estado):
            return nodo
        explorados.add(nodo.estado)
        for hijo in nodo.expandir(problema):
            if hijo.estado not in explorados and hijo not in frontera:
                frontera.append(hijo)
            elif hijo in frontera:
                incumbent = frontera[hijo]
                if f(hijo) < f(incumbent):
                    del frontera[incumbent]
                    frontera.append(hijo)
    return None

# ______________________________________________________________________________

# Busquedas Informadas (Heuristicas)

busqueda_voraz = busqueda_grafo_primero_mejor
# voraz busqueda primero el mejor se logra especificando f(n) = h(n).


def busqueda_a_estrella(problema, h = None):
    """La busqueda A* es una busqueda en grafos primero el mejor con f(n) = g(n) + h(n).
    Se necesita especificar la funcion h cuando se llame a la funcion busqueda_a_estrella
    , o en su caso se debe definir en la subclase de la clase Problema."""
    h = memoize(h or problema.h, 'h')
    return busqueda_grafo_primero_mejor(problema, lambda n: n.costo_camino + h(n))

# ______________________________________________________________________________
# Otros algoritmos de busqueda

def busqueda_recursiva_primero_mejor(problema, h=None):
    """[Figure 3.26]"""
    h = memoize(h or problema.h, 'h')

    def RBFS(problema, nodo, flimite):
        if problema.es_objetivo(nodo.estado):
            return nodo, 0   # (El segundo valor es immaterial)
        successors = nodo.expandir(problema)
        if len(successors) == 0:
            return None, infinito
        for s in successors:
            s.f = max(s.costo_camino + h(s), nodo.f)
        while True:
            # Ordenar por el valor mas bajo de f
            successors.sort(key=lambda x: x.f)
            best = successors[0]
            if best.f > flimite:
                return None, best.f
            if len(successors) > 1:
                alternative = successors[1].f
            else:
                alternative = infinito
            resultado, best.f = RBFS(problema, best, min(flimite, alternative))
            if resultado is not None:
                return resultado, best.f

    nodo = Nodo(problema.estado_inicial)
    nodo.f = h(nodo)
    resultado, bestf = RBFS(problema, nodo, infinito)
    return resultado