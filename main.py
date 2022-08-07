from login import Login
from validator import Validator

# Program main function
if __name__ == "__main__":
    credentials = Login()
    validator = Validator(credentials.userEmail, credentials.userPassword)
