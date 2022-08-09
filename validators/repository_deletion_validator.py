from validators.github_validator import GithubValidator
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class RepositoryDeletionValidator(GithubValidator):

    def __init__(self, driver: webdriver):
        super().__init__(driver)
