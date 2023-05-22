# Write your code here
import json
import re

def get_convert_data_from_json():
    """This function reads JSON from a standard output and loads it"""
    received_data_json = input()
    return json.loads(received_data_json)

def calculating_data_type_errors(loaded_json_data):
    """In this function we iterate through instances of loaded JSON,
    calculate the amount of errors per type and print them"""
    total_errors = 0
    err_bus_id = 0
    err_stop_id = 0
    err_stop_name = 0
    err_next_stop = 0
    err_stop_type = 0
    err_a_time = 0
    for instance in loaded_json_data:
        if isinstance(instance["bus_id"], int) is False:
            err_bus_id += 1
            total_errors += 1
        if isinstance(instance["stop_id"], int) is False:
            err_stop_id += 1
            total_errors += 1
        if isinstance(instance["stop_name"], str) is False or instance["stop_name"] == "":
            err_stop_name += 1
            total_errors += 1
        if isinstance(instance["next_stop"], int) is False:
            err_next_stop += 1
            total_errors += 1
        # if instance["stop_type"] not in ["S", "O", "F"]:
        if isinstance(instance["stop_type"], str) is False or len(instance["stop_type"]) > 1:
            err_stop_type += 1
            total_errors += 1
        if isinstance(instance["a_time"], str) is False or instance["a_time"] == "":
            err_a_time += 1
            total_errors += 1
    # total_errors = err_bus_id + err_stop_id + err_stop_name + err_next_stop + err_stop_type + err_a_time

    print("Type and required field validation: {} errors".format(total_errors))
    print("bus_id: {}".format(err_bus_id))
    print("stop_id: {}".format(err_stop_id))
    print("stop_name: {}".format(err_stop_name))
    print("next_stop: {}".format(err_next_stop))
    print("stop_type: {}".format(err_stop_type))
    print("a_time: {}".format(err_a_time))

def checking_data_format(loaded_json_data):
    """In this function we iterate through instances of loaded JSON,
        check formatting of stop_name, stop_type, a_time"""
    format_validation_total_error = 0
    stop_name_errors = 0
    stop_type_errors = 0
    a_time_errors = 0
    for instance in loaded_json_data:
        if not re.match(r"^[A-Z]\w+\s?\w+?\s(Road|Avenue|Boulevard|Street)$", instance["stop_name"]):
            # print(instance["stop_name"])
            stop_name_errors += 1
            format_validation_total_error += 1
        #if not re.match(r"(F|O|S)", instance["stop_type"]):
        if instance["stop_type"] not in ("S", "O", "F", ""):
            #if len(instance["stop_type"]) > 0:
                # print(instance["stop_type"])
            stop_type_errors += 1
            format_validation_total_error += 1
        if not re.match(r"^([01][0-9]|2[0-3]):([0-5][0-9])$", instance["a_time"]):
            a_time_errors += 1
            format_validation_total_error += 1
    print("Format validation: {} errors".format(format_validation_total_error))
    print("stop_name: {}".format(stop_name_errors))
    print("stop_type: {}".format(stop_type_errors))
    print("a_time: {}".format(a_time_errors))

def counting_bus_stops(loaded_json_data):
    """In this function we iterate through instances of loaded JSON,
        we count stops for each bus ID by creating a new dictionary"""
    bus_lines_n_stops_dict = {}
    for instance in loaded_json_data:
        # if bus ID isn't registered, add it to dictionary
        if instance["bus_id"] not in bus_lines_n_stops_dict:
            bus_lines_n_stops_dict[instance["bus_id"]] = 1
            print(bus_lines_n_stops_dict)
        else:
            bus_lines_n_stops_dict[instance["bus_id"]] += 1
            print(bus_lines_n_stops_dict)
    # print(bus_lines_n_stops_dict)
    print("Line names and number of stops:")
    for key in bus_lines_n_stops_dict.keys():
        # print(key, bus_lines_n_stops_dict[key])
        print("bus_id: " + str(key) + ", stops: " + str(bus_lines_n_stops_dict[key]))

def task4_getting_invalid_lines(loaded_json_data):
    """Getting lines that don't have start and/or finish"""
    bus_lines_n_types = {}
    list_of_stop_types = []
    for instance in loaded_json_data:
        if instance["bus_id"] in bus_lines_n_types:
            bus_lines_n_types[instance["bus_id"]] = bus_lines_n_types[instance["bus_id"]] + instance["stop_type"]
        else:
            bus_lines_n_types[instance["bus_id"]] = instance["stop_type"]
    # print(bus_lines_n_types)
    for bus_id, avail_stops in bus_lines_n_types.items():
        # print(bus_id, avail_stops)
        if avail_stops.count('S') != 1 or avail_stops.count('F') != 1:
            print("There is no start or end stop for the line: {}.".format(bus_id))
            exit()

def task4_counting_start_stop_transfer(loaded_json_data):
    set_of_start_stops = set()
    set_of_finish_stops = set()
    set_of_transfer_stops = set()
    bus_lines_stops_names = {}
    for instance in loaded_json_data:
        if instance["stop_type"] == "S":
            set_of_start_stops.add(instance["stop_name"])
        if instance["stop_type"] == "F":
            set_of_finish_stops.add(instance["stop_name"])
        if instance["stop_type"] == "O" or instance["stop_type"] == "":
            if instance["bus_id"] in bus_lines_stops_names:
                bus_lines_stops_names[instance["bus_id"]] = bus_lines_stops_names[instance["bus_id"]] + "," + instance["stop_name"]
            else:
                bus_lines_stops_names[instance["bus_id"]] = instance["stop_name"]

    for key in bus_lines_stops_names:
        bus_lines_stops_names[key] = set(bus_lines_stops_names[key].split(","))
    for key1 in bus_lines_stops_names:
        for key2 in bus_lines_stops_names:
            # print(bus_lines_stops_names[key1], bus_lines_stops_names[key2])
            if key1 != key2:
                common_stops = bus_lines_stops_names[key1].intersection(bus_lines_stops_names[key2])
                set_of_transfer_stops.update(common_stops)

    # print("Start stops: {} {}".format(len(set_of_start_stops), sorted(list(set_of_start_stops))))
    # print("Transfer stops: {} {}".format(len(set_of_transfer_stops), sorted(set_of_transfer_stops)))
    # print("Finish stops: {} {}".format(len(set_of_finish_stops), sorted(list(set_of_finish_stops))))
    return set_of_start_stops | set_of_finish_stops | set_of_transfer_stops

def task5_checking_time(loaded_json_data):
    print("Arrival time test:")
    previous_bus_id = 0
    previous_time_hours = 0
    previous_time_minutes = 0
    flag_all_correct = True
    dictionary_with_faulty_times = {}
    for instance in loaded_json_data:
        if instance["bus_id"] == previous_bus_id:
            if int(instance["a_time"][0:2]) < previous_time_hours or (int(instance["a_time"][0:2]) == previous_time_hours and int(instance["a_time"][3:5]) < previous_time_minutes):
                if instance["bus_id"] not in dictionary_with_faulty_times:
                    dictionary_with_faulty_times[instance["bus_id"]] = instance["stop_name"]
                flag_all_correct = False
        previous_bus_id = instance["bus_id"]
        previous_time_hours = int(instance["a_time"][0:2])
        previous_time_minutes = int(instance["a_time"][3:5])

    if flag_all_correct is True:
        print("OK")
    else:
        # print(dictionary_with_faulty_times)
        for bus_id, stop_name in dictionary_with_faulty_times.items():
            print("bus_id line {}: wrong time on station {}".format(bus_id, stop_name))

def task6_checking_invalid_ondemand(loaded_json_data, set_of_forbidden_stops):
    print(set_of_forbidden_stops)
    print("On demand stops test:")
    set_of_invalid_stops = set()

    for instance in loaded_json_data:
        if instance["stop_type"] == "O" and instance["stop_name"] in set_of_forbidden_stops:
            set_of_invalid_stops.add(instance["stop_name"])

    if len(set_of_invalid_stops) == 0:
        print("OK")
    elif len(set_of_invalid_stops) > 0:
        print("Wrong stop type: {}".format(sorted(list(set_of_invalid_stops))))

if __name__ == "__main__":
    prepared_json_data = get_convert_data_from_json()
    # calculating_data_type_errors(prepared_json_data)
    # checking_data_format(prepared_json_data)
    # counting_bus_stops(prepared_json_data)
    # task4_getting_invalid_lines(prepared_json_data)
    # task4_counting_start_stop_transfer(prepared_json_data)
    # task5_checking_time(prepared_json_data)
    task6_checking_invalid_ondemand(prepared_json_data, task4_counting_start_stop_transfer(prepared_json_data))
