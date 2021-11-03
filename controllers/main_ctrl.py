from PySide6.QtCore import QObject

'''
Aici facem urmatoarele:
1. executam logica aplicatiei si setam datele stocate in Model (referinta pasata in constructor)
'''



class MainController(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model
    