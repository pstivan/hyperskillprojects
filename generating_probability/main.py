import re
def task1_remove_non_0_1(string):
    new_string = ""
    for symbol in string:
        if symbol in ["0", "1"]:
            new_string = new_string + symbol
    return new_string

def task1_accumulating_string():
    resulting_string = ""
    print("Please provide AI some data to learn...")
    while len(resulting_string) < 100:
        print("The current data length is {}, {} symbols left".format(len(resulting_string), 100 - len(resulting_string)))
        print("Print a random string containing 0 or 1:")
        inserted_string = input()
        stripped_string = task1_remove_non_0_1(inserted_string)
        resulting_string = resulting_string + stripped_string
        if len(resulting_string) >= 100:
            print("Final data string:")
            print(resulting_string, "\n")
        # else:
        #     print("Current data length is {}, {} symbols left".format(len(resulting_string), 100 - len(resulting_string)))
    return resulting_string

def task1_list_of_occurrences(substring, fulltext):
    """This functions counts how many times specific substring exists"""
    return len(re.findall('(?={0})'.format(re.escape(substring)), fulltext))

def task2_calculate_triads():
    """This functions checks the amounts of XXX0 and XXX1, where XXX is 000, 001 ... 111"""
    list_of_triads = ["000", "001", "010", "011", "100", "101", "110", "111"]
    # Design of dictionary: {triad: [n_triad0, n_triad1]
    dictionary_of_triads = {}
    final_text = task1_accumulating_string()
    for triad in list_of_triads:
        dictionary_of_triads[triad] = [task1_list_of_occurrences(triad + "0", final_text), task1_list_of_occurrences(triad + "1", final_text)]
    return dictionary_of_triads

def task3_predict(probabilities_dictionary):
    # print(probabilities_dictionary)
    """Makes a 0-1 sequence prediction based on probability"""
    long_string = 1
    while long_string == 1:
        print("Print a random string containing 0 or 1:")
        test_string = input()
        if test_string == "enough":
            print("Game over!")
            exit()
        incorrect_symbols = 0
        for symbol in test_string:
            if symbol not in ["0", "1"]:
                incorrect_symbols += 1
        if len(test_string) > 3 and incorrect_symbols == 0:
            long_string = 0
    # list_of_triads = ["000", "001", "010", "011", "100", "101", "110", "111"]
    # generated_string = random.choice(list_of_triads)
    generated_string = test_string[:3]
    total = len(test_string) - 3
    for number in range(total):
        triad = test_string[number:number + 3]
        generated_string += '0' if probabilities_dictionary[triad][0] >= probabilities_dictionary[triad][1] else '1'
    correct = 0
    for x in range(total):
        if generated_string[3:][x] == test_string[3:][x]:
            correct += 1
    print("predictions:")
    print(generated_string[3:])
    # print("Computer guessed {} out of {} symbols right ({} %)".format(number_of_correct, len(generated_string), round(100 * number_of_correct/len(generated_string), 2)))
    print("Computer guessed {} out of {} symbols right ({} %)".format(correct, total, round(
        100 * correct / total, 2)))
    return correct, total

def task4_game(probabilities_dictionary):
    """Plays the game when computer has to correctly predict symbols. Initial bank is 1000 USD. + or - 1 usd for each incorrectly or correctly guessed"""
    print("""You have $1000. Every time the system successfully predicts your next press, you lose $1.
Otherwise, you earn $1. Print "enough" to leave the game. Let's go!\n""")
    bank = 1000
    while bank > 0:
        correct_guessed, total_length = task3_predict(probabilities_dictionary)
        bank = bank - correct_guessed + (total_length - correct_guessed)
        print("Your balance is now ${}".format(bank))
    print("Game over!")
if __name__ == '__main__':
    task4_game(task2_calculate_triads())
