CREATE TABLE Members (
	member_id		SERIAL		PRIMARY KEY,
	first_name		VARCHAR(255)	NOT NULL,	
	last_name		VARCHAR(255)	NOT NULL,	
	goal_weight		FLOAT             NOT NULL,
    current_weight  FLOAT             NOT NULL, 
    bmi             FLOAT             NOT NULL,
    registration_time   TIMESTAMP   NOT NULL UNIQUE
);

CREATE TABLE Trainers (
    trainer_id  SERIAL      PRIMARY KEY,
    first_name  VARCHAR(255)    NOT NULL,
    last_name   VARCHAR(255)    NOT NULL
);

CREATE TABLE Sessions (
    session_id      SERIAL      PRIMARY KEY,
    member_id		INT		    NOT NULL,
    trainer_id	    INT		    NOT NULL,
    day_of_week     VARCHAR(255)    NOT NULL,
    start_time      TIME            NOT NULL,

    FOREIGN KEY (member_id)
		  REFERENCES Members (member_id),
    FOREIGN KEY (trainer_id)
		  REFERENCES Trainers (trainer_id)
);

CREATE TABLE Availabilities (
    availability_id  SERIAL         PRIMARY KEY,
    trainer_id       INT            NOT NULL,
    day_of_week      VARCHAR(255)   NOT NULL,
    start_time       TIME           NOT NULL,
    end_time         TIME           NOT NULL,

    FOREIGN KEY (trainer_id)
		  REFERENCES Trainers (trainer_id)
);

CREATE TABLE Classes (
    class_id      SERIAL          PRIMARY KEY,
    class_day     VARCHAR(255)    NOT NULL,
    start_time    TIME            NOT NULL,
    end_time      TIME            NOT NULL,
    class_name    VARCHAR(255)    NOT NULL
);

CREATE TABLE Registrations (
    registration_id     SERIAL    PRIMARY KEY,
    class_id            INT		  NOT NULL,
    member_id	        INT		  UNIQUE NOT NULL,

    FOREIGN KEY (class_id)
		  REFERENCES Classes (class_id),
    FOREIGN KEY (member_id)
		  REFERENCES Members (member_id)
);

CREATE TABLE RoomBookings (
    room_booking_id     SERIAL          PRIMARY KEY,
    booking_status      VARCHAR(255)    NOT NULL,
    room_id             INT NOT NULL,
    class_id            INT NOT NULL,
    FOREIGN KEY (class_id) 
            REFERENCES Classes (class_id)
);

CREATE TABLE Equipment (
    equipment_id            SERIAL      PRIMARY KEY,
    equipment_name          VARCHAR(255),
    installation_date       DATE,
    last_maintenance_date   DATE,
    next_maintenance_date   DATE,
    status                  VARCHAR(255) NOT NULL
);

CREATE TABLE Bills (
    bill_id         SERIAL      PRIMARY KEY,
    bill_cost       float,
    payment_method  VARCHAR(255),
    paid_date       DATE,
    next_pay        DATE,
    member_id       INT         NOT NULL,

    FOREIGN KEY (member_id) 
            REFERENCES Members (member_id)
);
