from PySide6.QtWidgets import QDialogButtonBox, QGridLayout, QHBoxLayout, QLabel, QMainWindow, QMenuBar, QStackedLayout, QVBoxLayout, QPushButton, QWidget \
    , QMenuBar, QMenu, QTextEdit, QGraphicsScene, QGraphicsView, QDialog, QSlider, QStyle, QGraphicsProxyWidget
from PySide6.QtGui import QAction, QFont, QTextListFormat
from PySide6.QtMultimedia import QAudio, QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem, QVideoWidget
from PySide6.QtCore import QSizeF, Qt, QTimer
from views.QCodeEditor import QCodeEditor
from textparser import *


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

        self.previous_line_time = 0

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

        self.subtitle_label = QLabel('Light green', self)
        self.subtitle_label.resize(500, 50)
        self.subtitle_label.setStyleSheet("QLabel{font-size: 15pt; font-weight: bold;}")
        self.subtitle_label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        self.subtitle_label.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.subtitle_label.setAttribute(Qt.WA_TranslucentBackground)
        #self.subtitle_label.adjustSize()
        self.proxy_label = self.scene.addWidget(self.subtitle_label)
        self.proxy_label.setPos(self.scene.width()/2 - 200, self.scene.height() - 150)

        self.second_hbox = QHBoxLayout()
        self.main_vbox.addLayout(self.second_hbox)
        self.counter_play_pause = 0
        self.play_button = QPushButton()
        self.play_button.setFixedHeight(36)
        self.play_button.setFixedWidth(36)
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        self.second_hbox.addWidget(self.play_button)

        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.setEnabled(True)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)

        self.second_hbox.addWidget(self.position_slider)

        self.main_hbox = QHBoxLayout()
        self.main_vbox.addLayout(self.main_hbox)

        self.text_widget = QCodeEditor(view=self)
        self.main_hbox.addWidget(self.text_widget)

        self.text_widget2 = QCodeEditor(view=self)
        self.main_hbox.addWidget(self.text_widget2)

        self.text_widget3 = QCodeEditor(view=self)
        self.main_hbox.addWidget(self.text_widget3)

        self.add_line_button = QPushButton()    # butonul asta nu o sa fie in varianta finala - adaugarea de replica
                                                # se va face la apasarea tastei 'enter'! - vezi timer-ul de la final
        self.add_line_button.setText("Adauga replica")
        self.add_line_button.setMinimumHeight(self.text_widget.height()/4)
        self.main_hbox.addWidget(self.add_line_button)

        self.widget = QWidget()
        self.widget.setLayout(self.main_vbox)
        self.setCentralWidget(self.widget)
        self.setFocusPolicy(Qt.StrongFocus)


        self.fileMenu.triggered[QAction].connect(self._main_controller.file_handler)
        self.fileMenu.triggered[QAction].connect(self.add_media)
        self.save_srt.triggered.connect(self.export_to_srt)
        
        self.add_line_button.clicked.connect(self.add_line)
        self.play_button.clicked.connect(self.my_play)
        self.position_slider.sliderMoved.connect(self.set_position)

        #self.installEventFilter(self)

        self.text_timer = QTimer(self, timeout=self.update_text, interval=1000)
        self.counter = 0

    '''
    def keyPressEvent(self, qKeyEvent):
        #print(qKeyEvent.key())
        if(qKeyEvent.key() == Qt.Key_Enter):
            print(qKeyEvent.key())
            print(qKeyEvent.text())
    '''
    def update_text(self):
        self.counter += 5
        self.text = self.text_widget
        f2 = open("out_library.srt", "r")
        content = f2.readlines()
        self.subtitle_label.setText(content[int(self.position_slider.value() / 1000 / 5)].split("|")[1])


    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)


    def position_changed(self, position):
        self.position_slider.setValue(position)


    def set_position(self, position):
        self.media_player.setPosition(position)

    def my_play(self):
        self.counter = 0
        self.counter_play_pause += 1
        if(self.counter_play_pause % 2 == 1):
            self.media_player.play()
            self.text_timer.start()
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.media_player.pause()
            self.text_timer.stop()
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    
    def export_to_srt(self):
        try:
            self._model.export_to_srt()
            dlg = QDialog(self)
            dlg.setWindowTitle("Success!")
            dlg.exec()
        except Exception:
            dlg = QDialog(self)
            dlg.setWindowTitle("Fail")
            

    
    def add_media(self):
        self.media_player.setSource(self._main_controller.url)
        print(self._main_controller.url.toString())
        if(os.name[0] =='n' or os.name[0] =='N'):
            break_video(self._main_controller.url.toString()[8:])
        else:
            break_video(self._main_controller.url.toString())
        self.media_player.setVideoOutput(self.video_item)
        self.media_player.play()
        self.media_player.pause()

        f1 = open("out_model.srt", "r")
        f2 = open("out_library.srt", "r")
        for line in f2.readlines():
            self.text_widget2.insertPlainText(line)
        for line in f1.readlines():
            self.text_widget3.insertPlainText(line)
        self.text_widget2.setReadOnly(True)
        self.text_widget3.setReadOnly(True)

    def add_line(self):
        time = self.media_player.position()
        self._main_controller.line_handler(self.text_widget.replici_cu_indecsi, time, self.previous_line_time)
        self.previous_line_time = time


    # ... connect-uri cu gramada intre ce definim aici si ce e in controller
    # de asemenea, ascultam pentru semnale din model