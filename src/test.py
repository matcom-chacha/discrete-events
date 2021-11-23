import sys

from overloaded_harbor import Harbor_Simulator


def run_simulations(sim_time, number_s, creat_file):
    cum_delay = 0

    for i in range(number_s):
        if creat_file:
            simulator = Harbor_Simulator(
                [8, 2, 1, 0.25], [9, 12, 18], [1, 2, 3], st=sim_time, fn=str(i)
            )
        else:
            simulator = Harbor_Simulator(
                [8, 2, 1, 0.25], [9, 12, 18], [1, 2, 3], st=sim_time, createf=False
            )

        delay = simulator.run_simulation()
        cum_delay += delay

    print("Averiage delay time is: ", cum_delay / number_s)


if "__main__" == __name__:
    if len(sys.argv) > 4 or len(sys.argv) < 1:
        print(
            "Unnexpected number or arguments. Please provide sim_time(24), number_s(1000), creat_file(False)"
        )
    else:
        sim_time = 24
        number_s = 1000
        creat_file = False
        if len(sys.argv) == 2:
            _, sim_time = sys.argv
        elif len(sys.argv) == 3:
            _, sim_time, number_s = sys.argv
        elif len(sys.argv) == 4:
            _, sim_time, number_s, creat_file = sys.argv
            creat_file = True

        print("Starting ", number_s, "simulations of ", sim_time, " hours.")

        run_simulations(int(sim_time), int(number_s), creat_file)

