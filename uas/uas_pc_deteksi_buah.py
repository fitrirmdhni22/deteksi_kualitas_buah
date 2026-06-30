import cv2
import numpy as np
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class DeteksiBuahGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UAS Pengolahan Citra Digital - Deteksi Kualitas Buah")
        
        # Resolusi window utama
        self.root.geometry("1300x850")
        self.root.minsize(1024, 725)
        
        # Tema Warna Modern (Dark Mode)
        self.bg_dark = "#1e1e24"
        self.bg_card = "#2a2a32"
        self.fg_light = "#f5f5f7"
        self.accent_blue = "#007aff"
        self.color_good = "#34c759"  # Hijau (Buah Bagus)
        self.color_bad = "#ff3b30"   # Merah (Buah Busuk)
        
        self.root.configure(bg=self.bg_dark)
        
        # Variabel Data Gambar
        self.path_gambar = None
        self.cv_img_asli = None
        
        # Inisialisasi Komponen Antarmuka
        self.buat_layout()

    def buat_layout(self):
        """Membangun tata letak grid dan panel GUI"""
        # --- HEADER PANEL ---
        header = tk.Frame(self.root, bg=self.bg_card, height=70, relief=tk.RIDGE, bd=1)
        header.pack(fill=tk.X, side=tk.TOP)
        
        lbl_judul = tk.Label(header, text="DETEKSI KUALITAS BUAH", font=("Helvetica", 16, "bold"), fg=self.fg_light, bg=self.bg_card)
        lbl_judul.pack(side=tk.LEFT, padx=20, pady=10)
        
        lbl_sub = tk.Label(header, text="Mini Project UAS | Pengolahan Citra Digital", font=("Helvetica", 10, "italic"), fg="#a1a1aa", bg=self.bg_card)
        lbl_sub.pack(side=tk.RIGHT, padx=20, pady=15)

        # --- MAIN CONTAINER ---
        main_container = tk.Frame(self.root, bg=self.bg_dark)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # KIRI: Panel Kontrol & Hasil Analisis
        panel_kiri = tk.Frame(main_container, bg=self.bg_dark, width=320)
        panel_kiri.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        panel_kiri.pack_propagate(False)

        # KANAN: Grid Penampil Alur Citra (Menampung 10 Kotak Tahapan)
        self.panel_kanan = tk.Frame(main_container, bg=self.bg_card, bd=1, relief=tk.SOLID)
        self.panel_kanan.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- SEKSI TOMBOL KONTROL (KIRI) ---
        frame_tombol = tk.LabelFrame(panel_kiri, text=" Kontrol Aplikasi ", font=("Helvetica", 10, "bold"), bg=self.bg_card, fg=self.fg_light, padx=10, pady=10)
        frame_tombol.pack(fill=tk.X, pady=(0, 15))

        btn_style = {
            "font": ("Helvetica", 10, "bold"), 
            "fg": self.fg_light, 
            "bd": 0, 
            "cursor": "hand2", 
            "activebackground": "#3a3a4c", 
            "activeforeground": "white",
            "height": 2  
        }
        
        self.btn_upload = tk.Button(frame_tombol, text="📁 Upload Gambar", bg=self.accent_blue, command=self.upload_gambar, **btn_style)
        self.btn_upload.pack(fill=tk.X, pady=5)

        self.btn_proses = tk.Button(frame_tombol, text="⚙️ Proses Analisis", bg="#5856d6", command=self.proses_citra, **btn_style)
        self.btn_proses.pack(fill=tk.X, pady=5)

        self.btn_reset = tk.Button(frame_tombol, text="🔄 Reset", bg="#8e8e93", command=self.reset_aplikasi, **btn_style)
        self.btn_reset.pack(fill=tk.X, pady=5)

        self.btn_keluar = tk.Button(frame_tombol, text="❌ Keluar", bg=self.color_bad, command=self.root.quit, **btn_style)
        self.btn_keluar.pack(fill=tk.X, pady=5)

        # --- SEKSI HASIL KLASIFIKASI (KIRI) ---
        self.frame_hasil = tk.LabelFrame(panel_kiri, text=" Hasil Klasifikasi ", font=("Helvetica", 10, "bold"), bg=self.bg_card, fg=self.fg_light, padx=15, pady=15)
        self.frame_hasil.pack(fill=tk.BOTH, expand=True)

        self.lbl_status_title = tk.Label(self.frame_hasil, text="STATUS BUAH :", font=("Helvetica", 11, "bold"), fg="#a1a1aa", bg=self.bg_card)
        self.lbl_status_title.pack(anchor=tk.W, pady=(5, 2))
        self.lbl_status_val = tk.Label(self.frame_hasil, text="-", font=("Helvetica", 20, "bold"), fg=self.fg_light, bg=self.bg_card)
        self.lbl_status_val.pack(anchor=tk.W, pady=(0, 15))

        self.lbl_sehat_val = self.buat_row_metrik("Kesehatan Buah", "-")
        self.lbl_busuk_val = self.buat_row_metrik("Persentase Busuk/Bercak", "-")
        self.lbl_hsv_val = self.buat_row_metrik("Rata-rata Nilai HSV", "-")
        self.lbl_waktu_val = self.buat_row_metrik("Waktu Komputasi", "-")

        # --- SEKSI TAMPILAN MATRIKS GAMBAR (KANAN) ---
        for i in range(2):
            self.panel_kanan.rowconfigure(i, weight=1)
        for j in range(5):
            self.panel_kanan.columnconfigure(j, weight=1)

        self.display_boxes = {}
        tahapan_nama = [
            "1. Gambar Asli", "2. Grayscale", "3. Citra Biner (Threshold)", 
            "4. Histogram Equalization", "5. Mean Filter", "6. Median Filter", 
            "7. Gaussian Blur", "8. Edge Canny", "9. Segmentasi Buah (Otsu)", "Hasil Deteksi"
        ]
        
        idx = 0
        for r in range(2):
            for c in range(5):
                frame_box = tk.Frame(self.panel_kanan, bg=self.bg_dark, bd=1, relief=tk.SOLID)
                frame_box.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
                
                lbl_tag = tk.Label(frame_box, text=tahapan_nama[idx], font=("Helvetica", 8, "bold"), fg="#a1a1aa", bg=self.bg_dark)
                lbl_tag.pack(side=tk.TOP, fill=tk.X, pady=2)
                
                lbl_img = tk.Label(frame_box, text="Belum ada gambar", fg="#555562", bg=self.bg_dark, font=("Helvetica", 8))
                lbl_img.pack(fill=tk.BOTH, expand=True)
                
                self.display_boxes[idx] = lbl_img
                idx += 1

    def buat_row_metrik(self, label_text, default_val):
        lbl_title = tk.Label(self.frame_hasil, text=label_text, font=("Helvetica", 9), fg="#a1a1aa", bg=self.bg_card)
        lbl_title.pack(anchor=tk.W, pady=(4, 0))
        lbl_val = tk.Label(self.frame_hasil, text=default_val, font=("Helvetica", 11, "bold"), fg=self.fg_light, bg=self.bg_card)
        lbl_val.pack(anchor=tk.W, pady=(0, 8))
        return lbl_val

    def muat_gambar_ke_ui(self, mat_img, index_box):
        if mat_img is None:
            return
        if len(mat_img.shape) == 3:
            img_rgb = cv2.cvtColor(mat_img, cv2.COLOR_BGR2RGB)
        else:
            img_rgb = cv2.cvtColor(mat_img, cv2.COLOR_GRAY2RGB)
            
        img_pil = Image.fromarray(img_rgb)
        self.root.update_idletasks()
        box_width = self.display_boxes[index_box].winfo_width()
        box_height = self.display_boxes[index_box].winfo_height()
        
        if box_width < 10 or box_height < 10:
            box_width, box_height = 180, 180
            
        img_pil.thumbnail((box_width, box_height), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        self.display_boxes[index_box].configure(image=img_tk, text="")
        self.display_boxes[index_box].image = img_tk

    # ==========================================
    # WORKFLOW ALGORITMA PENGOLAHAN CITRA
    # ==========================================

    def upload_gambar(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp")]
        )
        if file_path:
            self.path_gambar = file_path
            self.cv_img_asli = cv2.imread(file_path)
            self.muat_gambar_ke_ui(self.cv_img_asli, 0)
            self.muat_gambar_ke_ui(self.cv_img_asli, 9)
            for i in range(1, 9):
                self.display_boxes[i].configure(image="", text="Menunggu Proses...")

    def preprocessing(self, img):
        """Tahap 1, 2, & 4: Konversi Grayscale, Biner Eksplisit, dan Histogram Equalization"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Poin 1: Konversi RGB ke Biner Eksplisit (Menggunakan nilai threshold statis tengah 127)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Poin 2: Perbaikan Kualitas Citra via Histogram Equalization
        equalized = cv2.equalizeHist(gray)
        return gray, binary, equalized

    def filtering_lengkap(self, img):
        """Tahap 3: Implementasi 3 Jenis Filter (Mean, Median, Gaussian)"""
        # A. Mean Filter (Menggunakan cv2.blur dengan kernel homogen)
        mean_fltr = cv2.blur(img, (5, 5))
        
        # B. Median Filter (Menggunakan cv2.medianBlur)
        median_fltr = cv2.medianBlur(img, 5)
        
        # C. Gaussian Filter (Menggunakan cv2.GaussianBlur)
        gaussian_fltr = cv2.GaussianBlur(median_fltr, (5, 5), 0)
        
        return mean_fltr, median_fltr, gaussian_fltr

    def edge_detection(self, img):
        """Tahap 4: Deteksi Tepi Canny"""
        return cv2.Canny(img, 30, 100)

    def segmentasi(self, img_equalized):
        """Tahap 5: Segmentasi Objek Menggunakan Otsu Thresholding + Pengisian Lubang Kontur"""
        _, mask_otsu = cv2.threshold(img_equalized, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        hsv = cv2.cvtColor(self.cv_img_asli, cv2.COLOR_BGR2HSV)
        v_channel = hsv[:, :, 2]
        _, mask_v_bright = cv2.threshold(v_channel, 248, 255, cv2.THRESH_BINARY_INV)
        mask_gabungan = cv2.bitwise_and(mask_otsu, mask_v_bright)
        
        mask_filled = np.zeros_like(mask_gabungan)
        kontur, _ = cv2.findContours(mask_gabungan, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for k in kontur:
            if cv2.contourArea(k) > 1200:  
                cv2.drawContours(mask_filled, [k], -1, 255, -1)
                
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        mask_buah_final = cv2.morphologyEx(mask_filled, cv2.MORPH_CLOSE, kernel)
        return mask_buah_final

    def analisis_hsv(self, img_bgr, mask_buah):
        """Tahap Analisis Cacat: Deteksi Cokelat Lebam Semu & Pembusukan Gelap"""
        hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        mean_hsv = cv2.mean(hsv, mask=mask_buah)[:3]
        
        lower_brown = np.array([7, 45, 20])
        upper_brown = np.array([26, 230, 150])
        mask_warna = cv2.inRange(hsv, lower_brown, upper_brown)
        
        v_channel = hsv[:, :, 2]
        _, mask_v_gelap = cv2.threshold(v_channel, 60, 255, cv2.THRESH_BINARY_INV)
        
        mask_cacat = cv2.bitwise_or(mask_warna, mask_v_gelap)
        mask_bercak_final = cv2.bitwise_and(mask_cacat, mask_buah)
        
        kernel_clean = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        mask_bercak_final = cv2.morphologyEx(mask_bercak_final, cv2.MORPH_OPEN, kernel_clean)
        
        return mean_hsv, mask_bercak_final

    def proses_citra(self):
        if self.cv_img_asli is None:
            messagebox.showwarning("Peringatan", "Silakan unggah gambar buah terlebih dahulu!")
            return

        start_time = time.time()
        
        # 1. Pipeline Konversi Citra & Perbaikan Kualitas
        img_gray, img_biner, img_equalized = self.preprocessing(self.cv_img_asli)
        
        # 2. Pipeline Filtering Lengkap
        img_mean, img_median, img_gaussian = self.filtering_lengkap(img_equalized)
        
        # 3. Pipeline Deteksi Tepi
        img_canny = self.edge_detection(img_gaussian)
        
        # 4. Pipeline Segmentasi Utama
        mask_buah = self.segmentasi(img_equalized)
        
        # 5. Pipeline Analisis Nilai HSV & Ekstraksi Bercak Cacat
        mean_hsv, mask_bercak = self.analisis_hsv(self.cv_img_asli, mask_buah)
        
        total_piksel_buah = cv2.countNonZero(mask_buah)
        if total_piksel_buah == 0: total_piksel_buah = 1
        
        img_hasil_visual = self.cv_img_asli.copy()
        kontur, _ = cv2.findContours(mask_bercak, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        piksel_busuk_valid = 0
        for k in kontur:
            luas_area = cv2.contourArea(k)
            if luas_area > 400:  
                x, y, w, h = cv2.boundingRect(k)
                aspek_rasio = float(w)/h
                if 0.25 < aspek_rasio < 4.0:
                    piksel_busuk_valid += luas_area
                    cv2.rectangle(img_hasil_visual, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    
        # Perhitungan Persentase Kualitas Akhir
        persentase_busuk = (piksel_busuk_valid / total_piksel_buah) * 100
        if persentase_busuk > 100: persentase_busuk = 100.0
        persentase_sehat = 100 - persentase_busuk
        
        # Batas ambang klasifikasi kualitas buah (Threshold Kelayakan = 5.0%)
        threshold_busuk = 5.0
        if persentase_busuk > threshold_busuk:
            status_buah, warna_indikator = "Buah Busuk", self.color_bad
        else:
            status_buah, warna_indikator = "Buah Bagus", self.color_good
        
        end_time = time.time()
        processing_duration = (end_time - start_time) * 1000

        # Update Seluruh 10 Tampilan Matriks Gambar ke Grid GUI
        self.muat_gambar_ke_ui(self.cv_img_asli, 0)
        self.muat_gambar_ke_ui(img_gray, 1)
        self.muat_gambar_ke_ui(img_biner, 2)
        self.muat_gambar_ke_ui(img_equalized, 3)
        self.muat_gambar_ke_ui(img_mean, 4)
        self.muat_gambar_ke_ui(img_median, 5)
        self.muat_gambar_ke_ui(img_gaussian, 6)
        self.muat_gambar_ke_ui(img_canny, 7)
        self.muat_gambar_ke_ui(mask_buah, 8)     
        self.muat_gambar_ke_ui(img_hasil_visual, 9)

        # Update Papan Statistik Informasi
        self.lbl_status_val.configure(text=status_buah, fg=warna_indikator)
        self.lbl_sehat_val.configure(text=f"{persentase_sehat:.1f}%", fg=warna_indikator)
        self.lbl_busuk_val.configure(text=f"{persentase_busuk:.1f}%")
        self.lbl_hsv_val.configure(text=f"H={int(mean_hsv[0])}  S={int(mean_hsv[1])}  V={int(mean_hsv[2])}")
        self.lbl_waktu_val.configure(text=f"{processing_duration:.2f} ms")

    def reset_aplikasi(self):
        self.path_gambar = None
        self.cv_img_asli = None
        self.lbl_status_val.configure(text="-", fg=self.fg_light)
        self.lbl_sehat_val.configure(text="-", fg=self.fg_light)
        self.lbl_busuk_val.configure(text="-")
        self.lbl_hsv_val.configure(text="-")
        self.lbl_waktu_val.configure(text="-")
        for i in range(10):
            self.display_boxes[i].configure(image="", text="Belum ada gambar")

if __name__ == "__main__":
    root_window = tk.Tk()
    app = DeteksiBuahGUI(root_window)
    root_window.mainloop()