<div align="center">

<img src="https://img.shields.io/badge/PDF-Studio_Pro-4F8EF7?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="PDF Studio Pro"/>

# PDF Studio Pro

**Modern, tamamen offline çalışan masaüstü PDF dönüştürücü**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-4F8EF7?style=flat-square)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-3DD68C?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)]()
[![Offline](https://img.shields.io/badge/Çalışma_Modu-100%25_Offline-F7C948?style=flat-square)]()

</div>

---

## 📸 Ekran Görüntüsü

> Koyu tema, neon mavi aksan rengi ve glassmorphism kart tasarımıyla modern bir arayüz.

```
┌─────────────────────────────────────────────────────────────────┐
│  PDF Studio                                           PRO       │
├─────────────────┬───────────────────────────────────────────────┤
│                 │  PDF → Word Dönüştürücü                       │
│  📄→📝 PDF→Word │  .pdf dosyalarını .docx formatına dönüştür    │
│  📝→📄 Word→PDF │                                               │
│  📄→📋 PDF→Txt  │  ┌─────────────────────────────────────────┐  │
│  📄→🖼️ PDF→Img  │  │  ⬆ Dosyaları Buraya Sürükleyin         │  │
│  📑+📑 Birleştir│  │       + Dosya Ekle   📁 Klasör          │  │
│                 │  └─────────────────────────────────────────┘  │
│                 │                                               │
│  v1.0 • Offline │  [dosya listesi...]        ▶ Dönüştür        │
└─────────────────┴───────────────────────────────────────────────┘
```

---

## ✨ Özellikler

| Araç | Girdi | Çıktı | Açıklama |
|------|-------|-------|----------|
| **PDF → Word** | `.pdf` | `.docx` | Metin, tablo ve düzeni koruyarak dönüştürür |
| **Word → PDF** | `.docx` `.doc` | `.pdf` | Microsoft Word veya LibreOffice ile dönüşüm |
| **PDF → Metin** | `.pdf` | `.txt` | Tüm metin içeriğini düz dosyaya aktarır |
| **PDF → Görsel** | `.pdf` | `.png` | Her sayfayı 2× çözünürlükte PNG olarak kaydeder |
| **PDF Birleştir** | `N × .pdf` | `.pdf` | Birden fazla PDF'i tek dosyada birleştirir |

**Arayüz özellikleri:**
- 🎨 Modern koyu tema (CustomTkinter)
- 📂 Toplu dosya ve klasör ekleme
- 📊 Dosya başına gerçek zamanlı durum takibi (Bekliyor / İşleniyor / Tamamlandı / Hata)
- 📁 Özel çıktı klasörü seçimi
- 🗑️ Tek tıkla dosya kaldırma
- ⚡ Çoklu iş parçacığı — UI donmaz

---

## 🚀 Kurulum

### Gereksinimler

- Python **3.9** veya üzeri
- **Windows:** Word → PDF için Microsoft Word önerilir
- **Linux / macOS:** Word → PDF için LibreOffice gereklidir

### Adım 1 — Repoyu klonla

```bash
git clone https://github.com/kullanici-adin/pdf-studio-pro.git
cd pdf-studio-pro
```

### Adım 2 — Sanal ortam oluştur (önerilir)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### Adım 3 — Bağımlılıkları yükle

```bash
pip install -r requirements.txt
```

### Adım 4 — Çalıştır

```bash
python app.py
```

---

## 📦 Bağımlılıklar

| Paket | Sürüm | Amaç |
|-------|-------|------|
| [customtkinter](https://github.com/TomSchimansky/CustomTkinter) | ≥5.2.0 | Modern GUI framework |
| [pdf2docx](https://github.com/ArtifexSoftware/pdf2docx) | ≥0.5.6 | PDF → Word dönüşümü |
| [PyMuPDF](https://github.com/pymupdf/PyMuPDF) | ≥1.23.0 | PDF işleme motoru |
| [Pillow](https://python-pillow.org) | ≥10.0.0 | Görsel işleme |
| [docx2pdf](https://github.com/AlJohri/docx2pdf) | ≥0.1.8 | Word → PDF dönüşümü |

---

## 📁 Proje Yapısı

```
pdf-studio-pro/
├── app.py              # Ana uygulama (809 satır)
├── requirements.txt    # Python bağımlılıkları
└── README.md           # Bu dosya
```

---

## 🔧 Kullanım

1. **Araç seçin** — Sol panelden dönüşüm modunu belirleyin
2. **Dosya ekleyin** — "Dosya Ekle" butonu ile dosya yükleyin
3. **Klasör seçin** *(isteğe bağlı)* — Çıktı konumu belirleyin; seçilmezse kaynak klasörü kullanılır
4. **Dönüştür** — Sağ alttaki butona tıklayın, her dosyanın durumunu takip edin

---

## 🔒 Gizlilik

> Tüm işlemler **yalnızca yerel makinenizde** gerçekleşir.  
> Hiçbir dosya internet üzerinden iletilmez veya üçüncü taraf servislere gönderilmez.

---

## 🛠️ Sorun Giderme

**`No module named 'tkinter'` hatası (Linux)**
```bash
sudo apt install python3-tk
```

**`docx2pdf` çalışmıyor (Linux/macOS)**
```bash
# LibreOffice kurulumu gerekli
sudo apt install libreoffice   # Ubuntu/Debian
brew install libreoffice        # macOS
```

**`customtkinter` görünüm bozukluğu (Windows)**
```bash
pip install customtkinter --upgrade
```

---

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır. Büyük değişiklikler için lütfen önce bir issue açın.

1. Fork'layın
2. Feature branch oluşturun: `git checkout -b feature/yeni-ozellik`
3. Commit edin: `git commit -m 'feat: yeni özellik eklendi'`
4. Push edin: `git push origin feature/yeni-ozellik`
5. Pull Request açın

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.

---

<div align="center">

**PDF Studio Pro** — Verileriniz, bilgisayarınızda kalır.

</div>
