from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)

        
        MainWindow.setStyleSheet("""
            QMainWindow {
                 border: none;
                 background-image: url('ArkaPlan.jpeg');
                 background-repeat: no-repeat;
                 background-position: center;
                 background-origin: content;
                 background-attachment: fixed;
                 background-size: 100%;
            }
        """)
        MainWindow.setWindowIcon(QtGui.QIcon("logo.png"))
        MainWindow.setWindowTitle("Alper Tech - Ürün Yönetim Uygulaması")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        layout = QtWidgets.QVBoxLayout(self.centralwidget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        
        self.label_title = QtWidgets.QLabel("🛒 Alper Tech - Ürün Yönetim Uygulaması")
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);  /* Saydam arka plan */
                font-size: 48px;
                font-weight: 900;
                color: #ffffff;
                text-shadow: 2px 2px 10px #000000;
            }
        """)
        layout.addWidget(self.label_title)

       
        self.kategori_widget = QtWidgets.QWidget()
        kategori_layout = QtWidgets.QGridLayout(self.kategori_widget)
        kategori_layout.setHorizontalSpacing(50)
        kategori_layout.setVerticalSpacing(30)

        kategori_stil = """
            QPushButton {
             background-color: rgba(25, 118, 210, 0.70);
                color: white;
                border-radius: 15px;
                padding: 15px 45px;
                font-size: 20px;
                font-weight: bold;
                border: 2px solid #1565c0;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """

        kategoriler = [
            ("💻 Laptop", "btn_laptop"),
            ("📱 Telefon", "btn_telefon"),
            ("🧾 Tablet", "btn_tablet"),
            ("📷 Kamera", "btn_kamera"),
            ("⌚ Akıllı Saat", "btn_akilli_saat"),
            ("🎧 Kulaklık", "btn_kulaklik"),
            ("🖥️ Monitör", "btn_monitor"),
            ("🖱️ Mouse", "btn_mouse")
        ]

        self.kategori_butonlar = {}
        for i, (text, name) in enumerate(kategoriler):
            btn = QtWidgets.QPushButton(text)
            btn.setObjectName(name)
            btn.setStyleSheet(kategori_stil)
            btn.setFixedSize(300, 100)
            self.kategori_butonlar[name] = btn
            kategori_layout.addWidget(btn, i // 4, i % 4)

        layout.addWidget(self.kategori_widget, alignment=QtCore.Qt.AlignCenter)

       
        self.islem_widget = QtWidgets.QWidget()
        hbox = QtWidgets.QHBoxLayout(self.islem_widget)
        hbox.setSpacing(30)

        buton_stil = """
            QPushButton {
                background-color: rgba(25, 118, 210, 0.90);
                color: white;
                border-radius: 15px;
                padding: 15px 45px;
                font-size: 20px;
                font-weight: bold;
                border: 2px solid #1565c0;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """

        self.pushButton = QtWidgets.QPushButton("🔄 Veri Çek")
        self.pushButton_2 = QtWidgets.QPushButton("📋 Listele")
        self.pushButton_3 = QtWidgets.QPushButton("⬆️ Ucuzdan Pahalıya")
        self.pushButton_4 = QtWidgets.QPushButton("⬇️ Pahalıdan Ucuza")
        self.pushButton_5 = QtWidgets.QPushButton("🔤 İsme Göre Sırala")
        self.pushButton_urun_al = QtWidgets.QPushButton("🛒 Ürün Al")

        for btn in [self.pushButton, self.pushButton_2, self.pushButton_3,
                    self.pushButton_4, self.pushButton_5, self.pushButton_urun_al]:
            btn.setStyleSheet(buton_stil)
            hbox.addWidget(btn)

        layout.addWidget(self.islem_widget)

      
        form_table_widget = QtWidgets.QWidget()
        form_table_layout = QtWidgets.QHBoxLayout(form_table_widget)
        form_table_layout.setSpacing(40)

        self.form = QtWidgets.QWidget()
        form_layout = QtWidgets.QFormLayout(self.form)
        label_style = "font-size: 20px; font-weight: bold; color: white;"
        input_style = """
            QLineEdit {
                border-radius: 15px;
                border: 2px solid #7f8c8d;
                padding: 10px 20px;
                font-size: 18px;
                background-color: rgba(255,255,255,0.85);
            }
        """

        self.lineEdit_isim = QtWidgets.QLineEdit()
        self.lineEdit_soyisim = QtWidgets.QLineEdit()
        self.lineEdit_tc = QtWidgets.QLineEdit()
        self.lineEdit_kategori = QtWidgets.QLineEdit()
        self.lineEdit_kategori.setReadOnly(True)
        self.lineEdit_urunid = QtWidgets.QLineEdit()

        for lbl, le in zip(["İsim:", "Soyisim:", "TC:", "Kategori:", "Ürün ID:"],
                           [self.lineEdit_isim, self.lineEdit_soyisim, self.lineEdit_tc,
                            self.lineEdit_kategori, self.lineEdit_urunid]):
            label = QtWidgets.QLabel(lbl)
            label.setStyleSheet(label_style)
            le.setStyleSheet(input_style)
            le.setFixedHeight(50)
            form_layout.addRow(label, le)

        form_table_layout.addWidget(self.form)

       
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Kategori", "Ad", "Fiyat", "Link"])
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setStyleSheet("""
            QTableWidget {
                border-radius: 10px;
                background-color: rgba(255,255,255,0.95);
                font-size: 17px;
            }
            QHeaderView::section {
                background-color: #1e88e5;
                color: white;
                font-weight: bold;
                padding: 8px;
            }
        """)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(180)

        form_table_layout.addWidget(self.tableWidget)
        layout.addWidget(form_table_widget)

        MainWindow.setCentralWidget(self.centralwidget)
