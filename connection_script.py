import sqlite3

departments = ("Accident and emergency services", "Bariatric surgery", "Bladder cancer services",
               "Breast Surgery", "Cardiac services (community)", "Cardiology","Child health care services",
               "Chronic Obstructive Pulmonary Disease", "Cognitive behavioural therapy services",
               "Colorectal cancer services", "Cardiothoracic surgery", "Children's & Adolescent Services",
               "Complementary Medicine", "Dementia Services", "Dental anxiety management", "Dental services (community)",
               "Diabetic Medicine", "Diagnostic Endoscopy", "Diagnostic Imaging", "Dermatology", "Emergency Abdominal Surgery",
               "Endocrine and thyroid surgery", "Epilepsy services", "Ear", "Endocrinology and Metabolic Medicine",
               "General Surgery", "Geriatric Medicine", "Gastrointestinal and Liver services", "General Medicine",
               "Gynaecology", "Haematology", "Imaging services", "Inpatient Diabetes", "Intensive Care",
               "Interventional Radiology", "Immunology", "Infectious Diseases", "Lung cancer services",
               "Major trauma", "Maternity services", "Mental Health - Adults of all ages", "Multiple sclerosis services",
               "Neonatal Care", "Neurological cancer services", "Neurophysiology services", "Neuro-psychology services",
               "Neurosurgery", "Neurology", "Obstetrics And Gynaecology", "Oesophago-Gastric cancer surgery",
               "Orthotics and Prosthetics", "Obstetrics", "Ophthalmology", "Oral and Maxillofacial Surgery",
               "Orthopaedics", "Paediatric Surgery", "Pain Management", "Palliative Medicine", "Pharmacy services",
               "Phlebotomy services", "Podiatry", "Prostate Cancer Service", "Physiotherapy", "Rehabilitation",
               "Restorative dentistry", "Rheumatology", "Respiratory Medicine", "Services of a dental hygienist",
               "Skin cancer services", "Sleep Medicine", "Speech and language services", "Sports and Exercise Medicine",
               "Stroke", "Therapy services", "Urology", "Urgent Treatment Centre")


conn = sqlite3.connect('../database.db')
fd = open('sqlcode.sql', 'r')
sqlFile = fd.read()
fd.close()
conn.executescript(sqlFile)
script='INSERT INTO Departments Values ("{}")'
for i in departments:
    conn.executescript(script.format(i))



