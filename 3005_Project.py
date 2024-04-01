import psycopg
from datetime import datetime

continueProgram = True
userChoice = 0
userTable = ""
userID = -1
userFN = ""
userLN = ""
userGoalWeight = ""
userCurrWeight = ""
userBMI = ""

def showMenu(title, options):
    choice = -1

    print(title)
    
    while(choice < 0 or choice > len(options) - 1):
        for i in range(len(options)):
            print(str(i) + ": " + options[i])
        choice = int(input("YOUR CHOICE: "))

        if(choice < 0 or choice > len(options) - 1):
            print("ERROR: Invalid input")

        print("")

    return choice

def registerMember(conn, curs, fn, ln, goalWeight, currWeight, bmi):
    time = str(datetime.now())
    curs.execute("INSERT INTO Members (member_id, first_name, last_name, goal_weight, current_weight, bmi, registration_time) VALUES (DEFAULT, '" + fn + "', '" + ln + "', " + goalWeight + ", " + currWeight + ", " + bmi + ", '" + time + "')")
    conn.commit()
    curs.execute("SELECT member_id FROM Members WHERE registration_time = '" + time + "'")

    memberID = str(cursor.fetchone()).strip("(),")
    print("Your user ID number is: " + memberID)

    return memberID

def manageMemberProfile(conn, curs, memberID):
    memberInput = ""
    choice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Change First Name", "Change Last Name", "Change Weight", "Change Goal Weight", "Change BMI"])

    if(choice == 0):
        memberInput = input("Enter new first name: ")
        curs.execute("UPDATE Members SET first_name = '" + memberInput + "' WHERE member_id = " + memberID)
    elif(choice == 1):
        memberInput = input("Enter new last name: ")
        curs.execute("UPDATE Members SET last_name = '" + memberInput + "' WHERE member_id = " + memberID)
    elif(choice == 2):
        memberInput = input("Enter your current weight: ")
        curs.execute("UPDATE Members SET current_weight = " + memberInput + " WHERE member_id = " + memberID)
    elif(choice == 3):
        memberInput = input("Enter new goal weight: ")
        curs.execute("UPDATE Members SET goal_weight = " + memberInput + " WHERE member_id = " + memberID)
    else:
        memberInput = input("Enter your current BMI: ")
        curs.execute("UPDATE Members SET bmi = " + memberInput + " WHERE member_id = " + memberID)

    conn.commit()

def displayDashboard(conn, curs, memberID):
    #INSERT EXCERCISE ROUTINE STUFF HERE
    
    curs.execute("SELECT current_weight FROM Members WHERE member_id = " + memberID)
    currentWeight = str(curs.fetchone()).strip("(),")
    curs.execute("SELECT goal_weight FROM Members WHERE member_id = " + memberID)
    goalWeight = str(curs.fetchone()).strip("(),")
    weightDiff = abs(int(currentWeight) - int(goalWeight))

    print("You are only " + str(weightDiff) + " lbs away from your goal weight!")

    curs.execute("SELECT bmi FROM Members WHERE member_id = " + memberID)
    print("Your current bmi is: " + str(curs.fetchone()).strip("(),"))

try:
    connection = psycopg.connect("dbname=3005_Project user=postgres password=ILove3005")
except BaseException:
    # Print an error if the database could not be connected to
    print("ERROR! Could not connect to database")
else:
    cursor = connection.cursor() # Creates a cursor which allows us to run queries on the database

    userChoice = showMenu("WHAT IS YOUR ROLE?", ["Member", "Trainer", "Admin"])

    if(userChoice == 0):
        userTable = "Members"

        userChoice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Login", "Register"])

        if(userChoice == 0):
            userID = input("What is your member ID? ")
            cursor.execute("SELECT * FROM Members WHERE member_id = " + userID)
            print("")

            while(cursor.rowcount == 0):
                print("ERROR: ID number does not belong to any member.")
                
                userID = input("What is your member ID? ")
                cursor.execute("SELECT * FROM Members WHERE member_id = " + userID)
                print("")
        else:
            userFN = input("What is your first name? ")
            userLN = input("What is your last name? ")
            userGoalWeight = input("What is your goal weight? ")
            userCurrWeight = input("What is your current weight? ")
            userBMI = input("What is your BMI? ")

            userID = registerMember(connection, cursor, userFN, userLN, userGoalWeight, userCurrWeight, userBMI)

        userChoice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Manage Profile", "Display Dashboard", "Manage Schedule"])

        if(userChoice == 0):
            manageMemberProfile(connection, cursor, userID)
        elif(userChoice == 1):
            displayDashboard(connection, cursor, userID)

    connection.close() # Closes the connection to the database
