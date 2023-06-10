import sys
import PySide6.QtWidgets as pq
from PySide6.QtGui import QAction, QIcon, QKeySequence, QPixmap, QHideEvent
from PySide6.QtCore import Qt, QSize
import spotify_artist_backend as sa


class MainWindow(pq.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Top Tracks")
        self.setFixedSize(950, 600)

        self.temp_window = None
        
        #data for the spotify api
        client_id = "2f92e1fb67bc417ba772633afa78846b"
        client_secret= "9d0d39cec6ed4776b9f53cdf64791857"
        #client_id = input("Enter ID: ")
        #client_secret = input("Enter secret: ")
        self.header = sa.get_header(client_id,client_secret)
        #gridlayout
        layout = pq.QGridLayout()

        #label for lineEdit
        label_id = pq.QLabel("Enter Artist ID")
        label_search = pq.QLabel("Enter search term")

        layout.addWidget(label_id, 0, 1) 
        layout.addWidget(label_search, 0, 4)

        #lineEdit for ID and Search
        self.artist_id_line = pq.QLineEdit()
        self.artist_id_line.setMaxLength(50)
        self.artist_id_line.setPlaceholderText("Confirm with Enter")
        self.artist_id_line.returnPressed.connect(self.artist_id_result)

        self.artist_search_line = pq.QLineEdit()
        self.artist_search_line.setMaxLength(50)
        self.artist_search_line.setPlaceholderText("Confirm with Enter")
        self.artist_search_line.returnPressed.connect(self.artist_search_result)

        layout.addWidget(self.artist_id_line, 1, 1)
        layout.addWidget(self.artist_search_line, 1, 4)

        #pixmap to display Graph, default image black background
        self.graph = QPixmap("black_bg.png")
        self.graph_label = pq.QLabel()
        self.graph_label.setPixmap(self.graph)
        self.graph_label.setFrameShape(pq.QFrame.Panel)
        #allows the image to scale
        self.graph_label.setScaledContents(True)
        #setting verticl and horizontal sizepolicy to ignored allows the image to be scaled to fill the whole label
        self.graph_label.setSizePolicy(pq.QSizePolicy.Ignored, pq.QSizePolicy.Ignored)

        layout.addWidget(self.graph_label, 2, 0, 6, 6)
        
        #empty widget for layout
        widget = pq.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        


    def artist_id_result(self):
        id = self.artist_id_line.selectedText()
        print(id)
        fig = sa.request_api_artist(id, self.header)
        self.graph_label.setPixmap(QPixmap("top_tracks.jpg"))

    def artist_search_result(self):
        search_term = self.artist_search_line.text()
        artist_selection = sa.artist_search(search_term, self.header)
        #print(artist_selection)
        try:
            artist_selection["name"]
        except TypeError:
            print("empty search field")
            return
        optionslist = []
        for index, row in artist_selection.iterrows():
            optionslist.append(row["name"])
        

        dia = pq.QMessageBox(self)
        dia.setWindowTitle("Confirm Selection")
        dia.setStandardButtons(pq.QMessageBox.Yes)
        
        
    def confirm(self, s):
        print("Ok")
        self.accept()



        
    


class temp_window(pq.QWidget):
    def __init__(self, selection, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Artist")

        
        self.return_value = None
        self.selection = selection
        layout = pq.QHBoxLayout()
        self.combox = pq.QComboBox()
        self.combox.addItems(self.selection["name"])

        button = pq.QPushButton("Conform selection")
        button.clicked.connect(self.confirmed)

        layout.addWidget(self.combox)
        layout.addWidget(button)
        self.setLayout(layout)
        print(self.selection)

    def confirmed(self):
        data = self.selection
        value = self.combox.currentText()
        print("confirmed value:", value)
        ID = data.loc[data["name"]==value]
        ret_id = ""
        for index, row in ID.iterrows():
            ret_id = row["id"]
        self.return_value = ret_id
        self.hide()
    


def main():
    app = pq.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()