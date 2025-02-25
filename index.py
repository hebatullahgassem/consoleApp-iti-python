import json
import re
import hashlib
from datetime import datetime

USER_DB = "users.json"
PROJECT_DB = "projects.json"

def load_users():
    try:
        with open(USER_DB, "r") as file:
            return json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        return{}
    
def save_users(users):
    with open(USER_DB, "w") as file:
        json.dump(users, file, indent=4)

def load_projects():
    try:
        with open(PROJECT_DB, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
def save_projects(projects):
    with open(PROJECT_DB, 'w') as file:
        json.dump(projects, file, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

def validate_phone(phone):
    return re.match(r"^01[0-2,5]{1}[0-9]{8}$", phone)

def validate_date(date_text):
    try: 
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

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
    return email

def admin_activate():
    users = load_users()
    email = input('enter user email to activate: ')

    if email in users:
        users[email]['activated'] = True
        save_users(users)
        print('user activated successfully!')
    else:
        print('user not found!')

def create_project(user_email):
    projects = load_projects()
    title = input('enter project title: ')
    details = input('enter project details: ')
    target = input('enter total target amount (EGP): ')
    start_date = input('enter start date (YYYY-MM-DD): ')
    end_date = input('enter end date (YYYY-MM-DD): ')

    if not validate_date(start_date) or not validate_date(end_date):
        print('invalid date format!')
        return
    
    project_id = len(projects) + 1
    projects[project_id] = {
        "owner": user_email,
        "title": title,
        "details": details,
        "target": target,
        "start_date": start_date,
        "end_date": end_date
    }
    save_projects(projects)

    print("project created successfully!")


def view_projects():
    projects = load_projects()
    for project_id, project in projects.items():
        print(f"\nID: {project_id}\nTitle: {project['title']}\nDetails: {project['details']}\nTarget: {project['target']} EGP\nStart Date: {project['start_date']}\nEnd Date: {project['end_date']}")


def main():
    logged_in_user = None

    while True:
        print('\nCrowdFunding App')
        print('1. Register')
        print('2. Login')
        print('3. Admin Activate User')
        print("4. Create Project")
        print("5. View Projects")
        print("6. Exit")

        choice = input('choose an option: ')

        if choice == '1':
            register()
        elif choice == '2':
            logged_in_user = login()
        elif choice == '3':
            admin_activate()
        elif choice == '4':
            if logged_in_user:
                create_project(logged_in_user)
            else:
                print("please log in first!")
        elif choice == '5':
            view_projects()
        elif choice == '6':
            break
        else:
            print('invalid choice!')

if __name__ == "__main__":
    main()