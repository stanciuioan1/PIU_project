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

    def add_line(self, info):
        #self.lines = self.lines + str(line) + " " + str(previous_time) + ' ' + str(time) + "\n"
        self.lines.append(info)
        #print(str(self.lines))   

    def export_to_srt(self, duration):
        if os.path.exists("out.srt"):
            os.remove("out.srt")
        f1 = open("out.srt", "w")
        a=1
        for i in self.lines:
            f1.write(str(i[2])+":" + str(i[3])+"|"+i[1]+"\n")
            a=i[3]


        f1.write(str(a)+":" + str(duration)+"| \n")
        #f1.write(str(self.lines))
        f1.close()