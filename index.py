import json
import re
import hashlib

USER_DB = "users.json"

def load_users():
    try:
        with open(USER_DB, "r") as file:
            return json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        return{}
    
def save_users(users):
    with open(USER_DB, "w") as file:
        json.dump(users, file, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

def validate_phone(phone):
    return re.match(r"^01[0-2,5]{1}[0-9]{8}$", phone)

def register():
    users = load_users()
    email = input("enter email: ")
    
    if email in users:
        print('email already register!')
        return
    
    if not validate_email(email):
        print('invalid email format!')
        return
    
    firstName = input('enter your first name: ')
    lastName = input('enter your last name: ')
    phone = input('enter your mobile number: ')

    if not validate_phone(phone):
        print('phone numberis not valid!')
        return
    
    password = input('enter password: ')
    confirmPassword = input('confirm password: ')

    if password != confirmPassword:
        print('passwords donnot match!')
        return
    
    users[email] = {
        "firstName": firstName,
        "lastName": lastName,
        "phone": phone,
        "hash_password": hash_password(password),
        "activated": False
    }
    save_users(users)
    print('registration successful! wait for activation.')

def login():
    users = load_users()
    email = input("Enter email: ")
    password = input("Enter password: ")

    if email not in users:
        print("no account found with this email!")
        return
    
    if not users[email]['activated']:
        print('account not activated. contact admid.')
        return
    
    if users[email]["hash_password"] != hash_password(password):
        print('incorrect password!')
        return
    
    print(f"welcome, {users[email]["firstName"]}!")

def admin_activate():
    users = load_users()
    email = input('enter user email to activate: ')

    if email in users:
        users[email]['activated'] = True
        save_users(users)
        print('user activated successfully!')
    else:
        print('user not found!')

def main():
    while True:
        print('\nCrowdFunding App')
        print('1. Register')
        print('2. Login')
        print('3. Admin Activate User')
        print('4. Exit')

        choice = input('choose an option: ')

        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            admin_activate()
        elif choice == '4':
            break
        else:
            print('invalid choice!')

if __name__ == "__main__":
    main()