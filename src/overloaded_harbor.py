import heapq
import queue
from rand_variables import gen_exp, gen_std_normal, gen_normal
import random

# problem constants for random vars:
t_arrival_lamda = 8  # tankers arrival lambda parameter
route1_lamda = 2  # route1 lambda parameter
route2_lamda = 1  # route2 lambda parameter
tb_route_lamda = 1  # tugboat solo route lambda parameter
cargo_med = [
    9,
    12,
    18,
]  # media parameter of cargo time distribution according to tanker size
cargo_var = [
    1,
    2,
    3,
]  # variance parameter of cargo time distribution according to tanker size


# items in this list will be saved using the sintax: (t, i)-> t: time, i:tanker ship arrival index
harbor_queue = queue.Queue()  # DEAL WITH NOT SUCRIPTABLE ERROR
docks_heap = []  # simulate queue using a heap
events_list = []  # save events using a list, Sort at the end.

t = 0  # simulation time

sta = 0  # small tanker ships arrives
mta = 0  # medium tanker ships arrives
bta = 0  # big tanker ships arrives

nt = 0  # tanker ships currently in the simulation

i = 0  # last number of tanker arrived(fist tanker is 0)

dock_tankers = 0  # number of tanker ships in the docks

tb_pos = 0  # tug boat postition-> 0: on harbor, 1: at the docks

# list to register tankers data according to their arrival order
ts_size = []  # tamaño del barco -> 0: small,  1: medium, 2: big
ts_arrival = []  # hora de arribo al puerto
ts_route1_time = []  # tiempo que le tomo recorrer la Ruta1: puerto-muelle
# quizas guardar tambien la hora a la que arrivo al muelle para saber tiempo de espera en el muelle y en el puerto por separado
ts_cargo_time = []  # tiempo que le tomo encargarse de la carga
ts_route2_time = []  # tiempo que le tomo recorrer la Ruta3: muelle-puerto
ts_departure = []  # hora de salida


# definir el tamaño del tanquero con prob 0.25 de que sea pequeño, 0.25 mediano y 0.50 grande
def define_tanker_size():
    # actualizar valores de tanques en simulacion (llevar los sizes como indices en un array para mapear mas facilmente)
    u = random.random()
    if u < 0.25:
        return 0
    elif u >= 0.25 and u < 0.50:
        return 1
    else:
        return 2


# generar el tiempo de llegada del proximo tanque dada la hora de llegada del actual
def gen_tanker_ship_arrival(ct):
    next_tanker_arrival = gen_exp(
        t_arrival_lamda
    )  # generar tiempo ahsta el prox arribo
    next_tanker_arrival += ct  # definir hora de llegada del prox barco sumando el tiempo actual al que demora el arribo
    ts_arrival[i] = next_tanker_arrival
    ts_size[i] = define_tanker_size()  # definir el tamaño del barco
    i += 1
    harbor_queue.put((next_tanker_arrival, i))  # añadir barco a la cola del puerto


def gen_cargo_time(s):
    cargo_time = gen_normal(cargo_med[s], cargo_var[s])


def take_tanker_to_dock():  # una idea para cambiar la lista es no llevarla y tener un indice del utlimo barco esperando en puerto
    (
        tanker_ship_at,
        tanker_ship_at_index,
    ) = harbor_queue.get()  # get first tanker awaiting at the harbor
    gen_tanker_ship_arrival(tanker_ship_at)  # generate next arrival
    r1_time = gen_exp(route1_lamda)  # generate route 1 time for this tanker
    ts_route1_time[tanker_ship_at_index] = r1_time
    t += r1_time  # update current simulation time
    cargo_time = gen_cargo_time(
        ts_size[tanker_ship_at_index]
    )  # generate cargo time for the tanker
    ts_cargo_time[tanker_ship_at_index] = cargo_time
    heapq.heappush(
        docks_heap, (t + cargo_time, tanker_ship_at_index)
    )  # add event to dock's heap
    dock_tankers += 1  # update number of tankers in docks
    tb_pos = 1  # update tugBoat position


def cross_solo():
    solo_route_time = gen_exp(tb_route_lamda)  # generate route time for tugBoat
    t += solo_route_time  # update current simulation time
    tb_pos = abs(tb_pos - 1)  # toggle tugBoat position


def wait():
    if not harbor_queue.empty():  # take next arrival time
        next_at = harbor_queue[0][0]
    else:
        next_at = 1000

    if docks_heap.qsize() > 0:  # take next tanker to finished with cargo
        next_cargo_ft = docks_heap[0][0]
    else:
        next_cargo_ft = 1000

    t = min(next_at, next_cargo_ft)  # update current simulation time


# atender puerto
def attend_harbor(t):
    if tb_pos == 0:  # if tugboat in harbor
        # if there are tankers awaiting in the harbor and there are free docks
        if not harbor_queue.empty() and harbor_queue[0][0] <= t and dock_tankers < 3:
            take_tanker_to_dock()
        # if there are not free docks or there is a tanker waiting at the docks
        elif dock_tankers == 3 or (docks_heap.qsize() > 0 and docks_heap[0][0] <= t):
            cross_solo()  # return_to_dock
        # fi there is no action to attend wait for next boat to arrive? o lo que dice abajo
        else:
            wait()  # in_harbor()  # hasta el proximo evento min(llegada de barco a puerto, bote listo en muelle)


def return_tanker_to_harbor():
    tanker_cargo_ft, tanker_ship_at_index = heapq.heappop(
        docks_heap
    )  # get tanker ready to leave
    r2_time = gen_exp(route2_lamda)  # generate route 2 time for this tanker
    ts_route2_time[tanker_ship_at_index] = r2_time
    t += r2_time  # update current simulation time
    ts_departure = t  # update departure time for current tanker
    dock_tankers -= 1  # update number of tankers in ducks
    tb_pos = 0  # update tugBoat position to harbor


# atender muelle
# attend pier or serve_dock
def attend_pier():
    if tb_pos == 1:  # if tugboat in the ducks
        # if there is a tanker ready to go back to the harbor
        if docks_heap.qsize() > 0 and docks_heap[0][0] <= t:
            return_tanker_to_harbor()
        # there are free docks and at least a tanker waiting at the harbor
        elif dock_tankers < 3 and (
            not harbor_queue.empty() and harbor_queue[0][0] <= t
        ):
            cross_solo()  # return_to_harbor
        # fi there is no action to attend wait for next boat to finish with cargo? o lo que dice abajo
        else:
            wait()  # in_duck # hasta el proximo evento min(llegada de barco a puerto, bote listo en muelle)


def run_simulation(sim_time):
    while t < sim_time:
        gen_tanker_ship_arrival(t)
        attend_harbor(t)
        attend_pier()


# al final añSadir a la lista de eventos los tanqueros que llegaron y no frueron atendidos.
# Decir que su tiempo de espera es mayor que el tiempo de llegada hasta el final?

# update number of tankers in simulation and st, mt and bt

