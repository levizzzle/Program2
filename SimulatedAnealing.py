import numpy as np


class SimulatedAnnealing:
    itemValues = []
    itemWeights = []
    itemScore = []

    rnd = np.random.RandomState(5)
    totalItems = 0
    weightLimit = 500
    startTemp = 120
    adjustTemp = 0.85
    overweightPenalty = 20
    dataInterval = 4000
    breakInterval = 40000
    maxIterations = 250000

    cargo = []
    neighbor = []

    cargoValue, cargoWeight = 0, 0

    def initializeCargo(self):
        (self.itemValues, self.itemWeights, self.itemScore) = self.getItemData(self)
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
        (self.cargoValue, self.cargoWeight) = self.calculateValueWeight(self, self.cargo)

        def setNeighbor():
            self.cargo = self.neighbor
            self.cargoValue = neighborValue
            self.cargoWeight = neighborWeight

        while iteration < self.maxIterations:
            self.neighbor = self.getNeighbor(self)
            (neighborValue, neighborWeight) = self.calculateValueWeight(self, self.neighbor)

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
                # print("Tracker: %7.1f    Value: %7.1f" % (trackerValue, self.cargoValue))

            if iteration % self.breakInterval == 0:
                if trackerValue == self.cargoValue:
                    break
                else:
                    trackerValue = self.cargoValue
            iteration += 1

        return self.cargo


def main():
    sa = SimulatedAnnealing
    sa.initializeCargo(sa)

    print("\nItem utility values: ")
    print(sa.itemValues)
    print("\nItem weights: ")
    print(sa.itemWeights)
    print("\nMax total weight = %d " % sa.weightLimit)
    print("Total items = %d " % sa.totalItems)

    print("\nSettings: ")
    # print("maxIterations = %d " % maxIterations)
    print("Starting Temperature = %0.1f " % sa.startTemp)
    print("Temperature Adjust = %0.2f " % sa.adjustTemp)
    print("Adjust Interval = %d " % sa.dataInterval)
    print("Break Interval = %d " % sa.breakInterval)


    print("\nStarting Anneal() ")
    cargo = sa.anneal(sa)
    print("Finished Anneal() ")

    print("\nBest cargo found: ")
    print(cargo)
    (value, weight) = sa.calculateValueWeight(sa, sa.cargo)
    print("\nTotal value of cargo = %0.1f " % value)
    print("Total weight of cargo = %0.1f " % weight)


if __name__ == "__main__":
    main()