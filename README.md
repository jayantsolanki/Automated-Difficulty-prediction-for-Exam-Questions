***
#  Automated-Difficulty-prediction-for-Exam-Questions

## Motivation
***
* To address the challenges faced in ensuring authenticity and fairness for Test-Takers to who attempt Online Exams.
* The challenge is to ensure each question set for test-taker contains questions of similar difficulty levels.
* Come-up with a web-application which will ensure that the questions are tagged with correct difficulty level for next iteration of Exam, using machine learning analysis on the performance of test-takers for previous exam.

## Ojectives achieved
***
* Identification of the features in the Exam Question Data
* Development of Machine Learning Algorithm for predicting the difficulty levels or tags of the Question Data
* Provide User Interface for Question Creators with following features:
  * Provision for performing Machine Learning analysis on Selected Exam Data
  * Creation of Analysis report on difficulty tagging for each year‘s Exam data
  * Statistics for change in the tags, that is, deficits and excess, overall
  * Adding new Questions
  * Editing Previous Questions
  * Provided Question Revision history and provision to mark question active or inactive
  * Provided Audit trail on Questions
  * Question Sets creation with the option of shuffling and pagination
  * User Management for Admin, Question Editor and Moderator


## Implementation
***
#### Workflow
<img src="https://github.com/jayantsolanki/Automated-Difficulty-prediction-for-Exam-Questions/blob/master/docs/PPT/block.png" width=80% height=80%>

#### Usecase
<img src="https://github.com/jayantsolanki/Automated-Difficulty-prediction-for-Exam-Questions/blob/master/docs/PPT/usecase.png" width=50% height=50%>

## Documentation
***
Report and documentation can be found on this [Documentation](https://github.com/jayantsolanki/Automated-Difficulty-prediction-for-Exam-Questions/tree/master/docs)

## Folder Tree
***
* [**docs**](https://github.com/jayantsolanki/Automated-Difficulty-prediction-for-Exam-Questions/tree/master/docs) contains documentation and paper
* [**release**](https://github.com/jayantsolanki/Automated-Difficulty-prediction-for-Exam-Questions/tree/master/release) contains implmentation codes and libraries
* [**src**](https://github.com/jayantsolanki/Automated-Difficulty-prediction-for-Exam-Questions/tree/master/src) contains codes
  * 611-Proj-Ques-Eval-Frontend: Contains the Website
  * Python-Web-Server: Provide REST APIs solution for running Machine Learning Algorithm

 
## Contributors
***
  * [Jayant Solanki](https://github.com/jayantsolanki)
  
## Instructor
***
Prof. Alan Hunt, CSE Dept. University at Buffalo - SUNY

## Tech-stack
* Machine Learning
  * Python 3.6
  * Tornado for Rest APIs
  * SQLAlchemy
  * Matplotlib for plotting the clusters
* Web Development
  * Laravel 5.4 with Symphony and Eloquent ORM
  * PHP 7
  * MySQL
  * Apache Server for deploying the Website
  * Bootstrap 3.6
  * Google Charts
  
## Acknowledgement
***
* e-Yantra, IIT-Bombay
## License
***
This project is open-sourced under [MIT License](http://opensource.org/licenses/MIT)
