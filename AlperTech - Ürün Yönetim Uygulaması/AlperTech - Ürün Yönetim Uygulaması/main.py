import sys
import requests
from bs4 import BeautifulSoup
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from veritabani import veritabani_hazirla
from tasarim import Ui_MainWindow

class UrunUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        veritabani_hazirla()

        self.secilen_kategori = None

       
        for ad, btn in self.ui.kategori_butonlar.items():
            btn.clicked.connect(lambda _, b=btn: self.kategori_sec(b.text().split()[1]))

       
        self.ui.pushButton.clicked.connect(self.veri_cek)
        self.ui.pushButton_2.clicked.connect(self.urunleri_listele)
        self.ui.pushButton_3.clicked.connect(lambda: self.sirala("ASC"))
        self.ui.pushButton_4.clicked.connect(lambda: self.sirala("DESC"))
        self.ui.pushButton_5.clicked.connect(self.isme_gore_sirala)
        self.ui.pushButton_urun_al.clicked.connect(self.urun_al)

    def baglanti(self):
        return mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="123456789", 
        database="urundb"
        )

    def kategori_sec(self, kategori):
        self.secilen_kategori = kategori
        self.ui.lineEdit_kategori.setText(kategori)
        QMessageBox.information(self, "Kategori Seçildi", f"📦 {kategori} kategorisi seçildi!")

    def veri_cek(self):
        if not self.secilen_kategori:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir kategori seçin!")
            return

        urls = {
            "Laptop": "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops",
            "Tablet": "https://webscraper.io/test-sites/e-commerce/allinone/phones/touch",
            "Telefon": "https://webscraper.io/test-sites/e-commerce/allinone/phones",
            "Kamera": "https://webscraper.io/test-sites/e-commerce/allinone/cameras",
            "Akıllı": "https://webscraper.io/test-sites/e-commerce/allinone/phones/touch",
            "Kulaklık": "https://webscraper.io/test-sites/e-commerce/allinone/computers",
            "Monitör": "https://webscraper.io/test-sites/e-commerce/allinone/computers",
            "Mouse": "https://webscraper.io/test-sites/e-commerce/allinone/computers"
        }

        try:
            url = urls.get(self.secilen_kategori, "")
            if not url:
                QMessageBox.warning(self, "Hata", "Bu kategori için veri kaynağı bulunamadı.")
                return

            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(r.content, "html.parser")

            urunler = []
            for urun in soup.select(".thumbnail"):
                ad = urun.select_one(".title")
                fiyat = urun.select_one(".price")
                link = urun.select_one(".title")
                if ad and fiyat and link:
                    urunler.append((self.secilen_kategori, ad.get_text(strip=True), fiyat.get_text(strip=True), "https://webscraper.io" + link["href"]))

            conn = self.baglanti()
            cursor = conn.cursor()
            cursor.executemany("INSERT INTO urunler (kategori, ad, fiyat, link) VALUES (%s, %s, %s, %s)", urunler)
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Başarılı", f"{len(urunler)} ürün başarıyla eklendi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def urunleri_listele(self):
        try:
            conn = self.baglanti()
            cursor = conn.cursor()
            if self.secilen_kategori:
                cursor.execute("SELECT * FROM urunler WHERE kategori = %s", (self.secilen_kategori,))
            else:
                cursor.execute("SELECT * FROM urunler")
            veriler = cursor.fetchall()
            conn.close()
            self.urunleri_goster(veriler)
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def sirala(self, yon):
        try:
            conn = self.baglanti()
            cursor = conn.cursor()
            query = "SELECT * FROM urunler"
            if self.secilen_kategori:
                query += f" WHERE kategori = '{self.secilen_kategori}'"
            query += f" ORDER BY CAST(REPLACE(REPLACE(fiyat,'$',''),'€','') AS DECIMAL(10,2)) {yon}"
            cursor.execute(query)
            veriler = cursor.fetchall()
            conn.close()
            self.urunleri_goster(veriler)
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def isme_gore_sirala(self):
        try:
            conn = self.baglanti()
            cursor = conn.cursor()
            if self.secilen_kategori:
                cursor.execute("SELECT * FROM urunler WHERE kategori = %s ORDER BY ad ASC", (self.secilen_kategori,))
            else:
                cursor.execute("SELECT * FROM urunler ORDER BY ad ASC")
            veriler = cursor.fetchall()
            conn.close()
            self.urunleri_goster(veriler)
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def urunleri_goster(self, veriler):
        self.ui.tableWidget.setRowCount(len(veriler))
        for satir, veri in enumerate(veriler):
            for sutun, deger in enumerate(veri):
                self.ui.tableWidget.setItem(satir, sutun, QTableWidgetItem(str(deger)))

    def urun_al(self):
        isim = self.ui.lineEdit_isim.text().strip()
        soyisim = self.ui.lineEdit_soyisim.text().strip()
        tc = self.ui.lineEdit_tc.text().strip()
        kategori = self.ui.lineEdit_kategori.text().strip()
        urunid_str = self.ui.lineEdit_urunid.text().strip()

        if not (isim and soyisim and tc and kategori and urunid_str):
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return
        if not urunid_str.isdigit():
            QMessageBox.warning(self, "Hata", "Ürün ID sayı olmalıdır.")
            return

        urunid = int(urunid_str)
        try:
            conn = self.baglanti()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM urunler WHERE id = %s", (urunid,))
            urun = cursor.fetchone()

            if not urun:
                QMessageBox.warning(self, "Bulunamadı", "Girilen Ürün ID bulunamadı.")
                conn.close()
                return

            cursor.execute("INSERT INTO alislar (isim, soyisim, tc, kategori, urun_id) VALUES (%s, %s, %s, %s, %s)", 
                           (isim, soyisim, tc, kategori, urunid))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Başarılı", f"{isim} {soyisim} ürünü başarıyla satın aldı! 🎉")
            self.ui.lineEdit_isim.clear()
            self.ui.lineEdit_soyisim.clear()
            self.ui.lineEdit_tc.clear()
            self.ui.lineEdit_kategori.clear()
            self.ui.lineEdit_urunid.clear()
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = UrunUygulamasi()
    pencere.showMaximized()
    sys.exit(app.exec_())
