from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QMainWindow, QMenuBar, QVBoxLayout, QPushButton, QWidget \
    , QMenuBar, QMenu, QTextEdit, QGraphicsScene, QGraphicsView
from PySide6.QtGui import QAction
from PySide6.QtMultimedia import QAudio, QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem, QVideoWidget
from PySide6.QtCore import QSizeF, Qt
from views.QCodeEditor import QCodeEditor



'''
Aici definim:
1. layout-ul si widget-urile care vor aparea in interfata, in constructor
2. conectam event-urile din widget-uri in functia respectiva din controller
3. ascultam pentru schimbari in model, adica apeluri de semnale QtWidgets
(referinte la model si controller sunt pasate in constructor)
'''


class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()
        self._model = model
        self._main_controller = main_controller
        self.setWindowTitle("SubMaker 2021")

        with open('./resources/dark.qss', 'r') as f:
            self.stylesheet = f.read() 
            self.setStyleSheet(self.stylesheet)

        self.main_vbox = QVBoxLayout()
        self.main_vbox.addStretch(1)


        self.menuBar = QMenuBar()   

        self.fileMenu = QMenu("&File", self)
        self.menuBar.addMenu(self.fileMenu)
        self.load_video = QAction("Load Video", self)
        self.save_video = QAction("Save Video", self)
        self.save_srt = QAction("Save To .srt File", self)
        self.menuBar.addAction(self.save_srt)
        self.fileMenu.addAction(self.load_video)
        self.fileMenu.addAction(self.save_video)
        self.setMenuBar(self.menuBar)

        self.audio_output = QAudioOutput()

        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)
        self.video_item = QGraphicsVideoItem()
        self.video_item.setSize(QSizeF(800, 600))
        self.scene = QGraphicsScene(self)
        self.graphics_view = QGraphicsView(self.scene)
        self.scene.addItem(self.video_item)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy(Qt.ScrollBarAlwaysOff))
        self.main_vbox.addWidget(self.graphics_view)

        self.main_hbox = QHBoxLayout()
        self.main_vbox.addLayout(self.main_hbox)

        self.text_widget = QCodeEditor()
        self.main_hbox.addWidget(self.text_widget)

        self.add_line_button = QPushButton()    # butonul asta nu o sa fie in varianta finala - adaugarea de replica
                                                # se va face la apasarea tastei 'enter'!
        self.add_line_button.setText("Adauga replica")
        self.add_line_button.setMinimumHeight(self.text_widget.height()/4)
        self.main_hbox.addWidget(self.add_line_button)

        self.widget = QWidget()
        self.widget.setLayout(self.main_vbox)
        self.setCentralWidget(self.widget)


        self.fileMenu.triggered[QAction].connect(self._main_controller.file_handler)
        self.fileMenu.triggered[QAction].connect(self.add_media)
        self.save_srt.triggered.connect(self._model.export_to_srt)
        
        self.add_line_button.clicked.connect(self.add_line)

    def add_media(self):
        self.media_player.setSource(self._main_controller.url)
        self.media_player.setVideoOutput(self.video_item)
        self.media_player.play()

    def add_line(self):
        line = self.text_widget.toPlainText()
        time = self.media_player.position()
        self.text_widget.clear()
        self._main_controller.line_handler(line, time)


    # ... connect-uri cu gramada intre ce definim aici si ce e in controller
    # de asemenea, ascultam pentru semnale din model