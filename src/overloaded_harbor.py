import heapq
import queue
from rand_variables import gen_exp, gen_std_normal, gen_normal
import random

# problem constants for random vars:
t_arrival_lamda = 8

# items in this list will be saved using the sintax: (t, i)-> t: time, i:tanker ship arrival index
harbor_queue = queue.Queue()
docks_queue = []  # simulate queue using a heap
events_list = []  # save events using a list, Sort at the end.

t = 0  # simulation time

sta = 0  # small tanker ships arrives
mta = 0  # medium tanker ships arrives
bta = 0  # big tanker ships arrives

st = 0  # small tanker ships currently in the simulation
mt = 0  # medium tanker ships in the simulation
bt = 0  # big tanker ships in the simulation

i = 0  # last number of tanker arrived(fist tanker is 0)

dock_tankers = 0  # number of tanker ships in the docks

tb_pos = 0  # tug boat postition-> 0: on harbor, 1: at the docks

# list to register tankers data according to their arrival order
ts_size = []  # tamaño del barco -> 0: small,  1: medium, 2: big
ts_arrival = []  # hora de arribo al puerto
ts_route1_time = []  # tiempo que le tomo recorrer la Ruta1: puerto-muelle
# quizas guardar tambien la hora a la que arrivo al muelle para saber tiempo de espera en el muelle y en el puerto por separado
ts_loading_time = []  # tiempo que le tomo encargarse de la carga
ts_route2_time = []  # tiempo que le tomo recorrer la Ruta3: muelle-puerto
ts_departure = []  # hora de salida


# definir el tamaño del tanquero con prob 0.25 de que sea pequeño, 0.25 mediano y 0.50 grande
def define_tanker_size():
    u = random.random()
    if u < 0.25:
        return 0
    elif u >= 0.25 and u < 0.50:
        return 1
    else:
        return 2


# generar el tiempo de llegada del proximo tanque dada la hora de llegada del actual
def gen_tanker_ship_arrival(t):
    next_tanker_arrival = gen_exp(
        t_arrival_lamda
    )  # generar tiempo ahsta el prox arribo
    next_tanker_arrival += t  # definir hora de llegada del prox barco sumando el tiempo actual al que demora el arribo
    ts_arrival[i] = next_tanker_arrival
    ts_size[i] = define_tanker_size()  # definir el tamaño del barco
    i += 1
    harbor_queue.put((next_tanker_arrival, i))  # añadir barco a la cola del puerto


def take_tanker_to_dock():
    pass


def return_to_dock():
    pass


# atender puerto
def attend_harbor(t):
    if tb_pos == 0:  # if tugboat in harbor
        # if there are tankers awaiting in the harbor
        if not harbor_queue.empty() and harbor_queue[0][0] >= t:
            take_tanker_to_dock()
        # se puede preguntar directamente por dock_tankers == 3
        # if there are not free docks or there is a tanker waiting at the ducks
        elif dock_tankers == 3 or docks_queue.qsize() > 1:
            return_to_dock()


def return_tanker_to_harbor():
    pass


def return_to_harbor():
    pass


def wait_in_harbor():
    pass


# atender muelle
# attend pier or serve_dock
def attend_pier():
    if tb_pos == 1:  # if tugboat in the ducks
        pass


def run_simulation(sim_time):
    while t < sim_time:
        gen_tanker_ship_arrival(t)
        attend_harbor(t)
        attend_pier()
