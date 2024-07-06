import sys
import pygame
from pygame.locals import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from io import StringIO, BytesIO
import tkinter as tk
from googletrans import Translator
import fitz  # Esta é a biblioteca PyMuPDF
from PIL import Image  # Esta é a biblioteca Pillow
import datetime
from urllib.parse import urlparse
from OpenSSL import crypto
import ssl
import socket
import requests
import math
from neo4j import GraphDatabase


class EditorTexto(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("user", "password"))  # Atualize a senha aqui

    def initUI(self):
        self.setWindowTitle('Editor de Texto')

        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.file_name_input = QLineEdit(self)
        self.file_name_input.setPlaceholderText("Nome do Arquivo")
        self.layout.addWidget(self.file_name_input)

        self.save_button = QPushButton('Salvar no Banco de Dados', self)
        self.save_button.clicked.connect(self.salvar_texto)
        self.layout.addWidget(self.save_button)

        self.load_button = QPushButton('Carregar do Banco de Dados', self)
        self.load_button.clicked.connect(self.carregar_texto)
        self.layout.addWidget(self.load_button)

        self.setLayout(self.layout)

    def salvar_texto(self):
        nome_arquivo = self.file_name_input.text()
        if nome_arquivo:
            conteudo = self.text_edit.toPlainText()
            with self.driver.session() as session:
                session.run("MERGE (f:File {name: $name}) SET f.content = $content", name=nome_arquivo, content=conteudo)

    def carregar_texto(self):
        nome_arquivo = self.file_name_input.text()
        if nome_arquivo:
            with self.driver.session() as session:
                result = session.run("MATCH (f:File {name: $name}) RETURN f.content AS content", name=nome_arquivo)
                record = result.single()
                if record:
                    self.text_edit.setPlainText(record["content"])
                else:
                    self.text_edit.setPlainText("Nenhum texto encontrado no banco de dados")

class TradutorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('InHouse Translate')
        self.label1 = QLabel('Digite o texto para traduzir:')
        self.texto_original = QTextEdit(self)
        self.label2 = QLabel('Escolha o idioma de origem:')
        self.combo_idioma_origem = QComboBox(self)
        self.combo_idioma_origem.setEditable(True)
        self.combo_idioma_origem.addItems(['en', 'es', 'fr', 'de', 'pt', 'it', 'nl', 'ru', 'ja', 'ko', 'zh-CN'])
        self.label3 = QLabel('Escolha o idioma de destino:')
        self.combo_idioma_destino = QComboBox(self)
        self.combo_idioma_destino.setEditable(True)
        self.combo_idioma_destino.addItems(['en', 'es', 'fr', 'de', 'pt', 'it', 'nl', 'ru', 'ja', 'ko', 'zh-CN'])
        self.button = QPushButton('Traduzir', self)
        self.button.clicked.connect(self.traduzir_texto)
        self.label4 = QLabel(self)
        self.label5 = QLabel(self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label1)
        vbox.addWidget(self.texto_original)
        vbox.addWidget(self.label2)
        vbox.addWidget(self.combo_idioma_origem)
        vbox.addWidget(self.label3)
        vbox.addWidget(self.combo_idioma_destino)
        vbox.addWidget(self.button)
        vbox.addWidget(self.label4)
        vbox.addWidget(self.label5)

        self.setLayout(vbox)

    def traduzir_texto(self):
        texto = self.texto_original.toPlainText()
        idioma_origem = self.combo_idioma_origem.currentText()
        idioma_destino = self.combo_idioma_destino.currentText()
        translator = Translator()
        traducao = translator.translate(texto, src=idioma_origem, dest=idioma_destino)
        texto_traduzido = traducao.text
        self.label4.setText(f'Texto original ({idioma_origem}): {texto}')
        self.label5.setText(f'Texto traduzido para {idioma_destino}: {texto_traduzido}')


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurações básicas da janela do navegador
        self.history = []

        self.extension_loaded = False
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Exibir tela de carregamento com Pygame
        self.show_loading_screen()

        # Configurações iniciais da janela principal
        self.setWindowTitle("NavegadorOS")
        self.showMaximized()

        self.add_tab("https://www.google.com")

        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        # Botões de navegação
        back_btn = QAction('←', self)
        back_btn.setStatusTip('Voltar para a página anterior')
        back_btn.triggered.connect(self.navigate_back)
        self.navbar.addAction(back_btn)

        forward_btn = QAction('→', self)
        forward_btn.setStatusTip('Avançar para a próxima página')
        forward_btn.triggered.connect(self.navigate_forward)
        self.navbar.addAction(forward_btn)

        reload_btn = QAction('⟲', self)
        reload_btn.setStatusTip('Recarregar a página atual')
        reload_btn.triggered.connect(self.reload_page)
        self.navbar.addAction(reload_btn)

        stop_btn = QAction('X', self)
        stop_btn.setStatusTip('Parar o carregamento da página atual')
        stop_btn.triggered.connect(self.stop_loading)
        self.navbar.addAction(stop_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)
        self.url_bar.insert("https://www.google.com")

        home_btn = QAction('Início', self)
        home_btn.setStatusTip('Ir para a página inicial')
        home_btn.triggered.connect(self.navigate_home)
        self.navbar.addAction(home_btn)

        self.navbar.addSeparator()

        open_url_btn = QAction('Abrir URL', self)
        open_url_btn.setStatusTip('Abrir URL')
        open_url_btn.triggered.connect(self.navigate_to_url)
        self.navbar.addAction(open_url_btn)

        close_tab_btn = QAction('Fechar Guia', self)
        close_tab_btn.setStatusTip('Fechar a guia atual')
        close_tab_btn.triggered.connect(self.close_tab)
        self.navbar.addAction(close_tab_btn)

        open_html_btn = QAction('Tradutor', self)
        open_html_btn.setStatusTip('Abrir Tradutor')
        open_html_btn.triggered.connect(self.open_translate)
        self.navbar.addAction(open_html_btn)

        open_text_editor_btn = QAction('Editor de Texto', self)
        open_text_editor_btn.setStatusTip('Abrir Editor de Texto')
        open_text_editor_btn.triggered.connect(self.open_text_editor)
        self.navbar.addAction(open_text_editor_btn)

        tkinter_tab_btn = QAction('✔', self)
        tkinter_tab_btn.setStatusTip('Segurity InHouse Browser')
        tkinter_tab_btn.triggered.connect(self.segurity)
        self.navbar.addAction(tkinter_tab_btn)

        new_tab_btn = QAction('+', self)
        new_tab_btn.setStatusTip('Abrir nova guia')
        new_tab_btn.triggered.connect(self.add_empty_tab)
        self.navbar.addAction(new_tab_btn)

        history_btn = QAction('Histórico', self)
        history_btn.setStatusTip('Visualizar histórico')
        history_btn.triggered.connect(self.show_history)
        self.navbar.addAction(history_btn)

        self.tabs.currentWidget().urlChanged.connect(self.update_urlbar)
        self.game_console = None
        print("Console do Desenvolvedor")

    def open_text_editor(self):
        text_editor = EditorTexto()
        self.tabs.addTab(text_editor, "Editor de Texto")
        self.tabs.setCurrentWidget(text_editor)

    def navigate_back(self):
        browser = self.current_browser()
        if browser:
            browser.back()

    def navigate_forward(self):
        browser = self.current_browser()
        if browser:
            browser.forward()

    def reload_page(self):
        browser = self.current_browser()
        if browser:
            browser.reload()

    def stop_loading(self):
        browser = self.current_browser()
        if browser:
            browser.stop()

    def show_loading_screen(self):
        # Configurações básicas do Pygame para a tela de carregamento
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        # Configurações da janela
        self.WINDOW_SIZE = (2400, 1350)
        self.FPS = 60
        pygame.init()
        clock = pygame.time.Clock()
        radius = 50
        angle1, angle2, angle3 = 0, 120, 240

        # Loop da tela de carregamento
        loading = True
        while loading:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Atualizar os ângulos das bolinhas
            angle1 += 2
            angle2 += 2
            angle3 += 2

            screen = pygame.display.set_mode(self.WINDOW_SIZE)
            pygame.display.set_caption('NavegadorOS')

            # Limpar a tela
            screen.fill(self.WHITE)

            # Desenhar as bolinhas
            center_x, center_y = self.WINDOW_SIZE[0] // 2, self.WINDOW_SIZE[1] // 2
            ball1_x = center_x + int(radius * math.cos(angle1 * math.pi / 180))
            ball1_y = center_y + int(radius * math.sin(angle1 * math.pi / 180))
            ball2_x = center_x + int(radius * math.cos(angle2 * math.pi / 180))
            ball2_y = center_y + int(radius * math.sin(angle2 * math.pi / 180))
            ball3_x = center_x + int(radius * math.cos(angle3 * math.pi / 180))
            ball3_y = center_y + int(radius * math.sin(angle3 * math.pi / 180))

            pygame.draw.circle(screen, self.RED, (ball1_x, ball1_y), 10)
            pygame.draw.circle(screen, self.GREEN, (ball2_x, ball2_y), 10)
            pygame.draw.circle(screen, self.BLUE, (ball3_x, ball3_y), 10)

            # Atualizar a tela
            pygame.display.flip()

            # Controlar a taxa de atualização
            clock.tick(self.FPS)

            # Condição para sair do loop
            # Condição para sair do loop de carregamento após um certo tempo
            if pygame.time.get_ticks() > 3000:  # Tempo em milissegundos (3 segundos)
                loading = False

        # Finaliza o Pygame para liberar recursos
        pygame.quit()

    def traduzir(self):
        self.game_console = TradutorApp(browser=self)
        self.tabs.addTab(self.game_console, "Tradutor")
        self.tabs.setCurrentWidget(self.game_console)

    def show_history(self):
        with open("history.HISTORY", "r") as arquivo:
            history = arquivo.read()

        with open("style.css", "r") as css_file:
            css_content = css_file.read()

        history_html = "<br>".join(history.splitlines())

        html_content = f"""<!DOCTYPE html>
        <html>
        <head>
            <title>History</title>
            <style>
                {css_content}
            </style>
        </head>
        <body>
            <div class="history">
                <h1>History</h1>
            </div>
            <p>{history_html}</p>
        </body>
        </html>"""

        browser_window = Browser()
        browser_window.add_tab(f"data:text/html,{html_content}")
        browser_window.showMaximized()

    def open_pdf_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir arquivo PDF", "", "Arquivos PDF (*.pdf);;Todos os arquivos (*)", options=options)

        if file_name:
            pdf_view = PDFViewer(file_name)
            self.tabs.addTab(pdf_view, f"PDF {file_name}")
            self.tabs.setCurrentWidget(pdf_view)

    def segurity(self):
        self.segurityroot = tk.Tk()
        self.segurityroot.title("Segurança de Sites")

        self.button = tk.Button(self.segurityroot, text="Ver segurança", command=self.verificar_seguranca)
        self.button.pack()

        self.seguranca = tk.Label(self.segurityroot, text="")
        self.seguranca.pack()

        self.ssl = tk.Label(self.segurityroot, text="Certificado SSL:")
        self.ssl.pack()

        self.ssl2 = tk.Label(self.segurityroot, text="")
        self.ssl2.pack()

        self.red = tk.Label(self.segurityroot, text="Redirecionamentos:")
        self.red.pack()

        self.red2 = tk.Label(self.segurityroot, text="")
        self.red2.pack()

        self.segurityroot.mainloop()

    def verificar_seguranca(self):
        url = self.url_bar.text()
        parsed_url = urlparse(url)

        if parsed_url.scheme == 'https':
            context = ssl.create_default_context()

            with socket.create_connection((parsed_url.hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=parsed_url.hostname) as ssock:
                    cert = ssock.getpeercert()

            x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, ssl.DER_cert_to_PEM_cert(cert))

            self.seguranca.config(text="A conexão é segura.")
            self.ssl2.config(text=f"Issuer: {x509.get_issuer()}\nSubject: {x509.get_subject()}\nValidade: {datetime.datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y GMT')} até {datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y GMT')}")
        else:
            self.seguranca.config(text="A conexão não é segura.")

        response = requests.get(url)
        if len(response.history) > 0:
            self.red2.config(text=f"O site foi redirecionado {len(response.history)} vezes.")
        else:
            self.red2.config(text="O site não foi redirecionado.")

    def open_translate(self):
        self.tradutor = TradutorApp()
        self.tradutor.show()

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.google.com"))

    def current_browser(self):
        current_widget = self.tabs.currentWidget()
        if isinstance(current_widget, QWebEngineView):
            return current_widget.page()
        else:
            return None

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.tabs.currentWidget().setUrl(QUrl(url))

    def update_urlbar(self, q):
        self.url_bar.setText(q.toString())

    def add_tab(self, url):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        i = self.tabs.addTab(browser, "Nova aba")
        self.tabs.setCurrentIndex(i)
        self.history.append(url)

    def add_empty_tab(self):
        self.add_tab("https://www.google.com")

    def open_html_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir arquivo HTML", "", "Arquivos HTML (*.html *.htm);;Todos os arquivos (*)")
        if file_name:
            with open(file_name, "r") as f:
                html = f.read()
                browser = QWebEngineView()
                browser.setHtml(html)
                i = self.tabs.addTab(browser, "Arquivo HTML")
                self.tabs.setCurrentIndex(i)

    def close_tab(self):
        if self.tabs.count() > 1:
            self.tabs.removeTab(self.tabs.currentIndex())
        else:
            self.close()

class PDFViewer(QScrollArea):
    def __init__(self, file_name):
        super().__init__()
        self.initUI(file_name)

    def initUI(self, file_name):
        self.setWindowTitle('PDF Viewer')
        self.pdf_document = fitz.open(file_name)
        self.pdf_pages = []
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)

        for page_num in range(len(self.pdf_document)):
            page = self.pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            qimage = QImage(img.tobytes("raw", "RGB"), img.size[0], img.size[1], QImage.Format_RGB888)
            qpixmap = QPixmap.fromImage(qimage)
            label = QLabel()
            label.setPixmap(qpixmap)
            self.layout.addWidget(label)
            self.pdf_pages.append(label)

        self.setWidget(self.container)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = Browser()
    main_window.setWindowTitle("PyNavegadorOS")
    main_window.showMaximized()

    sys.exit(app.exec_())
