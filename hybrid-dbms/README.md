# Hybrid SQL + NoSQL Mini-DBMS :



##### This project is a simple example of a hybrid database system that uses both MySQL and MongoDB. The system automatically decides where data should be stored based on its type. Structured and short data is saved in MySQL, while long or unstructured data such as large text or files is stored in MongoDB.

##### 

##### It shows how SQL and NoSQL can work together in one small application. The backend is built using FastAPI in Python, and there is a basic HTML page for entering and submitting data. Docker is used so everything can run smoothly without any manual setup.

##### 

##### About the Project

##### 

##### This project demonstrates how a single system can manage two types of databases. MySQL stores structured records or small text, while MongoDB is used when the data is unstructured or contains documents. This approach makes the system efficient.



#### How to Run :

#### 

###### 1 - Make sure Docker Desktop is installed and running.

###### 

###### 2 - Open the project folder in a terminal and run : docker compose up -d

###### 

###### 3 - Install the required Python packages: pip install -r requirements.txt

###### 

###### 4 - Start the backend server: uvicorn backend.main:app --reload --port 8000

###### 

###### 5 - Open frontend/index.html in your browser. Fill out the form and submit the data to test.

###### 

#### Tools Used: 



###### Python (FastAPI)

###### 

###### MySQL

###### 

###### MongoDB

###### 

###### SQLAlchemy and PyMongo

###### 

###### HTML and JavaScript

###### 

###### Docker



#### Project Goal



###### The goal of this project is to show how SQL and NoSQL databases can be combined to create a flexible data management system. It’s a small but complete demonstration of a modern hybrid DBMS that can handle both structured and unstructured information efficiently.

