import math
import time

# Best First Search utilizar� la l�gica �ltima entrada, primera salida. De esa forma, vamos a seguir profundizando (verticalmente) antes de buscar estados horizontales.
def Solve_By_BestFS(n):
    # Declarar variables
    # Valores de cada clavija o pivote
    peg1_value = peg2_value = peg3_value = 0

    # Lista para almacenar los estados adyacentes
    state_COLLECTION = []

    # lista utilizada para guardar las acciones que hemos realizado hasta para cada elemento en la lista anterior, para que podamos rastrear. El tama�o de esta lista siempre ser� el mismo que el de otra lista de COLECCI�N
    steps_till_now_COLLECTION = []

    # Esta lista es para almacenar los estados que ya hemos encontrado, para que no entremos en un ciclo infinito
    past_states = []

    # variables temporales para almacenar los pasos para el estado de trabajo actual y el siguiente estado adyacente
    steps_till_current_state = steps_till_next_state = []

    # Variable temporal para almacenar el valor del disco que se mueve
    Value_of_Disk = 0

    # Variable temporal para almacenar el estado actual y el siguiente estado adyacente
    current_state = new_state = []

    # Variable temporal para almacenar el disco que se mueve
    disk_on_top = 0

    # Variables Booleanas
    state_found_before = solution_found = False

    # Encuentra el valor total de todos los discos en funci�n de n n�mero de discos
    Value_of_All_Disks = int(math.pow(2, n + 1)) - 2

    # Estado inicial donde todos los discos est�n en Peg1. Debido a que las listas est�n indexadas comenzando por 0, simplemente ignoraremos el �ndice 0.
    current_state = [0, Value_of_All_Disks, 0, 0]

    # Inserte el estado inicial en la lista COLECCI�N
    state_COLLECTION.append(current_state)
    steps_till_now_COLLECTION.append(steps_till_current_state)
    past_states.append(current_state)

    # Bucle hasta encontrar la soluci�n
    while solution_found == False and len(state_COLLECTION) > 0:
        # Obtenga el MEJOR estado en la pila
        best_item = - 1
        for item in range(0,len(state_COLLECTION)):
            state = state_COLLECTION[item]
            for d in range(n-1, 0, -1):
                partial_solution_val = math.pow(2, d+1)-2
                if ((n+d)%2 == 0):
                    partial_solution_peg = 3
                else:
                    partial_solution_peg = 2
                if (state[partial_solution_peg] == partial_solution_val):
                    best_item = item
                    break
            if (best_item > -1):
                break
        if best_item == -1:
            best_item = 0

        current_state = state_COLLECTION.pop(best_item)
        # Obtenga los pasos correspondientes en la l�gica de COLECCI�N
        steps_till_current_state = steps_till_now_COLLECTION.pop(best_item)
        # Bucle todas las clavijas para la fuente para el movimiento del disco
        for source_peg in range(3, 0, -1):
            # si la clavija no tiene disco a partir de ahora, pase a la siguiente clavija
            if (current_state[source_peg] == 0):
                continue
            # Bucle todas las clavijas para el destino para el movimiento del disco
            for dest_peg in range(3, 0, -1):
                # Source Peg y Dest Peg no pueden ser iguales
                if (solution_found == True or source_peg == dest_peg):
                    continue
                # Bucle para cada tama�o de disco de peque�o a grande
                for disk_size in range(1, n + 1):
                    Value_of_Disk = int(math.pow(2, disk_size))
                    # Utilizando el operador Y Bitwise, encuentre el disco en la parte superior de esta clavija de origen
                    if ((current_state[source_peg] & Value_of_Disk) == Value_of_Disk):
                        disk_on_top = disk_size
                        break
                # La clavija de destino debe estar vac�a o el disco superior debe ser m�s grande que el disco que se est� moviendo
                if (current_state[dest_peg] == 0 or current_state[dest_peg] % Value_of_Disk == 0):
                    # Los siguientes pasos mueven el disco de origen a destino y crean un nuevo estado fuera del estado actual
                    new_state = list(current_state)
                    new_state[source_peg] = new_state[source_peg] - Value_of_Disk
                    new_state[dest_peg] = new_state[dest_peg] + Value_of_Disk
                    next_step = [disk_on_top, source_peg, dest_peg]
                    steps_till_next_state = list(steps_till_current_state)
                    steps_till_next_state.append(next_step)
                    # Compruebe si el nuevo estado es la soluci�n final que estamos buscando (todos los discos en la clavija 3)
                    if (new_state[3] == Value_of_All_Disks):
                        steps = 1
                        output = ""
                        for aseq in steps_till_next_state:
                            output = output + str(steps) + ": Mover Disco " + str(aseq[0]) + " desde clavija " + str(
                                aseq[1]) + " a " + str(aseq[2]) + "\n"
                            steps = steps + 1
                        print(output)
                        solution_found = True
                        return
                    # else - todav�a no encontramos la soluci�n
                    else:
                        # aseg�rese de que el nuevo estado no se haya descubierto antes
                        state_found_before = False
                        for past_state in past_states:
                            if (past_state[1] == new_state[1] and past_state[2] == new_state[2] and past_state[3] ==
                                new_state[3]):
                                state_found_before = True
                                break
                        # si este es el nuevo estado que descubrimos antes, luego agr�guelo a las listas de COLECCI�N
                        if state_found_before == False:
                            state_COLLECTION.append(new_state)
                            steps_till_now_COLLECTION.append(steps_till_next_state)
                            past_states.append(new_state)
                            
if __name__ == "__main__":
    n = 5
    start_time=time.time()
    print ("Resolver por el mejor metodo de primera busqueda:")
    Solve_By_BestFS(n)
    tiempo_ejecucion=time.time()-start_time
    print("\nEl tiempo de ejecucion del laberinto es", round(tiempo_ejecucion,6)," segundos")


