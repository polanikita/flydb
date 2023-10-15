CREATE TABLE Airport(
    airport_code char(3),
    name varchar(50),
    city varchar(20),
    country varchar(20),
    type varchar(20),
    PRIMARY KEY (airport_code)
);


CREATE TABLE Airline(
    name varchar(20), 
    PRIMARY KEY (name)
);


CREATE TABLE Airline_Staff(
    username varchar(20), 
    password varchar(50), 
    fname varchar (20),
    lname varchar (20), 
    working_airline varchar (20),
    PRIMARY KEY(username),
    FOREIGN KEY (working_airline) references Airline (name)
);

CREATE TABLE Staff_phone(
    username varchar (20),
    phone_num varchar(20),
    PRIMARY KEY(username), 
	FOREIGN KEY (username) references Airline_Staff (username)
);


CREATE TABLE Staff_email(
    username varchar (20),
    email_address varchar(30), 
    PRIMARY KEY(username), 
	FOREIGN KEY (username) references Airline_Staff (username)
);


CREATE TABLE Airplane( 
	airplane_id varchar (20), 
	airline_name varchar(20), 
	num_seats INT(4),  
	manufacture_date DATE, 
	manufacture_company varchar(20), 
	PRIMARY KEY(airplane_id, airline_name), 
	FOREIGN KEY(airline_name) references Airline(name)
);


CREATE TABLE Flight(
    flight_num varchar(10),
    dept_date DATE,
    dept_time TIME,
    airline_name varchar(20),
    dept_code char(3),
    arr_code char(3),
    airplane_id varchar(20), 
    arr_date DATE,
    arr_time TIME,
    base_ticket_price FLOAT(15,2),
    PRIMARY KEY(flight_num, dept_date, dept_time, airline_name),
    FOREIGN KEY(airline_name) REFERENCES Airline(name),
    FOREIGN KEY (dept_code) REFERENCES airport(airport_code),
    FOREIGN KEY (arr_code) REFERENCES Airport(airport_code),
    FOREIGN KEY (airplane_id) REFERENCES Airplane(airplane_id)
);




CREATE TABLE Status( 
	flight_num varchar(10),
	dept_date DATE,
	dept_time TIME, 
	airline_name varchar (20), 
	flight_status varchar (20),
	PRIMARY KEY(flight_num, dept_date, dept_time, airline_name),
	FOREIGN KEY(flight_num, dept_date, dept_time, airline_name) references Flight ( flight_num, dept_date, dept_time, airline_name)
);

CREATE TABLE Customer(
    email_address varchar (30),
    password varchar(50), 
    fname varchar(20), 
    lname varchar(20), 
    building_num INT(10), 
    street_name varchar(20), 
    apt_num INT(10), 
    city varchar(20), 
    state varchar(20),
    zip_code INT(20), 
    passport_exp_date DATE,
    passport_number varchar(20),
    passport_country varchar(20), 
    dob DATE,
    PRIMARY KEY (email_address)
    ); 

CREATE TABLE Customer_phone(
    email_address varchar (30), 
    phone_number varchar (20), 
    PRIMARY KEY(email_address), 
	FOREIGN KEY (email_address) references Customer (email_address)
);

CREATE TABLE Ticket( 
	ticket_id varchar (20), 
	flight_num varchar(10), 
	dept_date DATE, 
	dept_time TIME, 
	airline_name varchar(20), 
	PRIMARY KEY(ticket_id), 
    FOREIGN KEY (flight_num, dept_date, dept_time, airline_name) references Flight (flight_num, dept_date, dept_time, airline_name)
);

CREATE TABLE Purchase( 
	email_address varchar(30), 
	ticket_id varchar (20), 
	actual_price FLOAT(15, 2),
	card_type varchar(20), 
	card_num varchar(20), 
	card_name varchar(20),
	exp_date DATE, 
	purchase_date DATE, 
	purchase_time TIME, 
	passenger_email varchar (30), 
	passenger_fname varchar(20), 
	passenger_lname varchar(20),  
	passenger_dob DATE, 
	PRIMARY KEY(email_address, ticket_id), 
	FOREIGN KEY (email_address) references Customer (email_address), 
	FOREIGN KEY (ticket_id) references Ticket (ticket_id)
);

CREATE TABLE Flown( 
	email_address varchar(30), 
	flight_num varchar(10), 
	dept_date DATE, 
	dept_time TIME, 
	airline_name varchar(20), 
    ticket_id varchar(20),
    PRIMARY KEY (email_address, flight_num, dept_date, dept_time, airline_name), 
	FOREIGN KEY (email_address) references Customer (email_address), 
    FOREIGN KEY (flight_num, dept_date, dept_time, airline_name) references Flight( flight_num, dept_date, dept_time, airline_name),
    FOREIGN KEY (ticket_id) references Purchase (ticket_id)
);


	
CREATE TABLE Rates( 
    email_address varchar(30),
    ticket_id varchar (20),  
    flight_num varchar(10),
    dept_date DATE, 
    dept_time TIME, 
    airline_name varchar(20), 
    rating INT(2), 
    comments varchar(500), 
    PRIMARY KEY (Email_address, Flight_num, Dept_date, Dept_time, Airline_name),
    FOREIGN key (email_address, flight_num, dept_date, dept_time, airline_name) references flown (email_address, flight_num, dept_date, dept_time, airline_name),
    FOREIGN KEY (ticket_id) references Purchase (ticket_id)
);