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

    print("Only " + str(weightDiff) + " lbs away from goal weight.")

    curs.execute("SELECT bmi FROM Members WHERE member_id = " + memberID)
    print("Current bmi is: " + str(curs.fetchone()).strip("(),"))

def manageMemberSchedule(conn, curs, memberID):
    #choice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Schedule Personal Training Session", "Register For Group Fitness Class"])

    #if(choice == 0):
        #weekDay = ""
        #choice = showMenu("WHICH DAY WOULD YOU LIKE TO ADD AVAILABILITY FOR?", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

        #if(choice == 0):
        #    weekDay = "Monday"
        #elif(choice == 1):
        #    weekDay = "Tuesday"
        #elif(choice == 2):
        #    weekDay = "Wednesday"
        #elif(choice == 3):
        #    weekDay = "Thursday"
        #else:
        #    weekDay = "Friday"

        #startTime = showMenu("WHEN WOULD YOU LIKE YOUR SESSION TO START (Availability will go from this time to 2 hours ahead)?", ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"])
        #endTime = startTime + 2
        #if(endTime > 23):
        #    endTime -= 24
        
        #curs.execute("SELECT trainer_id, FROM Availabilities WHERE day_of_week = '" + weekDay + "' AND start_time <= " + startTime + " AND end_time >= " + endTime)
        #cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").replace("datetime.time", "").split(", ")
        #avList = []
    
        #for index, element in enumerate(cursList[::6]):
        #    avList.append(cursList[6 * index + 1] + ", START TIME: " + "%02d" % int(cursList[6 * index + 2]) + ":" + "%02d" % int(cursList[6 * index + 3]) + ", END TIME: " + "%02d" % int(cursList[6 * index + 4]) + ":" + "%02d" % int(cursList[6 * index + 5]))
        
        #trainerChoice = showMenu("REMOVE WHICH AVAILABILITY SLOT?", avList)
        #avID = cursList[trainerChoice * 2]

        #curs.execute("DELETE FROM Availabilities WHERE availability_id = " + avID)
        #conn.commit()

def manageTrainerSchedule(conn, curs, trainerID):
    choice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Remove Availability", "Add Availability"])

    if(choice == 0):
        curs.execute("SELECT availability_id, day_of_week, start_time, end_time FROM Availabilities WHERE trainer_id = " + trainerID)
        cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").replace("datetime.time", "").split(", ")
        avList = []
    
        for index, element in enumerate(cursList[::6]):
            avList.append(cursList[6 * index + 1] + ", START TIME: " + "%02d" % int(cursList[6 * index + 2]) + ":" + "%02d" % int(cursList[6 * index + 3]) + ", END TIME: " + "%02d" % int(cursList[6 * index + 4]) + ":" + "%02d" % int(cursList[6 * index + 5]))
        
        trainerChoice = showMenu("REMOVE WHICH AVAILABILITY SLOT?", avList)
        avID = cursList[trainerChoice * 2]

        curs.execute("DELETE FROM Availabilities WHERE availability_id = " + avID)
        conn.commit()
    else:
        weekDay = ""
        choice = showMenu("WHICH DAY WOULD YOU LIKE TO ADD AVAILABILITY FOR?", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

        if(choice == 0):
            weekDay = "Monday"
        elif(choice == 1):
            weekDay = "Tuesday"
        elif(choice == 2):
            weekDay = "Wednesday"
        elif(choice == 3):
            weekDay = "Thursday"
        else:
            weekDay = "Friday"

        startTime = showMenu("WHEN WOULD YOU LIKE YOUR AVAILABILITY TO START (Availability will go from this time to 6 hours ahead)?", ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"])
        endTime = startTime + 6
        if(endTime > 23):
            endTime -= 24

        curs.execute("INSERT INTO Availabilities (availability_id, trainer_id, day_of_week, start_time, end_time) VALUES (DEFAULT, " + trainerID + ", '" + weekDay + "', '" + str(startTime) + ":00', '" + str(endTime) + ":00')")
        conn.commit()
        
def viewMember(conn, curs):
    ln = input("What is the last name of the member who's profile you would like to view? ")
    curs.execute("SELECT member_id, first_name, last_name FROM Members WHERE last_name = '" + ln + "'")
    print("")

    while(cursor.rowcount == 0):
        print("ERROR: Last name number does not belong to any member.")
                
        ln = input("What is the last name of the member who's profile you would like to view? ")
        curs.execute("SELECT member_id, first_name, last_name FROM Members WHERE last_name = '" + ln + "'")
        print("")

    cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").split(", ")
    memberList = []
    
    for index, element in enumerate(cursList[::2]):
        memberList.append(cursList[2 * index + 1] + ", member ID: " + element)
        
    trainerChoice = showMenu("WHICH MEMBER'S PROFILE WOULD YOU LIKE TO VIEW?", memberList)
    memberID = cursList[trainerChoice * 2]

    print(cursList[trainerChoice * 2 + 1] + "'s Dashboard:")
    displayDashboard(conn, curs, memberID)
    
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
            
    elif(userChoice == 1):
        userTable = "Trainers"

        userID = input("What is your trainer ID? ")
        cursor.execute("SELECT * FROM Trainers WHERE trainer_id = " + userID)
        print("")

        while(cursor.rowcount == 0):
            print("ERROR: ID number does not belong to any member.")
                
            userID = input("What is your member ID? ")
            cursor.execute("SELECT * FROM Trainers WHERE trainer_id = " + userID)
            print("")

        userChoice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Manage Schedule", "View Member Profile"])

        if(userChoice == 0):
            manageTrainerSchedule(connection, cursor, userID)
        elif(userChoice == 1):
            viewMember(connection, cursor)

    connection.close() # Closes the connection to the database
