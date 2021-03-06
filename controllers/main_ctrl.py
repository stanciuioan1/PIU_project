from PySide6.QtCore import QObject, QDir
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import QFileDialog, QDialog
import cv2

'''
Aici facem urmatoarele:
1. executam logica aplicatiei si setam datele stocate in Model (referinta pasata in constructor)
'''



class MainController(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model
        self.url = None
        self.fps = None

    '''
    In functie de tipul de eveniment primit din meniul "file", o sa trebuiasca sa incarcam un video si sa il salvam cumva
    in model, sau sa extragem video-ul cu tot cu starea lui (subtitrari plasate, etc.) din model si sa il salvam pe disk
    (toata logica se face aici)
    '''
    def file_handler(self, q):
        if(q.text() == "Load Video"):
            self.url = self.load_video()
            self.cap = cv2.VideoCapture(str(self.url.toString()[8:]))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)

    
    def load_video(self):
        file_dialog = QFileDialog(None)
        file_dialog.setDirectory(QDir.currentPath())
        if(file_dialog.exec() == QDialog.Accepted):
            url = file_dialog.selectedUrls()[0]
            return url


    def save_video(self):
        pass

    def line_handler(self, replici_cu_indecsi, time, previous_time):
        temp = (replici_cu_indecsi[-1][0], replici_cu_indecsi[-1][1], previous_time, time)
        #print(replici_cu_indecsi[0][1] + ' ' + str(previous_time) + ' ' + str(time))
        self._model.add_line(temp)