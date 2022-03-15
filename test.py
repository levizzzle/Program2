import SimulatedAnealing as sa


def main():
    sa.initializeCargo()

    print("\nItem utility values: ")
    print(sa.itemValues)
    print("\nItem weights: ")
    print(sa.itemWeights)
    print("\nMax total weight = %d " % sa.weightLimit)

    print("\nSettings: ")
    # print("maxIterations = %d " % maxIterations)
    print("start_temperature = %0.1f " % sa.startTemp)
    print("alpha = %0.2f " % sa.adjustTemp)

    print("\nStarting anneal() ")
    cargo = sa.anneal()
    print("Finished anneal() ")

    print("\nBest cargo found: ")
    print(cargo)
    (value, weight) = sa.calculateValueWeight()
    print("\nTotal value of cargo = %0.1f " % value)
    print("Total weight of cargo = %0.1f " % weight)

    print("\nEnd demo ")


if __name__ == "__main__":
    main()
