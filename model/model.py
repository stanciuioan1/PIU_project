from PySide6.QtCore import QObject


'''
aici facem urmatoarele:
1. stocam datele si starea programului
2. implementam logica minimala pentru anuntarea schimbarilor asupra datelor
'''


class Model(QObject):
    def __init__(self):
        super().__init__()
        self.lines = ""

    def add_line(self, line, time):
        self.lines = self.lines + str(line) + " " + str(time) + "\n"

    def export_to_srt(self):
        with open("out.srt", 'w', encoding='utf-8') as f:
            f.write(self.lines)