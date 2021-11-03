from PySide6.QtCore import QObject


'''
aici facem urmatoarele:
1. stocam datele si starea programului
2. implementam logica minimala pentru anuntarea schimbarilor asupra datelor
'''


class Model(QObject):
    def __init__(self):
        super().__init__()