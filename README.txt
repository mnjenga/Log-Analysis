Website Log Analysis

This is a website log analysis application that will use information from the database to discover what kind of articles the site's readers like.

The Application runs from command line connecting to the database and uses SQL queries to analyze the log data, and print out feedback.

Prerequisites

1) The application uses Linux-based virtual machine (VM)
2) You Should have Python 2.7 and higher installed with psycopg2 module installed
3) The program runs on the terminal
4) The application uses postgres sql

Installing

1) Download the log_project.zip file
2) Extract the log_project.py file and save it in the root of your virtual machine


Running the Website

Once you have saved the log_project.py file
1) Go to your terminal and navigate to the root of your VM. Make sure you VM machine is up (eg for vigran by running vagrant up, and you are conected eg by running vagrant ssh)
2) Run the command '$ python log_project.py'
3) The application will run and print the output to screen as well as print to file. 
4) The db views are included in the log_project.py file



Authors

Moses Njenga
