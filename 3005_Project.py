import psycopg
from datetime import datetime, date, timedelta

continueProgram = True
userChoice = 0
userTable = ""
userID = -1
adminPassword = "iamadmin123"

# Shows a list of options and returns input from the user
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

# Registers a new member
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

# Allows members to manage their profiles
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

# Displays a member's dashboard
def displayDashboard(conn, curs, memberID):
    # Get member's current weight
    curs.execute("SELECT current_weight FROM Members WHERE member_id = " + memberID)
    currentWeight = str(curs.fetchone()).strip("(),")
    # Get member's goal weight
    curs.execute("SELECT goal_weight FROM Members WHERE member_id = " + memberID)
    goalWeight = str(curs.fetchone()).strip("(),")
    weightDiff = abs(float(currentWeight) - float(goalWeight)) # Calculate how far the member is from their goal weight
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

# Allows members to manage their schedule
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

            if(curs.rowcount == 0):
                # Tell user that there are no trainers available at the desired day/time
                print("ERROR: NO TRAINERS AVAILABLE FOR THE DAY/TIME DESIRED")
                print(cursList)
            else:
                # Get user's desired trainer that is available
                cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").replace(",", "").split(", ")
                trainerList = []
                for index, element in enumerate(cursList):
                    curs.execute("SELECT first_name, last_name FROM Trainers WHERE trainer_id = " + cursList[index])
                    trainerList.append(str(curs.fetchone()).replace(",", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", ""))
                memberChoice = showMenu("WHICH TRAINER WOULD YOU LIKE FOR YOUR SESSION?", trainerList)
                trainerID = cursList[memberChoice]

                choice = showMenu("HOW WOULD YOU LIKE TO PAY?", ["Visa", "Mastercard"])
                paymentMethod = ""
                if(choice == 0):
                    paymentMethod = "Visa"
                else:
                    paymentMethod = "Mastercard"
                
                print("Session successfully scheduled! You have a bill of 100 dollars which you must pay each month.")
                # Insert the sessionn into the Sessions table
                curs.execute("INSERT INTO Sessions (session_id, trainer_id, member_id, day_of_week, start_time) VALUES (DEFAULT, " + trainerID + ", " + memberID + ", '" + weekDay + "', '" + str(startTime) + ":00')")
                curs.execute("INSERT INTO Bills (bill_id, bill_cost, payment_method, paid_date, next_pay, member_id) VALUES (DEFAULT, %s, %s, %s, %s, %s) RETURNING *", ("100", paymentMethod, str(date.today()), str(date.today() + timedelta(days = 30)), memberID))
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
                choice = showMenu("HOW WOULD YOU LIKE TO PAY?", ["Visa", "Mastercard"])
                paymentMethod = ""
                if(choice == 0):
                    paymentMethod = "Visa"
                else:
                    paymentMethod = "Mastercard"
                
                print("Successfully registered for class! You have a bill of 100 dollars which you must pay each month.")
                # Insert the sessionn into the Sessions table
                curs.execute("INSERT INTO Bills (bill_id, bill_cost, payment_method, paid_date, next_pay, member_id) VALUES (DEFAULT, %s, %s, %s, %s, %s) RETURNING *", ("100", paymentMethod, str(date.today()), str(date.today() + timedelta(days = 30)), memberID))
                curs.execute("INSERT INTO Registrations (registration_id, class_id, member_id) VALUES (DEFAULT, " + classID + ", " + memberID + ")")
                conn.commit()

# Allows trainers to manage their schedule
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
        
# Shows all bookings in a formatted manner
def showBookings(bookings):
    print("HERE ARE ALL THE BOOKINGS:")
    print("Room Booking ID | Booking Status | Room ID | Class ID")
    print("-" * 80)

    # Iterate over the bookings and print each one
    for booking in bookings:
        # Print the formatted booking details
        print("{:<15} | {:<14} | {:<7} | {:<8}".format(booking[0], booking[1], booking[2], booking[3]))
    print("\n")

# Allows admins to manage rooms
def manageRoomBookings(conn, curs):
    curs.execute("SELECT * FROM RoomBookings")
    bookings = curs.fetchall()
    # Shows all bookings again using the previously made function
    showBookings(bookings)

    adminChoice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Create A Booking", "Show all Bookings", "Confirm/Cancel A Booking"])
    if(adminChoice == 0):
        # Creates a booking depending on what the user inputs
        roomID = input("Please enter which room you would like to book: ")
        classID = input("Please enter the class ID: ")
        
        # Inserts the information into the table as a new tuple
        try: 
            curs.execute("INSERT INTO RoomBookings (room_booking_id, booking_status, room_id, class_id) VALUES (DEFAULT, '%s', %s, %s)" % ("Pending", roomID, classID))
        except:
            print("\nBooking Not added due to invalid input.\n")
        else:
            conn.commit()
            print("\nBooking created successfully.\n")
    elif(adminChoice == 1):
        # Shows all bookings again using the previously made function
        curs.execute("SELECT * FROM RoomBookings")
        bookings = curs.fetchall()
        showBookings(bookings)
    elif(adminChoice == 2):
        # Asks for a booking id from the admin
        bookingID = input("Please enter the booking ID you would like to confirm/edit: ")
        curs.execute("SELECT * FROM RoomBookings WHERE room_booking_id = %s", (bookingID,))
        booking = curs.fetchone()

        if booking:
            # It extracts the relevant details
            roomID = booking[2]

            # Asks whether the admin wants to cancel or confirm a booking
            newStatus = showMenu("What action would you like to perform?", ["Cancel A Booking", "Confirm A Booking"])
            if(newStatus == 0):
                # Removes a tuple similar to one of the previous choices
                curs.execute("DELETE FROM RoomBookings WHERE room_booking_id = " + bookingID)
                conn.commit()
                print("Booking Removed Successfully.\n")
            else:
                # Otherwise...
                newStatus = "Confirmed"
                # First it checks for conflicts with confirmed bookings
                curs.execute("SELECT * FROM RoomBookings WHERE room_booking_id = " + bookingID + " AND booking_status = 'Confirmed'")
                conflictingBookings = curs.fetchall()
                
                if conflictingBookings:
                    print("There are conflicting bookings. Status cannot be changed.")
                else:
                    # Otherwise it updates booking status
                    curs.execute("UPDATE RoomBookings SET booking_status = %s WHERE room_booking_id = %s", (newStatus, bookingID))
                    conn.commit()
                    print("Booking status updated to confirmed successfully.")
        else:
            print("Booking not found.")
    else:
        print("Invalid input.")

# Function to show all the equipment in a formatted manner
def showEquipment(equipmentList):
    print("Equipment List:")
    print("ID  |  Name              | Installation Date | Last Maintenance Date | Next Maintenance Date | Status")
    for equipment in equipmentList:
        installDate = equipment[2].strftime("%Y-%m-%d")
        lastMainDate = equipment[3].strftime("%Y-%m-%d")
        nextMainDate = equipment[4].strftime("%Y-%m-%d")
        print("{:<3} | {:<18} | {:<17} | {:<21} | {:<21} | {:<10}".format(equipment[0], equipment[1], installDate, lastMainDate, nextMainDate, equipment[5]))

# Allows admins to edit and monitor equipment status
def monitorEquipment(conn, curs):
    # Create list of equipment for the show function
    curs.execute("SELECT * FROM Equipment")
    equipmentList = curs.fetchall()
    showEquipment(equipmentList)
    adminChoice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Add Equipment", "Remove Equipment", "Update Equipment", "Show all Equipment"])
    if(adminChoice == 0):
        # Retrieve information and insert into equipment table
        equipmentName = input("Please enter the name of the equipment: ")
        installationDate = str(date.today())
        lastMainDate = str(date.today())
        nextMainDate = str(date.today()+ timedelta(days = 365))
        status = "Good"
        curs.execute("INSERT INTO Equipment(equipment_name, installation_date, last_maintenance_date, next_maintenance_date, status) VALUES (%s, %s, %s, %s, %s)",(equipmentName, installationDate, lastMainDate, nextMainDate, status))
        conn.commit()
    elif(adminChoice == 1):
        # Deletes equipment from table based on user input
        equipmentID = input("Please enter the ID of the equipment you would like to remove: ")
        curs.execute("SELECT equipment_id FROM Equipment WHERE equipment_id =" + equipmentID)
        equipment = curs.fetchone()
        if equipment:
            curs.execute("DELETE FROM Equipment WHERE equipment_id=" + equipmentID)
            conn.commit()
            print("The equipment has been removes successfully.")
        else:
            print("This equipment does not exist")
    elif(adminChoice == 2):
        # Updates the equipment status and maintenence date accordingly
        equipmentID = input("Please enter the ID of the equipment you would like to update: ")
        curs.execute("SELECT equipment_id FROM Equipment WHERE equipment_id =" + equipmentID)
        equipment = curs.fetchone()
        if equipment:
            updateChoice = showMenu("CHOOSE AN OPTION:", ["Equipment Maintained", "Change Status"])
            if(updateChoice == 0):
                # Changes the maintenance date to today and sets the next maintenance date to one year later
                curs.execute("UPDATE Equipment SET last_maintenance_date = %s, next_maintenance_date = %s, status = %s WHERE equipment_id = %s", (str(date.today()), str(date.today()+ timedelta(days = 365)), "Good", equipmentID))
            elif(updateChoice == 1):
                # Allows user to describe and update the status of equipment
                statusIn = input("Please enter the status of the equipment: ")
                curs.execute("UPDATE Equipment SET status = %s WHERE equipment_id = %s", (statusIn, equipmentID))                
            conn.commit()
            print("The equipment has been updated successfully.")
        else:
            print("This equipment does not exist.")
    elif(adminChoice == 3):
        showEquipment(equipmentList)
    else:
        print("Invalid Input")

# Function to show classes in a formatted manner
def showClasses(classes):
    print("Class Schedule:")
    print("ID | Class Day | Start Time | End Time | Class Name")
    for classInfo in classes:
        startTime = classInfo[2].strftime("%H:%M:%S")
        endTime = classInfo[3].strftime("%H:%M:%S")
        print("{:<2} | {:<9} | {:<10} | {:<8} | {:<10}".format(classInfo[0], classInfo[1], startTime, endTime, classInfo[4]))

# Allows admin to update the schedule of the classes
def updateClassSched(conn, curs):
    choice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Update Class", "Create Class"])

    if(choice == 0):
        curs.execute("SELECT * FROM Classes")
        classes = curs.fetchall()
        showClasses(classes)
        try:
            classID = input("Please enter the class ID you would like to update: ")
            curs.execute("SELECT class_id, class_day, start_time, end_time, class_name FROM Classes WHERE class_id =" + classID)
            classUpdate = curs.fetchone()
        except:
            print("Invalid Class ID")
        else:
            # Gives options to user on what to update
            if classUpdate:
                adminChoice = showMenu("WHAT WOULD YOU LIKE TO UPDATE?", ["Class Day", "Start Time", "Class Name"])
                if(adminChoice == 0):
                    weekDay = ""
                    choice = showMenu("WHICH DAY WOULD YOU LIKE THE NEW CLASS TO BE ON?", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
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
                    curs.execute("UPDATE Classes SET class_day = %s WHERE class_id = %s", (weekDay, classID))
                    print("Class Updated Successfully.\n")
                elif(adminChoice == 1):
                    startTime = 6 + showMenu("WHEN WOULD YOU LIKE THE CLASS TO START (Class will go from this time to 2 hours ahead)?", ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"])
                    endTime = startTime + 2 # Calculate class end time            
                    curs.execute("UPDATE Classes SET start_time = %s, end_time = %s WHERE class_id = %s",(str(startTime) + ":00", str(endTime) + ":00", classID))
                    print("Class Updated Successfully.\n")
                elif(adminChoice == 2):
                    className = input("Please enter the new class name: ")
                    curs.execute("UPDATE Classes SET class_name = %s WHERE class_id = %s", (className, classID))
                    print("Class Updated Successfully.\n")
                else:
                    print("Invalid Input.")
                conn.commit()
            else:
                print("This class does not exist.")
    else:
        weekDay = ""
        choice = showMenu("WHICH DAY WOULD YOU LIKE THE CLASS TO BE ON?", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
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

        startTime = 6 + showMenu("WHEN WOULD YOU LIKE THE CLASS TO START (Class will go from this time to 2 hours ahead)?", ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"])
        endTime = startTime + 2 # Calculate class end time

        className = input("ENTER THE NAME OF THE CLASS: ")
            
        curs.execute("INSERT INTO Classes (class_id, class_day, start_time, end_time, class_name) VALUES (DEFAULT, '" + weekDay + "', '" + str(startTime) + ":00', '" + str(endTime) + ":00', '" + className + "')")
        conn.commit()

# Function to allow the admin to process a payment and show the receipt
def processPayments(conn, curs):
    choice = -1
    memberID = -1
    
    try:
        choice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Create Bill", "Pay Existing Bill"])
        # Receives information and adds to the table of bills accordingly
        memberID = input("Please input member ID: ")

        if(choice == 0):
            billCost = input("Enter bill cost: ")
            paymentMethod = input ("Enter payment method:")
            curs.execute("INSERT INTO Bills(bill_id, bill_cost, payment_method, paid_date, next_pay, member_id) VALUES (DEFAULT, %s, %s, %s, %s, %s) RETURNING *", (billCost, paymentMethod, str(date.today()), str(date.today() + timedelta(days = 30)), memberID))
        else:
            curs.execute("SELECT bill_id, bill_cost, payment_method, next_pay FROM Bills WHERE member_id = " + memberID)
            
    except:
        print("Invalid Input.")
    else:
        if(choice == 0):
            # Prints the receipt in the terminal
            bill = curs.fetchone()
            print("\n\nHERE IS YOUR BILL:")
            print("Bill ID: {}".format(bill[0]))
            print("Bill Cost: ${}".format(bill[1]))
            print("Payment Method: {}".format(bill[2]))
            if bill[3] is not None:
                print("Paid Date: {}".format(bill[3]))
            else:
                print("Paid Date: Not paid yet")
            if bill[4] is not None:
                print("Next Payment Date: {}".format(bill[4]))
            else:
                print("Next Payment Date: Not scheduled yet")
                
            print("Member ID: {} \n\n".format(bill[5]))
        else:
            billList = []
            cursList = str(curs.fetchall()).replace("[", "").replace("]", "").replace("', '", " ").replace("(", "").replace(")", "").replace("'", "").replace("datetime.date", "").split(", ")

            for index, element in enumerate(cursList[::6]):
                billList.append("$" + cursList[6 * index + 1] + " | Member ID: " + memberID + " | Payment Method: " + cursList[6 * index + 2])
            
            # Get user's desired class
            memberChoice = showMenu("WHICH BILL WOULD YOU LIKE TO PROCESS PAYMENT FOR?", billList)
            billID = cursList[6 * memberChoice]
            nextPay = datetime.strptime(cursList[6 * memberChoice + 3] + cursList[6 * memberChoice + 4] + cursList[6 * memberChoice + 5], "%Y%m%d")
            print(str(datetime.date(nextPay) + timedelta(days = 30)))
            curs.execute("UPDATE Bills SET next_pay = %s WHERE bill_id = %s", (str(datetime.date(nextPay) + timedelta(days = 30)), billID))
            curs.execute("UPDATE Bills SET paid_date = %s WHERE bill_id = %s", (str(date.today() + timedelta(days = 30)), billID))
        
    conn.commit()

# Allows trainers to see member dashboards
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
            
    elif(userChoice == 2):
        userTable = "Admin"
        # Take in the admin password to determin if user is an admin
        password = input("Please enter the admin password:\n")
        # Shows all the admin functions and does them depending on user input
        while(password != adminPassword):
            password = input("Please enter the admin password:\n")

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
                continueProgram = False; # Discontinue program
        # Run if user is a trainer
        elif(userTable == "Trainers"):
            userChoice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Manage Schedule", "View Member Profile", "QUIT"])

            if(userChoice == 0):
                manageTrainerSchedule(connection, cursor, userID)
            elif(userChoice == 1):
                viewMember(connection, cursor)
            else:
                continueProgram = False; # Discontinue program
        # Run if user is Admin
        elif(userTable == "Admin"):
            userChoice = showMenu("WHAT WOULD YOU LIKE TO DO?", ["Manage Room Bookings", "Monitor Equipment Maintenence", "Update Class Schedule", "Billing and Payment Proccessing", "QUIT"])
            if(userChoice == 0):
                manageRoomBookings(connection, cursor)
            elif(userChoice == 1):
                monitorEquipment(connection, cursor)
            elif(userChoice == 2):
                updateClassSched(connection, cursor)
            elif(userChoice == 3):
                processPayments(connection, cursor)
            else:
                continueProgram = False; # Discontinue program

    connection.close() # Closes the connection to the database
