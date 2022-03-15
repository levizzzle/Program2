class SimulatedAnnealing():
    itemValues = []
    itemWeights = []

    def __init__(self):
        (self.itemValues, self.itemWeights) = getItemData()

    def getItemData(self):
        textFile = open("Program2Input.txt", "r")
        lines = textFile.readlines()

        values, weights = [], []
        for line in lines:
            values.append(float(line.split()[0]))
            weights.append(float(line.split()[1]))
        textFile.close()

        return values, weights

    def initializeCargo(currentCargo, rnd):
        new_cargo = currentCargo
        for x in range(20):
            new_cargo[rnd.randint(400)] = 1

        return new_cargo

    def calculateValueWeight(cargo, values, weights, max_weight):
        value = 0.0  # total usefulness of cargo
        weight = 0.0  # total weight of cargo
        overweight = 0.0

        n = len(cargo)
        for i in range(n):
            if cargo[i] == 1:
                value += values[i]
                weight += weights[i]
        if weight > max_weight:  # too heavy to fit in vehicle
            overweight = weight - max_weight
            value -= (overweight * 20)
        return value, weight

    def neighborCargo(cargo, rnd):
        numItems = len(cargo)
        neighbor = np.copy(cargo)
        index = rnd.randint(numItems)

        if neighbor[index] == 0:
            neighbor[index] = 1
        elif neighbor[index] == 1:
            neighbor[index] = 0
        return neighbor

    def anneal(totalItems, rnd, values, weights, max_weight, maxIterations, startTemp, alpha):
        currentTemp = startTemp
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
                currentCargo = neighborCargo
                currentUtility = neighborUtility
            else:  # neighbor cargo is worse
                acceptProbability = np.exp((neighborUtility - currentUtility) / currentTemp)
                probability = rnd.random()
                if probability < acceptProbability:  # accept worse cargo anyway
                    currentCargo = neighborCargo
                    currentUtility = neighborUtility
                    # else don't accept

            # print("iter = %6d : curr value = %7.0f : \
            # curr temp = %10.2f " % (iteration, currentUtility, currentTemp))
            if iteration % interval == 0:
                print("iter = %6d : curr value = %7.0f : \
            curr temp = %10.2f " % (iteration, currentUtility, currentTemp))

            if currentTemp < 0.1:
                currentTemp = 0.1
            elif iteration % 4000 == 0:
                if currentUtility == trackerValue:
                    print("BREAK")
                    break
                else:
                    trackerValue = currentUtility
                currentTemp *= alpha
                # currentTemp = startTemp * \
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