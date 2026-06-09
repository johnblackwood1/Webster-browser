

import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QLineEdit,
    QPushButton,
    QTabBar
)
from PyQt6.QtWebEngineWidgets import QWebEngineView

ver = "2.0.2"

starturl = "https://www.protopage.com/"

class websterbrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Welcome to Webster!")
        self.setWindowTitle(f"Webster browser {ver}")
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(starturl))
        self.setCentralWidget(self.browser)
        navbar = QToolBar("Navigation")
        tabbar = QToolBar("Tabs")
        self.addToolBar(navbar)
        self.addToolBar(tabbar)
        back_button = QPushButton("Back")
        refresh_button = QPushButton("Refresh")
        addnewtab = QPushButton("+")
        self.tabs = QTabBar()
        navbar.addWidget(back_button)
        navbar.addWidget(refresh_button)
        tabbar.addWidget(self.tabs)
        tabbar.addWidget(addnewtab)
        addnewtab.clicked.connect(self.add_new_tab)
        self.tabs.currentChanged.connect(self.switch_tab)
        self.tab_history = {}
        self.tabs.addTab("Home")
        self.tab_history[0] = starturl
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        back_button.clicked.connect(self.browser.back)
        refresh_button.clicked.connect(self.browser.reload)
        self.url_bar = QLineEdit()
        navbar.addWidget(self.url_bar)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.browser.urlChanged.connect(self.update_url_bar)
    def navigate_to_url(self):
        raw_text = self.url_bar.text()
        self.browser.setUrl(QUrl(raw_text))
    def update_url_bar(self, qurl_object):
        url_string = qurl_object.toString()
        self.url_bar.setText(url_string)
        self.tabs.currentIndex()
        self.tab_history[self.tabs.currentIndex()] = url_string
    def switch_tab(self, index):
        if index in self.tab_history:
            target_url = self.tab_history[index]
            self.browser.setUrl(QUrl(target_url))
    def add_new_tab(self):
        new_index = self.tabs.addTab(f"Tab")
        self.tab_history[new_index] = starturl
        self.tabs.setCurrentIndex(new_index)
        print("Added a tab")
    def close_tab(self, index):
        if self.tabs.count() <= 1:
            self.close()
        self.tabs.removeTab(index)
        print("Closed a tab")
        new_history = {}
        for i in range(self.tabs.count()):
            if i < index:
                new_history[i] = self.tab_history[i]
            else:
                new_history[i] = self.tab_history[i + 1]
        self.tab_history = new_history





if __name__ == "__main__":

    app = QApplication(sys.argv)


    window = websterbrowser()


    window.show()


    sys.exit(app.exec())
