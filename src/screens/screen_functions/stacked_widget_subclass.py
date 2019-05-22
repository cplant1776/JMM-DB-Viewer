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

    def forward(self):
        self.setCurrentIndex(self.currentIndex() + 1)

    def backward(self):
        self.setCurrentIndex(self.currentIndex() - 1)

    def go_to_start_screen(self):
        self.setCurrentIndex(self.screen_dict['start'])

    def go_to_search_result_screen(self):
        self.setCurrentIndex(self.screen_dict['search_result'])

    def go_to_search_screen(self):
        self.setCurrentIndex(self.screen_dict['search'])

    def go_to_serial_screen(self):
        self.setCurrentIndex(self.screen_dict['serial'])

    def go_to_sro_screen(self):
        self.setCurrentIndex(self.screen_dict['sro'])

    def go_to_customer_screen(self):
        self.setCurrentIndex(self.screen_dict['customer'])

    def go_to_tester(self):
        print("test")
        self.setCurrentIndex(5)
