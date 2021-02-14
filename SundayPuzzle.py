import time
from itertools import permutations


# This program will attempt to solve NPR's Sunday Puzzle 1-31-21.
# It will use a brute force algorithm to look up all the possible four state routes in the contiguous US,
# removing duplicates, and then find all the permutations of letters the state abbreviations can make. Finally,
# the list of permutations will be referenced from a collection of common 8-letter words. The main runner function
# can supply a corpus under the constraint that the words to be searched are on each line individually.

# Function for determining routes. It takes in as arguments the desired start location as the variable
# input and then the adjacency list of states as the variable mapV.
def get_routes(input, mapV):
    prevPoint = None
    currPoint = input
    nextValues = mapV[currPoint]
    nextPoint = nextValues[0]
    traveled = [currPoint]
    size = 1
    results = []
    pruned = []
    while nextValues:
        while 4 > size >= 1:
            tempNext = traveled.copy()
            tempNext.append(nextPoint)
            if traveled not in pruned and tempNext not in pruned and tempNext not in results and nextPoint:
                if nextPoint not in traveled:
                    prevPoint = currPoint
                    currPoint = nextPoint
                    nextValues = mapV[currPoint].copy()
                    if nextValues:
                        nextPoint = nextValues[0]
                        traveled.append(currPoint)
                        size += 1
                    else:
                        break
                else:
                    if nextValues:
                        nextValues.pop(0)
                        nextPoint = nextValues[0] if nextValues else None
                    else:
                        break
            elif traveled in pruned:
                traveled.pop()
                size -= 1
                if traveled:
                    currPoint = traveled[-1]
                    prevPoint = traveled[-2] if len(traveled) >= 2 else None
                    nextValues = mapV[currPoint].copy()
                    nextPoint = nextValues[0]
            elif tempNext in pruned:
                # check next value
                if nextValues:
                    nextValues.pop(0)
                    nextPoint = nextValues[0] if nextValues else None
                else:
                    pathToPrune = traveled.copy()
                    pruned.append(pathToPrune)
                    traveled.pop()
                    size -= 1
                    if traveled:
                        currPoint = traveled[-1]
                        prevPoint = traveled[-2] if len(traveled) >= 2 else None
                        nextValues = mapV[currPoint].copy()
                        nextPoint = nextValues[0]
            elif tempNext in results:
                if nextValues:
                    nextValues.pop(0)
                    nextPoint = nextValues[0] if nextValues else None
                else:
                    break
            else:
                # prune this route because no other non-null options
                pathToPrune = traveled.copy()
                pruned.append(pathToPrune)
                traveled.pop()
                size -= 1
                if traveled:
                    currPoint = traveled[-1]
                    prevPoint = traveled[-2] if len(traveled) >= 2 else None
                    nextValues = mapV[currPoint].copy()
                    nextPoint = nextValues[0]
        if traveled not in results and traveled:
            path = traveled.copy()
            results.append(path)
            traveled.pop()
            size -= 1
            currPoint = traveled[-1]
            prevPoint = traveled[-2]
            nextValues = mapV[currPoint].copy()
            nextPoint = nextValues[0]
        elif traveled in results:
            traveled.pop()
            pathToPrune = traveled.copy()
            pruned.append(pathToPrune)
            buffer = currPoint
            currPoint = prevPoint
            prevPoint = buffer
            nextValues = mapV[currPoint].copy()
            nextPoint = nextValues[0]
            size -= 1
        else:
            break
    # Sort the paths and remove duplicates if not null
    if results:
        for path in results:
            path.sort()
        results.sort()
        # Then remove duplicates
        noDup = []
        for i in results:
            if i not in noDup:
                noDup.append(i)
        results = noDup
    return results


# Function to format the adjacency list from the supplied file.
def parse_states_from_file(file_name):
    states = {}
    with open(file_name, "r") as file:
        for line in file:
            line = line.strip("\n")
            line = line.split(",")
            states[line.pop(0)] = line
        file.close()
    return states


# Function to parse the supplied corpus line by line into a list.
def parse_words_from_file(file_name):
    list_words = []
    with open(file_name, "r") as file:
        for line in file:
            list_words.extend(line.split())
        file.close()
    return list_words


#  Main runner.
def main():
    print("Welcome to the NPR Sunday Puzzle Solver. It will solve the weekly puzzle of 1-31-21.")
    # Begin by getting the list of all the states from the input file and create an adjacency list.
    states_list = parse_states_from_file("states.txt")

    # Get all the 8 letter words from the input file
    words_list = parse_words_from_file('smaller_corpus.txt')
    # words_list = parse_words_from_file('corpus.txt')
    words_upper = [x.upper() for x in words_list]

    # Get all the routes for each state and then sort alphabetically
    all_routes = []
    for state in states_list:
        all_routes.append(get_routes(state, states_list))
    # all_routes.append(get_routes("WA", states_list))
    all_routes.sort()

    # Flatten out the lists for each state
    flat_list = [item for sublist in all_routes for item in sublist]

    # Turn the list of routes into strings
    string_routes = []
    for route in flat_list:
        temp_string = ''.join(route)
        string_routes.append(temp_string)

    # Get all the letter permutations for each route and remove duplicates
    string_permutations = []
    for route in string_routes:
        perms = [''.join(p) for p in permutations(route)]
        string_permutations.extend(perms)
    perm_no_dup = list(set(string_permutations))

    start = time.time()
    # Now check to see which permutations are in the list of common 8 letter words
    for perm in perm_no_dup:
        if perm in words_upper:
            print("Match found: ", perm)
    end = time.time()
    print("Time to search permutations: ", end - start)

if __name__ == "__main__":
    main()
