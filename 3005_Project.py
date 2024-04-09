import psycopg
from datetime import datetime

continueProgram = True
userChoice = 0
userTable = ""
userID = -1

def showMenu(title, options):
    choice = -1

    print(title)
    
    # While the user has not given a valid input to the menu, ask them for a valid response
    while(choice < 0 or choice > len(options) - 1):
        for i in range(len(options)):
            print(str(i) + ": " + options[i])
        choice = int(input("YOUR CHOICE: "))

        if(choice < 0 or choice > len(options) - 1):
            print("\nERROR: Invalid input\n") # Tell the user the reason for the error

    return choice

def registerMember(conn, curs):
    # Get input from the user required to register them
    fn = input("What is your first name? ")
    ln = input("What is your last name? ")
    goalWeight = input("What is your goal weight? ")
    currWeight = input("What is your current weight? ")
    bmi = input("What is your BMI? ")
    
    # Insert this new member into the Members table
    time = str(datetime.now())
    curs.execute("INSERT INTO Members (member_id, first_name, last_name, goal_weight, current_weight, bmi, registration_time) VALUES (DEFAULT, '" + fn + "', '" + ln + "', " + goalWeight + ", " + currWeight + ", " + bmi + ", '" + time + "')")
    conn.commit()
    
    # Get this new user's member id so that the application can tell them how to log in
    curs.execute("SELECT member_id FROM Members WHERE registration_time = '" + time + "'")
    memberID = str(cursor.fetchone()).strip("(),")
    print("\nProfile created! Your user ID number is: " + memberID + ". Log in with this ID whenever you want to log in!\n")

    return memberID

def manageMemberProfile(conn, curs, memberID):
    memberInput = ""
    choice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Change First Name", "Change Last Name", "Change Weight", "Change Goal Weight", "Change BMI"])

    if(choice == 0):
        # Update this member's first name
        memberInput = input("Enter new first name: ")
        curs.execute("UPDATE Members SET first_name = '" + memberInput + "' WHERE member_id = " + memberID)
    elif(choice == 1):
        # Update this member's first name
        memberInput = input("Enter new last name: ")
        curs.execute("UPDATE Members SET last_name = '" + memberInput + "' WHERE member_id = " + memberID)
    elif(choice == 2):
        # Update this member's first name
        memberInput = input("Enter your current weight: ")
        curs.execute("UPDATE Members SET current_weight = " + memberInput + " WHERE member_id = " + memberID)
    elif(choice == 3):
        # Update this member's first name
        memberInput = input("Enter new goal weight: ")
        curs.execute("UPDATE Members SET goal_weight = " + memberInput + " WHERE member_id = " + memberID)
    else:
        # Update this member's first name
        memberInput = input("Enter your current BMI: ")
        curs.execute("UPDATE Members SET bmi = " + memberInput + " WHERE member_id = " + memberID)

    print("\nProfile successfully updated!\n")
    conn.commit() # Commit changes to database

def displayDashboard(conn, curs, memberID):
    # Get member's current weight
    curs.execute("SELECT current_weight FROM Members WHERE member_id = " + memberID)
    currentWeight = str(curs.fetchone()).strip("(),")
    # Get member's goal weight
    curs.execute("SELECT goal_weight FROM Members WHERE member_id = " + memberID)
    goalWeight = str(curs.fetchone()).strip("(),")
    weightDiff = abs(int(currentWeight) - int(goalWeight)) # Calculate how far the member is from their goal weight
    # Get member's name
    curs.execute("SELECT first_name, last_name FROM Members WHERE member_id = " + memberID)
    name = str(curs.fetchone()).replace(",", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "")    
    
    print(name + "'s Dashboard:\n")

    print(name + "'s routines:")
    # Get all ids of classes that this user is registered for
    curs.execute("SELECT class_id FROM Registrations WHERE member_id = " + memberID)
    cursList = []
    
    if(curs.rowcount == 0):
        print("NONE")
    elif(curs.rowcount == 1):
        cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").replace(",", "")
    else:
        cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").split(", ")
    
    # Print all names of classes that member is registered in
    for element in cursList:
        curs.execute("SELECT class_name FROM Classes WHERE class_id = " + element)
        print("- " + str(curs.fetchone()).replace("(", "").replace(")", "").replace("'", "").replace(",", ""))
    
    print(name + " is only " + str(weightDiff) + " lbs away from their goal weight!")
  
    # Get and print member's bmi
    curs.execute("SELECT bmi FROM Members WHERE member_id = " + memberID)
    print(name + "'s current bmi is: " + str(curs.fetchone()).strip("(),") + "\n")

def manageMemberSchedule(conn, curs, memberID):
    choice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Schedule Personal Training Session", "Register For Group Fitness Class"])
    
    # Run if the user wants to schedule a personal training sessions
    if(choice == 0):
        choice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Sign Up For Personal Training Session", "Reschedule Personal Training Session", "Cancel Personal Training Session"])
        # Run if user wants to sign up for a personal training session
        if(choice == 0):
            # Get desired day of week for session
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
            
            # Get desired start time for session
            startTime = 6 + showMenu("WHEN WOULD YOU LIKE YOUR SESSION TO START (Availability will go from this time to 2 hours ahead)?", ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"])
            endTime = startTime + 2 # Calculate session end time
            
            # Get every available trainer for the desired day/time of the week
            curs.execute("SELECT trainer_id FROM Availabilities WHERE day_of_week = '" + weekDay + "' AND start_time <= '" + str(startTime) + ":00' AND end_time >= '" + str(endTime) + ":00' GROUP BY trainer_id EXCEPT SELECT trainer_id FROM Sessions sessions WHERE start_time = '" + str(startTime) + ":00' OR start_time = '" + str(startTime + 1) + ":00' OR start_time = '" + str(startTime - 1) + ":00' GROUP BY trainer_id")
            cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").replace(",", "").split(", ")

            if(curs.rowcount == 0):
                # Tell user that there are no trainers available at the desired day/time
                print("ERROR: NO TRAINERS AVAILABLE FOR THE DAY/TIME DESIRED")
            else:
                # Get user's desired trainer that is available
                trainerList = []
                for index, element in enumerate(cursList):
                    curs.execute("SELECT first_name, last_name FROM Trainers WHERE trainer_id = " + cursList[index])
                    trainerList.append(str(curs.fetchone()).replace(",", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", ""))
                memberChoice = showMenu("WHICH TRAINER WOULD YOU LIKE FOR YOUR SESSION?", trainerList)
                trainerID = cursList[memberChoice]
                
                print("Session successfully scheduled!")
                # Insert the sessionn into the Sessions table
                curs.execute("INSERT INTO Sessions (session_id, trainer_id, member_id, day_of_week, start_time) VALUES (DEFAULT, " + trainerID + ", " + memberID + ", '" + weekDay + "', '" + str(startTime) + ":00')")
                conn.commit() # Commit database changes
                
        # Run if user wants to reschedule a session
        elif(choice == 1):
            # Get all sessions that the user is registered for
            curs.execute("SELECT session_id, trainer_id, day_of_week, start_time FROM Sessions WHERE member_id = " + str(memberID))
            cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").replace("datetime.time", "").split(", ")
      
            if(curs.rowcount == 0):
                # Print an error if the user has no sessions scheduled
                print("ERROR: YOU HAVE NO SCHEDULED SESSIONS")
            else:
                sessionList = []
                # Add text which describes each sessions to sessionList
                for index, element in enumerate(cursList[::5]):
                    curs.execute("SELECT first_name, last_name FROM Trainers WHERE trainer_id = " + cursList[5 * index + 1])
                    sessionList.append("%02d" % int(cursList[5 * index + 3]) + ":" + "%02d" % int(cursList[5 * index + 4]) + " | Every " + cursList[5 * index + 2] + " with " + str(curs.fetchone()).replace(",", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", ""))
                
                # Make member choose from all their classes
                memberChoice = showMenu("WHICH SESSION WOULD YOU LIKE TO RESCHEDULE?", sessionList)
                sessionID = cursList[5 * memberChoice]
                trainerID = cursList[5 * memberChoice + 1]
                
                # Get user's desired day of week
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
                
                # Get user's desired start time
                startTime = 6 + showMenu("WHEN WOULD YOU LIKE YOUR SESSION TO START (Availability will go from this time to 2 hours ahead)?", ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"])
                endTime = startTime + 2 # Calculate session end time
                
                # Check if session trainer is available at that time
                curs.execute("SELECT trainer_id FROM Availabilities WHERE day_of_week = '" + weekDay + "' AND start_time <= '" + str(startTime) + ":00' AND end_time >= '" + str(endTime) + ":00' AND trainer_id = " + str(trainerID) + " GROUP BY trainer_id EXCEPT SELECT trainer_id FROM Sessions sessions WHERE session_id != " + str(sessionID) + " AND (start_time = '" + str(startTime) + ":00' OR start_time = '" + str(startTime + 1) + ":00' OR start_time = '" + str(startTime - 1) + ":00') GROUP BY trainer_id")
                cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").replace(",", "").split(", ")
          
                if(curs.rowcount == 0):
                    # Print error if trainer is not available
                    print("ERROR: TRAINER NOT AVAILABLE FOR THE DAY/TIME DESIRED")
                else:
                    # Update schedule and commit to database
                    print("Session successfully rescheduled!")
                    curs.execute("UPDATE Sessions SET start_time = '" + str(startTime) + ":00' WHERE session_id = " + sessionID)
                    conn.commit()
        # Run if user wants to cancel a session
        else:
            # Get all sessions that the user is registered for
            curs.execute("SELECT session_id, trainer_id, day_of_week, start_time FROM Sessions WHERE member_id = " + str(memberID))
            cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").replace("datetime.time", "").split(", ")

            if(curs.rowcount == 0):
                # Print an error if the user has no sessions scheduled
                print("ERROR: YOU HAVE NO SCHEDULED SESSIONS")
            else:
                sessionList = []
                # Add text which describes each sessions to sessionList
                for index, element in enumerate(cursList[::5]):
                    curs.execute("SELECT first_name, last_name FROM Trainers WHERE trainer_id = " + cursList[5 * index + 1])
                    sessionList.append("%02d" % int(cursList[5 * index + 3]) + ":" + "%02d" % int(cursList[5 * index + 4]) + " | Every " + cursList[5 * index + 2] + " with " + str(curs.fetchone()).replace(",", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", ""))
                
                # Get the member's desired class that they want to cancel
                memberChoice = showMenu("WHICH SESSION WOULD YOU LIKE TO CANCEL?", sessionList)
                sessionID = cursList[5 * memberChoice]
                
                print("Session successfully cancelled!")
                # Delete session and commit to database
                curs.execute("DELETE FROM Sessions WHERE session_id = " + sessionID)
                conn.commit()
    
    # Run if user wants to register for a group fitness class
    else:
        # Get all available classes
        curs.execute("SELECT class_id, class_name, class_day, start_time, end_time FROM Classes")
        cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "").replace("datetime.time", "").split(", ")
        classList = []
            
        if(curs.rowcount == 0):
            # Print error if there are no classes available
            print("NO CLASSES CURRENTLY AVAILABLE")
        else:
            # Add text describing each class to classList
            for index, element in enumerate(cursList[::7]):
                classList.append(cursList[7 * index + 1] + " | Every " + cursList[7 * index + 2] + " from " + "%02d" % int(cursList[7 * index + 3]) + ":" + "%02d" % int(cursList[7 * index + 4]) + " to " + "%02d" % int(cursList[7 * index + 5]) + ":" + "%02d" % int(cursList[7 * index + 6]))
            
            classList.insert(0, "None")
            # Get user's desired class
            memberChoice = showMenu("WHICH CLASS WOULD YOU LIKE TO SIGN UP FOR?", classList)

            if(memberChoice != 0):
                classID = cursList[7 * (memberChoice - 1)]
                
                # Register user and commit to database
                curs.execute("INSERT INTO Registrations (registration_id, class_id, member_id) VALUES (DEFAULT, " + classID + ", " + memberID + ")")
                conn.commit()

def manageTrainerSchedule(conn, curs, trainerID):
    choice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Remove Availability", "Add Availability"])
    
    # Run if trainer wants to remove availability
    if(choice == 0):
        # Get all trainer's availabilities
        curs.execute("SELECT availability_id, day_of_week, start_time, end_time FROM Availabilities WHERE trainer_id = " + trainerID)
        cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").replace("datetime.time", "").split(", ")
        avList = []
        
        # Add text describing each availability to avList
        for index, element in enumerate(cursList[::6]):
            avList.append(cursList[6 * index + 1] + ", START TIME: " + "%02d" % int(cursList[6 * index + 2]) + ":" + "%02d" % int(cursList[6 * index + 3]) + ", END TIME: " + "%02d" % int(cursList[6 * index + 4]) + ":" + "%02d" % int(cursList[6 * index + 5]))
        
        # Get availability slot that the user wants to delete
        trainerChoice = showMenu("REMOVE WHICH AVAILABILITY SLOT?", avList)
        avID = cursList[trainerChoice * 2]
        
        # Delete availability slot and commit to database
        curs.execute("DELETE FROM Availabilities WHERE availability_id = " + avID)
        conn.commit()
    
    # Run if trainer wants to create an availability slot
    else:
        # Get trainer's desired day of week
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
        
        # Get trainer's desired start time
        startTime = 6 + showMenu("WHEN WOULD YOU LIKE YOUR AVAILABILITY TO START (Availability will go from this time to 6 hours ahead)?", ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"])
        endTime = startTime + 6 # Calculate availability end time
        
        # Insert availability and commit to database
        curs.execute("INSERT INTO Availabilities (availability_id, trainer_id, day_of_week, start_time, end_time) VALUES (DEFAULT, " + trainerID + ", '" + weekDay + "', '" + str(startTime) + ":00', '" + str(endTime) + ":00')")
        conn.commit()
        
def viewMember(conn, curs):
    ln = input("What is the last name of the member who's profile you would like to view? ")
    # Get all members with the last name that was entered by the trainer
    curs.execute("SELECT member_id, first_name, last_name FROM Members WHERE last_name = '" + ln + "'")
    print("")
    
    # Run if the last name does not belong to any member
    if(cursor.rowcount == 0):
        print("ERROR: Last name number does not belong to any member.")
                

    cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").split(", ")
    memberList = []
    
    # Add text describing each member to memberList
    for index, element in enumerate(cursList[::2]):
        memberList.append(cursList[2 * index + 1] + ", member ID: " + element)
    
    # Get the member ID of the member that the trainer wants to view
    trainerChoice = showMenu("WHICH MEMBER'S PROFILE WOULD YOU LIKE TO VIEW?", memberList)
    memberID = cursList[trainerChoice * 2]
    
    # Display that member's dashboard
    displayDashboard(conn, curs, memberID)
    
try:
    connection = psycopg.connect("dbname=3005_Project user=postgres password=ILove3005")
except BaseException:
    # Print an error if the database could not be connected to
    print("ERROR! Could not connect to database")
else:
    cursor = connection.cursor() # Creates a cursor which allows us to run queries on the database
    
    # Get user's role
    userChoice = showMenu("WHAT IS YOUR ROLE?", ["Member", "Trainer", "Admin"])
    
    if(userChoice == 0):
        userTable = "Members"

        userChoice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Login", "Register"])
        
        if(userChoice == 0):
            # Get member ID so that the user can log in
            userID = input("What is your member ID? ")
            cursor.execute("SELECT * FROM Members WHERE member_id = " + userID)
            print("")
            
            # Run while the user has not input a valid member ID
            while(cursor.rowcount == 0):
                print("ERROR: ID number does not belong to any member.")
                
                userID = input("What is your member ID? ")
                cursor.execute("SELECT * FROM Members WHERE member_id = " + userID)
                print("")
        else:
            # Register the user as a new member
            userID = registerMember(connection, cursor)
            
    elif(userChoice == 1):
        userTable = "Trainers"
        
        # Get trainer ID so that the user can log in
        userID = input("What is your trainer ID? ")
        cursor.execute("SELECT * FROM Trainers WHERE trainer_id = " + userID)
        print("")
        
        # Run while the user has not input a valid trainer ID
        while(cursor.rowcount == 0):
            print("ERROR: ID number does not belong to any member.")
              
            userID = input("What is your member ID? ")
            cursor.execute("SELECT * FROM Trainers WHERE trainer_id = " + userID)
            print("")
    
    while(continueProgram):
        # Run if user is a member
        if(userTable == "Members"):
            userChoice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Manage Profile", "Display Dashboard", "Manage Schedule", "QUIT"])

            if(userChoice == 0):
                manageMemberProfile(connection, cursor, userID)
            elif(userChoice == 1):
                displayDashboard(connection, cursor, userID)
            elif(userChoice == 2):
                manageMemberSchedule(connection, cursor, userID)
            else:
                continueProgram = False; # Dsicontinue program
        # Run if user is a member
        elif(userTable == "Trainers"):
            userChoice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Manage Schedule", "View Member Profile", "QUIT"])

            if(userChoice == 0):
                manageTrainerSchedule(connection, cursor, userID)
            elif(userChoice == 1):
                viewMember(connection, cursor)
            else:
                continueProgram = False; # Disontinue program

    connection.close() # Closes the connection to the database
