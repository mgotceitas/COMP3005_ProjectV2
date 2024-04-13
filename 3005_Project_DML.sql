INSERT INTO Members (member_id, first_name, last_name, goal_weight, current_weight, bmi, registration_time)
VALUES
(DEFAULT, 'Kelly', 'Trojanowski', 130, 150, 23.5, CURRENT_TIMESTAMP - (interval '1 minute')),
(DEFAULT, 'Amira', 'Brehaut', 120, 140, 21.3, CURRENT_TIMESTAMP);

INSERT INTO Trainers (trainer_id, first_name, last_name)
VALUES
(DEFAULT, 'Matthew', 'Gotceitas'),
(DEFAULT, 'Vincent', 'Chen');

INSERT INTO Sessions (session_id, member_id, trainer_id, day_of_week, start_time)
VALUES
(DEFAULT, 1, 1, 'Monday', '7:00');

INSERT INTO Availabilities (availability_id, trainer_id, day_of_week, start_time, end_time)
VALUES
(DEFAULT, 1, 'Monday', '6:00', '12:00'),
(DEFAULT, 2, 'Friday', '12:00', '18:00');

INSERT INTO Classes (class_id, class_day, start_time, end_time, class_name)
VALUES
(DEFAULT, 'Tuesday', '6:00', '8:00', 'Zumba');

INSERT INTO Registrations (registration_id, class_id, member_id)
VALUES
(DEFAULT, 1, 2);

INSERT INTO RoomBookings (room_booking_id, booking_status, room_id, class_id)
VALUES
(DEFAULT, 'Confirmed', 101, 1);

INSERT INTO Equipment (equipment_id, equipment_name, installation_date, last_maintenance_date, next_maintenance_date, status)
VALUES 
(DEFAULT, 'Leg Press', '2024-04-13', '2024-04-13', '2025-04-13', 'Good'),
(DEFAULT, 'Squat Rack', '2024-04-13', '2024-04-13', '2025-04-13', 'Good');

INSERT INTO Bills (bill_id, bill_cost, payment_method, paid_date, next_pay, member_id)
VALUES
(DEFAULT, 100, 'Visa', '2024-04-13', '2024-05-13', 1),
(DEFAULT, 100, 'Mastercard', '2024-04-13', '2024-05-13', 2);