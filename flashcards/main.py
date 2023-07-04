# Write your code here
# import os
import random
import argparse
from io import StringIO

def task4_check_for_unique_term_definition(dictionary_key_term, dictionary_name, term_or_def="term"):
    """Checks if inserted term or definition is unique"""
    if term_or_def == "term":
        if dictionary_key_term in dictionary_name.keys():
            return True
        else:
            return False
    else:
        if dictionary_key_term in dictionary_name.values():
            return True
        else:
            return False

def task5_add_card(flashcard_dict, dictionary_with_errors, filename):
    """Adds a flash card if it's a unique one"""
    unique_card = False
    unique_definition = False
    print("The card:")
    print("The card:", file=filename)
    while unique_card is False:
        read_term = input()
        filename.write(read_term)
        if task4_check_for_unique_term_definition(read_term, flashcard_dict) is True:
            print("The term already exists. Try again:")
            print("The term already exists. Try again:", file=filename)
        else:
            unique_card = True
            dictionary_with_errors[read_term] = 0
    print("The definition of the card:")
    print("The definition of the card:", file=filename)
    while unique_definition is False:
        read_definition = input()
        filename.write(read_definition)
        # print()
        if task4_check_for_unique_term_definition(read_definition, flashcard_dict, term_or_def="def"):
            print("The definition already exists. Try again:")
            print("The definition already exists. Try again:", file=filename)
        else:
            unique_definition = True
    flashcard_dict[read_term] = read_definition
    print('The pair ("{}":"{}") has been added.'.format(read_term, read_definition))
    print('The pair ("{}":"{}") has been added.'.format(read_term, read_definition), file=filename)

def task5_remove_card(flashcard_dict, dictionary_with_errors, filename):
    """Removes desired card"""
    print("Which card?")
    print("Which card?", file=filename)
    card_to_remove = input()
    filename.write(card_to_remove)
    try:
        del flashcard_dict[card_to_remove]
        del dictionary_with_errors[card_to_remove]
        print("The card has been removed.")
        print("The card has been removed.", file=filename)
    except:
        print('Can\'t remove "{}": there is no such card.'.format(card_to_remove))
        print('Can\'t remove "{}": there is no such card.'.format(card_to_remove), file=filename)
def task3_collecting_flashcards(filename):
    """This function gets the amount of flashcards.
    In cycle it reads terms and definitions, returning resulting dictionary."""
    flashcards_dict = {}
    print("Input the number of cards:")
    print("Input the number of cards:", file=filename)
    number_of_cards = int(input())
    filename.write(number_of_cards)
    try_ = 1
    while number_of_cards > 0:
        valid_term_inserted = False
        print("The term for card #{}:".format(try_))
        print("The term for card #{}:".format(try_), file=filename)
        term = input()
        filename.write(term)
        while valid_term_inserted is False:
            if task4_check_for_unique_term_definition(term, flashcards_dict) is True:
                print('The term "{}" already exists. Try again:'.format(term))
                print('The term "{}" already exists. Try again:'.format(term), file=filename)
                term = input()
                filename.write(term)
            else:
                valid_term_inserted = True
        valid_definition_inserted = False
        print("The definition for card #{}:".format(try_))
        print("The definition for card #{}:".format(try_), file=filename)
        while valid_definition_inserted is False:
            definition = input()
            filename.write(definition)
            if task4_check_for_unique_term_definition(definition, flashcards_dict, False) is True:
                print('The definition "{}" already exists. Try again:'.format(definition))
                print('The definition "{}" already exists. Try again:'.format(definition), file=filename)
            else:
                valid_definition_inserted = True

        flashcards_dict[term] = definition
        number_of_cards -= 1
        try_ += 1
    return flashcards_dict

def task5_3_checking_terms(dictionary_with_answers, dictionary_with_errors, filename):
    """"Iterates through flashcards dictionary and checks the correctness of provided definitions"""
    amount_of_cards_to_check = int(input())
    filename.write(str(amount_of_cards_to_check))
    while amount_of_cards_to_check > 0:
        term, definition = random.choice(list(dictionary_with_answers.items()))
        print('Print the definition of "{}":'.format(term))
        print('Print the definition of "{}":'.format(term), file=filename)
        checked_answer = input()
        filename.write(checked_answer)
        if checked_answer == definition:
            print("Correct!")
            print("Correct!", file=filename)
        elif checked_answer in dictionary_with_answers.values():
            key_list = [key for key, val in dictionary_with_answers.items() if val == checked_answer]
            print('Wrong. The right answer is "{}", but your definition is correct for "{}".'.format(definition, key_list[0]))
            print('Wrong. The right answer is "{}", but your definition is correct for "{}".'.format(definition,
                                                                                                     key_list[0]), file=filename)
            # print(keys[0], dictionary_with_answers[keys[0]])
            new_amount_of_errors_for_card = dictionary_with_errors[term] + 1
            dictionary_with_errors[term] = new_amount_of_errors_for_card
        else:
            print('Wrong. The right answer is "{}".'.format(definition))
            print('Wrong. The right answer is "{}".'.format(definition), file=filename)
            new_amount_of_errors_for_card = dictionary_with_errors[term] + 1
            dictionary_with_errors[term] = new_amount_of_errors_for_card
        amount_of_cards_to_check -= 1

def task5_exports_dictionary(dictionary_with_answers, dictionary_with_errors, filename, is_cli):
    """Exports cards to a text file."""
    if is_cli is False:
        print("File name:")
        print("File name:", file=filename)
        file_name_to_export = input()
    else:
        file_name_to_export = is_cli
    filename.write(file_name_to_export)
    file = open(file_name_to_export, 'w')
    for key, value in dictionary_with_answers.items():
        file.write(key + " " + value + " " + str(dictionary_with_errors[key]) + "\n")
    file.close()
    print("{} cards have been saved.".format(len(dictionary_with_answers)))
    print("{} cards have been saved.".format(len(dictionary_with_answers)), file=filename)

def task5_import_dictionary(dictionary_with_answers, dictionary_with_errors, filename, is_cli):
    """Imports dictionary with answers, rewriting definitions"""
    if is_cli is False:
        print("File name:")
        print("File name:", file=filename)
        export_file_path = input()
    else:
        export_file_path = is_cli
    filename.write(export_file_path)
    try:
        lines_count = 0
        file1 = open(export_file_path, 'r')
        Lines = file1.readlines()
        for line in Lines:
            lines_count += 1
            line_list = line.split()
            dictionary_with_answers[line_list[0]] = line_list[1]
            dictionary_with_errors[line_list[0]] = int(line_list[2])
        print("{} cards have been loaded.".format(lines_count))
        print("{} cards have been loaded.".format(lines_count), file=filename)
    except:
        print("File not found.")
        print("File not found.", file=filename)

def task6_card_with_most_errors(dictionary_with_errors, filename):
    """Take a dictionary with input. Finds the key with highest value. If there're more than one, names all"""
    list_of_top_errors_keys = []
    # finding the maximal value
    maximal_value = 0
    for value in dictionary_with_errors.values():
        if value != 0 and value > maximal_value:
            maximal_value = value
    # findings terms with most errors:
    for key, value in dictionary_with_errors.items():
        if value == maximal_value:
            list_of_top_errors_keys.append(key)
    # checking the amount of keys, output depends on it
    if len(list_of_top_errors_keys) == 1 and maximal_value > 0:
        print('The hardest card is "{}". You have {} errors answering it'.format(list_of_top_errors_keys[0], maximal_value))
        print('The hardest card is "{}". You have {} errors answering it'.format(list_of_top_errors_keys[0],
                                                                                 maximal_value), file=filename)
    elif len(list_of_top_errors_keys) > 1 and maximal_value > 0:
        mentioning_all_card_string = ""
        for term in list_of_top_errors_keys:
            mentioning_all_card_string = mentioning_all_card_string + '"' + term + '"' + ',' + ' '
        print("hardest cards are {}".format(mentioning_all_card_string[:-2]))
        print("hardest cards are {}".format(mentioning_all_card_string[:-2]), file=filename)
    else:
        print("There are no cards with errors.")
        print("There are no cards with errors.", file=filename)

def task6_reset_stats(dictionary_with_errors, filename):
    """Replaces all value with zeros"""
    for key, value in dictionary_with_errors.items():
        dictionary_with_errors[key] = 0
    print(dictionary_with_errors)
    print("Card statistics have been reset.")
    print("Card statistics have been reset.", file=filename)


def task5_main_menu():
    """Endless cycle, waiting for operations with dictionties"""
    # Initializing parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--import_from')  # option that takes a value
    parser.add_argument('--export_to')
    args = parser.parse_args() # reading arguments
    # initializing the cards storage
    main_dictionary_with_cards = {}
    errors_dict = {}
    # start capturing all input and output
    memory_file = StringIO()
    # stop_word_for_cycle = False
    if args.import_from:
        task5_import_dictionary(main_dictionary_with_cards, errors_dict, memory_file, args.import_from)
    while True:
        print("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
        print("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):", file=memory_file)
        inserted_command = input()
        memory_file.write(inserted_command)
        if inserted_command == "exit":
            if args.export_to:
                task5_exports_dictionary(main_dictionary_with_cards, errors_dict, memory_file, args.export_to)
                exit()
            else:
                print("Bye bye!")
                print("Bye bye!", file=memory_file)
                exit()
        elif inserted_command == "add":
            task5_add_card(main_dictionary_with_cards, errors_dict, memory_file)
        elif inserted_command == "remove":
            task5_remove_card(main_dictionary_with_cards, errors_dict, memory_file)
        elif inserted_command == "ask":
            print("How many times to ask?")
            print("How many times to ask?", file=memory_file)
            # times_to_ask = int(input())
            task5_3_checking_terms(main_dictionary_with_cards, errors_dict, memory_file)
        elif inserted_command == "import":
            task5_import_dictionary(main_dictionary_with_cards, errors_dict, memory_file, False)
        elif inserted_command == "export":
            task5_exports_dictionary(main_dictionary_with_cards, errors_dict, memory_file, False)
        elif inserted_command == "log":
            print("File name:")
            print("File name:", file=memory_file)
            log_file_name = input()
            memory_file.write(log_file_name)
            contents = memory_file.getvalue()

            with open(log_file_name, "w") as log:
                for line in contents:
                    log.write(line)

            print("The log has been saved.")
            print("The log has been saved.", file=memory_file)
            # memory_file.write("string")
            # try:
            #     fd = open(log_file_name, 'w')
            #     # populate buf
            #     fd.write(memory_file.getvalue())
            #     print("The log has been saved.")
            # except:
            #     print("!!! Error of save !!!")
        elif inserted_command == "hardest card":
            task6_card_with_most_errors(errors_dict, memory_file)
        elif inserted_command == "reset stats":
            task6_reset_stats(errors_dict, memory_file)
        else:
            print("Unknown command")
            print("Unknown command", file=memory_file)

if __name__ == "__main__":
    task5_main_menu()
