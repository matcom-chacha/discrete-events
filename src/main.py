import sys
from overloaded_harbor import Harbor_Simulator

# Default values for the problem
# t_arrival_lamda = 8  # tankers arrival lambda parameter
# route1_lamda = 2  # route1 lambda parameter
# route2_lamda = 1  # route2 lambda parameter
# tb_route_lamda = 0.25  # tugboat solo route lambda parameter
# cargo_med = [
#     9,
#     12,
#     18,
# ]  # media parameter of cargo time distribution according to tanker size
# cargo_var = [
#     1,
#     2,
#     3,
# ]  # variance parameter of cargo time distribution according to tanker size
# st: simulation time 24


def run_simulation(sim_time, file_name, creat_file):

    if creat_file:
        simulator = Harbor_Simulator(
            [8, 2, 1, 0.25], [9, 12, 18], [1, 2, 3], st=sim_time, fn=file_name
        )
    else:
        simulator = Harbor_Simulator(
            [8, 2, 1, 0.25], [9, 12, 18], [1, 2, 3], st=sim_time, createf=False
        )

    delay = simulator.run_simulation()
    print("Averiage delay time is: ", delay)


if "__main__" == __name__:
    if len(sys.argv) > 3 or len(sys.argv) < 1:
        print(
            "Unnexpected number or arguments. Please provide sim_time(24), file_name(0)"
        )
    else:
        sim_time = 24
        file_name = 0
        creat_file = False
        if len(sys.argv) == 2:
            _, sim_time = sys.argv
        elif len(sys.argv) == 3:
            _, sim_time, file_name = sys.argv
            creat_file = True

        print("Starting simulations of ", sim_time, " hours")

        if creat_file:
            print("Writing to file ", file_name)

        run_simulation(int(sim_time), file_name, creat_file)

