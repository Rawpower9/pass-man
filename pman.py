#!/usr/bin/env python3
import base64
import getpass
import hashlib
import json
import subprocess
from cryptography.fernet import Fernet
import readchar
import sys
import os
import clipboard
import random
import threading
import datetime
import time as t

max_time = 30 # timeout after max_time (in seconds)
stop_proc = {}
end_all_threads = False
def input_t(text):
    global stop_proc
    id = gen_id(stop_proc=stop_proc)
    stop_proc[id] = False
    l = threading.Thread(target=end, args=(id,))
    l.start()
    output = input(text)
    stop_proc[id] = True
    return output

def gen_id(stop_proc):
    for k,v in stop_proc.items():
        if v == False:
            return k

    return len(stop_proc.items())

def end(id):
    global stop_proc, end_all_threads
    for i in range(int(max_time)):
        if end_all_threads:
            sys.exit(0)
        t.sleep(1)
    if not stop_proc[id]:
        os._exit(0)
    else:
        stop_proc[id] = False


    
def read_file(path):
    f = open(path+"pass.txt",'r')
    data = json.load(f)
    f.close()
    return data

def write_file(file, path):
    f = open(path+"pass.txt", 'w')
    json.dump(file, f, indent=6)
    print("written")
    f.close()

file="not init"

def load(fernet, path):
    global file
    file = read_file(path)
    main_menu(fernet, path)

def main_menu(fernet, path):
    global end_all_threads
    print("\nDo you want to")
    print("1. Add a site")
    print("2. Remove a site")
    print("3. View passwords")
    print("4. Generate a password")
    print()
    print("99. Quit")
    print()
    try:
        number = int(input_t("go_to> "))
    except:
        print("should be a number")
        main_menu(fernet,path)
    print()
    if number == 1:
        add_site(fernet)
    if number == 2:
        remove_site(fernet, path)
    if number == 3:
        view_sites(fernet)
    if number == 4:
        generate_password(fernet)
    else:
        end_all_threads = True
        sys.exit(0)



def generate_password(fernet):
    while True:
        gen_len = input_t("How long should the password be?\n")
        while True:
            try:
                gen_len = int(gen_len)
                break
            except TypeError:
                print("Type an integer!")
        security = input_t(
            "How secure do you want you password? (l=lower, u=upper, n=number, s=symbol; you may do a combination; type nothing if you want all)\n").lower()
        sec_list = []  # 33 to 126 [97-122=l][65-90=u][48-57=n][else=s]

        def arange(start, stop, step):
            res = []
            for i in range(start, stop, step):
                res.append(i)
            return res

        lower_list = arange(97, 122+1, 1)
        upper_list = arange(65, 90+1, 1)
        number_list = arange(48, 57+1, 1)
        symbol_list = arange(33, 48, 1) + arange(57+1, 65, 1) + \
            arange(90+1, 97, 1) + arange(122+1, 126+1, 1)

        if 'l' in security:
            sec_list += lower_list
        if 'u' in security:
            sec_list += upper_list
        if 'n' in security:
            sec_list += number_list
        if 's' in security:
            sec_list += symbol_list
        if security.strip() == "":
            sec_list = lower_list + upper_list + number_list + symbol_list

        password = ""
        for i in range(gen_len):
            rand = random.randint(0, len(sec_list)-1)
            password += chr(sec_list[rand])

        clipboard.copy(password)
        like_pass = input_t(
            "Your password has been copied to your clipboard, do you like it? (y/n)")
        if like_pass.lower() == 'y':
            break
    main_menu(fernet=fernet, path=path)

def take_input(words):
    global stop_proc
    id = gen_id(stop_proc=stop_proc)
    stop_proc[id] = False
    l = threading.Thread(target=end, args=(id,))
    l.start()
    given = ""
    sys.stdout.write(" ")
    while True:
        c = ''
        c = readchar.readchar()
        if ord(c) == 127:
            given = given[:-1]
        elif ord(c) == 13:
            for i in words:
                if given.strip() == i.strip():
                    stop_proc[id] = True
                    return given
            print("\n" + given, "does not match any known sites")
        elif ord(c) == 9:
            back = auto_complete(words, given)

            if len(back) == 1:
                given = back[0]
            elif len(back) == 0:
                pass
            else:
                for i in back:
                    print(i, end=", ")
                print()
        else:
            if 31 <= ord(c) <= 126:
                given += c
        sys.stdout.write("\r" + given + " ")
    return given

def auto_complete(items, word):
    final = []
    for i in items:
        if word in i:
            final.append(i)
    return final

def add_site(fernet):
    global file
    print("")
    print("What site do you want to add?")
    site = input_t("")
    for k in file.keys():
        if site.strip() == fernet.decrypt(k.encode('utf-8')).decode('utf-8').strip():
            print("This site already exists")
            print("Are you sure you want to continue?(y/n):   ")
            val = input_t("").lower()
            if val == "yes" or val == "y":
                break
            else:
                main_menu(fernet,path)
    everything = {}
    username = input_t("What is the username for this site?\n")
    while True:
        gen_pass = input_t("Do you want to generate a password? (The alternative is typing in your own password) (y/n):   ")
        if (gen_pass.lower() == 'y'):
            while True:
                gen_len = input_t("How long should the password be? (int): ")
                try:
                    gen_len = int(gen_len)
                    break
                except TypeError:
                    print("Type an integer!")
            security = input_t("How secure do you want you password? (l=lower, u=upper, n=number, s=symbol; you may do a combination; type nothing if you want all)").lower()
            sec_list = [] #33 to 126 [97-122=l][65-90=u][48-57=n][else=s]
            def arange(start, stop, step):
                res = []
                for i in range(start, stop, step):
                    res.append(i)
                return res


            lower_list = arange(97, 122+1, 1)
            upper_list = arange(65, 90+1, 1)
            number_list = arange(48, 57+1, 1)
            symbol_list = arange(33, 48, 1) + arange(57+1, 65, 1) + \
                arange(90+1, 97, 1) + arange(122+1, 126+1, 1)

            if 'l' in security:
                sec_list += lower_list
            if 'u' in security:
                sec_list += upper_list
            if 'n' in security:
                sec_list += number_list
            if 's' in security:
                sec_list += symbol_list
            if security.strip() == "":
                sec_list = lower_list + upper_list + number_list + symbol_list
            
            password = ""
            for i in range(gen_len):
                rand = random.randint(0,len(sec_list)-1)
                password += chr(sec_list[rand])
            
            clipboard.copy(password)
            like_pass = input_t("Your password has been copied to your clipboard, do you like it? (y/n):   ")
            if like_pass.lower() == 'y':
                break
        else:
            print("\nWhat is the password for this site?")
            password = getpass.getpass()
            print("To ensure we have the correct password, can you type it again?")
            password1 = getpass.getpass()
            if password1 == password:
                everything[fernet.encrypt("username".encode('utf-8')).decode('utf-8')] = fernet.encrypt(username.encode('utf-8')).decode('utf-8')
                everything[fernet.encrypt("password".encode('utf-8')).decode('utf-8')] = fernet.encrypt(password.encode('utf-8')).decode('utf-8')
                break
            else:
                print("Passwords did not match, please try again")
    while True:
        print("Any other fields? Type no to finish")
        user_field = input_t("")
        if user_field.lower() == "no" or user_field.lower() == "n":
            break
        print("")
        print("What will the value for " + user_field + " be?")
        user_val = input_t("")

        print("The field, " + '\033[1m' + user_field + "\033[0m and the value, " +  '\033[1m' + user_val + "\033[0m is correct?")
        val = input_t("")
        if val.lower() == 'y' or val.lower() == "yes":
            everything[fernet.encrypt(user_field.encode('utf-8')).decode('utf-8')] = fernet.encrypt(user_val.encode('utf-8')).decode('utf-8')
    print("Do you want to see all fields for ", str(site)+"? (yes/no)")
    val = input_t("")
    if val.lower() == "yes" or val.lower() == "y":
        while True:
            for v,k in everything.items():
                print("The field, " + '\033[1m' + v + "\033[0m has the value, " + '\033[1m' + k + "\033[0m")
            print("Do you want to change anything? (yes/no)")
            val = input_t("")
            if val.lower() == "yes" or val.lower() == "y":
                print("what field do you want to change?")
                val = take_input(everything.keys())
                for i in everything.keys():
                    if val in i:
                        print("what do you want to change the field",i,"to?")
                        val = input_t("")
                        everything[i] = val
                        print("The field, " + '\033[1m' + i + "\033[0m changed to " + '\033[1m' + val + "\033[0m")
                        print()

    file[fernet.encrypt(site.encode('utf-8')).decode('utf-8')] = everything
    write_file(file, path)
    main_menu(fernet, path)

def remove_site(fernet, path):
    global file
    print("\n")
    print("In order to ensure that this is actually you, we are going to undergo a quick security check. Enter your password")
    for i in range(3):
        try:
            gfg = hashlib.sha256(str.encode(getpass.getpass()))
        except:
            print("wrong password")
            raise IOError

        key = base64.urlsafe_b64encode(gfg.digest())
        try:
            fernet = Fernet(key)
        except:
            print("wrong password")
            continue
        if fernet.decrypt(open(path+'test.txt', 'rb').read()) == b'password':
            print("authenticated")
            sites = []
            for i in file.keys():
                sites.append(fernet.decrypt(i.encode('utf-8')).decode('utf-8'))
            print("Which site do you want to remove?")
            site = take_input(sites)
            for i, v in zip(sites, file.keys()):
                if site in i:
                    print("removing", i)
                    print("Are you sure you want to do this action?")
                    conf = input_t("")
                    if conf.lower() == "y" or conf.lower() == "yes":
                        print("removing", i)
                        file.pop(v)
                        write_file(file, path)
                    main_menu(fernet, path)


def view_sites(fernet):
    global file
    sites = []
    values = []
    for k,v in file.items(): #key,value
        sites.append(fernet.decrypt(k.encode('utf-8')).decode('utf-8'))
        values.append(v)
    print("Where do you want to get your creds from? (99 to quit)")
    print("go_to>")
    site = take_input(sites)
    if (site == "99"):
        main_menu(fernet, path)
    for num, sites in enumerate(sites):
        if site in sites:
            creds = values[num]
            keys = []
            values = []
            for k,v in creds.items():
                keys.append(fernet.decrypt(k.encode('utf-8')).decode('utf-8'))
                values.append(fernet.decrypt(v.encode('utf-8')).decode('utf-8'))
            print()
            while True:
                print()
                for number, site_name in enumerate(keys):
                    print(str(number)+". Copy the "+site_name)
                print("99. quit"+"\n")
                number = input_t("go_to>")
                if not number.isalnum():
                    print("Type a number")
                    continue
                if int(number) == 99:
                    break
                if int(number) >= len(values) or int(number) < 0:
                    continue
                clipboard.copy(values[int(number)])
            break
    main_menu(fernet, path)

if __name__ == "__main__":
    global now
    print("THIS IS YOUR PASSWORD MANAGER")
    print("PLEASE ENTER YOUR PASSWORD TO CONTINUE")
    for i in range(3):
        gfg = hashlib.sha256(str.encode(getpass.getpass()))
        key = base64.urlsafe_b64encode(gfg.digest())
        fernet = Fernet(key)
        path = subprocess.run(["which", "pman.py"], capture_output=True).stdout.decode().strip().removesuffix("pman.py")
        try:
            value = fernet.decrypt(open(path+'test.txt', 'rb').read()) == b'password'
        except:
            value = False
            print("wrong password")
        if value:
            print("authenticated")
            now = datetime.datetime.now()
            load(fernet, path)
            sys.exit(0)