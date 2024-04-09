import psycopg
from datetime import datetime

continueProgram = True
userChoice = 0
userTable = ""
userID = -1

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

def registerMember(conn, curs):
    fn = input("What is your first name? ")
    ln = input("What is your last name? ")
    goalWeight = input("What is your goal weight? ")
    currWeight = input("What is your current weight? ")
    bmi = input("What is your BMI? ")
            
    time = str(datetime.now())
    curs.execute("INSERT INTO Members (member_id, first_name, last_name, goal_weight, current_weight, bmi, registration_time) VALUES (DEFAULT, '" + fn + "', '" + ln + "', " + goalWeight + ", " + currWeight + ", " + bmi + ", '" + time + "')")
    conn.commit()
    curs.execute("SELECT member_id FROM Members WHERE registration_time = '" + time + "'")

    memberID = str(cursor.fetchone()).strip("(),")
    print("\nProfile created! Your user ID number is: " + memberID + "\n")

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

    print("\nProfile successfully updated!\n")
    conn.commit()

def displayDashboard(conn, curs, memberID):
    curs.execute("SELECT current_weight FROM Members WHERE member_id = " + memberID)
    currentWeight = str(curs.fetchone()).strip("(),")
    curs.execute("SELECT current_weight FROM Members WHERE member_id = " + memberID)
    currentWeight = str(curs.fetchone()).strip("(),")
    curs.execute("SELECT goal_weight FROM Members WHERE member_id = " + memberID)
    goalWeight = str(curs.fetchone()).strip("(),")
    weightDiff = abs(int(currentWeight) - int(goalWeight))

    curs.execute("SELECT first_name, last_name FROM Members WHERE member_id = " + memberID)
    name = str(curs.fetchone()).replace(",", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "")    
    print(name + "'s Dashboard:\n")

    print(name + "'s routines:")
    curs.execute("SELECT class_id FROM Registrations WHERE member_id = " + memberID)
    cursList = []
    
    if(curs.rowcount == 0):
        print("NONE")
    elif(curs.rowcount == 1):
        cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").replace(",", "")
    else:
        cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").split(", ")
        
    for element in cursList:
        curs.execute("SELECT class_name FROM Classes WHERE class_id = " + element)
        print("- " + str(curs.fetchone()).replace("(", "").replace(")", "").replace("'", "").replace(",", ""))
    
    print(name + " is only " + str(weightDiff) + " lbs away from their goal weight!")

    curs.execute("SELECT bmi FROM Members WHERE member_id = " + memberID)
    print(name + "'s current bmi is: " + str(curs.fetchone()).strip("(),") + "\n")

def manageMemberSchedule(conn, curs, memberID):
    choice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Schedule Personal Training Session", "Register For Group Fitness Class"])

    if(choice == 0):
        choice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Sign Up For Personal Training Session", "Reschedule Personal Training Session", "Cancel Personal Training Session"])
        if(choice == 0):
            weekDay = ""
            choice = showMenu("WHICH DAY OF THE WEEK WOULD YOU LIKE TO BOOK A SESSION FOR?", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

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

            startTime = 6 + showMenu("WHEN WOULD YOU LIKE YOUR SESSION TO START (Availability will go from this time to 2 hours ahead)?", ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"])
            endTime = startTime + 2
                
            curs.execute("SELECT trainer_id FROM Availabilities WHERE day_of_week = '" + weekDay + "' AND start_time <= '" + str(startTime) + ":00' AND end_time >= '" + str(endTime) + ":00' GROUP BY trainer_id EXCEPT SELECT trainer_id FROM Sessions sessions WHERE start_time = '" + str(startTime) + ":00' OR start_time = '" + str(startTime + 1) + ":00' OR start_time = '" + str(startTime - 1) + ":00' GROUP BY trainer_id")
            cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").replace(",", "").split(", ")

            if(curs.rowcount == 0):
                print("ERROR: NO TRAINERS AVAILABLE FOR THE DAY/TIME DESIRED")
            else:
                avList = []
                    
                for index, element in enumerate(cursList):
                    curs.execute("SELECT first_name, last_name FROM Trainers WHERE trainer_id = " + cursList[index])
                    avList.append(str(curs.fetchone()).replace(",", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", ""))

                memberChoice = showMenu("WHICH TRAINER WOULD YOU LIKE FOR YOUR SESSION?", avList)
                trainerID = cursList[memberChoice]

                print("Session successfully scheduled!")
                curs.execute("INSERT INTO Sessions (session_id, trainer_id, member_id, day_of_week, start_time) VALUES (DEFAULT, " + trainerID + ", " + memberID + ", '" + weekDay + "', '" + str(startTime) + ":00')")
                conn.commit()
        elif(choice == 1):
            curs.execute("SELECT session_id, trainer_id, day_of_week, start_time FROM Sessions WHERE member_id = " + str(memberID))
            cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").replace("datetime.time", "").split(", ")

            if(curs.rowcount == 0):
                print("ERROR: YOU HAVE NO SCHEDULED SESSIONS")
            else:
                avList = []
                
                for index, element in enumerate(cursList[::5]):
                    curs.execute("SELECT first_name, last_name FROM Trainers WHERE trainer_id = " + cursList[5 * index + 1])
                    avList.append("%02d" % int(cursList[5 * index + 3]) + ":" + "%02d" % int(cursList[5 * index + 4]) + " | Every " + cursList[5 * index + 2] + " with " + str(curs.fetchone()).replace(",", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", ""))

                memberChoice = showMenu("WHICH SESSION WOULD YOU LIKE TO RESCHEDULE?", avList)
                sessionID = cursList[5 * memberChoice]
                trainerID = cursList[5 * memberChoice + 1]

                weekDay = ""
                choice = showMenu("WHICH DAY OF THE WEEK WOULD YOU LIKE TO BOOK A RESCHEDULE ON?", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

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

                startTime = 6 + showMenu("WHEN WOULD YOU LIKE YOUR SESSION TO START (Availability will go from this time to 2 hours ahead)?", ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"])
                endTime = startTime + 2

                curs.execute("SELECT trainer_id FROM Availabilities WHERE day_of_week = '" + weekDay + "' AND start_time <= '" + str(startTime) + ":00' AND end_time >= '" + str(endTime) + ":00' AND trainer_id = " + str(trainerID) + " GROUP BY trainer_id EXCEPT SELECT trainer_id FROM Sessions sessions WHERE session_id != " + str(sessionID) + " AND (start_time = '" + str(startTime) + ":00' OR start_time = '" + str(startTime + 1) + ":00' OR start_time = '" + str(startTime - 1) + ":00') GROUP BY trainer_id")
                cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").replace(",", "").split(", ")

                if(curs.rowcount == 0):
                    print("ERROR: TRAINER NOT AVAILABLE FOR THE DAY/TIME DESIRED")
                else:
                    print("Session successfully rescheduled!")
                    curs.execute("UPDATE Sessions SET start_time = '" + str(startTime) + ":00' WHERE session_id = " + sessionID)
                    conn.commit()
        else:
            curs.execute("SELECT session_id, trainer_id, day_of_week, start_time FROM Sessions WHERE member_id = " + str(memberID))
            cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").replace("datetime.time", "").split(", ")

            if(curs.rowcount == 0):
                print("ERROR: YOU HAVE NO SCHEDULED SESSIONS")
            else:
                avList = []
                
                for index, element in enumerate(cursList[::5]):
                    curs.execute("SELECT first_name, last_name FROM Trainers WHERE trainer_id = " + cursList[5 * index + 1])
                    avList.append("%02d" % int(cursList[5 * index + 3]) + ":" + "%02d" % int(cursList[5 * index + 4]) + " | Every " + cursList[5 * index + 2] + " with " + str(curs.fetchone()).replace(",", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", ""))

                memberChoice = showMenu("WHICH SESSION WOULD YOU LIKE TO CANCEL?", avList)
                sessionID = cursList[5 * memberChoice]

                print("Session successfully cancelled!")
                curs.execute("DELETE FROM Sessions WHERE session_id = " + sessionID)
                conn.commit()

    else:
        curs.execute("SELECT class_id, class_name, class_day, start_time, end_time FROM Classes")
        cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "").replace("datetime.time", "").split(", ")
        avList = []
            
        if(curs.rowcount == 0):
            print("NO CLASSES CURRENTLY AVAILABLE")
        else:
            for index, element in enumerate(cursList[::7]):
                avList.append(cursList[7 * index + 1] + " | Every " + cursList[7 * index + 2] + " from " + "%02d" % int(cursList[7 * index + 3]) + ":" + "%02d" % int(cursList[7 * index + 4]) + " to " + "%02d" % int(cursList[7 * index + 5]) + ":" + "%02d" % int(cursList[7 * index + 6]))

            avList.insert(0, "None")
            memberChoice = showMenu("WHICH CLASS WOULD YOU LIKE TO SIGN UP FOR?", avList)

            if(memberChoice != 0):
                classID = cursList[7 * (memberChoice - 1)]
                
                curs.execute("INSERT INTO Registrations (registration_id, class_id, member_id) VALUES (DEFAULT, " + classID + ", " + memberID + ")")
                conn.commit()

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

        startTime = 6 + showMenu("WHEN WOULD YOU LIKE YOUR AVAILABILITY TO START (Availability will go from this time to 6 hours ahead)?", ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"])
        endTime = startTime + 6

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
            userID = registerMember(connection, cursor)
            
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

    while(continueProgram):
        if(userTable == "Members"):
            userChoice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Manage Profile", "Display Dashboard", "Manage Schedule", "QUIT"])

            if(userChoice == 0):
                manageMemberProfile(connection, cursor, userID)
            elif(userChoice == 1):
                displayDashboard(connection, cursor, userID)
            elif(userChoice == 2):
                manageMemberSchedule(connection, cursor, userID)
            else:
                continueProgram = False;
        elif(userTable == "Trainers"):
            userChoice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Manage Schedule", "View Member Profile", "QUIT"])

            if(userChoice == 0):
                manageTrainerSchedule(connection, cursor, userID)
            elif(userChoice == 1):
                viewMember(connection, cursor)
            else:
                continueProgram = False;

    connection.close() # Closes the connection to the database
