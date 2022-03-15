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
    interval = 4000
    maxIterations = 250000

    cargo = []
    neighbor = []

    cargoValue, cargoWeight = 0, 0

    # def __init__(self)
    #     print("XXXXXXXXXXXXXXXXXXXX")
    #     (self.itemValues, self.itemWeights, self.itemScore) = self.getItemData()
    #     self.totalItems = len(self.itemValues)
    #     self.initializeCargo()

    @classmethod
    def initializeCargo(cls):
        (cls.itemValues, cls.itemWeights, cls.itemScore) = cls.getItemData()
        cls.totalItems = len(cls.itemValues)
        newCargo = np.zeros(cls.totalItems, dtype=np.int64)

        for x in range(20):
            newCargo[cls.rnd.randint(cls.totalItems)] = 1
        return newCargo

    @classmethod
    def getItemData(cls):
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

    @classmethod
    def calculateValueWeight(cls):
        totalValue, totalWeight, overweight = 0.0, 0.0, 0.0

        for index in range(cls.totalItems):
            if cls.cargo[index] == 1:
                totalValue += cls.itemValues[index]
                totalWeight += cls.itemWeights[index]

        if totalWeight > cls.weightLimit:  # too heavy to fit in vehicle
            overweight = totalWeight - cls.weightLimit
            totalValue -= (overweight * cls.overweightPenalty)
        return totalValue, totalWeight

    @classmethod
    def getNeighbor(cls):
        neighbor = np.copy(cls.cargo)
        index = cls.rnd.randint(cls.totalItems)

        if neighbor[index] == 0:
            neighbor[index] = 1
        elif neighbor[index] == 1:
            neighbor[index] = 0
        return neighbor

    @classmethod
    def anneal(cls):
        print("Initial Cargo Stored: ")
        print(cls.cargo)

        iteration = 0
        trackerValue = 0
        currentTemp = cls.startTemp
        (cls.cargoValue, cls.cargoWeight) = cls.calculateValueWeight()

        while iteration < cls.maxIterations:
            cls.neighbor = cls.getNeighbor()
            (neighborValue, neighborWeight) = cls.calculateValueWeight()

            cargoMin = 1000 - cls.cargoValue
            neighborMin = 1000 - neighborValue
            if neighborMin < cargoMin:
                cls.cargo = cls.neighbor
                cls.cargoValue = neighborValue
            else:
                acceptProbability = np.exp((neighborValue - cls.cargoValue) / currentTemp)
                probability = cls.rnd.random()
                if probability < acceptProbability:
                    cls.cargo = cls.neighbor
                    cls.cargoValue = neighborValue

            if iteration % cls.interval == 0:
                print("iter = %6d : curr value = %7.0f : curr temp = %10.2f "
                      % (iteration, cls.cargoValue, currentTemp))
                if cls.cargoValue == trackerValue:
                    print("BREAK")
                    break
                else:
                    trackerValue = cls.cargoValue
                    currentTemp *= cls.adjustTemp
            iteration += 1

        return cls.cargo


def __init__():
    sa = SimulatedAnnealing