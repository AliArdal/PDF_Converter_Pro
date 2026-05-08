"""
PDF Studio Pro - Modern PDF Converter
Tamamen offline çalışır | CustomTkinter tabanlı
Ağ bağlantısı gerekmeden lokalde kullanabileceğiniz ilovepdf-smallpdf ihtiyacınız gerekmiyor artık
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import sys
from pathlib import Path
import time

# ─── Kütüphane yüklemeleri ─────────────────────────────────────────────────
try:
    from pdf2docx import Converter as PDF2DOCXConverter
    PDF2DOCX_OK = True
except ImportError:
    PDF2DOCX_OK = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_OK = True
except ImportError:
    PYMUPDF_OK = False

try:
    from docx2pdf import convert as docx2pdf_convert
    DOCX2PDF_OK = True
except ImportError:
    DOCX2PDF_OK = False

try:
    from PIL import Image, ImageTk
    PIL_OK = True
except ImportError:
    PIL_OK = False


# ─── Renk Paleti ───────────────────────────────────────────────────────────
COLORS = {
    "bg_dark":      "#0D0F14",
    "bg_panel":     "#13161E",
    "bg_card":      "#1A1E2A",
    "bg_hover":     "#1F2433",
    "accent":       "#4F8EF7",
    "accent_light": "#7EB3FF",
    "accent_glow":  "#1A3460",
    "success":      "#3DD68C",
    "warning":      "#F7C948",
    "error":        "#F75555",
    "text_primary": "#EDF2FF",
    "text_secondary":"#8892A4",
    "text_muted":   "#4A5568",
    "border":       "#252A38",
    "border_light": "#303650",
}


# ─── Uygulama Sınıfı ───────────────────────────────────────────────────────
class PDFStudioApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Uygulama ayarları
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("PDF Studio Pro")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.configure(fg_color=COLORS["bg_dark"])

        # Durum değişkenleri
        self.input_files: list[str] = []
        self.output_folder: str = ""
        self.current_mode: str = "pdf2word"
        self.is_converting: bool = False

        # Dönüşüm modu tanımları
        self.modes = {
            "pdf2word":  {"label": "PDF → Word",   "icon": "📄→📝", "ext_in": [".pdf"],  "ext_out": ".docx"},
            "word2pdf":  {"label": "Word → PDF",   "icon": "📝→📄", "ext_in": [".docx", ".doc"], "ext_out": ".pdf"},
            "pdf2txt":   {"label": "PDF → Metin",  "icon": "📄→📋", "ext_in": [".pdf"],  "ext_out": ".txt"},
            "pdf2img":   {"label": "PDF → Görsel", "icon": "📄→🖼️", "ext_in": [".pdf"],  "ext_out": "_page.png"},
            "merge_pdf": {"label": "PDF Birleştir","icon": "📑+📑",  "ext_in": [".pdf"],  "ext_out": ".pdf"},
        }

        self._build_ui()

    # ══════════════════════════════════════════════════════════════════════
    # UI İNŞASI
    # ══════════════════════════════════════════════════════════════════════

    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main()
        self._switch_mode("pdf2word")

    # ── Kenar Çubuğu ───────────────────────────────────────────────────
    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, width=230, corner_radius=0,
            fg_color=COLORS["bg_panel"],
            border_width=1, border_color=COLORS["border"]
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(20, weight=1)

        # Logo alanı
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=(24, 8), sticky="ew")

        ctk.CTkLabel(
            logo_frame,
            text="PDF",
            font=ctk.CTkFont("Segoe UI", 26, weight="bold"),
            text_color=COLORS["accent"]
        ).pack(side="left")
        ctk.CTkLabel(
            logo_frame,
            text=" Studio",
            font=ctk.CTkFont("Segoe UI", 26),
            text_color=COLORS["text_primary"]
        ).pack(side="left")

        ctk.CTkLabel(
            self.sidebar,
            text="PRO",
            font=ctk.CTkFont("Segoe UI", 9, weight="bold"),
            text_color=COLORS["bg_dark"],
            fg_color=COLORS["accent"],
            corner_radius=4,
            width=30, height=16
        ).grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Bölüm başlığı
        ctk.CTkLabel(
            self.sidebar, text="DÖNÜŞÜM ARAÇLARI",
            font=ctk.CTkFont("Segoe UI", 9),
            text_color=COLORS["text_muted"]
        ).grid(row=2, column=0, padx=20, pady=(0, 6), sticky="w")

        # Mod butonları
        self.mode_buttons: dict[str, ctk.CTkButton] = {}
        for i, (key, val) in enumerate(self.modes.items()):
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"  {val['icon']}  {val['label']}",
                font=ctk.CTkFont("Segoe UI", 13),
                anchor="w",
                height=40,
                corner_radius=8,
                fg_color="transparent",
                text_color=COLORS["text_secondary"],
                hover_color=COLORS["bg_hover"],
                border_width=0,
                command=lambda k=key: self._switch_mode(k)
            )
            btn.grid(row=3+i, column=0, padx=12, pady=2, sticky="ew")
            self.mode_buttons[key] = btn

        # Ayarlar
        ctk.CTkFrame(
            self.sidebar, height=1,
            fg_color=COLORS["border"]
        ).grid(row=19, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(
            self.sidebar,
            text="v1.0  •  Offline",
            font=ctk.CTkFont("Segoe UI", 10),
            text_color=COLORS["text_muted"]
        ).grid(row=21, column=0, padx=20, pady=(0, 16), sticky="sw")

    # ── Ana Alan ───────────────────────────────────────────────────────
    def _build_main(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # Üst başlık
        self._build_header()

        # Dosya ekleme / drop alanı
        self._build_dropzone()

        # Dosya listesi
        self._build_file_list()

        # Alt panel (çıktı + buton)
        self._build_bottom_bar()

        # Progress bar
        self._build_progress()

    def _build_header(self):
        header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header.grid(row=0, column=0, padx=28, pady=(24, 0), sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(
            header, text="PDF → Word Dönüştürücü",
            font=ctk.CTkFont("Segoe UI", 20, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        self.subtitle_label = ctk.CTkLabel(
            header, text=".pdf dosyalarını .docx formatına dönüştür",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLORS["text_secondary"]
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(2, 0))

        # Dosya sayısı badge
        self.file_count_label = ctk.CTkLabel(
            header,
            text="0 dosya",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=COLORS["text_muted"],
            fg_color=COLORS["bg_card"],
            corner_radius=12,
            padx=12, pady=4
        )
        self.file_count_label.grid(row=0, column=2, rowspan=2, sticky="e")

    def _build_dropzone(self):
        # Drop zone frame
        drop_outer = ctk.CTkFrame(
            self.main_frame,
            fg_color=COLORS["bg_card"],
            corner_radius=12,
            border_width=2,
            border_color=COLORS["border"]
        )
        drop_outer.grid(row=1, column=0, padx=28, pady=(16, 0), sticky="ew")
        drop_outer.grid_columnconfigure((0,1,2), weight=1)

        # Drop metni
        drop_inner = ctk.CTkFrame(drop_outer, fg_color="transparent")
        drop_inner.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        drop_inner.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            drop_inner,
            text="⬆  Dosyaları Buraya Sürükleyin",
            font=ctk.CTkFont("Segoe UI", 13),
            text_color=COLORS["text_secondary"]
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            drop_inner,
            text="veya dosya seçmek için butona tıklayın",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=COLORS["text_muted"]
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))

        # Butonlar
        btn_frame = ctk.CTkFrame(drop_outer, fg_color="transparent")
        btn_frame.grid(row=0, column=2, padx=20, pady=16, sticky="e")

        ctk.CTkButton(
            btn_frame,
            text="+ Dosya Ekle",
            font=ctk.CTkFont("Segoe UI", 12, weight="bold"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_light"],
            text_color="#FFFFFF",
            corner_radius=8,
            height=36,
            width=120,
            command=self._add_files
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            btn_frame,
            text="📁 Klasör",
            font=ctk.CTkFont("Segoe UI", 12),
            fg_color=COLORS["bg_hover"],
            hover_color=COLORS["border_light"],
            text_color=COLORS["text_secondary"],
            corner_radius=8,
            height=36,
            width=90,
            command=self._add_folder
        ).pack(side="left")

    def _build_file_list(self):
        # Dosya listesi
        list_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=COLORS["bg_card"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )
        list_frame.grid(row=2, column=0, padx=28, pady=12, sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)

        # Liste başlık
        list_header = ctk.CTkFrame(list_frame, fg_color="transparent")
        list_header.grid(row=0, column=0, padx=16, pady=(12, 6), sticky="ew")
        list_header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            list_header, text="DOSYA",
            font=ctk.CTkFont("Segoe UI", 10),
            text_color=COLORS["text_muted"]
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            list_header, text="BOYUT",
            font=ctk.CTkFont("Segoe UI", 10),
            text_color=COLORS["text_muted"]
        ).grid(row=0, column=2, sticky="e", padx=(0, 90))

        ctk.CTkLabel(
            list_header, text="DURUM",
            font=ctk.CTkFont("Segoe UI", 10),
            text_color=COLORS["text_muted"]
        ).grid(row=0, column=3, sticky="e", padx=(0, 20))

        # Ayraç
        ctk.CTkFrame(list_frame, height=1, fg_color=COLORS["border"]).grid(
            row=1, column=0, sticky="ew", padx=0
        )

        # Scrollable liste
        self.scroll_frame = ctk.CTkScrollableFrame(
            list_frame,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["border_light"]
        )
        self.scroll_frame.grid(row=2, column=0, sticky="nsew", padx=4, pady=4)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Boş durum
        self.empty_label = ctk.CTkLabel(
            self.scroll_frame,
            text="Henüz dosya eklenmedi\n\nYukarıdaki butonu kullanarak\ndosya ekleyebilirsiniz",
            font=ctk.CTkFont("Segoe UI", 13),
            text_color=COLORS["text_muted"],
            justify="center"
        )
        self.empty_label.pack(expand=True, pady=60)

        self.file_row_widgets: list[dict] = []

    def _build_bottom_bar(self):
        bar = ctk.CTkFrame(
            self.main_frame,
            fg_color=COLORS["bg_panel"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )
        bar.grid(row=3, column=0, padx=28, pady=(0, 8), sticky="ew")
        bar.grid_columnconfigure(1, weight=1)

        # Çıktı klasörü
        left = ctk.CTkFrame(bar, fg_color="transparent")
        left.grid(row=0, column=0, padx=16, pady=12, sticky="ew")

        ctk.CTkLabel(
            left, text="Çıktı Klasörü",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=COLORS["text_secondary"]
        ).pack(side="top", anchor="w")

        folder_row = ctk.CTkFrame(left, fg_color="transparent")
        folder_row.pack(fill="x", pady=(4, 0))

        self.folder_entry = ctk.CTkEntry(
            folder_row,
            placeholder_text="Seçilmedi - kaynak dosya konumuna kaydedilecek",
            font=ctk.CTkFont("Segoe UI", 11),
            fg_color=COLORS["bg_card"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            width=400, height=32
        )
        self.folder_entry.pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            folder_row,
            text="Gözat",
            font=ctk.CTkFont("Segoe UI", 11),
            fg_color=COLORS["bg_hover"],
            hover_color=COLORS["border_light"],
            text_color=COLORS["text_secondary"],
            corner_radius=6,
            height=32, width=70,
            command=self._browse_output
        ).pack(side="left")

        # Temizle butonu
        ctk.CTkButton(
            bar,
            text="🗑  Temizle",
            font=ctk.CTkFont("Segoe UI", 11),
            fg_color="transparent",
            hover_color=COLORS["bg_hover"],
            text_color=COLORS["text_muted"],
            corner_radius=6,
            height=32, width=90,
            command=self._clear_files
        ).grid(row=0, column=1, padx=8, pady=12)

        # Dönüştür butonu
        self.convert_btn = ctk.CTkButton(
            bar,
            text="▶  Dönüştür",
            font=ctk.CTkFont("Segoe UI", 13, weight="bold"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_light"],
            text_color="#FFFFFF",
            corner_radius=8,
            height=40, width=140,
            command=self._start_conversion
        )
        self.convert_btn.grid(row=0, column=2, padx=16, pady=12)

    def _build_progress(self):
        self.progress_frame = ctk.CTkFrame(
            self.main_frame, fg_color="transparent"
        )
        self.progress_frame.grid(row=4, column=0, padx=28, pady=(0, 20), sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)

        progress_top = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        progress_top.pack(fill="x")
        progress_top.grid_columnconfigure(0, weight=1)

        self.progress_label = ctk.CTkLabel(
            progress_top, text="",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=COLORS["text_secondary"]
        )
        self.progress_label.pack(side="left")

        self.progress_percent = ctk.CTkLabel(
            progress_top, text="",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=COLORS["accent"]
        )
        self.progress_percent.pack(side="right")

        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            fg_color=COLORS["bg_card"],
            progress_color=COLORS["accent"],
            corner_radius=4,
            height=6
        )
        self.progress_bar.pack(fill="x", pady=(6, 0))
        self.progress_bar.set(0)
        self.progress_frame.pack_forget()

    # ══════════════════════════════════════════════════════════════════════
    # MOD DEĞİŞTİRME
    # ══════════════════════════════════════════════════════════════════════

    def _switch_mode(self, key: str):
        self.current_mode = key
        info = self.modes[key]

        # Buton stillerini güncelle
        for k, btn in self.mode_buttons.items():
            if k == key:
                btn.configure(
                    fg_color=COLORS["accent_glow"],
                    text_color=COLORS["accent_light"],
                    border_width=1,
                    border_color=COLORS["accent"]
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS["text_secondary"],
                    border_width=0
                )

        # Başlık güncelle
        titles = {
            "pdf2word":  ("PDF → Word Dönüştürücü", ".pdf dosyalarını .docx formatına dönüştür"),
            "word2pdf":  ("Word → PDF Dönüştürücü", ".docx ve .doc dosyalarını PDF'e dönüştür"),
            "pdf2txt":   ("PDF → Metin Çıkarıcı",   "PDF içindeki tüm metni .txt dosyasına aktar"),
            "pdf2img":   ("PDF → Görsel Dönüştürücü","Her sayfayı ayrı PNG görseline çevir"),
            "merge_pdf": ("PDF Birleştirici",        "Birden fazla PDF dosyasını tek dosyada birleştir"),
        }
        t, s = titles[key]
        self.title_label.configure(text=t)
        self.subtitle_label.configure(text=s)

        # Mevcut dosyaları temizle
        self._clear_files()

    # ══════════════════════════════════════════════════════════════════════
    # DOSYA YÖNETİMİ
    # ══════════════════════════════════════════════════════════════════════

    def _add_files(self):
        exts = self.modes[self.current_mode]["ext_in"]
        types = [("Desteklenen Dosyalar", " ".join(f"*{e}" for e in exts))]
        files = filedialog.askopenfilenames(filetypes=types)
        for f in files:
            if f not in self.input_files:
                self.input_files.append(f)
        self._refresh_list()

    def _add_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return
        exts = self.modes[self.current_mode]["ext_in"]
        for f in Path(folder).iterdir():
            if f.suffix.lower() in exts and str(f) not in self.input_files:
                self.input_files.append(str(f))
        self._refresh_list()

    def _browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)

    def _clear_files(self):
        self.input_files.clear()
        self._refresh_list()

    def _remove_file(self, path: str):
        if path in self.input_files:
            self.input_files.remove(path)
        self._refresh_list()

    def _refresh_list(self):
        # Tüm satırları temizle
        for w in self.file_row_widgets:
            w["frame"].destroy()
        self.file_row_widgets.clear()

        count = len(self.input_files)
        self.file_count_label.configure(text=f"{count} dosya")

        if count == 0:
            self.empty_label.pack(expand=True, pady=60)
            return

        self.empty_label.pack_forget()

        for i, path in enumerate(self.input_files):
            self._add_file_row(i, path)

    def _add_file_row(self, idx: int, path: str):
        p = Path(path)
        size = p.stat().st_size if p.exists() else 0
        size_str = self._format_size(size)

        row_bg = COLORS["bg_hover"] if idx % 2 == 0 else "transparent"

        frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=row_bg,
            corner_radius=6,
            height=44
        )
        frame.pack(fill="x", padx=4, pady=2)
        frame.pack_propagate(False)
        frame.grid_columnconfigure(1, weight=1)

        # Dosya ikonu
        ext = p.suffix.lower()
        icons = {".pdf": "📄", ".docx": "📝", ".doc": "📝", ".txt": "📋", ".png": "🖼️"}
        icon = icons.get(ext, "📎")

        ctk.CTkLabel(
            frame, text=icon,
            font=ctk.CTkFont("Segoe UI", 16),
            width=32
        ).grid(row=0, column=0, padx=(10, 4), pady=8, sticky="w")

        # Dosya adı
        ctk.CTkLabel(
            frame,
            text=p.name,
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLORS["text_primary"],
            anchor="w"
        ).grid(row=0, column=1, padx=4, pady=8, sticky="ew")

        # Boyut
        ctk.CTkLabel(
            frame,
            text=size_str,
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=COLORS["text_muted"],
            width=70
        ).grid(row=0, column=2, padx=8, pady=8, sticky="e")

        # Durum
        status_lbl = ctk.CTkLabel(
            frame,
            text="Bekliyor",
            font=ctk.CTkFont("Segoe UI", 10),
            text_color=COLORS["text_muted"],
            fg_color=COLORS["bg_card"],
            corner_radius=4,
            padx=8, pady=2,
            width=70
        )
        status_lbl.grid(row=0, column=3, padx=8, pady=8, sticky="e")

        # Sil butonu
        del_btn = ctk.CTkButton(
            frame,
            text="✕",
            font=ctk.CTkFont("Segoe UI", 11),
            fg_color="transparent",
            hover_color=COLORS["error"],
            text_color=COLORS["text_muted"],
            width=28, height=28,
            corner_radius=4,
            command=lambda p=path: self._remove_file(p)
        )
        del_btn.grid(row=0, column=4, padx=(4, 10), pady=8, sticky="e")

        self.file_row_widgets.append({
            "frame": frame,
            "path": path,
            "status": status_lbl
        })

    @staticmethod
    def _format_size(size: int) -> str:
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    # ══════════════════════════════════════════════════════════════════════
    # DÖNÜŞÜM İŞLEMLERİ
    # ══════════════════════════════════════════════════════════════════════

    def _start_conversion(self):
        if not self.input_files:
            messagebox.showwarning("Uyarı", "Lütfen önce dosya ekleyin.")
            return
        if self.is_converting:
            return

        self.is_converting = True
        self.convert_btn.configure(
            text="⏳ Dönüştürülüyor...",
            state="disabled",
            fg_color=COLORS["bg_hover"]
        )

        # Progress bar göster (frame grid ile yerleştirildiği için grid kullan)
        self.progress_frame.grid()

        thread = threading.Thread(target=self._convert_all, daemon=True)
        thread.start()

    def _convert_all(self):
        total = len(self.input_files)
        for i, path in enumerate(self.input_files):
            pct = i / total

            self.after(0, lambda p=pct, i=i: (
                self.progress_bar.set(p),
                self.progress_label.configure(text=f"İşleniyor: {Path(path).name[:45]}..."),
                self.progress_percent.configure(text=f"{int(p*100)}%"),
                self._set_file_status(i, "İşleniyor...", COLORS["warning"])
            ))

            success, msg = self._convert_single(path)

            status_text = "✓ Tamamlandı" if success else "✗ Hata"
            status_color = COLORS["success"] if success else COLORS["error"]

            idx = i
            self.after(0, lambda idx=idx, t=status_text, c=status_color: 
                self._set_file_status(idx, t, c))

            if not success:
                self.after(0, lambda m=msg, p=path: 
                    messagebox.showerror("Hata", f"{Path(p).name}:\n{m}"))

        self.after(0, self._conversion_done)

    def _convert_single(self, path: str) -> tuple[bool, str]:
        mode = self.current_mode
        out_dir = self.output_folder or str(Path(path).parent)

        try:
            if mode == "pdf2word":
                return self._pdf_to_word(path, out_dir)
            elif mode == "word2pdf":
                return self._word_to_pdf(path, out_dir)
            elif mode == "pdf2txt":
                return self._pdf_to_txt(path, out_dir)
            elif mode == "pdf2img":
                return self._pdf_to_img(path, out_dir)
            elif mode == "merge_pdf":
                return self._merge_pdfs()
        except Exception as e:
            return False, str(e)
        return False, "Bilinmeyen mod"

    def _pdf_to_word(self, path: str, out_dir: str) -> tuple[bool, str]:
        if not PDF2DOCX_OK:
            return False, "pdf2docx kütüphanesi yüklü değil"
        out = os.path.join(out_dir, Path(path).stem + ".docx")
        cv = PDF2DOCXConverter(path)
        cv.convert(out, start=0, end=None)
        cv.close()
        return True, out

    def _word_to_pdf(self, path: str, out_dir: str) -> tuple[bool, str]:
        if not DOCX2PDF_OK:
            return False, "docx2pdf kütüphanesi yüklü değil"
        out = os.path.join(out_dir, Path(path).stem + ".pdf")
        docx2pdf_convert(path, out)
        return True, out

    def _pdf_to_txt(self, path: str, out_dir: str) -> tuple[bool, str]:
        if not PYMUPDF_OK:
            return False, "PyMuPDF kütüphanesi yüklü değil"
        out = os.path.join(out_dir, Path(path).stem + ".txt")
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        return True, out

    def _pdf_to_img(self, path: str, out_dir: str) -> tuple[bool, str]:
        if not PYMUPDF_OK:
            return False, "PyMuPDF kütüphanesi yüklü değil"
        doc = fitz.open(path)
        stem = Path(path).stem
        for i, page in enumerate(doc):
            mat = fitz.Matrix(2, 2)  # 2x zoom = yüksek kalite
            pix = page.get_pixmap(matrix=mat)
            out = os.path.join(out_dir, f"{stem}_sayfa{i+1:03d}.png")
            pix.save(out)
        doc.close()
        return True, f"{len(doc)} sayfa kaydedildi"

    def _merge_pdfs(self) -> tuple[bool, str]:
        if not PYMUPDF_OK:
            return False, "PyMuPDF kütüphanesi yüklü değil"
        if len(self.input_files) < 2:
            return False, "En az 2 PDF dosyası gerekli"
        out_dir = self.output_folder or str(Path(self.input_files[0]).parent)
        out = os.path.join(out_dir, "birlestirilmis.pdf")
        doc = fitz.open()
        for f in self.input_files:
            doc.insert_pdf(fitz.open(f))
        doc.save(out)
        doc.close()
        return True, out

    def _set_file_status(self, idx: int, text: str, color: str):
        if idx < len(self.file_row_widgets):
            self.file_row_widgets[idx]["status"].configure(
                text=text,
                text_color=color
            )

    def _conversion_done(self):
        self.is_converting = False
        self.progress_bar.set(1.0)
        self.progress_label.configure(text="✓ Tüm dosyalar tamamlandı")
        self.progress_percent.configure(text="100%")
        self.convert_btn.configure(
            text="▶  Dönüştür",
            state="normal",
            fg_color=COLORS["accent"]
        )

        # 3sn sonra progress'i sıfırla ve gizle
        self.after(3000, lambda: (
            self.progress_bar.set(0),
            self.progress_label.configure(text=""),
            self.progress_percent.configure(text=""),
            self.progress_frame.grid_remove()
        ))


# ─── Giriş Noktası ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = PDFStudioApp()
    app.mainloop()
