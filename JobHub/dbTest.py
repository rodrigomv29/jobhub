from main import User
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

def verify(user, password):
    print(user)
    print("Encripted password!")
    print(password)
    test_passed = 0
    list = User.query.all()
    second_list = {0: "username", 1: "email",2: "password"}
    
    for i in range(0, len(list)):
        second_list = list[i] 
    
        selection_1 = second_list.username
        selection_3 = second_list.password
        
        print(selection_1)
        print(selection_3)
        
        if selection_1 == user:
            test_passed = test_passed + 1
        
        if selection_3 == password:
             test_passed = test_passed + 1
        
    
    return test_passed


print("hello!")
user = str(input())
print("Hello2!")
password = str(input())
#pw_hash = bcrypt.generate_password_hash(password)
#bcrypt.check_password_hash(pw_hash, password)
test = verify(user, password)
    
print(test)
    #print(selection_1)
    #print(selection_2)
    #print(selection_3)

#for i in range(0, len(list)):
  
#    if i == (len(list)-1):
#        print (str(list[i]))

#for i in range(0, len(list)):
#      if i == (len(list) - 1):
#            second_list = list[i]       

#selection_1 = second_list.username
#selection_2 = second_list.email
#selection_3 = second_list.password