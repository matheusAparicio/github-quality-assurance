from login import Login
from github_validator import GithubValidator

credentials = Login()
validator = GithubValidator(credentials.userEmail, credentials.userPassword)

# Program main function
if __name__ == "__main__":
    validator.validateLogin()
    validator.validateRepositoryCreation()
    #validator.validateSearch()
    validator.finalizeValidator()
