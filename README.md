# SPM

# Setup Guide:

## 1. pip install -r requirements.txt

## 2. Turn on WAMP (or MAMP if you are on Mac, LAMP if you are on Linux)

## 3. Copy the codes from Database_init.sql and in phpmyadmin, login with your credentials and go to SQL and paste out the code
### a. You can opt to import the sql file as well however, this may lead to some bugs (so we recommend copy pasting the codes instead)

## 4. Create a '.env' file that includes the URL to our database (with mysqlconnector)
### a. For example, on default Windows:
###    dbURL = mysql+mysqlconnector://root@localhost:3306/one_stop_lms

## 5. Run course_and_class.py --> python course_and_class.py

## 6. Access the home page (as a learner/trainer) at http://localhost:5001/home

## 7. Access the home page (as a HR/admin) at http://localhost:5001/hr-home


## Note:

## If there are any issues, please email us at wellsonah.2019@scis.smu.edu.sg

## Future work:
## As user logins have not yet been implemented, we have made the default user to UserID 1 -- which is a senior engineer who has classes enrolled and classes to teach.

## As for HR/admin, there are no user restrictions as of now. There is no need to specify any login credentials as the page is currently "open" to all users.

## When user logins are implemented, this will be fixed.