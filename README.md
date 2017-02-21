# Instacart-Shopper-Challenege

## Pre-requites
* python 2.7
* Django 1.4

## Setup Environment
* Install pip
    * sudo apt-get install python-pip
* Install django 
    * sudo pip install django=1.4
* Install git
    * sudo apt-get install git

## Setup Application
* Checkout Instacart-Shopping-Challenge from github
    * git clone https://github.com/osg9c1/Instacart-Shopper-Challenege.git
    * cd Instacart-Shopper-Challenege/instacart
* add the development.sqlite3 to Instacart-Shopping-Challenge/instacart/, as the 
  size of the file is larger than 100MB so I wasn't able to push to github.

* python manage.py syncdb
* python manage.py runserver



## Apps: 
I have created 2 separate apps for each part of the problem, each with its own model, views and templates.

### Shopper Applicants
  local setup link : http://localhost:8000/instacart/shoppers
  Here is the heroku link for the app : http://hidden-brushlands-72379.herokuapp.com/instacart/shoppers/


### Applicant Analysis
   local setup link: http://localhost:8000/instacart/applicant_analysis
    
    Since the development.sqlite3 file was greater than 100MB, I wasn't able to push it to git and 
    hence heroku, so it needs to be  run locally 
 
   Trade off: In the Applicants model, I would have modeled it with workflow_state 
   as an IntegerField with choices as <applied,quiz_started,quiz_completed,onboarding_requested,onboarding_completed,hired,rejected >, to make the query faster as interger comparisons are 
   faster than string comparisons 
