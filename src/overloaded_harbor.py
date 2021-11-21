import heapq
import queue
from rand_variables import gen_exp, gen_normal

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

dock_tankers = 0  # number of tanker ships in the docks

# list to register tankers data according to their arrival order
ts_type = []
ts_arrival = []  # hora de arribo al puerto
ts_route1_time = []  # tiempo que le tomo recorrer la Ruta1: puerto-muelle
# quizas guardar tambien la hora a la que arrivo al muelle para saber tiempo de espera en el muelle y en el puerto por separado
ts_loading_time = []  # tiempo que le tomo encargarse de la carga
ts_route2_time = []  # tiempo que le tomo recorrer la Ruta3: muelle-puerto
ts_departure = []  # hora de salida

# generar el tiempo de llegada del proximo tanque dada la hora de llegada del actual
def gen_tanker_ship_arrival(t):
    pass


# atender puerto
def attend_harbor():
    pass


# atender muelle
# attend pier or serve_dock
def attend_pier():
    pass


def run_simulation(t):
    pass
