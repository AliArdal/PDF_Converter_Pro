# PDF Studio Pro

Modern, tamamen offline çalışan masaüstü PDF dönüştürücü.


![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-4F8EF7?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-3DD68C?style=flat-square)
![Offline](https://img.shields.io/badge/Mod-100%25_Offline-F7C948?style=flat-square)


<img width="1600" height="929" alt="WhatsApp Image 2026-05-08 at 10 05 54" src="https://github.com/user-attachments/assets/c47505c8-572d-4be3-af6e-a97909696986" />
<img width="1600" height="932" alt="WhatsApp Image 2026-05-08 at 10 05 54(1)" src="https://github.com/user-attachments/assets/1109dc46-c1fe-4fa2-bdad-0acec9e8abad" />


---

## Özellikler

| Araç | Girdi | Çıktı | Açıklama |
|------|-------|-------|----------|
| PDF → Word | `.pdf` | `.docx` | Metin, tablo ve düzeni koruyarak dönüştürür |
| Word → PDF | `.docx` `.doc` | `.pdf` | Microsoft Word veya LibreOffice ile dönüşüm |
| PDF → Metin | `.pdf` | `.txt` | Tüm metin içeriğini düz dosyaya aktarır |
| PDF → Görsel | `.pdf` | `.png` | Her sayfayı 2x çözünürlükte PNG olarak kaydeder |
| PDF Birleştir | N x `.pdf` | `.pdf` | Birden fazla PDF'i tek dosyada birleştirir |

- Modern koyu tema (CustomTkinter)
- Toplu dosya ve klasör ekleme
- Dosya başına gerçek zamanlı durum takibi
- Özel çıktı klasörü seçimi
- Çoklu iş parçacığı — UI donmaz
- Internet bağlantısı gerekmez

---

## Kurulum

Python 3.9 veya üzeri gereklidir.

```bash
git clone https://github.com/kullanici-adin/pdf-studio-pro.git
cd pdf-studio-pro
pip install -r requirements.txt
python app.py
```

Sanal ortam ile kullanmak için:

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
python app.py
```

---

## Bağımlılıklar

| Paket | Sürüm | Amaç |
|-------|-------|------|
| customtkinter | >=5.2.0 | Modern GUI framework |
| pdf2docx | >=0.5.6 | PDF to Word dönüşümü |
| PyMuPDF | >=1.23.0 | PDF işleme motoru |
| Pillow | >=10.0.0 | Görsel işleme |
| docx2pdf | >=0.1.8 | Word to PDF dönüşümü |

---

## Proje Yapısı

```
pdf-studio-pro/
├── app.py              # Ana uygulama
├── requirements.txt    # Bağımlılıklar
└── README.md
```

---

## Kullanım

1. Sol panelden dönüşüm modunu seçin
2. Dosya Ekle butonu ile dosyaları ekleyin
3. İsteğe bağlı olarak çıktı klasörü belirleyin
4. Dönüştür butonuna tıklayın

---

## Gizlilik

Tüm işlemler yalnızca yerel makinenizde gerçekleşir.
Hiçbir dosya internet üzerinden iletilmez.

---

## Sorun Giderme

**tkinter hatası (Linux)**
```bash
sudo apt install python3-tk
```

**docx2pdf çalışmıyor (Linux/macOS)**
```bash
sudo apt install libreoffice   # Ubuntu/Debian
brew install libreoffice       # macOS
```

---


