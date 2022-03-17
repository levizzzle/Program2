# # import numpy as np
# #
# #
# # class SimulatedAnnealing:
# #     itemValues = []
# #     itemWeights = []
# #     itemScore = []
# #
# #     rnd = np.random.RandomState(5)
# #     totalItems = 0
# #     weightLimit = 500
# #     startTemp = 200
# #     adjustTemp = 0.85
# #     overweightPenalty = 20
# #     interval = 4000
# #     maxIterations = 250000
# #
# #     cargo = []
# #     neighbor = []
# #
# #     cargoValue, cargoWeight = 0, 0
# #
# #     @staticmethod
# #     def initializeCargo(self):
# #         (self.itemValues, self.itemWeights, self.itemScore) = self.getItemData()
# #         self.totalItems = len(self.itemValues)
# #         newCargo = np.zeros(self.totalItems, dtype=np.int64)
# #
# #         for x in range(20):
# #             newCargo[self.rnd.randint(self.totalItems)] = 1
# #
# #         self.cargo = newCargo
# #
# #     @staticmethod
# #     def getItemData():
# #         textFile = open("Program2Input.txt", "r")
# #         lines = textFile.readlines()
# #
# #         values, weights, scores = [], [], []
# #         for line in lines:
# #             value = float(line.split()[0])
# #             weight = float(line.split()[1])
# #             score = value/weight
# #             values.append(value)
# #             weights.append(weight)
# #             scores.append(score)
# #         textFile.close()
# #         return values, weights, scores
# #
# #     @staticmethod
# #     def calculateValueWeight(self, cargo):
# #         totalValue, totalWeight, overweight = 0.0, 0.0, 0.0
# #
# #         for index in range(self.totalItems):
# #             if cargo[index] == 1:
# #                 totalValue += self.itemValues[index]
# #                 totalWeight += self.itemWeights[index]
# #
# #         if totalWeight > self.weightLimit:  # too heavy to fit in vehicle
# #             overweight = totalWeight - self.weightLimit
# #             totalValue -= (overweight * self.overweightPenalty)
# #         return totalValue, totalWeight
# #
# #     @staticmethod
# #     def getNeighbor(self):
# #         neighbor = np.copy(self.cargo)
# #         index = self.rnd.randint(self.totalItems)
# #         if neighbor[index] == 0:
# #             neighbor[index] = 1
# #         elif neighbor[index] == 1:
# #             neighbor[index] = 0
# #         return neighbor
# #
# #     @staticmethod
# #     def anneal(self):
# #         print("Initial Cargo Stored: ")
# #         print(self.cargo, "\n")
# #
# #         iteration = 0
# #         trackerValue = 0
# #         currentTemp = self.startTemp
# #         (self.cargoValue, self.cargoWeight) = self.calculateValueWeight(self, self.cargo)
# #
# #         while iteration < self.maxIterations:
# #             self.neighbor = self.getNeighbor(self)
# #             (neighborValue, neighborWeight) = self.calculateValueWeight(self, self.neighbor)
# #
# #             cargoMin = 1000 - self.cargoValue
# #             neighborMin = 1000 - neighborValue
# #             if neighborMin < cargoMin:
# #                 self.cargo = self.neighbor
# #                 self.cargoValue = neighborValue
# #             else:
# #                 acceptProbability = np.exp((neighborValue - self.cargoValue) / currentTemp)
# #                 probability = self.rnd.random()
# #                 if probability < acceptProbability:
# #                     self.cargo = self.neighbor
# #                     self.cargoValue = neighborValue
# #
# #
# #             if iteration % self.interval == 0:
# #                 print("iter = %6d : curr value = %7.0f : curr temp = %10.2f "
# #                       % (iteration, self.cargoValue, currentTemp))
# #                 if trackerValue == self.cargoValue:
# #                     break
# #                 else:
# #                     trackerValue = self.cargoValue
# #                     currentTemp *= self.adjustTemp
# #             iteration += 1
# #
# #         return self.cargo
#
# import SimulatedAnealing as SA
#
# def main():
#     SA.initializeCargo(SA)
#
#     print("\nItem utility values: ")
#     print(SA.itemValues)
#     print("\nItem weights: ")
#     print(SA.itemWeights)
#     print("\nMax total weight = %d " % SA.weightLimit)
#     print("Total items = %d " % SA.totalItems)
#
#     print("\nSettings: ")
#     # print("maxIterations = %d " % maxIterations)
#     print("Starting Temperature = %0.1f " % SA.startTemp)
#     print("Temperature Adjust = %0.2f " % SA.adjustTemp)
#     print("Adjust Interval = %0.2f " % SA.interval)
#
#     print("\nStarting Anneal() ")
#     cargo = SA.anneal(SA)
#     print("Finished Anneal() ")
#
#     print("\nBest cargo found: ")
#     print(cargo)
#     (value, weight) = SA.calculateValueWeight(SA, SA.cargo)
#     print("\nTotal value of cargo = %0.1f " % value)
#     print("Total weight of cargo = %0.1f " % weight)
#
#
# if __name__ == "__main__":
#     main()
