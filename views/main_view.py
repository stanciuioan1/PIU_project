from PySide6.QtWidgets import QMainWindow


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
        
        # ... connect-uri cu gramada intre ce definim aici si ce e in controller
        # de asemenea, ascultam pentru semnale din model