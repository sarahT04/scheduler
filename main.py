from scheduler import Scheduler
from utils import check_UI, return_UC

file_path = 'schedule_weekly.json'

input("Enter to continue..\nCommands are: 'see (day)', 'daily', 'today', 'add/ins', 'delete'")
while True:
    sc = Scheduler(file_path)
    sc.refresh()
    UI = input("\nEnter your command\n> ").lower().split(' ')
    command, day, time = check_UI(UI)
    if command == 'daily':
        print('\nDaily')
        sc.print_schedule(sc.daily_schedules, sc.daily_time)
    elif command == 'today':
        print(f'\nToday - {sc.today}')
        sc.print_schedule(sc.today_schedules, sc.today_time)
    elif command == 'see':
        print('\n' + day)
        sc.see_schedule(day)
    elif command == 'add' or command.startswith('ins'):
        # Enter the schedules
        UC = return_UC()
        # Insert the schedule
        sc.insert_update(day, time, UC)  # day time and schedules
    elif command.startswith('del'):
        UC = return_UC('delete')
        if UC is True:
            sc.delete(day, time)
        # Delete the appointed schedule on day and time
        else:
            sc.delete(day, time, UC)
