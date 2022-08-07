import os


class Login:

    def __init__(self):
        self.userEmail = ""
        self.userPassword = ""
        self.verifyLoginFile()

    def verifyLoginFile(self):
        if os.path.exists("credentials.txt"):
            print("Já existem credenciais de login. Usá-las para os teste?")
            loginChoice = input("(S/s): Você usará as credenciais salvas para logar.\n"
                                "(N/n): As credenciais atuais serão apagadas e você digitará outra.\n"
                                "Qual sua escolha?: ")
            if loginChoice.lower() == 's':
                with open("credentials.txt", 'r') as file:
                    self.userEmail = file.readline()[:-1]
                    self.userPassword = file.readline()
            else:
                self.deleteLoginInfo()
                self.getLoginInfo()
        else:
            self.getLoginInfo()

    def getLoginInfo(self):
        self.userEmail = input("Digite seu email para login no Github: ")
        self.userPassword = input("Digite sua senha: ")
        persistChoice = input("Gostaria de salvar suas credenciais?"
                              "(s/n): ")
        if persistChoice.lower() == 's':
            self.persistLoginInfo()
        else:
            pass

    def persistLoginInfo(self):
        file = open("credentials.txt", 'w')
        file.write(f"{self.userEmail}\n"
                   f"{self.userPassword}")
        file.close()

    @staticmethod
    def deleteLoginInfo():
        os.remove("credentials.txt")
