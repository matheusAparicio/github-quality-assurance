from login import Login
from validator import GithubValidator

# Program main function
if __name__ == "__main__":
    credentials = Login()
    validator = GithubValidator(credentials.userEmail, credentials.userPassword)
    validator.validateLogin()
    validator.validateSearch()
    validator.finalizeValidator()
