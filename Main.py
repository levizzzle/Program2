# knapsack_annealing.py
# using classical simulated annealing
# Python 3.7.6 (Anaconda3 2020.02)

# items  0  1  2  3  4  5  6  7  8  9
# values 79 32 47 18 26 85 33 40 45 59
# sizes 85 26 48 21 22 95 43 45 55 52
# max size = 101

# maximize value

import numpy as np

def get_item_useful_weight():
    text_file = open("Program2Input.txt", "r")
    data = text_file.readline()
    text_file.close()
    print(data)

def total_useful_weight(cargo, useful, weights, max_size):
    # total usefulness and weight of a specified item
    usefulness = 0.0  # total usefulness of cargo
    weight = 0.0  # total weight of cargo
    n = len(cargo)
    for i in range(n):
        if cargo[i] == 1:
            usefulness += useful[i]
            weight += weights[i]
    if weight > max_size:  # too heavy to fit in vehicle
        usefulness = 0.0
    return (usefulness, weight)


def adjacent(cargo, rnd):
    numItems = len(cargo)
    result = np.copy(cargo)
    index = rnd.randint(numItems)
    if result[index] == 0:
        result[index] = 1
    elif result[index] == 1:
        result[index] = 0
    return result


def solve(n_items, rnd, values, sizes, max_size, max_iter, start_temperature, alpha):
    # solve using simulated annealing
    curr_temperature = start_temperature
    curr_cargo = np.ones(n_items, dtype=np.int64)
    print("Initial guess: ")
    print(curr_cargo)

    (curr_valu, curr_size) = total_useful_weight(curr_cargo, values, sizes, max_size)
    iteration = 0
    interval = (int)(max_iter / 10)
    while iteration < max_iter:
        # pct_iters_left = \
        #  (max_iter - iteration) / (max_iter * 1.0)
        adj_cargo = adjacent(curr_cargo, rnd)
        (adj_v, _) = total_useful_weight(adj_cargo, values, sizes, max_size)

        if adj_v > curr_valu:  # better so accept adjacent
            curr_cargo = adj_cargo;
            curr_valu = adj_v
        else:  # adjacent cargo is worse
            accept_p = np.exp((adj_v - curr_valu) / curr_temperature)
            p = rnd.random()
            if p < accept_p:  # accept worse cargo anyway
                curr_cargo = adj_cargo;
                curr_valu = adj_v
                # else don't accept

        if iteration % interval == 0:
            print("iter = %6d : curr value = %7.0f : \
        curr temp = %10.2f " % (iteration, curr_valu, curr_temperature))

        if curr_temperature < 0.00001:
            curr_temperature = 0.00001
        else:
            curr_temperature *= alpha
            # curr_temperature = start_temperature * \
            # pct_iters_left * 0.0050
        iteration += 1

    return curr_cargo


def main():
    print("\nBegin knapsack simulated annealing demo ")
    print("Goal is to maximize value subject \
    to max size constraint ")

    values = np.array([79, 32, 47, 18, 26, 85, 33, 40, 45, 59])
    sizes = np.array([85, 26, 48, 21, 22, 95, 43, 45, 55, 52])
    max_size = 101

    print("\nItem values: ")
    print(values)
    print("\nItem sizes: ")
    print(sizes)
    print("\nMax total size = %d " % max_size)

    rnd = np.random.RandomState(5)  # 3 .98 = 117,100
    max_iter = 1000
    start_temperature = 10000.0
    alpha = 0.98

    print("\nSettings: ")
    print("max_iter = %d " % max_iter)
    print("start_temperature = %0.1f " % start_temperature)
    print("alpha = %0.2f " % alpha)

    print("\nStarting solve() ")
    cargo = solve(10, rnd, values, sizes, max_size, max_iter, start_temperature, alpha)
    print("Finished solve() ")

    print("\nBest cargo found: ")
    print(cargo)
    (v, s) = total_useful_weight(cargo, values, sizes, max_size)
    print("\nTotal value of packing = %0.1f " % v)
    print("Total size  of packing = %0.1f " % s)

    print("\nEnd demo ")

    get_item_useful_weight()


if __name__ == "__main__":
    main()
