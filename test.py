import numpy as np
adj_utility = 500
curr_utility = 450
curr_temperature = 100
rnd = np.random.RandomState(5)  # 3 .98 = 117,100


accept_p = np.exp((adj_utility - curr_utility) / curr_temperature)
p = rnd.random()

print(accept_p, p)
for x in range(5):
    print(rnd.random())