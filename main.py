from login import Login
from validators.github_validator import GithubValidator
from validators.login_validator import LoginValidator
from validators.search_validator import SearchValidator
from validators.repository_creation_validator import RepositoryCreationValidator
from selenium import webdriver

credentials = Login()
webDriver = webdriver.Firefox()
gitValidator = GithubValidator(webDriver)
loginValidator = LoginValidator(webDriver, credentials.userName, credentials.userPassword)
searchValidator = SearchValidator(webDriver)
repositoryCreationValidator = RepositoryCreationValidator(webDriver)

# Program main function
if __name__ == "__main__":
    loginValidator.validateLogin()
    searchValidator.validateSearch()
    # validator.validateRepositoryCreation()
    #validator.finalizeValidator()
