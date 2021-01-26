-- added autoincrement to fields



CREATE TABLE Staff
(
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    address TEXT(255) NOT NULL,
    phoneNumber TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT(255) NOT NULL,
    role TEXT NOT NULL,
    userID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT

);

CREATE TABLE DeactiveStaff
(
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    address TEXT(255) NOT NULL,
    phoneNumber TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT(255) NOT NULL,
    role TEXT NOT NULL,
    userID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT

);



create TABLE Departments(
    department TEXT NOT NULL
);


CREATE TABLE Slots(
                      slotID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                      doctorID INTEGER NOT NULL,
                      startTime TEXT NOT NULL
);

-- Slots dummy data
INSERT INTO Slots(doctorID,startTime) VALUES
(2,"2021-02-15 10:00:00")
                                                         ,(2,"2021-02-15 10:20:00")
                                                         ,(2,"2021-02-15 10:40:00")
                                                         ,(2,"2021-02-15 11:00:00")
                                                         ,(2,"2021-02-15 11:20:00")
                                                         ,(2,"2021-02-15 11:40:00");
INSERT INTO Slots(doctorID,startTime) VALUES
(4,"2021-02-15 09:00:00")
                                                          ,(4,"2021-02-22 09:20:00")
                                                          ,(4,"2021-02-22 09:40:00")
                                                          ,(4,"2021-02-15 10:00:00")
                                                          ,(4,"2021-02-15 14:20:00")
                                                          ,(4,"2021-02-15 14:40:00");
INSERT INTO Slots(doctorID,startTime) VALUES
(8,"2021-02-15 10:00:00")
                                                          ,(8,"2021-02-22 10:20:00")
                                                          ,(8,"2021-02-22 10:40:00")
                                                          ,(8,"2021-02-15 14:00:00")
                                                          ,(8,"2021-02-15 14:20:00")
                                                          ,(8,"2021-02-15 14:40:00");
INSERT INTO Slots(doctorID,startTime) VALUES
(10,"2021-01-14 10:00:00")
                                           ,(10,"2021-01-14 11:20:00")
                                           ,(10,"2021-01-14 11:40:00")
                                           ,(10,"2021-01-14 14:00:00")
                                           ,(10,"2021-02-20 14:20:00")
                                           ,(10,"2021-02-20 14:40:00");
INSERT INTO Slots(doctorID,startTime) VALUES
(10,"2021-02-15 10:00:00")
                                             ,(10,"2021-02-15 11:20:00")
                                             ,(10,"2021-02-15 11:40:00")
                                             ,(10,"2021-02-15 14:00:00")
                                             ,(10,"2021-02-23 14:20:00")
                                             ,(10,"2021-02-23 14:40:00");
INSERT INTO Slots(doctorID,startTime) VALUES
(10,"2021-03-15 10:00:00")
                                           ,(10,"2021-03-15 12:20:00")
                                           ,(10,"2021-03-15 12:40:00")
                                           ,(10,"2021-03-15 14:00:00")
                                           ,(10,"2021-03-22 14:20:00")
                                           ,(10,"2021-03-22 14:40:00");


CREATE TABLE Patients
-- Deleted drug_use, Changed PhoneNumber to TEXT
(

    userID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,

    gender TEXT NOT NULL,
    dateOfBirth TEXT NOT NULL,
    NHSnumber INTEGER NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    email TEXT NOT NULL,
    address TEXT(255) NOT NULL,
    phoneNumber TEXT NOT NULL,
    password TEXT NOT NULL,
    height REAL,
    weight REAL,
    smokingBehavior TEXT,
    exercise TEXT,
    drinkingBehavior TEXT,
    confirmed CHAR NOT NULL Default "n"

);

CREATE TABLE Appointments
    -- Status (Confirmed/Not confirmed/Cancelled)
-- startTime+date -> dateTime
(
    appointmentID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    dateTime TEXT NOT NULL,
    notes TEXT,
    patientProblem TEXT,
    management TEXT,
    status TEXT NOT NULL,
    patientID INTEGER NOT NULL,
    doctorID INTEGER NOT NULL,
    followup DATETIME,
    FOREIGN KEY (patientID) REFERENCES Patients(userID),
    FOREIGN KEY (doctorID) REFERENCES Staff(userID)
);

CREATE TABLE Referral
    -- New table (just a message, need to talk about emailing system)
-- added date
(
    referralID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    department TEXT NOT NULL,
    referralNotes TEXT NOT NULL,
    referringDoctorID INTEGER NOT NULL,
    patientID INTEGER NOT NULL,
    FOREIGN KEY (patientID) REFERENCES Patients(userID),
    FOREIGN KEY (referringDoctorID) REFERENCES Staff(userID)
);

CREATE TABLE Prescriptions
(
    prescriptionID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    treatment TEXT NOT NULL,
    description TEXT,
    appointmentID INTEGER NOT NULL,
    patientID INTEGER NOT NULL,
    doctorID INTEGER NOT NULL,
    FOREIGN KEY (patientID) REFERENCES Patients(userID),
    FOREIGN KEY (doctorID) REFERENCES Staff(userID),
    FOREIGN KEY (appointmentID) REFERENCES Appointments(appointmentID)

);

CREATE TABLE Immunisations
(
    immunisationID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    immunisation TEXT NOT NULL,
    description TEXT,
    patientID INTEGER NOT NULL,
    doctorID INTEGER NOT NULL,
    FOREIGN KEY (patientID) REFERENCES Patients(userID),
    FOREIGN KEY (doctorID) REFERENCES Staff(userID)
);


CREATE TABLE AllergiesAndAdverse
(
    allergyAdverseID INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT,
    date TEXT NOT NULL,
    allergyAdverse TEXT NOT NULL,
    description TEXT,
    patientID INTEGER NOT NULL,
    FOREIGN KEY (patientID) REFERENCES Patients(userID)
);

CREATE TABLE Diagnoses
-- Ongoing added, DiagnosisID removed(?)
(
    appointmentID INTEGER NOT NULL,
    date TEXT NOT NULL,
    diagnosis TEXT NOT NULL,
    description TEXT,
    doctorID INTEGER NOT NULL,
    patientID INTEGER NOT NULL,
    ongoing TEXT NOT NULL,
    FOREIGN KEY (doctorID) REFERENCES Staff(userID),
    FOREIGN KEY (patientID) REFERENCES Patients(userID),
    FOREIGN KEY (appointmentID) REFERENCES Appointments(appointmentID)
);

CREATE TABLE Labs
(
    labID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    test TEXT NOT NULL,
    result TEXT NOT NULL,
    patientID INTEGER NOT NULL,
    doctorID INTEGER NOT NULL,
    FOREIGN KEY (patientID) REFERENCES Patients(userID),
    FOREIGN KEY (doctorID) REFERENCES Staff(userID)
);


-- Patients Dummy data

INSERT INTO Patients (userID,gender,dateOfBirth, NHSnumber, firstName,lastName,email,address,phoneNumber,password,height,weight,smokingBehavior,exercise,drinkingBehavior,confirmed) VALUES (0,'Prefer not to say',"1997-12-25",9800462430,'Kim','Thomas','fpatterson@yahoo.com','50 Guild Street
London, SE14 8JW','077 0652 7978','P5K7bUdZJJVA3Km7uF_DmD12uYp2WB51deEo49hj6CU=',168,73,'Smoked before but stopped','2','2 to 3 times a month','n');
-- Password:FPatterson!
INSERT INTO Patients (userID,gender,dateOfBirth, NHSnumber, firstName,lastName,email,address,phoneNumber,password,height,weight,smokingBehavior,exercise,drinkingBehavior,confirmed) VALUES (1,'Prefer not to say',"2015-03-14",9372821037,'Keith','Foster','kennedychristine@gmail.com','34 Guild Street
London, E9 5JQ','070 2885 3315','3UNnUGVIWnliRrUyrFCnlHI6Lk21Dh-2DrOW-WguvzY=',140,40,'Smoke ocassionaly','1','Once a week','y');
-- Password:KChristine!
INSERT INTO Patients (userID,gender,dateOfBirth, NHSnumber, firstName,lastName,email,address,phoneNumber,password,height,weight,smokingBehavior,exercise,drinkingBehavior,confirmed) VALUES (2,'Female',"1993-01-14",9287170565,'Jose','Spencer','ohill@thompson.biz','48 Guild Street
London, N1 2JR','077 7879 8456','nbwQVyCD_qMEk4GtlRkOLHBN8MDHrP_Yjr5TZmMKRCU=',180,41,'Smoked before but stopped','2','3 to 11 times in the past year','y');
-- Password:OHill!
INSERT INTO Patients (userID,gender,dateOfBirth, NHSnumber, firstName,lastName,email,address,phoneNumber,password,height,weight,smokingBehavior,exercise,drinkingBehavior,confirmed) VALUES (3,'Prefer not to say',"1996-02-10",4926810052,'Christine','Khan','lindsey54@collins.biz','54 Crown Street
London N4 7XW','070 5389 8123','QEl8mZWOU4WfSVmmMAo6jhYmwJvZgBOZrIrSCkF61Po=',171,42,'Never smoked','7','Twice a week','y');
-- Password:Lindsey!
INSERT INTO Patients (userID,gender,dateOfBirth, NHSnumber, firstName,lastName,email,address,phoneNumber,password,height,weight,smokingBehavior,exercise,drinkingBehavior,confirmed) VALUES (4,'Female',"1970-07-23",7637904115,'Nicole','Clark','kimberlybrooks@brown-nguyen.com','45 Union Terrace
London, E1 8KP','077 3242 3456','pGaZVYU1ePgGKt4Augew1emqrFjizILEMA4BBISwsPM=',178,48,'Smoked before but stopped','10','3 to 4 times a week','y');
-- Password:KBrooks!
INSERT INTO Patients (userID,gender,dateOfBirth, NHSnumber, firstName,lastName,email,address,phoneNumber,password,height,weight,smokingBehavior,exercise,drinkingBehavior,confirmed) VALUES (5,'Female',"1988-01-19",4689864530,'Alexis','Baldwin','ruizwendy@yahoo.com','69 Union Terrace
London, E2 3PL','077 8823 4531','7B4CVvJXl7NJDwPUtqCxwYdDTkgzpWrcTbdn2ctym4o=',172,36,'Smoke frequently','3','3 to 4 times a week','y');
-- Password:RWendy!
INSERT INTO Patients (userID,gender,dateOfBirth, NHSnumber, firstName,lastName,email,address,phoneNumber,password,height,weight,smokingBehavior,exercise,drinkingBehavior,confirmed) VALUES (6,'Other',"2000-06-16",3093003383,'Kaitlyn','Diaz','gmiller@ramirez.com','54 Park Road
London, W2 4PL','078 2341 2342','H93cnAlegKRw9Mho6eOwu1-Ijw99DaULBJPb3cqPndg=',145,84,'Smoked before but stopped','2','Once a month','y');
-- Password:GMiller!
INSERT INTO Patients (userID,gender,dateOfBirth, NHSnumber, firstName,lastName,email,address,phoneNumber,password,height,weight,smokingBehavior,exercise,drinkingBehavior,confirmed) VALUES (7,'Male',"1990-10-06",1873716694,'William','Nguyen','brendanthomas@gmail.com','29 Finsbury Avn
London SW6 1PU','077 3342 2342','z6xHkCPBvTa-5dcAosMPEWQ3mzkwwa5lBWygQeKpGVs=',218,90,'Smoke ocassionaly','4','1 or 2 times in the past year','y');
-- Password:BThomas!
INSERT INTO Patients (userID,gender,dateOfBirth, NHSnumber, firstName,lastName,email,address,phoneNumber,password,height,weight,smokingBehavior,exercise,drinkingBehavior,confirmed) VALUES (8,'Male',"1952-09-20",7389503360,'Cynthia','Christensen','amandaflores@hotmail.com','89 Bond St
London SE7 2LF','020 2356 2574','6CBqUDebbJsCBCdW0VeF3uJDNtKaUOTys7lqH98rBJ0=',214,74,'Smoked before but stopped','7','Once a month','y');
-- Password:AFlores!
INSERT INTO Patients (userID,gender,dateOfBirth, NHSnumber, firstName,lastName,email,address,phoneNumber,password,height,weight,smokingBehavior,exercise,drinkingBehavior,confirmed) VALUES (9,'Prefer not to say',"1955-08-28",3182850730,'Leslie','Lee','wesley46@hotmail.com','23 Riches Road
London SE2 1PT','234 3463 3463','mk47CYQwgV_-92PIPYIf_rbsVQx7OSs-mRi1GXBXX68=',164,83,'Smoked before but stopped','9','1 or 2 times in the past year','y');
-- Password:Wesley!
INSERT INTO Patients (userID,gender,dateOfBirth, NHSnumber, firstName,lastName,email,address,phoneNumber,password,height,weight,smokingBehavior,exercise,drinkingBehavior,confirmed) VALUES (10,'Male',"1975-08-28",3182850730,'Simon','Paulson','patient@gmail.com','45 Roadly Road
London S1 7HP','072 2324 3452','vCXZT6qd9Xd8jGlnY0EIju1b_H8RnCcTUPNwWY6DU1E=',164,83,'Smoked before but stopped','9','1 or 2 times in the past year','y');
-- Password:Password!

-- Lab results dummy data
INSERT INTO Labs (date, test, result, patientID, doctorID)
VALUES ("2018-07-22","blood pressure", "140/89", 2, 2);

INSERT INTO Labs (date, test, result, patientID, doctorID)
VALUES ("2017-08-27","blood pressure", "120/78", 10, 10);

INSERT INTO Labs (date, test, result, patientID, doctorID)
VALUES ("2014-02-27","blood pressure", "115/65", 5, 2);

INSERT INTO Labs (date, test, result, patientID, doctorID)
VALUES ("2018-07-22","liver enzymes", "ALT 50 U/L, AST 15 U/L, GGT <10 U/l", 2, 10);

INSERT INTO Labs (date, test, result, patientID, doctorID)
VALUES ("2016-07-12","liver enzymes", "ALT 35 U/L, AST 18 U/L, GGT <17 U/l", 7, 2);

INSERT INTO Labs (date, test, result, patientID, doctorID)
VALUES ("2019-12-05","liver enzymes", "ALT 50 U/L, AST 11 U/L, GGT <34 U/l", 1, 2);

INSERT INTO Labs (date, test, result, patientID, doctorID)
VALUES ("2014-01-29","ECG", "ST elevation, abnormal rhythm", 10, 1);

INSERT INTO Labs (date, test, result, patientID, doctorID)
VALUES ("2020-08-03","ECG", "All normal", 10, 0);

INSERT INTO Labs (date, test, result, patientID, doctorID)
VALUES ("2014-02-27","Chlamydia text", "Positive", 2, 10);


-- AllergiesAndAdverse dummy data
INSERT INTO AllergiesAndAdverse (date, allergyAdverse, description, patientID)
VALUES ("2019-03-22","Bee sting allergy", "Severe anaphylatic shock. Must carry epipen at all times", 4);

INSERT INTO AllergiesAndAdverse (date, allergyAdverse, description, patientID)
VALUES ("2010-05-14","Dust mite allergy", "Mild allergy, causes rashes and rhinitis", 10);

INSERT INTO AllergiesAndAdverse (date, allergyAdverse, description, patientID)
VALUES ("2012-09-17","Hayfever", "Experiences rhinitis, itchy and red eyes", 10);

INSERT INTO AllergiesAndAdverse (date, allergyAdverse, description, patientID)
VALUES ("2009-11-05","Hayfever", "Severe hayfever occuring around midsummer. Runny nose,
    and eye reactions" , 10);

INSERT INTO AllergiesAndAdverse (date, allergyAdverse, description, patientID)
VALUES ("2009-02-05","Latex allergy", "Patient comes up in hives on contact with latex.
  Use alternative gloves", 7);

INSERT INTO AllergiesAndAdverse (date, allergyAdverse, description, patientID)
VALUES ("2009-04-05","penicillin", "Severe reaction. Nausea and vomitting", 4);

INSERT INTO AllergiesAndAdverse (date, allergyAdverse, description, patientID)
VALUES ("2009-09-05","Warfarin", "Severe bleeding adverse event", 2);

INSERT INTO AllergiesAndAdverse (date, allergyAdverse, description, patientID)
VALUES ("2020-12-05","Prednisone", "Skin thinning and wrist fracture
   during extended course", 5);

-- Patients dummy data
-- Appointments dummy data
INSERT INTO Appointments (dateTime, patientProblem, notes, management, status,  patientID, doctorID)
VALUES
("2021-01-04 10:00:00",'Patient has come in complaining of excess tiredness, frequent and foamy urination', 'I suspect this patient may have diabetes', 'Referring patient to endocrinology department to assess for diabetes', 'Attended',  10, 10),
("2020-11-23 10:10:00", 'Steven has telephone in with a severe cough and temperature', 'Suspected COVID-19', 'Patient referred for COVID testing', 'Attended', 10, 1),
("2020-01-04 14:40:00", 'Patient was telephoned for follow-up', 'informed patient of positive covid test result', 'Patient to drink lots of fluids and remain isolated, will attended ER if symptoms worsen', 'Attended', 10, 10),
("2021-01-05 11:20:00", Null, Null, Null, 'Missed', 10, 10),
("2021-01-13 11:20:00", Null, Null, Null, 'Confirmed', 10, 10),
("2021-01-15 10:00:00", Null, Null, Null,  'Not Confirmed',  10 , 0),
("2021-01-26 14:40:00", Null, Null, Null,  'Confirmed', 5, 10),
("2021-01-26 10:40:00", Null, Null, Null, 'Not confirmed', 6, 1),
("2021-01-26 10:40:00", Null, Null, Null, 'Not confirmed', 10, 1),
("2021-01-26 10:40:00", Null, Null, Null, 'Not confirmed', 10, 10),
("2021-02-13 10:00:00", Null, Null, Null,  'Confirmed', 2, 10),
("2021-02-16 10:00:00", Null, Null, Null,  'Confirmed', 3, 10),
("2021-02-26 11:20:00", Null, Null, Null,  'Not confirmed', 7, 10),
("2021-02-26 10:00:00", Null, Null, Null,  'Confirmed', 10, 10),
("2021-02-27 14:20:00", Null, Null, Null,  'Not confirmed',  2, 10),
("2021-03-03 17:00:00", Null, Null, Null,  'Confirmed', 3, 10),
("2021-03-13 14:20:00", Null, Null, Null,  'Not confirmed',  2, 10),
("2021-03-20 14:20:00", Null, Null, Null,  'Confirmed',  2, 10);

-- Referral dummy data
INSERT INTO Referral (date, department, referralNotes, referringDoctorID, patientID)
VALUES
("2010-11-24", "Endocrinology and Metabolic Medicine", 'I am referring Simon to you for suspected diabetes. Request that he is given blood test and assessed for type 2 diabetes ', 2, 10),
("2020-21-23", "Complementary Medicine", 'Patient has suspected COVID, please send him a test', 10, 10),
("2020-12-01", "Cardiology", 'I am referring this patient to you for suspected arythmia after he has come to me complaining of heart palpitations and chest pain', 8, 10),
("2020-12-03", "Cardiology", 'Please see this patient who requests your opinion on hypertension. ', 8, 1),
("2020-12-06", "Gastroenterology ", 'Enlargement of lymph nodes - suspected abdominal cancer. ', 8, 10);

-- Prescriptions dummy data
INSERT INTO Prescriptions (date, treatment, description, appointmentID, patientID, doctorID)
VALUES
("2010-11-24", "Insulin", "1m x 28. One injection  daily as directed", 1, 10, 0),
("2018-06-16", "Steroid spray", "56mg per dl. two sprays per day", 2, 10, 1),
("2017-05-24", "Nasonex", "140 doses. Two sprays per day", 3, 10, 2),
("2019-02-18", "Bricanyl", "200 doses. One dose per day", 3, 10, 0),
("2019-11-24", "eumovate", "15g. Apply once a day", 3, 4, 1),
("2020-11-25", "Warfarin", "1m x 28. Take one tablet daily as directed", 4, 1, 2),
("2020-11-25", "Nasonex", "140 doses. Two sprays per da", 4, 10, 10),
("2020-11-26", "Warfarin", "1m x 28. Take one tablet daily as directed", 5, 5, 10),
("2020-11-26", "Warfarin", "2m x 28. Take one tablet daily as directed", 5, 5, 10),
("2020-11-26", "Bricanyl", "200 doses. One dose per day", 5, 5, 2);

-- Immunisations dummy data
INSERT INTO Immunisations (date, immunisation, description,  patientID, doctorID)
VALUES
("2019-11-24", "Hepatitus B", "N/A", 1, 5),
("2019-11-24", "influenza shot", "N/A",  1, 6),
("2019-11-24", "influenza shot", "N/A",  10, 8),
("2020-11-25", "influenza shot", "N/A", 1, 7),
("2020-11-25", "Pneumococcal (PPV) vaccine", "N/A", 1, 10),
("2020-11-26", "influenza sho", "N/A", 10, 10),
("2020-11-26", "Hepatitus B", "N/A", 5, 2),
("2012-11-26", "HPV", "N/A", 10, 2),
("2020-11-26", "3-in-1 teenage booster MenACWY", "N/A", 5, 2),
("2021-01-08", "COVID-19 vaccine", "Oxford serum injection", 10, 10);

-- Diagnoses dummy data
INSERT INTO Diagnoses (appointmentID, date, diagnosis, description, doctorID, patientID, ongoing)
VALUES
(1, "2010-11-24", "Diabetes", "N/A", 2, 10, "Yes"),
(2, "2019-11-24", "Eye infection", "N/A", 2, 10, "No"),
(3, "2017-11-24", "Shingles", "N/A", 4, 10, "No"),
(4, "2020-11-25", "Covid-19", "N/A", 3, 10, "No"),
(5, "2020-11-26", "Covid-19", "N/A", 10, 2, "No");




-- Staff

INSERT INTO `Staff` (`userID`,`firstName`,`lastName`,`address`,`phoneNumber`,`email`,`password`,`role`)
VALUES (0,"Odette","Collier","32 Hallam Rd, N15 3HP","0357 854 6219","ut.nisi@posuereenimnisl.org","Gd89GgTaTlCjpgW2Dpbo_U-Is5lpYmpCg-YP_2E7du8=","GP"), -- password: ut.nisi!
       (1,"Joseph","Mayer","2 Guild St, S1 E19","0800 051206","diam.lorem@vitae.com","0qylTUHN5VEwIzS-8zFU_TR56aMYdNIb0u1gpHcaszg=","GP"), -- password: diam.lore!
       (2,"Chase","Gentry","5 Crawly Rd, E2 7PI","0800 745874","vel.vulputate.eu@ligulaAeneaneuismod.org","LKwlN6Oyav2Q_m55d3BD0g1ZqFu0xnHhX9K1awcSsd8=","GP"), -- password: vel.vulputate.eu!
       (3,"Amal","Faulkner","119 Holloway Rd, NE5 9GP","(014365) 52165","et@Sedeu.net","nxr1Kk8j1ItwS-218IlhaCPdRxV6NOs-2HEazLT_rEk=","admin"), -- password: et!
       (4,"Wendy","Bentley","5 Dolor Rd, N1 7PR","07863 865451","egestas.Duis.ac@rutrum.org","Q-SZVpEepfMOfmOUGJF7f4NvbAPpIHI8VCqDDkNaiR0=","admin"), -- password: egestas.Duis.ac!
       (5,"Cedric","Lara","10 Holloway Rd, NE5 4GP","0800 1111","volutpat.Nulla@Quisquefringilla.co.uk","-F3yd-G6sbhHER8aiu2J70svuF44nJYv3knL2Q7-koQ=","GP"), -- password: volutpat.Nulla!
       (6,"Sean","Atkinson","23 Park Road, N15 2LP","055 0890 3266","Maecenas.malesuada.fringilla@ornareelitelit.ca","i4zVQlBgzcVB8YnCrng0N-XQ6E8bVqUczSEoQR6ABPA=","GP"), -- password: Maecenas.malesuada.fringilla!
       (7,"Brendan","Steele","5 Falkland Road, N8 6PL","0500 160194","vestibulum@blanditatnisi.ca","da7eg0SJYLEpu1ETWq_oPZaYN5UfducYSUwuHvkUnI0=","GP"), -- password: vestibulum!
       (8,"Stacy","Sawyer","5 Fairfax Road", "N8 6PZ","a.malesuada@QuisquevariusNam.co.uk","wM0sE-m7e7F4gNyBd0AWB5nEVJOw8EPSLMhUBIX_jAM=","GP"), -- password: a.malesuada!
       (9,"Simon","Amstel","8 Adams St, E9 7LP","(01680) 70700","admin@gmail.com","vCXZT6qd9Xd8jGlnY0EIju1b_H8RnCcTUPNwWY6DU1E=","admin"), -- password: Password!
       (10,"Gary","Busey","19 Yepper St, S9 E8","(01680) 70700","gp@gmail.com","vCXZT6qd9Xd8jGlnY0EIju1b_H8RnCcTUPNwWY6DU1E=","GP"); -- password: Password!

-- INSERT INTO `myTable` (`userID`,`firstName`,`lastName`,`address`,`phoneNumber`,`email`,`password`,`role`,`employmentStartDate`) VALUES (11,"Jayme","Whitehead","P.O. Box 880, 3581 Vel St.","0845 46 49","magnis.dis.parturient@ut.org","RMC70EUP8DK","admin","29-05-2020 13:23:15"),(12,"Deanna","Beasley","9088 Nibh. Ave","0845 46 49","Mauris@elementumpurus.co.uk","CPK76OPI0UM","admin","04-10-2020 06:33:43"),(13,"Ria","Cooper","553-1000 Quisque Avenue","0839 243 8561","diam.luctus.lobortis@anteiaculisnec.org","IPJ05DXI0UA","GP","10-06-2020 19:14:33"),(14,"Winifred","Manning","P.O. Box 603, 7394 Cubilia Street","(0110) 677 0765","purus.Nullam.scelerisque@turpisAliquamadipiscing.ca","PVP59NBA4BE","admin","18-02-2020 20:02:11"),(15,"Beatrice","Howe","1159 Dignissim St.","0975 150 5754","a@facilisis.com","LRR42LCL6PS","admin","20-04-2020 10:09:27"),(16,"Gary","Webster","Ap #305-7836 Nunc St.","07624 976652","ac.facilisis@quisdiam.org","IHU38AFO9KX","admin","29-10-2021 04:54:51"),(17,"Kasimir","Potter","3528 Ornare, St.","070 2858 2000","purus.accumsan@Maurisvel.org","ZAE29CSW2XG","GP","11-01-2020 16:48:04"),(18,"Kareem","Peck","231-3871 Eget, Avenue","0800 323008","sagittis.felis@in.com","TTZ66TRB1XH","admin","13-12-2020 09:34:22"),(19,"Quentin","Small","Ap #108-3813 Nonummy. Av.","055 3444 0869","Nam.porttitor.scelerisque@anteMaecenas.ca","DPO69FBB1XU","GP","29-04-2021 09:08:16"),(20,"Ingrid","Heath","2882 Scelerisque Avenue","0866 874 5776","inceptos@ipsumSuspendissenon.edu","HOI00USA8WO","GP","05-05-2020 03:58:39");
-- INSERT INTO `myTable` (`userID`,`firstName`,`lastName`,`address`,`phoneNumber`,`email`,`password`,`role`,`employmentStartDate`) VALUES (21,"Travis","Thomas","9917 Porta Av.","0845 46 49","dolor.tempus@Etiamimperdietdictum.ca","LSW11KUV5SX","GP","23-09-2021 17:30:29"),(22,"Shellie","Gamble","635-508 Proin St.","070 6289 8080","Donec@lacusvariuset.edu","ILA99KJU7OQ","admin","08-06-2021 23:13:35"),(23,"Caryn","Chandler","P.O. Box 516, 3052 Enim. Avenue","07624 557540","est.ac@temporbibendum.edu","AKR41TWM1GJ","admin","17-10-2020 11:39:31"),(24,"Joan","Chavez","Ap #522-9705 Ac Av.","056 2508 7043","auctor@tincidunt.net","YBM20BFH1OR","admin","01-01-2021 19:24:02"),(25,"Melvin","Rose","Ap #193-7293 Egestas. Avenue","0310 957 1104","malesuada.fames.ac@sedestNunc.net","YPQ23IUN4BV","GP","25-05-2021 11:47:32"),(26,"Len","Henderson","P.O. Box 785, 8552 Lacus Av.","070 1427 1270","augue.malesuada@semvitaealiquam.net","HCC74XTO2WT","GP","31-01-2020 13:19:31"),(27,"Zena","Decker","439-9653 Sed Road","056 6121 9985","Cras.lorem.lorem@Pellentesque.org","IFP53BPJ1SA","GP","23-12-2020 07:07:31"),(28,"Hiroko","Shields","4670 Dui, Avenue","07624 183680","non@at.net","ZLD92CVU1SX","admin","10-10-2020 00:42:14"),(29,"Logan","Kidd","P.O. Box 791, 2318 Quam. Road","07624 502321","at.arcu.Vestibulum@sit.co.uk","LFB28FEC1WN","GP","07-09-2020 03:42:24"),(30,"Uta","Neal","252-5102 Lectus. St.","0800 372 5047","nunc@at.co.uk","OOV53XPT9SM","admin","27-02-2021 23:16:52");
-- INSERT INTO `myTable` (`userID`,`firstName`,`lastName`,`address`,`phoneNumber`,`email`,`password`,`role`,`employmentStartDate`) VALUES (31,"Zia","Richard","P.O. Box 970, 8583 A Avenue","056 7392 2608","dis.parturient@nequenonquam.co.uk","DKX27PSJ6QP","admin","06-11-2020 16:26:52"),(32,"Maile","Vang","167-7195 Elit, Road","07624 674280","eu@atpretium.com","MMO86MCP0HO","admin","24-05-2020 02:34:08"),(33,"Patricia","Holder","Ap #188-3571 Orci Avenue","0800 362 7023","lectus.a@Pellentesque.net","PQH76XFP4PH","GP","27-05-2020 16:42:26"),(34,"Octavia","Willis","4986 Fusce Avenue","070 8166 3990","et.ultrices@interdum.org","XEA89DTL5RF","GP","13-04-2021 14:36:55"),(35,"Cruz","Murphy","P.O. Box 960, 7208 Arcu. Rd.","07467 507160","Donec@augueSed.com","XPF61KQC2JE","admin","12-04-2021 11:01:24"),(36,"Price","Gilliam","P.O. Box 618, 6347 Pede. Ave","(023) 1810 1232","eu.odio.Phasellus@quislectusNullam.com","ZUR36IMR3AU","admin","13-12-2021 06:52:23"),(37,"Ginger","Eaton","618 Eu Avenue","07448 256100","sit.amet@tellus.net","JYS16CCU1MZ","GP","02-03-2020 20:49:20"),(38,"Hadley","Morrow","P.O. Box 442, 5632 Vivamus Rd.","0500 202988","penatibus@scelerisque.com","PLK64QNS2CF","admin","31-03-2020 05:09:11"),(39,"Adrienne","Bush","Ap #170-9916 Lacinia Rd.","(01879) 44420","ipsum.sodales@malesuadaInteger.com","UFQ44GVS7YO","GP","11-06-2020 02:45:48"),(40,"Wayne","Gibson","Ap #369-6087 Semper. St.","(01377) 86090","mi@ipsum.co.uk","XGV81CBW7NH","GP","25-11-2020 19:45:03");
-- INSERT INTO `myTable` (`userID`,`firstName`,`lastName`,`address`,`phoneNumber`,`email`,`password`,`role`,`employmentStartDate`) VALUES (41,"Venus","Santiago","773 Congue Av.","076 1776 3113","odio@nectempusscelerisque.ca","RIF46ZNP8GT","admin","23-08-2020 22:33:52"),(42,"Kendall","Wilkinson","552 Amet Rd.","(01627) 22853","tincidunt@Nuncpulvinararcu.net","PLO06UEP3ZH","admin","15-11-2021 15:34:01"),(43,"Jena","Miller","8139 Mauris Avenue","0845 46 44","Nullam@Sednulla.com","GCW97XCX4YE","GP","21-10-2021 23:13:24"),(44,"Ross","Golden","P.O. Box 433, 2771 Amet, Street","(0171) 109 6817","velit.dui@tellus.org","KYC04ZKB9PQ","GP","25-05-2021 07:04:24"),(45,"Lydia","Contreras","656-5470 Quis Av.","0845 46 45","Suspendisse.aliquet.sem@orciconsectetuereuismod.net","BPP10XZS2OP","admin","20-01-2021 07:34:58"),(46,"Alexa","Jones","605-9290 Facilisis, St.","(01406) 08230","congue@Duiscursusdiam.net","QXR89LKJ0QH","GP","11-02-2021 08:04:04"),(47,"Brielle","Harmon","9880 Odio. Avenue","0500 539825","Sed@Cras.edu","UOX18SDL7AR","GP","29-05-2021 23:44:46"),(48,"Clio","Spencer","Ap #548-2131 Nec, Rd.","(028) 9209 4841","nascetur.ridiculus@ultricesposuerecubilia.co.uk","VAI66XKU0QM","admin","19-06-2021 06:21:55"),(49,"Galena","Hogan","P.O. Box 335, 3682 Proin Street","0845 46 49","Aliquam.erat@a.com","GNH79PHC1JJ","GP","08-09-2020 23:35:29"),(50,"Nerea","Reynolds","P.O. Box 237, 516 Purus. St.","07677 484257","porta@tellusidnunc.org","QBG68GJN9TR","GP","22-02-2021 23:48:12");
-- INSERT INTO `myTable` (`userID`,`firstName`,`lastName`,`address`,`phoneNumber`,`email`,`password`,`role`,`employmentStartDate`) VALUES (51,"Jade","Wall","3941 Tellus Ave","(016977) 1174","ligula@Sed.org","NEI36RBD5HM","GP","13-05-2020 07:35:48"),(52,"Priscilla","Weiss","Ap #825-9993 Suspendisse St.","0800 918 7234","sociis.natoque.penatibus@aliquet.ca","OVU81WBN8LU","GP","08-06-2020 13:28:39"),(53,"Whoopi","Rich","9124 Metus. Street","(024) 4074 5879","sem@odioAliquam.net","OQW47HCF0IH","admin","09-09-2021 15:00:40"),(54,"Serina","Bright","5204 A Rd.","0800 527184","quis.accumsan@ligulaNullam.org","REA03KLU7NC","GP","29-06-2021 16:56:14"),(55,"Susan","Bean","148-8762 Ac St.","(016977) 4062","cursus@aclibero.co.uk","MBX02CRL1UQ","admin","24-07-2021 18:44:31"),(56,"Adara","Coleman","P.O. Box 882, 7215 Sit Rd.","0800 036 3012","purus.mauris@sociisnatoque.org","VPB28CUS9PO","GP","01-10-2021 02:41:37"),(57,"Hayley","Glass","5511 Et St.","(01326) 653880","in@egetmetuseu.co.uk","ZQD42QZU5WC","GP","23-08-2021 19:45:53"),(58,"Tarik","Stein","4660 Tellus Rd.","070 2718 1104","id@Donec.net","GIF61RSE7IA","GP","28-11-2021 08:37:20"),(59,"Hadassah","Morrison","653-9080 Mauris Avenue","(01761) 97921","pharetra.nibh@infaucibusorci.edu","QEF29ODJ7AQ","GP","25-10-2020 07:40:15"),(60,"Hedwig","Campbell","P.O. Box 584, 6464 Sed, Rd.","(0151) 187 5992","dui.nec@consequatpurusMaecenas.com","LMR51ECI7RZ","admin","27-06-2021 13:31:08");
-- INSERT INTO `myTable` (`userID`,`firstName`,`lastName`,`address`,`phoneNumber`,`email`,`password`,`role`,`employmentStartDate`) VALUES (61,"Judah","Petty","Ap #638-6956 Hymenaeos. St.","070 1647 0378","tempor.est@convallisdolor.co.uk","MEB43KNV1TK","GP","20-01-2020 06:41:43"),(62,"Stuart","Melton","4100 Elementum, St.","(018081) 81470","Nulla.eu@egestashendrerit.com","QWI23AQM1VK","GP","03-07-2020 22:41:43"),(63,"Harper","Velez","Ap #929-3892 Aliquet Road","(020) 8073 3263","luctus.sit@necenimNunc.net","RKT72MBA9XD","GP","25-03-2021 23:56:53"),(64,"Abraham","Dawson","4270 Morbi Rd.","(019305) 57224","lacus.varius.et@sem.org","GQB51ZIM9ZD","admin","16-01-2020 07:01:50"),(65,"Elliott","Garner","Ap #655-9789 Aliquet Ave","0800 481743","convallis.dolor.Quisque@antedictum.edu","FHJ26KTN5LG","GP","01-11-2021 11:45:57"),(66,"Jorden","Mcneil","P.O. Box 709, 1409 Enim St.","0500 252136","dolor@Craseu.co.uk","RDD53WDN0TS","GP","05-08-2020 09:09:29"),(67,"Alea","Eaton","807-5589 Orci Avenue","(01511) 76276","nisi.Mauris@maurisipsumporta.com","CJN13CBK6VG","admin","29-10-2021 02:45:32"),(68,"Eden","Alston","P.O. Box 266, 7543 Amet Av.","0800 1111","facilisis@Donecfelis.ca","XCL88SCY2FR","GP","24-07-2021 14:28:19"),(69,"Sawyer","Hinton","460 Mollis Road","0845 46 49","lacus@CrasinterdumNunc.ca","OUF96MHX1LL","admin","06-12-2020 21:37:24"),(70,"Quemby","Castaneda","4107 Laoreet Ave","(01198) 61088","orci@Duisatlacus.co.uk","AYG34LCM4LA","GP","29-03-2021 07:49:18");
-- INSERT INTO `myTable` (`userID`,`firstName`,`lastName`,`address`,`phoneNumber`,`email`,`password`,`role`,`employmentStartDate`) VALUES (71,"Candice","Norton","5795 Tincidunt St.","0500 737542","montes.nascetur@nonvestibulum.co.uk","XAE97FES6HM","GP","27-02-2020 13:36:25"),(72,"Tyrone","Owen","Ap #297-9455 Vitae St.","0800 889817","id@Crasegetnisi.edu","RVP58RQB9LW","admin","14-12-2020 19:39:55"),(73,"Mohammad","Forbes","Ap #237-5473 Pellentesque Rd.","055 7821 4232","feugiat.metus.sit@nonummyFusce.org","DFI59IKV8ZV","GP","24-06-2021 04:31:14"),(74,"Abigail","Holder","1526 Augue St.","0800 468873","diam@Pellentesqueut.co.uk","IMR72NKA3CL","admin","29-02-2020 23:20:22"),(75,"Ashton","Stanley","409-7901 Mi Ave","(0151) 449 5556","nisl.Nulla@egestashendrerit.com","NKN01UUM1HZ","admin","06-07-2021 21:53:40"),(76,"Sheila","Floyd","412-6203 Ac Ave","055 2721 5447","nec.euismod@semconsequatnec.org","ZEJ76OER5HQ","admin","30-09-2020 05:59:54"),(77,"Kermit","Jenkins","P.O. Box 220, 4090 Nec Road","0822 847 5490","Phasellus@Quisque.org","EQP83XDV7TU","GP","08-05-2021 13:25:08"),(78,"Robin","Herman","4615 Donec St.","0333 454 8606","erat.neque@elitelit.net","OFK68PTV4HY","admin","19-12-2019 11:56:29"),(79,"Grady","Warren","674-9973 Eu, Av.","055 9157 1983","dictum@Crasloremlorem.co.uk","WBR05LNO5BG","admin","18-05-2021 16:49:29"),(80,"Lars","Joyner","Ap #400-7431 Sapien, Road","056 6218 7188","faucibus.Morbi@at.edu","IHW31SJJ3FX","admin","12-07-2021 21:59:43");
-- INSERT INTO `myTable` (`userID`,`firstName`,`lastName`,`address`,`phoneNumber`,`email`,`password`,`role`,`employmentStartDate`) VALUES (81,"Gage","Oneil","P.O. Box 938, 4562 Placerat, Rd.","(027) 4496 3333","egestas.Fusce@auctor.org","MCA75ZAY1HZ","GP","02-08-2020 16:08:19"),(82,"Gail","Vazquez","Ap #851-9122 Nulla Avenue","(0161) 122 0668","Integer.sem.elit@commodohendrerit.net","BPY17GFC1NH","GP","29-09-2021 17:31:15"),(83,"Dai","Lucas","Ap #961-6592 In St.","(0191) 200 8091","interdum.Sed.auctor@Vestibulumut.com","LUP30QLY9TD","GP","10-03-2021 13:21:47"),(84,"Basia","Odonnell","P.O. Box 212, 954 Eget Rd.","0845 46 40","adipiscing.ligula@bibendumullamcorper.co.uk","MPR51OAL5LV","GP","29-08-2021 08:52:45"),(85,"Lev","Mclaughlin","3050 Mollis. Street","0800 1111","bibendum.Donec@nequesed.co.uk","FDF39GJG9BP","admin","19-10-2020 11:44:54"),(86,"Len","Johns","372 Integer Road","0500 421113","lorem@Cum.com","NOR84EDH5ZH","admin","04-12-2020 14:53:21"),(87,"Grady","Strong","P.O. Box 152, 4570 Sed Ave","0800 247 8416","pretium.aliquet@sitametconsectetuer.org","DMT90RLZ8VI","admin","10-06-2020 10:56:34"),(88,"Reagan","Clements","Ap #694-5198 Ornare. St.","0800 892 8371","nostra.per.inceptos@orci.ca","ZCW33JHE1JF","admin","27-04-2020 09:18:11"),(89,"Destiny","Hamilton","P.O. Box 850, 2305 Non Rd.","(0115) 857 9267","nulla.Integer@Duisami.org","UKT47RJZ2JN","admin","29-02-2020 06:29:31"),(90,"Holly","Morales","P.O. Box 954, 1585 Sit St.","(016977) 5295","urna.et@Duis.net","SOZ18KCO5ZS","admin","26-10-2020 19:22:03");
-- INSERT INTO `myTable` (`userID`,`firstName`,`lastName`,`address`,`phoneNumber`,`email`,`password`,`role`,`employmentStartDate`) VALUES (91,"Kiona","Clay","851-1109 Eu Rd.","(011492) 25627","id.sapien@gravidasagittisDuis.net","WJY76HWP9FA","admin","22-11-2021 01:42:20"),(92,"Eliana","Chapman","7458 Eros St.","076 9363 0515","Nulla.facilisis@at.org","OKV92GKW7OA","admin","05-05-2021 05:26:34"),(93,"Octavia","Fletcher","2855 Congue Ave","0800 992 1517","dolor.elit@Praesenteu.com","TCP92YDF7VK","GP","03-05-2020 10:40:46"),(94,"Emily","Stanley","Ap #550-9783 Quam Rd.","(016977) 0730","sit.amet.consectetuer@arcu.edu","TSZ97AUN6KS","admin","10-08-2020 21:41:11"),(95,"Avram","Duncan","P.O. Box 126, 3827 Justo. Avenue","0500 226650","Aenean@risusvariusorci.net","FXW29LFX7GT","admin","22-11-2020 06:41:13"),(96,"Kelsie","Simmons","9496 Molestie St.","(0113) 178 5285","ullamcorper.Duis@posuere.org","PQK68UAV5VV","admin","25-02-2020 17:56:13"),(97,"Arsenio","Day","3935 Mi Av.","0397 501 7141","elit@egestas.edu","PTU09QLQ2NP","admin","19-10-2020 22:49:42"),(98,"Amos","Gonzalez","751-1077 Mus. Av.","0800 1111","sem.consequat.nec@sedtortor.co.uk","PFZ09XZD9YZ","admin","26-04-2021 19:46:03"),(99,"Brendan","Frost","P.O. Box 464, 6075 Tellus Av.","(01638) 792070","ullamcorper.viverra@utmi.ca","PBQ93EOS7SS","GP","05-09-2021 01:21:44"),(100,"Blaine","Ingram","P.O. Box 632, 3244 Nullam Street","(010142) 46562","non@aliquet.co.uk","NGI91EEN4DD","admin","12-10-2020 19:53:44");
