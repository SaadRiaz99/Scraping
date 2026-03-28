-- ==========================================================
-- HOSPITAL MANAGEMENT SYSTEM: MS ACCESS WILDCARD QUERIES
-- ==========================================================

-- Query 6: Search for Specialties containing "Physician"
-- ----------------------------------------------------------
SELECT Name, Specialty 
FROM staff 
WHERE Specialty LIKE "*Physician*";


-- Query 7: List patients with phone numbers starting with "0300"
-- ----------------------------------------------------------
SELECT Name, Phone 
FROM Patient 
WHERE Phone LIKE "0300*";


-- Query 8: Find medicines starting with letters A through M
-- ----------------------------------------------------------
SELECT Medicine, Price 
FROM medicine 
WHERE Medicine LIKE "[A-M]*";


-- Query 9: Find Doctors whose names end with "an"
-- ----------------------------------------------------------
SELECT Name 
FROM staff 
WHERE Name LIKE "Dr *an";


-- Query 10: Search for medicines containing "cin" in their name
-- ----------------------------------------------------------
SELECT Medicine, Price 
FROM medicine 
WHERE Medicine LIKE "*cin*";
