from PySide6.QtWidgets import QMainWindow, QMenuBar, QVBoxLayout, QPushButton, QWidget \
    , QMenuBar, QMenu, QTextEdit
from PySide6.QtGui import QAction
from PySide6.QtMultimedia import QAudio, QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget



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
        main_vbox = QVBoxLayout()
        main_vbox.addStretch(1)
        '''
        button1 = QPushButton(text="1")
        main_vbox.addWidget(button1)
        button2 = QPushButton(text="2")
        main_vbox.addWidget(button2)
        '''

        menuBar = QMenuBar()   

        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        load_video = QAction("Load Video", self)
        save_video = QAction("Save Video", self)
        fileMenu.addAction(load_video)
        fileMenu.addAction(save_video)
        self.setMenuBar(menuBar)

        widget = QWidget()
        widget.setLayout(main_vbox)


        self.audio_output = QAudioOutput()

        self.media_player = QMediaPlayer(widget)
        self.media_player.setAudioOutput(self.audio_output)
        self.video_widget = QVideoWidget(widget)
        self.video_widget.resize(self.screen().availableGeometry().width(), self.screen().availableGeometry().height()/2)
        self.text_widget = QTextEdit(widget)
        #self.text_widget.resize(self.screen().availableGeometry().width(), self.screen().availableGeometry().height()/2)

        self.setCentralWidget(widget)

        fileMenu.triggered[QAction].connect(self._main_controller.file_handler)
        fileMenu.triggered[QAction].connect(self.add_media)

    def add_media(self):
        self.media_player.setSource(self._main_controller.url)
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.play()

    # ... connect-uri cu gramada intre ce definim aici si ce e in controller
    # de asemenea, ascultam pentru semnale din model