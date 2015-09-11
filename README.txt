Prerequisites
-Python
-PostgreSQL

Quick start
-Install Vagrant and VurtualBox.
-Clone the fullstack-nanodegree-vm from following address:
  https://github.com/udacity/fullstack-nanodegree-vm
-Launch the vm with "vagrant up" command.
-Connect to the vm with "ssh" command.
-"CD" to "tournament" folder.
-For getting the database ready enter the following command on the  command line:
 "psql \i tournament.sql;".
-Run "tournament_test.py" with the following command to see the results:
 "python tournament_test.py".

What's included
-tournament_results/
 |-- tournament/
 |   |--  tournament.py
 |   |--  tournament_test.py
 |   |--  tournament.sql
 |--README.txt
