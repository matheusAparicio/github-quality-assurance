from validators.github_validator import GithubValidator
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.string_utilities import StringUtilities


class RepositoryCreationValidator(GithubValidator):

    def __init__(self, driver: webdriver):
        super().__init__(driver)

    def validateRepositoryCreation(self):
        self.driver.get("https://github.com/")
        # Waits until find a new repository button.
        try:
            WebDriverWait(self.driver, timeout=10).until(
                EC.visibility_of_any_elements_located((By.XPATH, "/html/body/div[5]/div/aside/div/div[2]/div/h2/a | "
                                                                 "/html/body/div[5]/div/aside/div/div[1]/div/div/a[1]"))
            )
            newRepositoryButton = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/aside/div/div[2]/div/h2/a | "
                                                                     "/html/body/div[5]/div/aside/div/div[1]/div/div/a[1]")
            newRepositoryButton.click()
            self.__configureRepository()
            self.__validateNewProject()

        except:
            print("[!] Repository creation error! No create repository button was found.")
            return

    def __configureRepository(self):
        WebDriverWait(self.driver, timeout=10).until(
            EC.visibility_of_element_located((By.ID, "repository_name"))
        )
        # Configures the new repository.
        self.driver.find_element(By.ID, "repository_name").send_keys(f"{StringUtilities.randomString(6)}-"
                                                                     f"{StringUtilities.randomString(6)}")
        self.driver.find_element(By.ID, "repository_visibility_private").click()

        # Waits until the confirm button is enabled.
        try:
            WebDriverWait(self.driver, timeout=10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary"))
            )
            self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        except:
            print("[!] Failure! Project name wasn't accepted.")

    # Search for the code button of the new project.
    # In the case that it isn't found, an error is returned.
    def __validateNewProject(self):
        try:
            WebDriverWait(self.driver, timeout=5).until(
                EC.visibility_of_element_located((By.ID, "code-tab"))
            )
            print("[+] Repository creation working successfully!")
        except:
            print("[!] Repository creation failure.")
