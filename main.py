import datetime
import os
import argparse


class Company:
    def __init__(self, name):
        self.__name = name
        self.employees = []

    def add_employee(self, employee):
        if isinstance(employee, Employee):
            self.employees.append(employee)

    def find_best_appointment_time(self, date_, number_of_needed_employees, appointment_time):
        list_of_available_employees = []
        earliest_date_worth_to_check = datetime.datetime.max - datetime.timedelta(hours=100)
        i = 0
        appends_instantly = 0
        date = date_
        while True:
            i += 1
            list_of_available_employees = []
            earliest_date_worth_to_check = datetime.datetime.max - datetime.timedelta(hours=100)
            for employee in self.employees:
                if not len(employee.unavailable):
                    list_of_available_employees.append(employee)
                elif date + appointment_time < employee.unavailable[0]:
                    list_of_available_employees.append(employee)
                elif date > max(employee.unavailable):
                    appends_instantly += 1
                    list_of_available_employees.append(employee)
                else:
                    earliest_date_worth_to_check_has_changed = True
                    prev = None
                    for id_, time in enumerate(employee.unavailable):
                        if prev is None:
                            prev = time
                        else:
                            if id_ % 2:
                                if time > date:
                                    if time + datetime.timedelta(seconds=1) < earliest_date_worth_to_check:
                                        earliest_date_worth_to_check = time + datetime.timedelta(seconds=1)
                                        break
                            else:
                                if time > date:#start
                                    if time >= date + appointment_time:
                                        list_of_available_employees.append(employee)
                                        break
                                    else:
                                        if employee.unavailable[id_ + 1] + datetime.timedelta(seconds=1) < earliest_date_worth_to_check:
                                            earliest_date_worth_to_check = employee.unavailable[id_ + 1] + datetime.timedelta(seconds=1)
                                            break
            if len(list_of_available_employees) >= number_of_needed_employees:
                break
            date = earliest_date_worth_to_check
        if appends_instantly == number_of_needed_employees:
            date = max(employee.unavailable) + datetime.timedelta(seconds=1)
        print(f"Closest available date is : {date}")
        print("Present employees : ", end="")
        for id, emplyee in enumerate(list_of_available_employees):
            if id > 0:
                print(", ", end="")
            print(f"{emplyee}", end="")
        print("\n")
        set_meeting = None
        while set_meeting != 'y' and set_meeting != 'n':
            set_meeting = input("Do you want to set a meeting? [y/n] : ")
        if set_meeting == 'y':
            for employee in list_of_available_employees:
                employee.insert_unavailability_time(date, date + appointment_time)
                employee.unavailable.sort()
                f = open(employee.path, 'a')
                f.writelines("\n" + str(date) + " - " + str(date + appointment_time))
        else:
            next_meeting = None
            while next_meeting != 'y' and next_meeting != 'n':
                next_meeting = input("Do you want to search for other appointment? [y/n] : ")
            if next_meeting == 'y':
                to_remove_dates = [date, date + appointment_time]
                for employee in list_of_available_employees:
                    employee.insert_unavailability_time(date, date + appointment_time)
                    employee.unavailable.sort()
                    employee.print_unavailability_time()
                self.find_best_appointment_time(date + appointment_time, number_of_needed_employees, appointment_time)
                for employee in list_of_available_employees:
                    for el in to_remove_dates:
                        employee.unavailable.remove(el)
        return list_of_available_employees, date


class Employee:
    def __init__(self, name, path):
        self.__name = (name.replace("_", " ")).title()
        self.path = path
        self.unavailable = []

    def insert_unavailability_time(self, begin: datetime, end: datetime):
        self.unavailable.append(begin)
        self.unavailable.append(end)
        self.unavailable.sort()

    def __str__(self):
        return self.__name


def main():
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--calendars', action='store', type=str, required=True)
    my_parser.add_argument('--duration_in_minutes', action='store', type=int, required=True)
    my_parser.add_argument('--minimum_people', action='store', type=int, required=True)
    my_parser.add_argument('--appointment_date', action='store', type=str, required=True)
    args = my_parser.parse_args()
    current_folder = os.getcwd()
    direct_folder = args.calendars.replace("/", "") + "\\"
    file = current_folder + "\\" + args.calendars.replace("/", "")
    without_extra_slash = os.path.normpath(file)
    comp = Company(args.calendars.replace("/", ""))
    list_of_files = list(os.listdir(without_extra_slash))
    list_of_txt_files = [el for el in list_of_files if ".txt" in el]
    for el in list_of_txt_files:
        file_name = el
        x = open(direct_folder + el)
        p1 = Employee(file_name.rsplit(".", 2)[0], direct_folder + file_name)
        for line in x.readlines():
            try:
                # defining if it is all day or few hours
                if len(line) < 15:
                    begin_date = datetime.datetime.strptime(str(line.rstrip("\n")), "%Y-%m-%d")
                    end_date = begin_date + datetime.timedelta(hours=23, minutes=59, seconds=59)
                    p1.insert_unavailability_time(begin_date, end_date)
                else:
                    sep = line.split(" - ", 2)
                    begin = sep[0]
                    end = sep[1]
                    begin_date = datetime.datetime.strptime(begin, "%Y-%m-%d %H:%M:%S")
                    end_date = datetime.datetime.strptime(str(end.rstrip("\n")), "%Y-%m-%d %H:%M:%S")
                    p1.insert_unavailability_time(begin_date, end_date)
            except:
                raise ValueError("Wrong text format")
        comp.add_employee(p1)
    appointment_time = datetime.timedelta(minutes=args.duration_in_minutes)
    appointment_date = datetime.datetime.strptime(str(args.appointment_date), "%Y-%m-%d_%H:%M:%S")
    comp.find_best_appointment_time(appointment_date, args.minimum_people, appointment_time - datetime.timedelta(seconds=1))


if __name__ == '__main__':
    main()
