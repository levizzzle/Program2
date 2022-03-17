import numpy as np


class SimulatedAnnealing:
    itemValues = []
    itemWeights = []
    itemScore = []

    rnd = np.random.RandomState(5)
    totalItems = 0
    weightLimit = 500
    startTemp = 182
    adjustTemp = 0.86
    overweightPenalty = 20
    dataInterval = 4000
    breakInterval = 40000
    maxIterations = 250000

    cargo = []
    neighbor = []

    cargoValue, cargoWeight = 0, 0

    def initializeCargo(self):
        (self.itemValues, self.itemWeights, self.itemScore) = self.getItemData()
        self.totalItems = len(self.itemValues)
        newCargo = np.zeros(self.totalItems, dtype=np.int64)

        for x in range(20):
            newCargo[self.rnd.randint(self.totalItems)] = 1

        self.cargo = newCargo

    def getItemData(self):
        textFile = open("Program2Input.txt", "r")
        lines = textFile.readlines()

        values, weights, scores = [], [], []
        for line in lines:
            value = float(line.split()[0])
            weight = float(line.split()[1])
            score = value/weight
            values.append(value)
            weights.append(weight)
            scores.append(score)
        textFile.close()
        return values, weights, scores

    def calculateValueWeight(self, cargo):
        totalValue, totalWeight, overweight = 0.0, 0.0, 0.0

        for index in range(self.totalItems):
            if cargo[index] == 1:
                totalValue += self.itemValues[index]
                totalWeight += self.itemWeights[index]

        if totalWeight > self.weightLimit:  # too heavy to fit in vehicle
            overweight = totalWeight - self.weightLimit
            totalValue -= (overweight * self.overweightPenalty)
        return totalValue, totalWeight

    def getNeighbor(self):
        neighbor = np.copy(self.cargo)
        index = self.rnd.randint(self.totalItems)
        if neighbor[index] == 0:
            neighbor[index] = 1
        elif neighbor[index] == 1:
            neighbor[index] = 0
        return neighbor

    def anneal(self):
        print("Initial Cargo Stored: ")
        print(self.cargo, "\n")

        iteration = 0
        trackerValue = 0
        currentTemp = self.startTemp
        (self.cargoValue, self.cargoWeight) = self.calculateValueWeight(self.cargo)

        def setNeighbor():
            self.cargo = self.neighbor
            self.cargoValue = neighborValue
            self.cargoWeight = neighborWeight

        while iteration < self.maxIterations:
            self.neighbor = self.getNeighbor()
            (neighborValue, neighborWeight) = self.calculateValueWeight(self.neighbor)

            cargoMin = 1000 - self.cargoValue
            neighborMin = 1000 - neighborValue
            if neighborMin < cargoMin:
                setNeighbor()
            else:
                acceptProbability = np.exp((neighborValue - self.cargoValue) / currentTemp)
                probability = self.rnd.random()
                if probability < acceptProbability:
                    setNeighbor()

            if iteration % self.dataInterval == 0:
                currentTemp *= self.adjustTemp
                print("iteration = %6d  ---|>  utility value = %7.1f       weight = %5.1f       temperature = %5.3f "
                      % (iteration, self.cargoValue, self.cargoWeight, currentTemp))

            if iteration % self.breakInterval == 0:
                if trackerValue == self.cargoValue:
                    break
                else:
                    trackerValue = self.cargoValue
            iteration += 1

        return self.cargo


def main():
    sa = SimulatedAnnealing()
    # sa.initializeCargo()

    print("\nItem utility values: ")
    print(sa.itemValues)
    print("\nItem weights: ")
    print(sa.itemWeights)
    print("\nMax total weight = %d " % sa.weightLimit)
    print("Total items = %d " % sa.totalItems)

    print("\nSettings: ")
    print("Starting Temperature = %0.1f " % sa.startTemp)
    print("Temperature Adjust = %0.2f " % sa.adjustTemp)
    print("Adjust Interval = %d " % sa.dataInterval)
    print("Break Interval = %d " % sa.breakInterval)
    # file = open("results.txt", "a")
    results = []
    # for change in range(75, 95):
    #     for temp in range(50, 250):
    #         if change % 2 == 0 and temp % 2 == 0:
    sa.initializeCargo()
    # sa.adjustTemp = float(change/100)
    # sa.startTemp = temp
    print("\nStarting Anneal() ")
    cargo = sa.anneal()
    print("Finished Anneal() ")

    print("\nBest cargo found: ")
    print(cargo)
    (value, weight) = sa.calculateValueWeight(sa.cargo)
    print("\nTotal value of cargo = %0.1f " % value)
    print("Total weight of cargo = %0.1f " % weight)
    # results.append(["Change: %f, Temp: %f, Value: %f, Weight: %f" % (change, temp, value, weight)])
    # file.write("Change: %f, Temp: %f, Value: %f, Weight: %f\n" % (change, temp, value, weight))
    # print(["Change: %f, Temp: %f, Value: %f, Weight: %f" % (change, temp, value, weight)])
    # file.close()


if __name__ == "__main__":
    main()