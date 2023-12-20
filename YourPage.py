import markdown

options_of_organizations = {
    "Moleques da Programação"
}

class TransformInMarkDown:
    def __init__(Autor, Versao, dataprogram):
        with open("YourPage.md", "a") as arquivo:
            arquivo.write(f"Author: {Autor}\n")
            arquivo.write(f"Version: {Versao}\n")
            arquivo.write(f"Program Creation Date: {dataprogram}\n")
    
    def personalizer(Autor, Versao, dataprogram, namefile):
        with open(namefile, "a") as arquivo:
            arquivo.write(f"Author: {Autor}\n")
            arquivo.write(f"Version: {Versao}\n")
            arquivo.write(f"Program Creation Date: {dataprogram}\n")


class TransformInHTML:
    def __init__(myhtml):
        file = myhtml

        html = markdown.markdown(file)

        print(html)