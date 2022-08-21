# kindly_chatbot
This repo is created to solve interview assignment- Chatbot

## File Structure
* chatbot_server.py:- This is the starting point of application. Run this file to start the server and the apis. Run this as ```python3 chatbot_server.py```
* chatbot_helper.py:- This file consists of helper functions to serve api requests
* logger.py:- This file defined logger for logging messages
* config.py:- This is used to have config for the application
* constants.py:- This file contains all the constants value
* chatbot_config.json:- This json file can be used to alter default values specified in constants.py file
* chatbot_client.py:- This file serves as chatbot client in addition to Postman, Insomnia. It can start with asking language option and then questions
* requirements.txt: This file specifies all the packages to run above application. Run this as `pip3 install -r requirements.txt`

# APIs created
Created two APIs. One for the greeting and second one to generate response for the question

* Greeting API: /api/conversation/start
```
REQUEST: POST http://localhost/api/conversation/start
REQUEST BODY: {“language”: “en”}
RESPONSE: {'user_id': '9003427b-2142-484c-81c1-db39111e6585', 'message': 'Hi there!'}
```

```
REQUEST: POST http://localhost/api/conversation/start 
REQUEST BODY: {"language": "nb"}
RESPONSE: {'user_id': 'a5fec511-0477-45af-9308-dcb6d436fd76', 'message': 'Heisann!'}
```

* Message API: /api/conversation/message
```
REQUEST: POST http://localhost/api/conversation/message
REQUEST BODY: {"message": "Do you know any robot jokes?"}
RESPONSE: {'message': 'Why did the robot start school again? He had become quite rusty ...'}
```

```
REQUEST: POST http://localhost/api/conversation/message
REQUEST BODY: {"message": "Kan du noen robotvitser?"}
RESPONSE: {'message': 'Vet du hvorfor roboter tar sommerferie? For å lade batteriene!'}
```

 # Initial Setup

 Install all the dependencies mentioned in requirements.txt. Create a virtualenv and then use pip3 to install dependencies

 ```
 virtualenv <path>
 source <path>/bin/activate
 pip3 instal -r requirements.txt
 ```

 # Run Application

 Activate above created virtualenv, Then run chatbot_server.py file

 ```
 source <path>/bin/activate
 python3 chatbot_server.py
 ```

 # Run Chatbot Client
Activate above created virtualenv, Then run chatbot_server.py file. While application is running, run chatbot_client.py

```
source <path>/bin/activate
python3 chatbot_server.py
python3 chatbot_client.py
```

OUTPUT:-
 ```
python chatbot_client.py
Enter the language to use. Choices (en or nb):
en
Response Status code: 200
Response Json: {'user_id': '857b8dc6-6fbe-4e43-871b-0faa36704981', 'message': 'Hello! I am a chatbot!'}
Response    User_ID: 857b8dc6-6fbe-4e43-871b-0faa36704981    Message: Hello! I am a chatbot!

Enter the message you want to send to chatbot. To quit enter X or x
yes
Response Status code: 200
Response Json: {'message': 'Yes!'}
Response    User_ID: 857b8dc6-6fbe-4e43-871b-0faa36704981    Message: Yes!

Enter the message you want to send to chatbot. To quit enter X or x
yes
Response Status code: 200
Response Json: {'message': 'Yes!'}
Response    User_ID: 857b8dc6-6fbe-4e43-871b-0faa36704981    Message: Yes!

Enter the message you want to send to chatbot. To quit enter X or x
machine learning
Response Status code: 200
Response Json: {'message': 'Chatbots made in Kindly are intelligent because they use machine learning, a technology that enables computers to learn from data.This allows chatbots to understand natural language by looking at actual language examples. Kind of like humans do!'}
Response    User_ID: 857b8dc6-6fbe-4e43-871b-0faa36704981    Message: Chatbots made in Kindly are intelligent because they use machine learning, a technology that enables computers to learn from data.This allows chatbots to understand natural language by looking at actual language examples. Kind of like humans do!

Enter the message you want to send to chatbot. To quit enter X or x
more about machine learning
Response Status code: 200
Response Json: {'message': 'Unlike most other solutions, our NLU (Natural Language Understanding) models are "always on", provide you with instant feedback, and grow with your chatbots. This means that you can take advantage of the latest and greatest in NLU from the very beginning of your chatbot journey, and watch your model become even smarter as heavy-weight training sessions are periodically run behind the scenes.'}
Response    User_ID: 857b8dc6-6fbe-4e43-871b-0faa36704981    Message: Unlike most other solutions, our NLU (Natural Language Understanding) models are "always on", provide you with instant feedback, and grow with your chatbots. This means that you can take advantage of the latest and greatest in NLU from the very beginning of your chatbot journey, and watch your model become even smarter as heavy-weight training sessions are periodically run behind the scenes.

Enter the message you want to send to chatbot. To quit enter X or x
x
GoodBye
 ```