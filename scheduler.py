import json


class Scheduler:

    def __init__(self, filename):
        self.filename = filename
        self.days = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
        self.presets = ['def', 'def', 'def', 'def']  # will be implemented in the future
        with open(filename) as f:
            self.file = json.load(f)
        # this is for daily
        self.daily_schedules = []  # this gets the schedules in daily
        self.daily_time = []  # and also its respective time
        # this is for weekly
        self.today = ''
        self.today_schedules = []
        self.today_time = []
        self.today_schedule_dict = {}

    def save(self) -> None:
        """
        Saves to the JSON file
        """
        with open(self.filename, 'w') as f:
            json.dump(self.file, f)


    def refresh(self) -> None:
        """
        The main purpose of this method is to refresh the schedule on every While Loop.
        :return: Refreshed daily and weekly schedule
        """
        # daily schedule
        daily_dict = self.file["Daily"]["schedule"]
        for i in sorted(daily_dict.keys()):
            self.daily_time.append(i)
            self.daily_schedules.append(daily_dict[i])

        # weekly schedule
        from datetime import datetime
        self.today = self.days[datetime.today().weekday()]  # Get the day abbreviation.
        self.today_schedule_dict = self.file[self.today]["schedule"]
        for i in sorted(self.today_schedule_dict.keys()):
            self.today_time.append(i)
            self.today_schedules.append(self.today_schedule_dict[i])

    def see_schedule(self, day: str) -> None:
        """
        :param day: See which day of schedule
        :return: printed schedule
        """
        if day == 'Today':
            day = self.today
        try:
            day_schedule_dict = self.file[day]["schedule"]
            self.print_schedule(list(day_schedule_dict.values()), list(day_schedule_dict.keys()))
        except KeyError:
            print("Key error! It doesn't exist!")

    @staticmethod
    def print_schedule(schedule: list, time: list) -> None:
        """
        :param schedule: schedules list
        :param time: time list
        :return: this will parse and print the date, what time, and the schedule
        """
        if len(schedule) == 0:
            print('Nothing to show yet...\n')
        else:
            print()
            for i in range(len(schedule)):
                print(time[i])
                for t, j in enumerate(schedule[i], 1):
                    print(f'{t}. {j}')
                print()

    def insert_update(self, day: str, time: str, schedule: list) -> None:
        """
        :param day: the day of the schedule
        :param time: the time of the schedule
        :param schedule: list
        :return: inserting to the json
        """
        count = 0
        if day == 'Today':
            day = self.today
        for item in schedule:
            try:  # this will update them
                # Example : {"Wed": {"schedule": {'12:00' : ['Brush teeth']}}}
                json_schedule = self.file[day]["schedule"][time]
                if item not in json_schedule:
                    json_schedule += [item]
                    count += 1
                else:  # this happens if schedule is already in schedule
                    print(f"Schedule: '{item}' is already in schedule. Discarding..")
            except KeyError:  # this will insert schedule
                self.file[day]["schedule"][time] = [item]
                count += 1
        if count:
            print(f"Succesfully updated {count} schedule.")
        self.save()

    def delete(self, day: str, time: str, schedule=None) -> None:
        """
        :param day: the day of the schedule
        :param time: the time of the schedule
        :param schedule: list or None which means delete all schedule
        :return: deleting to the json
        """
        if day == 'Today':
            day = self.today
        if schedule is None:  # if it doesnt specify any schedule, delete everything
            del self.file[day]["schedule"][time]
            print(f"Succesfully deleted all schedule from day and time of: {day}, {time}")
        else:
            print(f"Deleting schedules from {day}, with time: {time}")
            for i in schedule:
                try:
                    # I am deleting schedule from its index.
                    i = int(i)
                    try:
                        del self.file[day]["schedule"][time][i - 1]  # delete if by index
                        print(f"Successfully deleted schedule #{i}")
                    except ValueError:
                        print(f"Value '{str(i)}' not in the dictionary. Exiting...")
                except ValueError:
                    # Deleting schedule from its schedule.
                    try:
                        # I have to use index because I am deleting from a list.
                        index = self.file[day]["schedule"][time].index(i)  # delete if by the schedule
                        print(f"Succesfully deleted schedule '{self.file[day]['schedule'][time][index]}'.")
                        del self.file[day]["schedule"][time][index]
                    except ValueError:
                        print(f"Value '{i}' not in the dictionary. Exiting...")
            # Checks if nothing is in schedule and deletes it
            if not self.file[day]["schedule"][time]:
                del self.file[day]["schedule"][time]
        # Saves it.
        self.save()
