import requests

url = 'http://localhost'
suffix_start = '/api/conversation/start'
suffix_message = '/api/conversation/message'

session = requests.Session()

print('Enter the language to use. Choices (en or nb): ')
language = input()
while language not in ['en', 'nb']:
    print(f"Previous selected language: {language} not in choices (en or nb). Please enter again: ")
    language = input()

data = {'language': language}
resp = session.post(url=f"{url}{suffix_start}", data=data)
resp_json = resp.json()
print(f"Response Status code: {resp.status_code}")
print(f"Response Json: {resp_json}")
user_id = resp_json['user_id']
message = resp_json['message']
print(f"Response    User_ID: {user_id}    Message: {message}")

while True:
    print("\nEnter the message you want to send to chatbot. To quit enter X or x")
    question = input()
    if question in ['X', 'x']:
        print("GoodBye")
        exit(0)
    data = {'user_id': user_id, 'message': question}
    resp = session.post(url=f"{url}{suffix_message}", data=data)
    resp_json = resp.json()
    print(f"Response Status code: {resp.status_code}")
    print(f"Response Json: {resp_json}")
    message = resp_json['message']
    print(f"Response    User_ID: {user_id}    Message: {message}")