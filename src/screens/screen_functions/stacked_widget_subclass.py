from PyQt5 import QtWidgets


class MyStackWidget(QtWidgets.QStackedWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_dict = {"start": 0,
                            "search_result": 1,
                            "search": 2,
                            "serial": 3,
                            "sro": 4,
                            "customer": 5}
        self.previous_screen_index = 0

    def forward(self):
        self.setCurrentIndex(self.currentIndex() + 1)

    def backward(self):
        self.setCurrentIndex(self.currentIndex() - 1)

    def go_to_screen(self, screen):
        self.previous_screen_index = self.currentIndex()
        self.setCurrentIndex(self.screen_dict[screen])

    def go_to_previous_screen(self):
        tmp = self.currentIndex()
        self.setCurrentIndex(self.previous_screen_index)
        self.previous_screen_index = tmp
