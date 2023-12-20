"organizacoes.py"

options_of_organizations = {
    "Moleques da Programação"
}

class ErroCompany:
    def __init__():
        print("Erro. Companhia não listada.")

def organization(option):
    if option in options_of_organizations:
        with open("Informations.INFORMCOMPANY") as arquivo:
            arquivo.write(f"Company: {option}")
            print("Companhia inclusa com sucesso!")
    else:
        print(ErroCompany)