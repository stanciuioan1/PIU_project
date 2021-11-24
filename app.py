from model.model import Model
from controllers.main_ctrl import MainController
from views.main_view import MainView

from PySide6.QtWidgets import QApplication
import sys

'''
aplicatia nu este inca functionala pentru ca trebuiesc facuti cum trebuie constructorii din obiecte si
apelati constructorii din QObject (super.__init__(...))
'''

class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = Model()
        self.main_controller = MainController(self.model)
        self.main_view = MainView(self.model, self.main_controller)
        self.main_view.showMaximized()


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())
