# Deleting or inserting prompt
def return_UC(arg=''):
    UC = []
    if arg == '':
        arg = 'insert'
    for i in range(1, 11):
        schedule_input = input(f"Enter schedule you want to {arg} (#{i}/10): ")
        if not end_schedule(schedule_input.lower()):
            UC.append(schedule_input)
        elif end_schedule(schedule_input.lower()):  # If user finished inputting their schedule
            break
        if arg == 'delete':
            if schedule_input == 'all':
                return True
    return UC


# User command errors and stuffs
def check_UI(UI: list):
    command = UI[0]
    command_list = ['add', 'insert', 'delete', 'see', 'daily', 'today']
    if command not in command_list:
        return print("Unknown command.")
    if command == 'today' or command == 'daily':
        return command, None, None
    try:
        day = UI[1].title()
    except IndexError:
        day = input("What day?\n> ").title()
    if command == 'see':
        return command, day, None
    try:
        time = UI[2].title()
    except IndexError:
        time = input("What time?\n> ").title()
    return command, day, time


def end_schedule(word):
    return True if word == 'end' or word == 'stop' or word == 'done' else False
