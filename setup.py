import base64
import getpass
import hashlib
import json
from cryptography.fernet import Fernet



if __name__ == "__main__":
    print("THIS IS YOUR PASSWORD MANAGER SETUP TOOL")
    print("You will be prompted to enter your password for this password manager. If your forget your password, then all the data that this password manager stores will be lost. Make sure that you do not forget this password")


    while True:
        gfg = hashlib.sha256(str.encode(getpass.getpass()))
        print("To ensure that we have the correct password (without typos), type the same password again")
        gfg1 = hashlib.sha256(str.encode(getpass.getpass()))
        if gfg.__eq__(gfg1):
            print("successful")
            break
        else:
            print("The passwords didn't match")
            print("try again")

    key = base64.urlsafe_b64encode(gfg.digest())
    fernet = Fernet(key)
    with open('test.txt', 'wb') as file:
        file.write(fernet.encrypt(b'password'))
        #Your password is not replaced by 'password'. 'password' is just a message to check if the user typed the correct password later
        #If the user types the wrong password, the test.txt file will be decrypted incorrectly, and the password manager will prompt the user for their password again

    
    #Create the pass.txt file
    file = {}
    f = open('pass.txt', 'w')
    json.dump(file, f, indent=6)
    f.close()
    print("Process Completed Successfully")