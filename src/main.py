from overloaded_harbor import Harbor_Simulator

simulator = Harbor_Simulator([8, 2, 1, 0.25], [9, 12, 18], [1, 2, 3], "50", 24)

# Values used for the problem
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
# fn: file name 0
# st: simulation time 24


# if "__main__" == __name__:
#     if len(sys.argv) > 3:
#         print("Unnexpected number or arguments")
#     else:
#         if len(sys.argv) == 2:
#             _, name = sys.argv
#             hours = 24
#         else:
#             _, hours, name = sys.argv
#         print("Starting simulation ", name, " with ", hours, " hours")
#         simulator = Harbor_Simulator(
#             [8, 2, 1, 0.25], [9, 12, 18], [1, 2, 3], name, int(hours)
#         )

#         # run_simulation(int(hours), name)
