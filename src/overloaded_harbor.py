import heapq
import queue
import random
import sys
from rand_variables import gen_exp, gen_normal
from utils import create_file, edit_file, write_data


class Harbor_Simulator:
    def __init__(
        self, lambda_vals, cargo_med_vals, cargo_var_vals, st=24, fn=0, createf=True
    ):
        self.max_t = sys.maxsize
        self.sim_time = st  # simulation time
        self.name = fn  # name of a file to write simulation info
        self.createf = createf  # Write results in a file

        # problem constants for random vars:
        self.t_arrival_lamda = lambda_vals[0]  # tankers arrival lambda parameter
        self.route1_lamda = lambda_vals[1]  # route1 lambda parameter
        self.route2_lamda = lambda_vals[2]  # route2 lambda parameter
        self.tb_route_lamda = lambda_vals[3]  # tugboat solo route lambda parameter
        self.cargo_med = cargo_med_vals  # media parameter of cargo time distribution according to tanker size
        self.cargo_var = cargo_var_vals  # variance parameter of cargo time distribution according to tanker size

        # items in this list will be saved using the sintax: (t, i)-> t: time, i:tanker ship arrival index
        self.harbor_queue = []
        self.docks_heap = []  # simulate queue using a heap
        # self.events_list = []  # save events using a list, Sort at the end.

        self.t = 0  # simulation time

        self.sta = 0  # small tanker ships arrives
        self.mta = 0  # medium tanker ships arrives
        self.bta = 0  # big tanker ships arrives

        self.nt = 0  # tanker ships currently in the simulation

        self.i = 0  # last number of tanker arrived(fist tanker is 0)

        self.dock_tankers = 0  # number of tanker ships in the docks

        self.tb_pos = 0  # tug boat postition-> 0: on harbor, 1: at the docks

        # list to register tankers data according to their arrival order
        self.ts_size = []  # tanker size -> 0: small,  1: medium, 2: big
        self.ts_arrival = []  # tanker arrival
        self.ts_route1_time = []  # tanker's route1 time Route1: harbor->dock
        self.ts_cargo_time = []  # tanker's cargo time
        self.ts_route2_time = []  # tanker's route1 time Route2: dock->harbor
        self.ts_departure = []  # tankers departure

    # define tanker size with o.25 prob of being small, 0.25 medium and 0.50 big
    def define_tanker_size(self):
        u = random.random()
        if u < 0.25:
            self.sta += 1
            return 0
        elif u >= 0.25 and u < 0.50:
            self.mta += 1
            return 1
        else:
            self.bta += 1
            return 2

    # initialize values for a given tanker
    def initialize_arrays_site_for_new_tanker(self):
        self.ts_size.append(-1)
        self.ts_arrival.append(-1)
        self.ts_route1_time.append(-1)
        self.ts_cargo_time.append(-1)
        self.ts_route2_time.append(-1)
        self.ts_departure.append(-1)

    # generate arrival of next tanker
    def gen_tanker_ship_arrival(self, ct, late_gen=False):
        next_tanker_arrival = gen_exp(
            1 / self.t_arrival_lamda
        )  # gen interval time until next arrival

        next_tanker_arrival += ct  # add stimated time to current one
        if next_tanker_arrival <= self.sim_time:
            if late_gen and next_tanker_arrival < self.t:
                return
            self.initialize_arrays_site_for_new_tanker()
            self.ts_arrival[self.i] = next_tanker_arrival
            self.ts_size[self.i] = self.define_tanker_size()  # define new tanker's size
            self.nt += 1  # update tankers in simulation
            heapq.heappush(
                self.harbor_queue, (next_tanker_arrival, self.i)
            )  # add tanker to harbor's queue
            self.i += 1  # update last tanker index

    # generate cargo time for a tanker of a given size s
    def gen_cargo_time(self, s):
        cargo_time = gen_normal(self.cargo_med[s], self.cargo_var[s])
        return cargo_time

    # togBoat takes first tanker waiting in harbor to the docks
    def take_tanker_to_dock(self):
        (tanker_ship_atime, tanker_ship_index) = heapq.heappop(
            self.harbor_queue
        )  # get first tanker awaiting at the harbor

        if self.createf:
            edit_file(
                self.name,
                str(self.t)
                + ":"
                + " tugBoat picks tanker #"
                + str(tanker_ship_index)
                + " who arrived at "
                + str(tanker_ship_atime),
            )

        self.gen_tanker_ship_arrival(tanker_ship_atime)  # generate next arrival

        r1_time = gen_exp(
            1 / self.route1_lamda
        )  # generate route 1 time for this tanker
        self.ts_route1_time[tanker_ship_index] = r1_time
        self.t += r1_time  # update current simulation time

        if self.createf:
            edit_file(
                self.name,
                str(self.t)
                + ":"
                + " tugBoat leaves tanker #"
                + str(tanker_ship_index)
                + " in the ducks",
            )

        cargo_time = self.gen_cargo_time(
            self.ts_size[tanker_ship_index]
        )  # generate cargo time for the tanker
        self.ts_cargo_time[tanker_ship_index] = cargo_time
        heapq.heappush(
            self.docks_heap, (self.t + cargo_time, tanker_ship_index)
        )  # add event to dock's heap
        self.dock_tankers += 1  # update number of tankers in docks
        self.tb_pos = 1  # update tugBoat position

    # tugBoat cross to the other side of the bay
    def cross_solo(self):
        solo_route_time = gen_exp(
            1 / self.tb_route_lamda
        )  # generate route time for tugBoat

        if self.createf:
            edit_file(
                self.name,
                str(self.t) + ":" + " tugBoat leaves " + str(self.tb_pos) + " solo",
            )

        self.t += solo_route_time  # update current simulation time
        self.tb_pos = abs(self.tb_pos - 1)  # toggle tugBoat position

        if self.createf:
            edit_file(
                self.name,
                str(self.t) + ":" + " tugBoat gets to " + str(self.tb_pos) + " solo",
            )

    # tugBoat waits for next tanker arrival or a tanker that finishes with cargo
    def wait(self):
        if len(self.harbor_queue) > 0:  # take next arrival time
            next_at = self.harbor_queue[0][0]
            narrival = self.harbor_queue[0]
        else:
            next_at = self.max_t
            narrival = -1

        if self.tb_pos == 1 and self.dock_tankers == 3:
            next_at = self.max_t

        if len(self.docks_heap) > 0:  # take next tanker to finished with cargo
            next_cargo_ft = self.docks_heap[0][0]
            ncargof = self.docks_heap[0]
        else:
            next_cargo_ft = self.max_t
            ncargof = -1

        if self.createf:
            edit_file(
                self.name,
                str(self.t)
                + ": "
                + str(len(self.harbor_queue))
                + " tanker(s) on the harbor. "
                + str(self.dock_tankers)
                + " on the docks. Next arrival: "
                + str(narrival)
                + ". Next tanker to finish loading: "
                + str(ncargof),
            )

            edit_file(
                self.name,
                str(self.t)
                + ":"
                + " tugBoat has nothing to do. Let's wait in "
                + str(self.tb_pos),
            )

        m = min(next_at, next_cargo_ft)
        if m != self.max_t:  # if there is an event waiting
            self.t = m  # update current simulation time

        if self.createf:
            edit_file(self.name, str(self.t) + ":" + " tugBoat ready to work.")

    # atender puerto
    def attend_harbor(self):
        if self.tb_pos == 0:  # if tugboat in harbor
            # if there are tankers awaiting in the harbor and there are free docks
            if (
                len(self.harbor_queue) > 0
                and self.harbor_queue[0][0] <= self.t
                and self.dock_tankers < 3
            ):
                self.take_tanker_to_dock()
            # if there are not free docks or there is a tanker waiting at the docks
            elif self.dock_tankers == 3 or (
                len(self.docks_heap) > 0 and self.docks_heap[0][0] <= self.t
            ):
                self.cross_solo()  # return_to_dock
            # if there is no action to attend wait for next event
            else:
                self.wait()  # in_harbor()

    # return the first tanker that has completed the cicle to harbor
    def return_tanker_to_harbor(self):
        tanker_cargo_ft, tanker_ship_index = heapq.heappop(
            self.docks_heap
        )  # get first tanker ready to leave

        if self.createf:
            edit_file(
                self.name,
                str(self.t)
                + ":"
                + " tugBoat picks tanker #"
                + str(tanker_ship_index)
                + ", who spend "
                + str(self.ts_cargo_time[tanker_ship_index])
                + " hours loading from the docks",
            )

        r2_time = gen_exp(
            1 / self.route2_lamda
        )  # generate route 2 time for this tanker
        self.ts_route2_time[tanker_ship_index] = r2_time
        self.t += r2_time  # update current simulation time
        self.ts_departure[
            tanker_ship_index
        ] = self.t  # update departure time for current tanker

        if self.createf:
            edit_file(
                self.name,
                str(self.t)
                + ":"
                + " tugBoat says gb to tanker #"
                + str(tanker_ship_index)
                + " at the harbor",
            )
        self.dock_tankers -= 1  # update number of tankers in ducks
        self.tb_pos = 0  # update tugBoat position to harbor
        self.nt -= 1  # update number of tankers in the simulation

    # serve_dock
    def attend_pier(self):
        if self.tb_pos == 1:  # if tugboat in the ducks
            # if there is a tanker ready to go back to the harbor
            if len(self.docks_heap) > 0 and self.docks_heap[0][0] <= self.t:
                self.return_tanker_to_harbor()
            # there are no free docks || there are free docks and at least a tanker waiting at the harbor
            elif self.dock_tankers == 0 or (
                self.dock_tankers < 3
                and (len(self.harbor_queue) > 0 and self.harbor_queue[0][0] <= self.t)
            ):
                self.cross_solo()  # return_to_harbor
            # if there is no action to attend wait for next event
            else:
                self.wait()  # in_duck

    # calculate values required for the problem
    def get_stadistics(self):
        delay = [self.ts_departure[x] - self.ts_arrival[x] for x in range(self.i)]
        delay_media = sum(delay) / len(delay)
        return delay_media

    # run harbor simualtion
    def run_simulation(self):
        if self.createf:
            create_file(self.name, self.sim_time, "", True)

        self.gen_tanker_ship_arrival(self.t)
        while self.t < self.sim_time or self.nt > 0:
            if self.t < self.sim_time and self.nt == 0:  # generate extra tanker if none
                if self.i > 0:
                    pt = self.ts_arrival[self.i - 1]
                else:
                    pt = self.t
                self.gen_tanker_ship_arrival(pt, True)
            self.attend_harbor()
            self.attend_pier()

        delay = self.get_stadistics()

        if self.createf:
            write_data(
                self.name,
                [
                    "\n",
                    "------------------------------------------------------------------------------",
                    "Stadistics:",
                    "Total arrivals: " + str(self.i),
                    "small tankers arrivals: " + str(self.sta),
                    "medium tankers arrivals: " + str(self.mta),
                    "big tankers arrivals: " + str(self.bta),
                    "ts_size: " + str(self.ts_size),
                    "ts_arrival: " + str(self.ts_arrival),
                    "ts_route1_time: " + str(self.ts_route1_time),
                    "ts_cargo_time: " + str(self.ts_cargo_time),
                    "ts_route2_time" + str(self.ts_route2_time),
                    "ts_departure: " + str(self.ts_departure),
                    "average delay: " + str(delay),
                ],
            )

        return delay
