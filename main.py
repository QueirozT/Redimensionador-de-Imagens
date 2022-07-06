"""
Programa que redimensiona Imagens

Este programa utiliza uma interface gráfica para coletar uma imagem e redimensiona-la retornando uma imagem nova.

Estou convertendo o arquivo.ui para .py para facilitar a criação do programa e do executável ao final.
Comando usado para converter o arquivo.ui: pyuic5 display.ui -o display.py

Criando o arquivo executável:
    1° Instalando o pyinstaller:
        pip install pyinstaller

    2° Criando o arquivo Executável:
        pyinstaller --noconsole --name="Redimensionador" --icon="uteis/icone.ico" --onefile main.py
            --noconsole: Sem Console na execução do arquivo
            --name: Define o nome do arquivo de saída
            --icon: Define o icone do arquivo executável
            --onefile: Cria apenas um arquivo.exe
"""
from email.errors import InvalidMultipartContentTransferEncodingDefect
import sys
from pathlib import Path
from uteis.display import *  # Importa o arquivo convertido de .ui para .py
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap

# Esta classe tem que herdar do PyQt5 e do display.py
class Conversor(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)  # Inicializando o PyQt5
        super().setupUi(self)  # Inicializando o arquivo.py convertido
        
        # Setando a tela inicial
        self.stackedWidget.setCurrentWidget(self.pgInicial)

        # Definindo os botões e ações da tela Inicial
        self.btnCaminho.clicked.connect(self.procurar_arquivo)
        self.inputCaminho.textChanged.connect(self.valida_caminho)
        self.inputCaminho.returnPressed.connect(self.abrir_arquivo)

        # Definindo os botões e ações da tela de Redimensionamento
        self.inputHeight.setEnabled(False) # Tornando o campo inativo por padrão
        self.btnAjust.clicked.connect(self.ajustar_proporcao)
        self.btnVoltar.clicked.connect(self.voltar)
        self.btnRedimensionar.clicked.connect(self.redimensionar)
        self.btnSalvar.clicked.connect(self.salvar)

    # Métodos da tela inicial
    def abrir_arquivo(self):
        if self.btnCaminho.text() == 'Abrir':
            self.stackedWidget.setCurrentWidget(self.pgRedimensionar)
            self.inputCaminho.setText('')

    def valida_caminho(self):
        caminho = self.inputCaminho.text()
        if caminho[-4:] == '.jpg' or caminho[-4:] == '.png':
            if Path(caminho).exists():
                self.btnCaminho.setText('Abrir')
                self.original_img = QPixmap(caminho)
                self.img.setPixmap(self.original_img)
                self.inputWidth.setText(str(self.original_img.width()))
                self.inputHeight.setText(str(self.original_img.height()))
            else:
                self.btnCaminho.setText('Localizar')
        else:
            self.btnCaminho.setText('Localizar')

    def procurar_arquivo(self):
        if self.btnCaminho.text() == 'Localizar':
            imagem, _ = QFileDialog.getOpenFileName(
                caption='Abrir Imagem',
                directory=f'{Path.joinpath(Path.home(), "Pictures")}',
                filter='Arquivos JPG(*.jpg);; Arquivos PNG(*.png);; Todos os arquivos(*)',
            )
            if 'JPG' or 'PNG' in imagem.upper():
                self.inputCaminho.setText(imagem)
                self.btnCaminho.setText('Abrir')
                self.original_img = QPixmap(imagem)
                self.img.setPixmap(self.original_img)
                self.inputWidth.setText(str(self.original_img.width()))
                self.inputHeight.setText(str(self.original_img.height()))
        elif self.btnCaminho.text() == 'Abrir' and Path(self.inputCaminho.text()).exists():
            self.stackedWidget.setCurrentWidget(self.pgRedimensionar)
            self.inputCaminho.setText('')
            self.btnCaminho.setText('Localizar')
        else:
            self.btnCaminho.setText('Localizar')


    # Métodos da tela de Redimensionamento
    def voltar(self):
        self.stackedWidget.setCurrentWidget(self.pgInicial)
        self.btnAjust.setCheckState(False)

    def redimensionar(self):
        if self.btnAjust.checkState():
            largura = int(self.inputWidth.text())
            altura = int(self.inputHeight.text())
            self.nova_imagem = self.original_img.scaled(largura, altura)
            self.img.setPixmap(self.nova_imagem)
        else:
            largura = int(self.inputWidth.text())
            self.nova_imagem = self.original_img.scaledToWidth(largura)
            self.img.setPixmap(self.nova_imagem)
            self.inputWidth.setText(str(self.nova_imagem.width()))
            self.inputHeight.setText(str(self.nova_imagem.height()))

    def ajustar_proporcao(self):
        if not self.btnAjust.checkState():
            self.inputHeight.setEnabled(False)
        else:
            self.inputHeight.setEnabled(True)

    def salvar(self):
        imagem, _ = QFileDialog.getSaveFileName(
            caption='Salvar Imagem',
            directory=f'{Path.joinpath(Path.home(), "Pictures")}',
            filter='Arquivos JPG(*.jpg);; Arquivos PNG(*.png);; Todos os arquivos(*)',
        )
        self.nova_imagem.save(imagem)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    conversor = Conversor()
 
    conversor.show()
    app.exec_()
