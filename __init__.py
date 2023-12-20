"__init__"
"Authors"


#import tkinter as tk
#from tkinter import ttk

class Author:
    def __init__(self, Autor):
        self.author = Autor
        with open("Informations.INFORMCOMPANY", "a") as arquivo:
            arquivo.write(f"Autor: {self.author}\n")

        print(f"Olá, {self.author}! Bem vindo a comunidade Moleques da Programação!")
        print("Enviar \033[Informations.INFORMCOMPANY\033[0m para matheus.schwebel@gmail.com.")

    def ImprimirAuthor(self):
        print(f"Autor: {self.author}")


class Version:
    def __init__(self, Versao):
        self.version = Versao
        with open("Informations.INFORMCOMPANY", "a") as arquivo:
            arquivo.write(f"Versao: {self.version}\n")
        
        print("Enviar \033[Informations.INFORMCOMPANY\033[0m para matheus.schwebel@gmail.com.")

    def ImprimirVersao(self):
        print(f"Versao: {self.version}")

class DataProgram:
    def __init__(self, dataprogram):
        self.data = dataprogram

        with open("Informations.INFORMCOMPANY", "a") as arquivo:
            arquivo.write(f"Data: {self.data}\n")

        print("Enviar \033[Informations.INFORMCOMPANY]\003[0m para matheus.schwebel@gmail.com")
    
    def ImprimirData(self):
        print(f"Data: {self.data}")

class NameProgram:
    def __init__(self, name):
        self.nameprogram = name

        with open("Informations.INFORMCOMPANY", "a") as arquivo:
            arquivo.write(f"Name of Program: {self.nameprogram}")

        print(f"Enviar \033[Informations.INFORMCOMPANY]\003[0m para matheus.schwebel@gmail.com")

    def ImprimirName(self):
        print(f"Name: {self.nameprogram}")



