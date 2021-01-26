# e-Health Patient Management System

Welcome to Djekiin Health, a privacy-first healthcare management system built by Group 3!

For your ease of marking, we have created this note. It lists:  

(1) Configuration & Cautionary Notes

(2) How to Start (Log-in Credentials)

(3) Highlights of our Application

###### (1) Configuration & Cautionary Notes

* This is a GUI application, built with Python 3, Tkinter, and SQLite. 
* It must be run with Python 3.9 as its interpreter.

* Some minimum-level configurations are required: 
    * Install tkcalender
      * pip install tkcalendar
    * Install certifi
      * pip install certifi
    * Install Babel
      * pip install Babel
    
* Please also note that, Tkinter functions well on both Windows and MacOS; however, we believe the UI looks better on Windows. Therefore, the video is filmed on a Windows computer exclusively.

###### (2) How to Start (Log-in Credentials)

Please run the login.py first to initialise the user journey. 
To decide the type of user you want to log in with (Admin, GP, Patient), please select one of the three options at the top.
You may use the following log-in credentials to log-in as Admin, GP or Patient.

Admin: 
* username: admin@gmail.com
* password: Password!

GP:
* username: gp@gmail.com
* password: Password!

Patient (confirmed patient):

* username: patient@gmail.com
* password: Password!

Patient (not confirmed by ADMIN):
* username: patientnotconfirmed@gmail.com
* password: Password!


note: 'not confirmed' means that, Patient has successfully submitted a registration form via login.py, but the account has not been approved by the ADMIN. ADMIN can approve the patient registration form in the ADMIN console: Register Patients > Confirm Patients > Double Click a Patient row > Confirm/Delete


Please note that as outlined by the brief, only a Patient can register a new account; GP can only be registered by admins in the admin console.
To test the email notification functionality, the test patient account should be registered with a functioning email address.

After logging in, the user journey should be self-explanatory based on the GUI.

To log out, go to the Menu Bar > File > Logout


###### (3) Highlights of our Application:

* **_Object Orientated Design_:**

The choice of the programming style is made based on few assumptions. For example, a Patient Management System inherently carries characteristics that are congruent with Object Orientated Programming (OOP) principles. (1) it can be maintained that an Admin and GP shares many similar capabilities but each to a different extent. OOP style allows us to abstract and encapsulate some of them; thereby, produce cleaner, re-usable, and more efficient code. (2) OOP is a common industry practice for agile engineering.

* **_Focus on privacy features_:**

We wanted to build features that are not only interesting to us but also ones that could solve a real-world NHS problem. Our research dictates that the healthcare industry is undergoing rapid digital transformation, yet some of their approach to privacy (e.g. GP to keep Patient information confidential) still remains at a paper-level: consensus-based contracts. Confidentiality is key for every healthcare system, but new privacy features must not be so restrictive that they reduce the efficiency of practice staff, who need to regularly update patient records with information such as lab results or new diagnoses. Therefore, we identified the opportunity to build privacy features for the digital age. The cornerstone of such is our 'Viewers Log' feature: ADMIN can see a 'log' of which member of staff viewed whose patient record at what time. This introduces a degree of transparency and check and balances within the information system; thereby, deterring misbehaviours and catching them if need be to enhance privacy measures.

* **_A realistic and robust 'Patient Record' and consultation system_:**

Our 'Patient Record' feature organises an extensive level of the actual patient information that would be handled by an  NHS GP practice. We designed this feature based on user interviews of real healthcare industry personnel. As a result, it covers patient information including Consultation history, Medication, Clinical History, Immunisations, Referrals and Results.

This research also fed into the development of the 'Consultation Form', for GPs to use in consultations with patients and update their records. We connected this form to the SNOMED-CT database -- the current gold standard medical concept database that all NHS digital services are now expected to use  -- allowing GPs to search for any diagnosis term or treatment. 

* **_Graphical User Interface_:**

Although not explicitly required by the coursework brief, we challenged ourselves further by implementing a Tkinter-based GUI. We believe that this not only enhances the usability of our application for the end-user, but also illustrates additional evidence of our technical proficiency with Python.

---
With thanks from the developers:

<ins>**D**</ins>erek, <ins>**J**</ins>etsun, <ins>**E**</ins>lina, <ins>**K**</ins>o, <ins>**I**</ins>mran, <ins>**I**</ins>skander and <ins>**N**</ins>arcis

We hope you enjoy **DJEKIIN** Health




