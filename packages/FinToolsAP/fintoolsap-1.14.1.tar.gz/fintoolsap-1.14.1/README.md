# Financial Tools Andrew Perry (FinToolsAP)

Author: Andrew Maurice Perry
Email: Andrewpe@berkeley.edu
Start Date: 06/20/2023

Overall Module Description:
This module implements several tools that are commonly used 
in finance and economics. Currently includes LocalDatabase and
Fama French functionally. 

Version Date: 11/06/2023
Version Updates: Production build of local database

-----------------------------------------------------------------------------------

Local Database
----------------------

Description: 
Implement a local database that can be used to greatly speed up work flow.
The database is meant for financial data but can be used to store any type of
data. The class uses a SQLite3 backend to manage the database via sqlalchemy
and provides a python3 wrapper making the use of the data database very 
quick and efficient by returning a pandas dataframe object that is formatted to
(i.e. correct datatypes, only specified columns, sorted, etc).
Data can be added in two ways: (1) CSV files can be read 
into the database from a local folder and (2) the database also interfaces 
with Whartons Research Data Services to automatically download specified tables.

Database File Structure:

save_directory/database_name/
	|-- database_name.db
	|-- DatabaseParameters.py
	|-- CSVtoSQL/
	|-- CreateTables/

database_name.db: This is the main database file storing all of the data. This file 
should NOT be modified. Modifying this file may compromise the operation of the 
local database. However, this is a SQL database that can be opened/modified by 
using SQLite3. 

CSVtoSQL/: This folder contains the CSV files that should be read into the database. 
This is particularly useful for large files that cannot be stored in RAM. The method of 
reading in the CSV files completely bypasses system memory and moves data around
on disk. The name that is given the the CSV file in this folder will be the name of the 
table inside the SQL database.

CreateTables/: This folder contains python scripts used to make user defined tables.
These tables can use data that is already present within the database or additional 
files stored outside the database. These scripts will create tables in the database with 
the same name as the script itself and are run in the order specified in the 
DatabaseParameters.py file and "Tables.CREATED_TABLES" attribute. (See below)

DatabaseParameters.py (DBP): This file defines how the database operates. It is organized 
as several python classes. Classes are used to define information required by the database. 
This is the most important file for the operation of the database. 
This is the file that the user of the database should use to modify the operation of 
the database. Below is a description of the structure of the DBP file:

"Tables" Class: 
The tables class defines the tables that are in the database, this includes
the tables that are downloaded from Wharton Research Data Services (WRDS), tables
that should be read in from CSV files in the CSVtoSQL/ folder, and the tables that are 
user created and stored in the database. Additionally, if downloading tables from WRDS
your WRDS username must be specified in the Tables class with the attribute 
"WRDS_USERNAME". 



Adding Data:

Creating Custom Tables:

Querying the Database:







