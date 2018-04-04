import random

binary = [0, 1]
pop_size = 5
pop_limit = 81920
string_size = 5
string_list = []
recom_prob = 0.6


# A function that checks the fitness for onemax
def fitness(string):
    fit = 0  # initialize accumulator
    for c in string:  # iterate over every element in the string, increment accumulator for each 1 seen
        if c is 1:
            fit += 1
    return fit  # return accumulator (the number of 1's)


# A function that performs binary tournament selection of k = 2 and returns the chosen parent
def selection(population):
    s1 = random.choice(population)
    s2 = random.choice(population)
    # print("Selection 1 is {} and Selection 2 is {}".format(s1, s2))
    parent = s1 if (fitness(s1) > fitness(s2)) else s2
    return parent


# A function that performs mutation on a string, flipping bits with a probability of 1/N
def mutate(string):
    for i in range(0, string_size):
        if random.random() < (1/string_size):
            string[i] = 1 if (string[i] is 0) else 0
    return string


# A function that performs uniform crossover recombination on two strings with given probability
def recombination(p1, p2):
    c1 = []
    c2 = []
    if random.random() > recom_prob:  # with 40% probability, copy the parents to the children
        # print("Copying the parents to the children\n")
        c1 = p1
        c2 = p2
    else:  # with 60% probability, perform recombination
        # print("Random recombination\n")
        for i in range(0, string_size):
            test = random.choice([1, 2])  # randomly choose whether to give parent 1's bit to child 1 or child 2
            if test is 1:
                c1.append(p1[i])
                c2.append(p2[i])
            else:
                c1.append(p2[i])
                c2.append(p1[i])
    c1 = mutate(c1)  # mutate the children regardless of whether they were copied or recombined
    c2 = mutate(c2)
    return c1, c2


# A function to get and display stats about the population
def fitness_stats(population):
    totalfit = 0
    lowestfit = fitness(population[0])
    lowindex = 0
    highestfit = fitness(population[0])
    highindex = 0

    for i in range(0, pop_size):  # for each element in the population:
        currentfit = fitness(population[i])  # get the fitness
        totalfit += currentfit  # add to our running fitness total
        if currentfit < lowestfit:  # if its our new low fitness, reflect that
            lowestfit = currentfit
            lowindex = i
        elif currentfit > highestfit:  # if its our new high fitness, reflect that
            highestfit = currentfit
            highindex = i

    averagefit = totalfit / pop_size  # calculate average fitness

    # display statistics
    print("The average fitness is {}".format(averagefit))
    print("The highest fitness is {} with fitness {}".format(population[highindex], highestfit))
    print("The lowest fitness is {} with fitness {}".format(population[lowindex], lowestfit))
    return averagefit


# A function to perform replacement - finds the two most fit parents and keeps them, but replaces the rest with children
def replacement(population, child_list):
    highest1 = population[0]
    highidx1 = 0
    fit1 = fitness(highest1)
    highest2 = population[1]
    highidx2 = 1
    fit2 = fitness(highest2)

    for index, parent in enumerate(population):
        if not ((index is highidx1) or (index is highidx2)):
            currentfit = fitness(parent)
            if currentfit > fit1:
                highest1 = parent
                highidx1 = index
            elif currentfit > fit2:
                highest2 = parent
                highidx2 = index

    newpop = [highest1, highest2]
    # print("The highest fitness parents are: {} at indexes {} and {}".format(newpop, highidx1, highidx2))
    for child in child_list:
        newpop.append(child)

    return newpop


# A function to generate a list of children
def generate_children(population, child_list):
    while len(child_list) < (pop_size - 2):
        p1 = selection(population)
        p2 = selection(population)
        c1, c2 = recombination(p1, p2)
        child_list.append(c1)
        child_list.append(c2)
    while len(child_list) > (pop_size - 2):
        lowest = child_list[0]
        lowfit = fitness(lowest)
        for child in child_list:
            if fitness(child) < lowfit:
                lowest = child
                lowfit = fitness(child)
        child_list.remove(lowest)
    return child_list


# generate random binary strings of pop_size size
def initialize():
    for i in range(0, pop_size):
        newstring = random.choices(binary, k=string_size)
        string_list.append(newstring)


def generational_loop():
    global string_list
    avgfit = fitness_stats(string_list)
    increased = 0
    numgens = 0
    while increased < 3:
        child_list = []
        child_list = generate_children(string_list, child_list)
        string_list = replacement(string_list, child_list)
        newfit = fitness_stats(string_list)
        if newfit > avgfit:
            # print("Increased")
            avgfit = newfit
            increased = 0
        else:
            # print("No increase")
            avgfit = newfit
            increased += 1
        numgens += 1

    print("Terminating loop: ")
    print("Number of generations taken: {}".format(numgens))
    localopt = fitness(string_list[0])
    for item in string_list:
        if fitness(item) > localopt:
            localopt = fitness(item)
    return localopt


def overall(popsize, stringsize):
    global pop_size
    global string_size
    pop_size = popsize
    string_size = stringsize

    initialize()
    localopt = generational_loop()
    return localopt


stringsize = input("Please enter the desired size of the string: ")
try:
    stringsize = int(stringsize)
except ValueError:
    print("Error! You must enter a valid integer.")
    exit(1)

popsize = 10
while popsize < pop_limit:
    index = 0
    success = False
    while index < 5:
        runopt = overall(popsize, stringsize)
        print("Run optimum: {}".format(runopt))
        if runopt < stringsize:
            index = 10
        else:
            index += 1
    if index is 5:
        print("Done!")
        success = True
        break
    else:
        popsize = 2 * popsize
        print("Popsize is now {}".format(popsize))

# TO DO: finish the bisection algorithm, and make the statistics output to a file
# if success:
#     upperlimit = popsize
#     lowerlimit = popsize/2
#     midpoint = (upperlimit - lowerlimit)/2
#
