# write your code here
import re 

def task3_converting_input():
    """We receive either space-separated integers or commands or help/exit command"""
    received_data = input()
    # print(received_data)
    return received_data

def task3_4_processing_received_data(recv_data):
    # print(recv_data[0])
    if recv_data == '' or recv_data == []:
        pass
    elif recv_data == "/exit":
        print("Bye!")
        exit()
    elif recv_data == "/help":
        print("""The program calculates the sum or a result of subtraction for n of numbers.
        if the user inputs --, it should be read as +; if they input ----, it should be read as ++, and so on.""")
    elif re.search(r"\/\w", recv_data):
        print("Unknown command")
    else:
        # sum_of_inserted_numbers = 0
        # for number in recv_data:
        #     sum_of_inserted_numbers += int(number)
        try:
            print(eval(recv_data))
        except:
            print("Invalid expression")

def task7_check_parenthesis(input_mathematical_formula):
    characters_list = []
    for element in input_mathematical_formula:
        try:
            if element == "(":
                characters_list.append(1)
            elif element == ")":
                characters_list.pop()
        except:
            return False
    if len(characters_list) == 0:
        return True
    else:
        return False
def task6_7_working_with_variables():
    """We suppose that the name of a variable (identifier) can contain only Latin letters.
    A variable can have a name consisting of more than one letter.
    The case is also important; for example, n is not the same as N.
    The value can be an integer number or a value of another variable.
    It should be possible to set a new value to an existing variable.
    To print the value of a variable you should just type its name."""
    variables_storage_dict = {}
    while True:
        received_input = task3_converting_input().strip()
        # Converting input to the list
        received_input_list = received_input.split()
        # Checking for commands
        if task7_check_parenthesis(received_input) is False:
            print("Invalid expression")
            continue
        if re.search(r"\/{2,}", received_input):
            print("Invalid expression")
            continue
        try:
            print(int(eval(received_input)))
        except:
            if received_input == "/exit":
                print("Bye!")
                exit()
            elif received_input == "/help":
                print("""The program calculates the sum or a result of subtraction for n of numbers.
                    if the user inputs --, it should be read as +; if they input ----, it should be read as ++, and so on.""")
            elif re.search(r"\/\w", received_input):
                print("Unknown command")
            elif re.search(r"\*{2,}", received_input):
                print("Invalid expression")
            elif re.search(r"\/{2,}", received_input):
                print("Invalid expression")
            elif received_input == "":
                pass
            elif received_input[-1] in ["-", "+", "*", "/"]:
                print("Invalid expression")
            # Case when there's = (equality) sign
            elif "=" in received_input:
                if len(received_input_list) == 1:
                    received_input_list = list(received_input_list[0])
                if len(received_input_list) == 2:
                    if "=" in received_input_list[0]:
                        received_input_list = [*list(received_input_list[0]), *received_input_list[-1]]
                    elif "=" in received_input_list[1]:
                        received_input_list = [*received_input_list[0], *list(received_input_list[-1])]
                if not re.search(r"^[a-zA-Z]+$", received_input_list[0]):
                    print("Invalid identifier")
                elif received_input.count("=") > 1:
                    print("Invalid assignment")
                elif re.search(r"^[a-zA-Z]+$", received_input_list[2]):
                    try:
                        variables_storage_dict[received_input_list[0]] = variables_storage_dict[received_input_list[2]]
                    except:
                        print("Unknown variable")
                elif not re.search(r"^\d+$", received_input_list[2]):
                    print("Invalid assignment")
                else:
                    variables_storage_dict[received_input_list[0]] = received_input_list[-1]
            # Case when there's a math expression
            elif "+" in received_input or "-" in received_input or "*" in received_input or "/" in received_input:
                resulting_expression = ""
                # print(received_input_list)
                if len(received_input_list) == 1:
                    received_input_list = list(received_input_list[0])
                for element in received_input_list:
                    if re.search(r"^\++$", element) or re.search(r"^\-+$", element):
                        resulting_expression = resulting_expression + element
                    elif element in ["*", "/", "(", ")"]:
                        resulting_expression = resulting_expression + element
                    elif element in variables_storage_dict.keys():
                        try:
                            resulting_expression = resulting_expression + variables_storage_dict[element]
                        except:
                            print("Unknown variable")
                            #print(resulting_expression, variables_storage_dict[element])
                    else:
                        resulting_expression = resulting_expression + element
                try:
                    print(int(eval(resulting_expression)))
                except:
                    print("failed to eval {}".format(resulting_expression))
                    print(variables_storage_dict)
                    print(received_input_list)
            else:
                try:
                    print(variables_storage_dict[received_input])
                except:
                    print("Unknown variable")



if __name__ == "__main__":
    # while True:
    #     task3_4_processing_received_data(task3_converting_input())
    task6_7_working_with_variables()
