import mysql.connector

def veritabani_hazirla():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789"
        )
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS urundb")
        cursor.execute("USE urundb")

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urunler (
                id INT AUTO_INCREMENT PRIMARY KEY,
                kategori VARCHAR(50),
                ad VARCHAR(255),
                fiyat VARCHAR(100),
                link VARCHAR(255)
            )
        """)

      
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alislar (
                id INT AUTO_INCREMENT PRIMARY KEY,
                isim VARCHAR(100),
                soyisim VARCHAR(100),
                tc VARCHAR(20),
                kategori VARCHAR(50),
                urun_id INT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (urun_id) REFERENCES urunler(id)
            )
        """)

        conn.commit()
        conn.close()
        print("✅ Veritabanı ve tablolar hazır.")
    except Exception as e:
        print("❌ Veritabanı oluşturma hatası:", e)


if __name__ == "__main__":
    veritabani_hazirla()
