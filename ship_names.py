import sys

def main():
    #import the text data
    fb = open("Desktop/ship_names/yob.csv", "r")
    data = fb.readlines()
    refined = []
    for line in data:
        parsed = line.split(",")
        refined.append((parsed[0].lower(), int(parsed[2].strip())))
    #create a table of letter -> letter => frequency
    #build the bigram frequency hashtable
    frequency_table = {}
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for letter1 in alphabet:
        for letter2 in alphabet:
            #print(letter1 + letter2)# works as expected!
            frequency_table[letter1 + letter2] = 0

    #count the frequencies of letter pairings
    #for each word
    for word_data in refined:
        word = word_data[0]
        #take each pair of letters
        for i in range (0, len(word) - 1):
            pair = word[i] + word[i + 1]
            #add the frequency of the name to that pair's location in the table
            frequency_table[pair] += word_data[1]

    #now build the length-table
    length_table = {}
    for i in range(0,30):
        length_table[i] = 0

    for name_frequency_combination in refined:
        #add the number of times this name has occured to the total of how many names of this length have been given
        length_table[len(name_frequency_combination[0])] += name_frequency_combination[1]

    #print(length_table)

    #get input
    name1, name2, setting, number_of_names = get_input()
    #make possibilities
    combos = make_possibilities(name1, name2, setting)
    #score
    for nick_name in combos:
        nick_name[1] = score(nick_name[0], frequency_table, length_table)
    #sort by score
    combos = sort_by_value(combos)
    #print top 
    print_names(number_of_names, combos)

def print_names(x, names):
    for i in range(1, x + 1):
        print(names[-i])


#finds out the setting for combination and the names
def get_input():
    setting = input("Are you using first names only (F), last names only (L), or both (B)? ")
    setting = setting.lower()
    number_of_names = input("How many names do you want? ")
    number_of_names = int(number_of_names.strip())
    name_1 = input("enter person one: ")
    name_2 = input("enter person two: ")
    #formatting the names, no newlines, no caps
    name_2 = name_2.strip().lower()
    name_1 = name_1.strip().lower()
    return (name_1, name_2, setting, number_of_names)


def make_possibilities(name_1, name_2, setting):
    #squash the two names into every combination, add to the list with its score
    combos = []

    #if there are two names to be combined
    if setting == "b":
        name_1_first = name_1.split(" ")[0]
        name_2_first = name_2.split(" ")[0]
        name_1_last = name_1.split(" ")[1]
        name_2_last = name_2.split(" ")[1]
        for item in combine(name_1_first, name_2_first):
            combos.append([(item), -1])
        for item in combine(name_2_first, name_1_first):
            combos.append([(item), -1])
        for item in combine(name_1_last, name_2_last):
            combos.append([(item), -1])
        for item in combine(name_2_last, name_1_last):
            combos.append([(item), -1])

    #only one name to be combined
    else:
        for item in combine(name_1, name_2):
            combos.append([(item), -1])
        for item in combine(name_2, name_1):
            combos.append([(item), -1])

    return combos

#takes a list of lists in the format [name, score] and sorts them by score
def sort_by_value(combos):
    sorted_list = []
    #insertion sort
    for i in range(0, len(combos)):
        mindex = 0
        j = 0
        while j < len(combos):
            if combos[j][1] < combos[mindex][1]:
                mindex = j
            j += 1
        sorted_list.append(combos[mindex])
        del combos[mindex]
    return sorted_list


#figures out a score based on bigrams and length, then adds each score together and returns the sum
def score(string, data, length_table):
    # for every pair of letters, add the value to the total, and add one to count of letters
    total = 0
    count = 0
    for i in range(0, len(string) - 1):
        pair = string[i] + string[i + 1]
        total += data[pair]
        count += 1
    # the average becomes the letterscore
    letterscore = total // count
    # now let's find the lengthscore
    len_score = length_table[len(string)]

    #this is to prevvent lenth from being the most important metric
    length_bias = 0.5

    len_score *= length_bias

    return len_score + letterscore



def combine(name1, name2):
    parts1 = []
    #name one is cut into every possible string starting from the second letter*
    for i in range(2, len(name1) + 1):
        parts1.append(name1[:i])
    parts2 = []
    #name two is cut into every possible string ending to the second to last letter*
    for i in range(0, len(name2) - 2):
        parts2.append(name2[i:])
    output = []
    #every possible piece is combined
    for part1 in parts1:
        for part2 in parts2:
            output.append(part1 + part2)
    return output
    #* would you call it a ship name if is was just a name with an extra letter? no.

main()