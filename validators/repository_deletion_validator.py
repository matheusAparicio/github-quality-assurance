from validators.github_validator import GithubValidator
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class RepositoryDeletionValidator(GithubValidator):

    def __init__(self, driver: webdriver, userName: str):
        super().__init__(driver)
        self.userName = userName
        self.repositoryName = ''

    # Runs after the repository creation and delete the created repository.
    def validateRepositoryDeletion(self):
        try:
            self.driver.find_element(By.ID, "settings-tab").click()
        except:
            print("[!] Repository deletion error! Repository page not found.")

        # Wait until the repository rename input is visible, then save it.
        WebDriverWait(self.driver, timeout=5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "details.flex-md-order-1 > summary:nth-child(1)"))
        )
        self.repositoryName = self.driver.find_element(By.ID, "rename-field").get_attribute("value")

        # Clicks in the delete repository button, then send the confirmation input to delete.
        self.driver.find_element(By.CSS_SELECTOR, "details.flex-md-order-1 > summary:nth-child(1)").click()
        self.driver.find_element(By.CSS_SELECTOR, "details.flex-md-order-1 > details-dialog:nth-child(2) > "
                                                  "div:nth-child(3) > form:nth-child(4) > p:nth-child(3) > "
                                                  "input:nth-child(1)").send_keys(f"{self.userName}/{self.repositoryName}")

        # Waits until the confirm delete button became clickable.
        try:
            WebDriverWait(self.driver, timeout=10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-danger:nth-child(4)"))
            )
            self.driver.find_element(By.CSS_SELECTOR, "button.btn-danger:nth-child(4)").click()
            self.__confirmDeletion()
        except:
            print("[!] Repository deletion failure! The confirmation input wasn't properly typed.")

    # Checks the page url after deletion. Then try to open the deleted repository page.
    def __confirmDeletion(self):
        try:
            WebDriverWait(self.driver, timeout=5).until(
                EC.url_to_be(f"https://github.com/{self.userName}?tab=repositories")
            )
            self.driver.get(f"https://github.com/{self.userName}/{self.repositoryName}")
            WebDriverWait(self.driver, timeout=5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.position-relative:nth-child(2) > "
                                                                      "img:nth-child(1)"))
            )
            print("[+] Repository deletion working successfully!")
        except:
            print("[!] The repository deletion has encountered an error!")
