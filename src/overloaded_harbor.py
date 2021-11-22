import heapq
import queue
import random
import sys
from rand_variables import gen_exp, gen_normal
from utils import create_file, edit_file, write_data

name = 0
sim_time = 24
max_t = sys.maxsize
# problem constants for random vars:
t_arrival_lamda = 8  # tankers arrival lambda parameter
route1_lamda = 2  # route1 lambda parameter
route2_lamda = 1  # route2 lambda parameter
tb_route_lamda = 0.25  # tugboat solo route lambda parameter
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
# harbor_queue = queue.Queue()  # TO DEAL WITH NOT SUCRIPTABLE ERROR use a heap
harbor_queue = (
    []
)  # se puede prescindir de esta con un indice referenciando al proximo tanquero
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
    global sta, mta, bta
    # actualizar valores de tanques en simulacion
    u = random.random()
    if u < 0.25:
        sta += 1
        return 0
    elif u >= 0.25 and u < 0.50:
        mta += 1
        return 1
    else:
        bta += 1
        return 2


def initialize_arrays_site_for_new_tanker():
    global ts_size, ts_arrival, ts_route1_time, ts_cargo_time, ts_route2_time, ts_departure

    ts_size.append(-1)
    ts_arrival.append(-1)
    ts_route1_time.append(-1)
    ts_cargo_time.append(-1)
    ts_route2_time.append(-1)
    ts_departure.append(-1)


# generar el tiempo de llegada del proximo tanque dada la hora de llegada del actual
def gen_tanker_ship_arrival(ct, late_gen=False):
    global t_arrival_lamda, i, ts_arrival, ts_size, harbor_queue, nt, t
    next_tanker_arrival = gen_exp(
        1 / t_arrival_lamda
    )  # generar tiempo hasta el prox arribo

    next_tanker_arrival += ct  # definir hora de llegada del prox barco sumando el tiempo actual al que demora el arribo
    if next_tanker_arrival <= sim_time:
        if late_gen and next_tanker_arrival < t:
            return
        initialize_arrays_site_for_new_tanker()
        ts_arrival[i] = next_tanker_arrival
        ts_size[i] = define_tanker_size()  # definir el tamaño del barco
        nt += 1  # update tankers in simulation
        heapq.heappush(
            harbor_queue, (next_tanker_arrival, i)
        )  # añadir barco a la cola del puerto
        i += 1  # update last tanker index


# generate cargo time for a tanker of a given size s
def gen_cargo_time(s):
    cargo_time = gen_normal(cargo_med[s], cargo_var[s])
    return cargo_time


# togBoat takes first tanker waiting in harbor to the docks
def take_tanker_to_dock():
    global harbor_queue, ts_route1_time, t, ts_cargo_time, docks_heap, dock_tankers, tb_pos
    (tanker_ship_atime, tanker_ship_index) = heapq.heappop(
        harbor_queue
    )  # get first tanker awaiting at the harbor
    edit_file(
        name,
        str(t)
        + ":"
        + " tugBoat picks tanker #"
        + str(tanker_ship_index)
        + " who arrived at "
        + str(tanker_ship_atime),
    )

    gen_tanker_ship_arrival(tanker_ship_atime)  # generate next arrival

    r1_time = gen_exp(1 / route1_lamda)  # generate route 1 time for this tanker
    ts_route1_time[tanker_ship_index] = r1_time
    t += r1_time  # update current simulation time
    edit_file(
        name,
        str(t)
        + ":"
        + " tugBoat leaves tanker #"
        + str(tanker_ship_index)
        + " in the ducks",
    )
    cargo_time = gen_cargo_time(
        ts_size[tanker_ship_index]
    )  # generate cargo time for the tanker
    ts_cargo_time[tanker_ship_index] = cargo_time
    heapq.heappush(
        docks_heap, (t + cargo_time, tanker_ship_index)
    )  # add event to dock's heap
    dock_tankers += 1  # update number of tankers in docks
    tb_pos = 1  # update tugBoat position


# tugBoat cross to the other side of the bay
def cross_solo():
    global tb_pos, t, tb_route_lamda
    solo_route_time = gen_exp(1 / tb_route_lamda)  # generate route time for tugBoat
    edit_file(name, str(t) + ":" + " tugBoat leaves " + str(tb_pos) + " solo")
    t += solo_route_time  # update current simulation time
    tb_pos = abs(tb_pos - 1)  # toggle tugBoat position
    edit_file(name, str(t) + ":" + " tugBoat gets to " + str(tb_pos) + " solo")


# tugBoat waits for next tanker arrival or a tanker that finishes with cargo
def wait():
    global harbor_queue, docks_heap, t

    if len(harbor_queue) > 0:
        narrival = harbor_queue[0]
    else:
        narrival = -1
    if len(docks_heap) > 0:
        ncargof = docks_heap[0]
    else:
        ncargof = -1

    edit_file(
        name,
        str(t)
        + ": "
        + str(len(harbor_queue))
        + " tanker(s) on the harbor. "
        + str(dock_tankers)
        + " on the docks. Next arrival: "
        + str(narrival)
        + ". Next tanker to finish loading: "
        + str(ncargof),
    )

    edit_file(
        name, str(t) + ":" + " tugBoat has nothing to do. Let's wait in " + str(tb_pos)
    )
    if len(harbor_queue) > 0:  # take next arrival time
        next_at = harbor_queue[0][0]
    else:
        next_at = max_t

    if tb_pos == 1 and dock_tankers == 3:
        next_at = max_t

    if len(docks_heap) > 0:  # take next tanker to finished with cargo
        next_cargo_ft = docks_heap[0][0]
    else:
        next_cargo_ft = max_t

    m = min(next_at, next_cargo_ft)
    if m != max_t:  # if there is an event waiting
        t = m  # update current simulation time
    edit_file(name, str(t) + ":" + " tugBoat ready to work.")


# atender puerto
def attend_harbor():
    global tb_pos, harbor_queue, dock_tankers, docks_heap
    if tb_pos == 0:  # if tugboat in harbor
        # if there are tankers awaiting in the harbor and there are free docks
        if len(harbor_queue) > 0 and harbor_queue[0][0] <= t and dock_tankers < 3:
            take_tanker_to_dock()
        # if there are not free docks or there is a tanker waiting at the docks
        elif dock_tankers == 3 or (len(docks_heap) > 0 and docks_heap[0][0] <= t):
            cross_solo()  # return_to_dock
        # if there is no action to attend wait for next boat to arrive? o lo que dice abajo
        else:
            wait()  # in_harbor()  # hasta el proximo evento min(llegada de barco a puerto, bote listo en muelle)


# return the first tanker that has completed the cicle to harbor
def return_tanker_to_harbor():
    global docks_heap, route2_lamda, ts_route2_time, t, ts_departure, dock_tankers, tb_pos, nt
    tanker_cargo_ft, tanker_ship_index = heapq.heappop(
        docks_heap
    )  # get first tanker ready to leave
    edit_file(
        name,
        str(t)
        + ":"
        + " tugBoat picks tanker #"
        + str(tanker_ship_index)
        + ", who spend "
        + str(ts_cargo_time[tanker_ship_index])
        + " hours loading from the docks",
    )
    r2_time = gen_exp(1 / route2_lamda)  # generate route 2 time for this tanker
    ts_route2_time[tanker_ship_index] = r2_time
    t += r2_time  # update current simulation time
    ts_departure[tanker_ship_index] = t  # update departure time for current tanker
    edit_file(
        name,
        str(t)
        + ":"
        + " tugBoat says gb to tanker #"
        + str(tanker_ship_index)
        + " at the harbor",
    )
    dock_tankers -= 1  # update number of tankers in ducks
    tb_pos = 0  # update tugBoat position to harbor
    nt -= 1  # update number of tankers in the simulation


# atender muelle or serve_dock
def attend_pier():
    global tb_pos, docks_heap, dock_tankers, harbor_queue, t
    if tb_pos == 1:  # if tugboat in the ducks
        # if there is a tanker ready to go back to the harbor
        if len(docks_heap) > 0 and docks_heap[0][0] <= t:
            return_tanker_to_harbor()
        # there are free docks and at least a tanker waiting at the harbor
        elif dock_tankers < 3 and (len(harbor_queue) > 0 and harbor_queue[0][0] <= t):
            cross_solo()  # return_to_harbor
        # if there is no action to attend wait for next boat to finish with cargo? o lo que dice abajo
        else:
            wait()  # in_duck # hasta el proximo evento min(llegada de barco a puerto, bote listo en muelle)


# calculate values required for the problem
def get_stadistics():
    global ts_departure, ts_arrival, i, nt
    # arreglar si finalmente se espera que todos los barcos salgan del puerto
    delay = [ts_departure[x] - ts_arrival[x] for x in range(i)]
    delay_media = sum(delay) / len(delay)
    print("The average waiting time for the tankers is:", delay_media)
    return delay_media


# run harbor simualtion
def run_simulation(hours, fname):
    global t, sim_time, name
    name = fname
    sim_time = hours
    create_file(name, sim_time, "", True)
    gen_tanker_ship_arrival(t)
    while t < sim_time or nt > 0:
        if t < sim_time and nt == 0:
            gen_tanker_ship_arrival(ts_arrival[i - 1], True)
        attend_harbor()
        attend_pier()
    delay = get_stadistics()
    write_data(
        name,
        [
            "\n",
            "------------------------------------------------------------------------------",
            "Stadistics:",
            "Total arrivals: " + str(i),
            "small tankers arrivals: " + str(sta),
            "medium tankers arrivals: " + str(mta),
            "big tankers arrivals: " + str(bta),
            "ts_size: " + str(ts_size),
            "ts_arrival: " + str(ts_arrival),
            "ts_route1_time: " + str(ts_route1_time),
            "ts_cargo_time: " + str(ts_cargo_time),
            "ts_route2_time" + str(ts_route2_time),
            "ts_departure: " + str(ts_departure),
            "average delay: " + str(delay),
        ],
    )


if "__main__" == __name__:
    if len(sys.argv) > 3:
        print("Unnexpected number or arguments")
    else:
        if len(sys.argv) == 2:
            _, name = sys.argv
            hours = 24
        else:
            _, hours, name = sys.argv
        print("Starting simulation ", name, " with ", hours, " hours")
        run_simulation(int(hours), name)
