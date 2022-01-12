from PySide6.QtCore import QObject
import os


'''
aici facem urmatoarele:
1. stocam datele si starea programului
2. implementam logica minimala pentru anuntarea schimbarilor asupra datelor
'''


class Model(QObject):
    def __init__(self):
        super().__init__()
        self.lines = []

    def add_line(self, replici_cu_indecsi, time, previous_time):
        #self.lines = self.lines + str(line) + " " + str(previous_time) + ' ' + str(time) + "\n"
        temp = []
        for replica in replici_cu_indecsi:
            temp.append((replica[0], replica[1], previous_time, time))
        self.lines = temp    

    def export_to_srt(self):
        if os.path.exists("out.srt"):
            os.remove("out.srt")
        f1 = open("out.srt", "w")
        f1.write(str(self.lines))
        f1.close()