import os
from cryptography.fernet import Fernet
from getpass import getpass


class Login:

    def __init__(self):
        self.userName = ""
        self.userPassword = ""
        self.__fernet = self.__initializeKey()
        self.__verifyLoginFile()

    # Checks existence of saved credentials. If it doesn't exist, new credentials are received.
    def __verifyLoginFile(self):
        if os.path.exists("credentials.txt"):
            print("Já existem credenciais de login. Usá-las para os teste?")
            loginChoice = input("(S/s): Você usará as credenciais salvas para logar.\n"
                                "(N/n): As credenciais atuais serão apagadas e você digitará outra.\n"
                                "Qual sua escolha?: ")
            while loginChoice.lower() != 's' and loginChoice.lower() != 'n':
                print("Comando não reconhecido. Tente novamente.")
                loginChoice = input("(S/s): Você usará as credenciais salvas para logar.\n"
                                    "(N/n): As credenciais atuais serão apagadas e você digitará outra.\n"
                                    "Qual sua escolha?: ")
            if loginChoice.lower() == 's':
                with open("credentials.txt", 'rb') as file:
                    lines = file.readlines()
                    self.userName = self.__fernet.decrypt(lines[0]).decode()
                    self.userPassword = self.__fernet.decrypt(lines[1]).decode()
            else:
                self.__deleteLoginInfo()
                self.__getLoginInfo()
        else:
            self.__getLoginInfo()

    # Receives credentials by user input and ask if it will be persisted.
    def __getLoginInfo(self):
        self.userName = input("Digite seu nome de usuário para login no Github: ")
        self.userPassword = getpass("Digite sua senha: ")
        persistChoice = input("Gostaria de salvar suas credenciais?"
                              "(s/n): ")
        while persistChoice.lower() != 's' and persistChoice.lower() != 'n':
            print("Comando não reconhecido. Tente novamente.")
            persistChoice = input("Gostaria de salvar suas credenciais?"
                                  "(s/n): ")
        if persistChoice.lower() == 's':
            self.__persistLoginInfo()
        else:
            pass

    def __persistLoginInfo(self):
        file = open("credentials.txt", 'wb')
        file.write(self.__fernet.encrypt(self.userName.encode()))
        file.write("\n".encode("utf-8"))
        file.write(self.__fernet.encrypt(self.userPassword.encode()))
        file.close()

    def __initializeKey(self):
        try:
            with open('key.txt', 'rb') as f:
                key = f.readline()
        except FileNotFoundError:
            with open('key.txt', 'wb') as f:
                key = Fernet.generate_key()
                f.write(key)
        return Fernet(key)

    @staticmethod
    def __deleteLoginInfo():
        os.remove("credentials.txt")
