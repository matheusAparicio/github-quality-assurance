from login import Login
from validators.github_validator import GithubValidator
from validators.login_validator import LoginValidator
from validators.search_validator import SearchValidator
from validators.repository_creation_validator import RepositoryCreationValidator
from validators.repository_deletion_validator import RepositoryDeletionValidator
from selenium import webdriver

credentials = Login()
webDriver = webdriver.Firefox()
githubValidator = GithubValidator(webDriver)
loginValidator = LoginValidator(webDriver, credentials.userName, credentials.userPassword)
searchValidator = SearchValidator(webDriver)
repositoryCreationValidator = RepositoryCreationValidator(webDriver)
repositoryDeletionValidator = RepositoryDeletionValidator(webDriver, credentials.userName)

# Program main function
if __name__ == "__main__":
    loginValidator.validateLogin()
    searchValidator.validateSearch()
    repositoryCreationValidator.validateRepositoryCreation()
    repositoryDeletionValidator.validateRepositoryDeletion()
    githubValidator.finalizeValidator()
