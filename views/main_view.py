from PySide6.QtWidgets import QMainWindow, QMenuBar, QVBoxLayout, QPushButton, QWidget \
    , QMenuBar, QMenu


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
        self.main_controller = main_controller
        self.setWindowTitle("SubMaker 2021")
        #self.resize(400,200)
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
        self.setMenuBar(menuBar)

    

        widget = QWidget()
        widget.setLayout(main_vbox)
        self.setCentralWidget(widget)

        # ... connect-uri cu gramada intre ce definim aici si ce e in controller
        # de asemenea, ascultam pentru semnale din model