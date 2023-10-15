
INSERT INTO airline (name) VALUES ('Jet Blue');
INSERT INTO airline (name) VALUES ('United Airlines');
INSERT INTO airline (name) VALUES ('Avianca Airlines');

INSERT INTO airport (airport_code, name, city, country, type) 
VALUES ('JFK', 'John F. Kennedy', 'NYC', 'United States', 'International');


INSERT INTO airport (airport_code, name, city, country, type) 
VALUES ('PVG', 'Shanghai Pudong International Airport', 'Shanghai', 'China', 'International') ;


INSERT INTO customer VALUES('nikipola@gmail.com', 'test123', 'Niki', 'Pola', 1020, 'Lafayette Street', 109, 'New York City', 'New York', 10013, '2026-10-20', 124009124, 'United States', '2002-07-29');

INSERT INTO customer VALUES('jashuang@gmail.com', 'password123', 'Jason', 'Huang', NULL, 'Willoughby Street', 11, 'New York City', 'New York', 12001, '2027-11-22', 821939812, 'United States', '2001-09-02');

INSERT INTO customer VALUES('keerthipolam@gmail.com', 'rootpassword', 'Keerthi', 'Polam', 4, 'Black Gum Drive', NULL, 'Monmouth Junction', 'New Jersey', 19230, '2030-08-10', 23493052, 'United States', '2002-04-16');


INSERT INTO airplane VALUES(11092390, 'Jet Blue', 300, '2010-07-20', 'Boeing');
INSERT INTO airplane VALUES(1124094, 'United Airlines', 450, '2008-09-03', 'Boeing');
INSERT INTO airplane VALUES(89290, 'Avianca Airlines', 232, '2017-09-03', 'Lockheed Martin');


INSERT INTO airline_staff VALUES('biancareal', 'therealbianca123', 'Bianca', 'Real', 'Jet Blue') ;


INSERT INTO flight VALUES('121', '2023-04-06', '19:30:00', 'Jet Blue', 'JFK', 'PVG', '89290', '2023-07-04', '06:30:00', 1502.0);

INSERT INTO flight VALUES('98', '2023-04-03', '12:05:00', 'United Airlines', 'JFK', 'PVG', 1124094, '2023-04-04', '14:30:00', 1395.50);

INSERT INTO flight VALUES('121', '2023-04-02', '08:30:00', 'Jet Blue', 'PVG', 'JFK', 89290, '2023-04-02', '15:45:00', 2150.99);

INSERT INTO flight VALUES('156', '2023-05-16', '18:15:00', 'United Airlines', 'PVG', 'JFK', 89290, '2023-05-17', '04:17:00', 1495.50);



INSERT INTO sets VALUES('121', '2023-04-06', '19:30:00', 'Jet Blue', 'on-time');


INSERT INTO sets VALUES('98', '2023-04-03', '12:05:00', 'United Airlines', 'delayed');

INSERT INTO sets VALUES('156', '2023-05-16', '18:15:00', 'United Airlines', 'on-time');




INSERT INTO ticket VALUES ('1011', '121', '2023-04-06', '19:30:00', 'Jet Blue');

INSERT INTO ticket VALUES ('2014', '98', '2023-04-03', '12:05:00', 'United Airlines');

INSERT INTO ticket VALUES('123', '156', '2023-05-16', '18:15:00', 'United Airlines');

INSERT INTO purchase VALUES('nikipola@gmail.com', '2014', '2102.1', 'credit', '129141090', 'American Express', '2026-06-07', '2023-01-06', '18:16:00', 'nikipola@gmail.com', 'Niki', 'Pola', '2002-07-29');

INSERT INTO purchase VALUES('jashuang@gmail.com', '123', 1335.3, 'debit', '102412', 'Visa', '2027-03-01', '2023-02-03', '20:20:00', 'gwenstefani@gmail.com', 'Gwen', 'Stefani', '2002-08-29');









