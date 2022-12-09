# =====importing libraries===========
# Import library to display the date
from datetime import date

# ====Login Section====

usernames = []  # Create two empty lists to store the usernames and passwords separate
passwords = []
user_file = open("user.txt", "r")  # Open the "user.txt" file in read format
file_lines = user_file.readlines()
for line in file_lines:  # Separating each line, indexing them to add the username and passwords
    user_info = (line.strip()).split(", ")  # To the respective lists
    usernames.append(user_info[0].lower())
    passwords.append(user_info[1].lower())

user_file.close()  # Closing the file


# This Function is to create a new user in the "user.txt" file but needs variable username checked beforehand
def reg_user(username):
    if username == "admin":  # Checks if it's the admin
        while True:
            new_username = input("\nPlease enter a new username: ")  # Request new username and password
            if new_username in usernames:
                print("This username already exists.")
                continue
            new_password = input("\nPlease enter your new password: ")
            password_confirm = input("\nPlease confirm your password: ")
            if new_password != password_confirm:  # This checks if the confirmation of password matches
                print("Passwords don't match")
                continue
            else:
                with open("user.txt", "a") as users_file:  # This adds the new user credentials to the user file
                    users_file.write(f"\n{new_username}, {new_password}")
                print(f"\nNew user {new_username} added!\n")
                break
        users_file.close()
    else:
        print("\nSorry, only the admin can use this feature.")  # If the user isn't admin they will get this error


# This Function adds a new task to the "tasks.txt" file
def add_task():
    with open("tasks.txt", "a") as user_task_file:  # opens the "task.txt" file in append mode
        task_user = input("\nWho is the new task being allocated to: ")  # Collects all relevant info from user
        task_title = input("\nWhat is the task title: ")
        task_desc = input("\nPlease give a brief description of the task: ")
        task_due_date = input("\nWhat is the due date for the task: ")
        today = date.today().strftime("%d %b %Y")
        user_task_file.write(f"{task_user}, {task_title}, {task_desc}, {today}, {task_due_date}, No\n")
    print("\nTask added!")  # Write to the file with the new task information, displays a completion message
    user_task_file.close()  # Close the file


# This Function displays all the tasks from "tasks.txt" to the screen
def view_task():
    with open("tasks.txt", "r") as user_task_file:  # Open relevant file in read mode
        tasks = user_task_file.readlines()
        for task in tasks:
            task_line = task.strip().split(", ")  # separates each line using strip and split functions
            print(f'''\nTask to be completed by: \t{task_line[0]}  
Task Title: \t\t\t\t{task_line[1]}
Task Description: \t\t\t{task_line[2]}
Task is due: \t\t\t\t{task_line[4]}
Task Status: \t\t\t\t{task_line[5]}
                    ''')  # use indexing to display the correct info
            user_task_file.close()  # Close the file


# This Function displays all the tasks from "tasks.txt" that are assigned to the user logged in, to the screen
def view_mine():
    saved_tasks = []  # Create an empty list variable to store specific tasks assigned to user
    with open("tasks.txt", "r") as user_task_file:
        tasks = user_task_file.readlines()
        task_iterator = 1  # Create a task iterator to label each task that is displayed
        for task in tasks:
            task_line = task.strip().split(", ")
            if task_line[0] == login_username:  # Using an if statement to determine which info to use
                print(f'''\nTask No.{task_iterator}
Task to be completed by: \t{task_line[0]}
Task Title: \t\t\t\t{task_line[1]}
Task Description: \t\t\t{task_line[2]}
Task is due: \t\t\t\t{task_line[4]}
Task Status: \t\t\t\t{task_line[5]}
                     ''')  # use indexing to display the correct info
                task_iterator += 1
                saved_tasks.append(task_line)

        if not saved_tasks:  # Displays a relevant error message if there are no tasks and returns to the menu
            print("\nYou have no tasks.")
            return

    view_specific_task = int(input("\nWhich Task would you like to view? (e.g. for task No.1 enter 1) or Enter -1 "
                                   "to return to the Main Menu: "))

    while view_specific_task != -1:  # Using a while statement to return to the menu if "-1" is selected
        if view_specific_task in range(task_iterator + 1):  # This if statement displays the task chosen
            print(f'''\nTask No.{view_specific_task}
Task to be completed by: \t{saved_tasks[view_specific_task - 1][0]}
Task Title: \t\t\t\t{saved_tasks[view_specific_task - 1][1]}
Task Description: \t\t\t{saved_tasks[view_specific_task - 1][2]}
Task is due: \t\t\t\t{saved_tasks[view_specific_task - 1][4]}
Task Status: \t\t\t\t{saved_tasks[view_specific_task - 1][5]}
                                         ''')
            complete_or_edit = input("Would you like to mark this task as complete? "
                                     "Or edit this task?(Mark or Edit): ").lower()
            # This if statement changes the task completion selection from "No" to "Yes"
            if complete_or_edit == "mark":
                saved_tasks[view_specific_task - 1][5] = "Yes"
                print("\nThis Task has been up updated to Complete!")  # Lets the user know this change has happened

                tasks_not_assigned_to_user = []  # Create an empty list to and all the other tasks too

                for task in tasks:
                    task_line = task.strip().split(", ")
                    if task_line[0] != login_username:
                        tasks_not_assigned_to_user.append(task_line)

                # This empty list within this for loop is given all the assigned tasks to the user in a format
                # Suitable to be written back to the "tasks.txt" file with the changes made to the completion selection
                all_joined_tasks = []
                for task in saved_tasks:
                    user_joined_tasks = ", ".join(task)
                    all_joined_tasks.append(user_joined_tasks)

                # This is writing to the file all the users tasks
                with open("tasks.txt", "w") as user_task_file:
                    for task in all_joined_tasks:
                        user_task_file.write(f"{task}\n")

                # This is appending the same file with the rest of the tasks for different users
                for task in tasks_not_assigned_to_user:
                    joined_tasks = ", ".join(task)
                    with open("tasks.txt", "a+") as user_task_file:
                        user_task_file.write(f"{joined_tasks}\n")
                break

            # This only edits the task if it is marked incomplete, and can alter task assignment and completion date
            elif complete_or_edit == "edit":
                if saved_tasks[view_specific_task - 1][5] == "No":
                    task_assignment = input("\nWho would you like to assign this task to? ")
                    task_completion = input("\nWhat is the new due date of this task? ")
                    saved_tasks[view_specific_task - 1][0] = task_assignment
                    saved_tasks[view_specific_task - 1][4] = task_completion

                    tasks_not_assigned_to_user = []

                    # This follows the same logic as the above if statement and rewrites the file and appends it.
                    # Displays to the user that these changes have been made.
                    for task in tasks:
                        task_line = task.strip().split(", ")
                        if task_line[0] != login_username:
                            tasks_not_assigned_to_user.append(task_line)

                    all_joined_tasks = []
                    for task in saved_tasks:
                        user_joined_tasks = ", ".join(task)
                        all_joined_tasks.append(user_joined_tasks)

                    with open("tasks.txt", "w") as user_task_file:
                        for task in all_joined_tasks:
                            user_task_file.write(f"{task}\n")

                    for task in tasks_not_assigned_to_user:
                        joined_tasks = ", ".join(task)
                        with open("tasks.txt", "a+") as user_task_file:
                            user_task_file.write(f"{joined_tasks}\n")
                    print(f"\nThis task has been assigned to \033[1m{task_assignment}\033[0m "
                          f"and the new due date is \033[1m{task_completion}\033[0m")
                else:
                    print("\nThis task can not be edited, as it is already complete.")

                    break

        # If they enter and invalid selection an appropriate error message is displayed
        else:
            print("This task does not exist.")
            break

    user_task_file.close()  # Close the file


# This Function takes some statistics from "user.txt" & "tasks.txt" and writes this information to new respective files
def generate_report():
    # Create variables for statistics I want to track from "tasks.txt" and set them all to zero to be appended later
    total_amount_of_tasks = 0
    total_completed_tasks = 0
    total_uncompleted_tasks = 0
    not_complete_and_overdue = 0
    today = date.today().strftime("%d %b %Y")  # Create a variable for today's date in the same format for consistency
    with open("tasks.txt", "r") as user_task_file:
        tasks = user_task_file.readlines()
        for task in tasks:
            total_amount_of_tasks += 1  # Iterate through each line to calculate number of total tasks
            task_line = task.strip().split(", ")
            if task_line[5] == "Yes":  # Iterate through completed tasks to calculate number of tasks
                total_completed_tasks += 1
            elif task_line[5] == "No":  # Iterate through uncompleted tasks to calculate number of tasks
                total_uncompleted_tasks += 1
                if today > task_line[4]:  # This statement leads on from the previous to check if it also overdue
                    not_complete_and_overdue += 1  # Iterates through these and calculate the total amount

    user_task_file.close()

    # Create variables to calculate percentages for the statistical breakdown
    percentage_not_completed = round((total_uncompleted_tasks / total_amount_of_tasks) * 100)
    percentage_overdue = round((not_complete_and_overdue / total_uncompleted_tasks) * 100)

    # Writing to a new file "task_overview.txt" to display in an easy-to-read manner all the statistics calculated
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(f"Task Overview\n"
                                 f"The total number of tasks:                   {total_amount_of_tasks}\n"
                                 f"The total number of completed tasks:         {total_completed_tasks}\n"
                                 f"The total number of uncompleted tasks:       {total_uncompleted_tasks}\n"
                                 f"No. of tasks that are uncompleted & overdue:"
                                 f" {not_complete_and_overdue}\n"
                                 f"Uncompleted percentage:   {percentage_not_completed}%\n"
                                 f"Overdue percentage:       {percentage_overdue}%")

    task_overview_file.close()

    # Create variables for statistics to track from "user.txt" and "tasks.txt", set them all to 0 to be appended later
    number_of_tasks_for_user = 0
    user_completed_tasks = 0
    user_not_complete_and_overdue = 0
    with open("user.txt", "r") as users_file:
        users = users_file.readlines()
        total_amount_of_users = len(users)  # Iterate through the user file to calculate number of users
    users_file.close()

    # checking the username against the tasks this creates statistics for the particular user
    with open("tasks.txt", "r") as user_task_file:
        tasks = user_task_file.readlines()
        for task in tasks:
            task_line = task.strip().split(", ")
            if login_username == task_line[0]:
                number_of_tasks_for_user += 1
                if task_line[5] == "Yes":
                    user_completed_tasks += 1
                elif task_line[5] == "No":
                    total_uncompleted_tasks += 1
                    if today > task_line[4]:
                        user_not_complete_and_overdue += 1
    user_task_file.close()

    # Again create variables to calculate percentages for the statistical breakdown
    percentage_of_tasks_assigned_to_user = round((number_of_tasks_for_user / total_amount_of_tasks) * 100)
    user_completion_percentage = round((user_completed_tasks / number_of_tasks_for_user) * 100)
    user_overdue_percentage = round((user_not_complete_and_overdue / number_of_tasks_for_user) * 100)

    # Writing to a new file "user_overview.txt" to display in an easy-to-read manner all the statistics calculated
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f"User Overview\n"
                                 f"The total number of Users:          {total_amount_of_users}\n"
                                 f"The total number of Tasks:          {total_amount_of_tasks}\n"
                                 f"\n"
                                 f"{login_username} Overview\n"
                                 f"The total number of your tasks:           {number_of_tasks_for_user}\n"
                                 f"Percentage of tasks assigned to you:      {percentage_of_tasks_assigned_to_user}%\n"
                                 f"Task completion percentage:               {user_completion_percentage}%\n"
                                 f"Task Incomplete percentage:               {100 - user_completion_percentage}%\n"
                                 f"Percentage of tasks incomplete & overdue: {user_overdue_percentage}%")
    user_overview_file.close()

    print("\nReport has been generated!")  # Display to the user that this function has been completed


while True:  # Creating a while loop to request the username and password and validate them
    login_username = (input("Please enter your username: ")).lower()
    login_password = (input("\nPlease enter your password: ")).lower()

    if login_username not in usernames:  # If the username doesn't exist program displays an error message
        print("\nThis username is incorrect, please try again.")
        continue
    elif login_username in usernames and login_password not in passwords:  # Also an error if the password is wrong
        print("\nIncorrect Password.")
        continue
    else:  # Otherwise the program displays a welcome message to the user
        print(f"\nWelcome {login_username}!")
        break

number_of_user = 0  # Set counters for the number of lines for the users and tasks files to enumerate them
number_of_tasks = 0

while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    if login_username == "admin":  # if the user is admin they are displayed the menu with extra options
        menu = input('''\nSelect one of the following Options below:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        vm - View my task
        ds - Display Statistics
        gr - Generate Reports
        e - Exit
        : ''').lower()

    else:
        menu = input('''\nSelect one of the following Options below:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        vm - view my task
        gr - Generate Reports
        e - Exit
        : ''').lower()

    if menu == 'r':
        ''' This block checks who the user is, if it is the admin they can add a new user, if not they are displayed
        an error message and taken back to the menu.'''
        reg_user(login_username)

    elif menu == 'a':
        # This block adds a new task to the task file
        add_task()

    elif menu == 'va':
        # This block displays all tasks in the "task.txt" file in an organised fashion
        view_task()

    elif menu == 'vm':
        # This block displays all tasks that the current user has in the "task.txt" file in an organised fashion
        view_mine()

    elif menu == 'ds':
        # This Block calls on the generate_report() function then displays those statistics to the user
        generate_report()
        print()
        # This just opens the files generated from the above function and displays the contents to the screen
        with open("user_overview.txt", "r") as user_overview:
            print(user_overview.read())
        print()
        with open("task_overview.txt", "r") as task_overview:
            print(task_overview.read())

        user_overview.close()
        task_overview.close()

    elif menu == 'gr':
        # This block generates two new files "user_overview.txt" & "task_overview.txt" with relevant statistics
        generate_report()

    elif menu == 'e':  # Display a goodbye message when user decides to exit
        print('\nGoodbye!!!')
        exit()

    else:  # If they enter an invalid choice, displays an error message
        print("You have made a wrong choice, Please Try again")
