CREATE TABLE Members (
	member_id		SERIAL		PRIMARY KEY,
	first_name		VARCHAR(255)	NOT NULL,	
	last_name		VARCHAR(255)	NOT NULL,	
	goal_weight		INT             NOT NULL,
    current_weight  INT             NOT NULL, 
    bmi             INT             NOT NULL,
    registration_time   TIMESTAMP   NOT NULL UNIQUE
);

CREATE TABLE Routines (
    routine_id      SERIAL      PRIMARY KEY,
    member_id		INT		    NOT NULL,
    routine_name    VARCHAR(255)	NOT NULL,

    FOREIGN KEY (member_id)
		REFERENCES Members (member_id)
);

CREATE TABLE Trainers (
    trainer_id  SERIAL      PRIMARY KEY,
    first_name  VARCHAR(255)    NOT NULL,
    last_name   VARCHAR(255)    NOT NULL
);

CREATE TABLE Sessions (
    session_id      SERIAL    PRIMARY KEY,
    member_id		    INT		    NOT NULL,
    trainer_id	    INT		    NOT NULL,
    routine_id      INT      NOT NULL,

    FOREIGN KEY (member_id)
		  REFERENCES Members (member_id),
    FOREIGN KEY (trainer_id)
		  REFERENCES Trainers (trainer_id)
);

CREATE TABLE Availabilities (
    availability_id  SERIAL      PRIMARY KEY,
    trainer_id  INT     NOT NULL,
    day_of_week  VARCHAR(255)    NOT NULL,
    start_time   TIME    NOT NULL,
    end_time   TIME    NOT NULL,

    FOREIGN KEY (trainer_id)
		  REFERENCES Trainers (trainer_id)
);

CREATE TABLE Classes (
    class_id      SERIAL    PRIMARY KEY,
    trainer_id	    INT		    NOT NULL,
    class_day       VARCHAR(255)    NOT NULL UNIQUE,
    start_time      TIME      NOT NULL,
    end_time      TIME      NOT NULL,
    class_name      VARCHAR(255)    NOT NULL UNIQUE,

    FOREIGN KEY (trainer_id)
		  REFERENCES Trainers (trainer_id)
);

CREATE TABLE Registrations (
    registration_id      SERIAL    PRIMARY KEY,
    class_id     INT		    NOT NULL,
    member_id	   INT		    UNIQUE NOT NULL,

    FOREIGN KEY (class_id)
		  REFERENCES Classes (class_id),
    FOREIGN KEY (member_id)
		  REFERENCES Members (member_id)
);