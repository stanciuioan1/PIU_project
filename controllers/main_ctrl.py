from PySide6.QtCore import QObject

'''
Aici facem urmatoarele:
1. executam logica aplicatiei si setam datele stocate in Model (referinta pasata in constructor)
'''



class MainController(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model

    '''
    In functie de tipul de eveniment primit din meniul "file", o sa trebuiasca sa incarcam un video si sa il salvam cumva
    in model, sau sa extragem video-ul cu tot cu starea lui (subtitrari plasate, etc.) din model si sa il salvam pe disk
    (toata logica se face aici)
    '''
    def file_handler(self, q):
        print("handle: " + q.text())
        pass