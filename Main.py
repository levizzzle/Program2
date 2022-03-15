import numpy as np


def getItemData():
    text_file = open("Program2Input.txt", "r")
    lines = text_file.readlines()

    utility_arr = []
    weight_arr = []
    for line in lines:
        utility_arr.append(float(line.split()[0]))
        weight_arr.append(float(line.split()[1]))

    text_file.close()
    return utility_arr, weight_arr


def initializeCargo(currentCargo, rnd):
    new_cargo = currentCargo
    for x in range(20):
        new_cargo[rnd.randint(400)] = 1

    return new_cargo

def getItemRank(index):
    (values, weights) = getItemData()
    return values[index]/weights[index]

def highValueItem(values, weights):
    totalValues = 0
    totalWeights = 0
    items = []
    sumQuality = 0
    sumWeight = 0
    for index in range(len(values)):
        totalValues += values[index]
        totalWeights += weights[index]
        quality = values[index]/weights[index]
        if quality >= 0.7445:
            sumQuality += values[index]
            sumWeight += weights[index]
            items.append([index, quality])
    avgValuePerWeight = totalValues/totalWeights
    print(avgValuePerWeight)
    sortedItems = sorted(items, key=lambda  x: -x[1])
    print("Utility: ", sumQuality, " Weight: ", sumWeight)

def totalUtilityWeight(cargo, values, weights, max_weight):
    utility = 0.0  # total usefulness of cargo
    weight = 0.0  # total weight of cargo
    overweight = 0.0

    n = len(cargo)
    for i in range(n):
        if cargo[i] == 1:
            utility += values[i]
            weight += weights[i]
    if weight > max_weight:  # too heavy to fit in vehicle
        overweight = weight - max_weight
        utility -= (overweight * 20)
    return utility, weight


def neighbor(cargo, rnd):
    numItems = len(cargo)
    result = np.copy(cargo)
    index = rnd.randint(numItems)
    # while(getItemRank(index) < 0.74):
    #     index = rnd.randint(numItems)
    if result[index] == 0:
        result[index] = 1
    elif result[index] == 1:
        result[index] = 0
    return result


def anneal(totalItems, rnd, values, weights, max_weight, maxIterations, start_temperature, alpha):
    curr_temperature = start_temperature
    currentCargo = np.zeros(totalItems, dtype=np.int64)
    currentCargo = initializeCargo(currentCargo, rnd)
    print("Initial guess: ")
    print(currentCargo)

    (currentUtility, currentWeight) = totalUtilityWeight(currentCargo, values, weights, max_weight)
    iteration = 0
    interval = (int)(maxIterations / 1000)
    trackerValue = 0
    while iteration < maxIterations:
        neighborCargo = neighbor(currentCargo, rnd)
        (neighborUtility, _) = totalUtilityWeight(neighborCargo, values, weights, max_weight)

        currMin = 1000 - currentUtility
        neighborMin = 1000 - neighborUtility
        if neighborMin < currMin:  # better so accept neighbor
            currentCargo = neighborCargo;
            currentUtility = neighborUtility
        else:  # neighbor cargo is worse
            acceptProbability = np.exp((neighborUtility - currentUtility) / curr_temperature)
            probability = rnd.random()
            if probability < acceptProbability:  # accept worse cargo anyway
                currentCargo = neighborCargo;
                currentUtility = neighborUtility
                # else don't accept

        # print("iter = %6d : curr value = %7.0f : \
        # curr temp = %10.2f " % (iteration, currentUtility, curr_temperature))
        if iteration % interval == 0:
            print("iter = %6d : curr value = %7.0f : \
        curr temp = %10.2f " % (iteration, currentUtility, curr_temperature))

        if curr_temperature < 0.1:
            curr_temperature = 0.1
        elif iteration % 4000 == 0:
            if currentUtility == trackerValue:
                print("BREAK")
                break
            else:
                trackerValue = currentUtility
            curr_temperature *= alpha
            # curr_temperature = start_temperature * \
            # pct_iters_left * 0.0050
        iteration += 1

    return currentCargo


def main():
    (utility_values, weights) = getItemData()
    max_weight = 500

    print("\nItem utility values: ")
    print(utility_values)
    print("\nItem weights: ")
    print(weights)
    print("\nMax total weight = %d " % max_weight)

    rnd = np.random.RandomState(5)  # 3 .98 = 117,100
    maxIterations = 300000
    start_temperature = 120.0
    alpha = 0.92

    print("\nSettings: ")
    print("maxIterations = %d " % maxIterations)
    print("start_temperature = %0.1f " % start_temperature)
    print("alpha = %0.2f " % alpha)

    print("\nStarting anneal() ")
    cargo = anneal(400, rnd, utility_values, weights, max_weight, maxIterations, start_temperature, alpha)
    print("Finished anneal() ")

    print("\nBest cargo found: ")
    print(cargo)
    (utility, weight) = totalUtilityWeight(cargo, utility_values, weights, max_weight)
    print("\nTotal value of cargo = %0.1f " % utility)
    print("Total weight of cargo = %0.1f " % weight)

    print("\nEnd demo ")

    highValueItem(utility_values, weights)

if __name__ == "__main__":
    main()
