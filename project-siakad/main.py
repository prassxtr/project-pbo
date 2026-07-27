# ============================================================
# main.py - Lapisan Controller / App
# SIAKAD Mini - Sistem Informasi Akademik
# ============================================================

import tkinter as tk
from tkinter import messagebox

from model import (DatabaseManager, UserModel, MahasiswaModel,
                   MataKuliahModel, KRSModel, KHSModel)
from view import (Tema, LoginFrame, DashboardFrame, MahasiswaFrame,
                  MataKuliahFrame, KRSFrame, KHSFrame)


class AppController(tk.Tk):
    """Controller utama. Mewarisi tk.Tk."""

    def __init__(self):
        super().__init__()
        self.title("SIAKAD Mini — Sistem Informasi Akademik")
        self.geometry("1000x750")
        self.minsize(900, 650)
        self.configure(bg=Tema.BG_DARK)

        # Inisialisasi Model (Encapsulation)
        self.__db = DatabaseManager("siakad.db")
        self.__user_model = UserModel(self.__db)
        self.__mhs_model = MahasiswaModel(self.__db)
        self.__mk_model = MataKuliahModel(self.__db)
        self.__krs_model = KRSModel(self.__db)
        self.__khs_model = KHSModel()

        # State User
        self.__current_user = None

        # Tampilkan Login terlebih dahulu
        self._tampilkan_login()
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    # ============================================================
    # SISTEM LOGIN & LOGOUT
    # ============================================================
    def _tampilkan_login(self):
        self.login_frame = LoginFrame(self, self)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def proses_login(self, username, password):
        try:
            user_data = self.__user_model.login(username, password)
            self.__current_user = user_data

            messagebox.showinfo("Login Berhasil",
                                f"Selamat datang, {user_data['nama_lengkap']}!")

            self.login_frame.pack_forget()
            self.login_frame.destroy()

            self._buat_menu_bar()
            self._buat_sidebar()
            self._buat_frame_switching()
            self._tampilkan_halaman("dashboard")

        except Exception as e:
            messagebox.showerror("Login Gagal", str(e))
            self.login_frame.clear_form()

    def _proses_logout(self):
        if messagebox.askyesno("Konfirmasi Logout",
                               "Apakah Anda yakin ingin keluar?"):
            self.__current_user = None
            self.config(menu="")
            if hasattr(self, 'sidebar'):
                self.sidebar.destroy()
            if hasattr(self, 'container'):
                self.container.destroy()
            if hasattr(self, '__frames'):
                self.__frames.clear()
            self._tampilkan_login()

    # ============================================================
    # MENU BAR (WAJIB sesuai Panduan Proyek)
    # ============================================================
    def _buat_menu_bar(self):
        menubar = tk.Menu(self, bg=Tema.BG_SIDEBAR, fg=Tema.TEXT_LIGHT,
                          activebackground=Tema.ACCENT,
                          activeforeground="white",
                          font=Tema.FONT_SMALL, relief="flat", bd=0)


        self.config(menu=menubar)

    # ============================================================
    # SIDEBAR
    # ============================================================
    def _buat_sidebar(self):
        self.sidebar = tk.Frame(self, bg=Tema.BG_SIDEBAR, width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Info User Login
        user_frame = tk.Frame(self.sidebar, bg=Tema.BG_SIDEBAR)
        user_frame.pack(fill=tk.X, pady=(20, 10), padx=15)

        tk.Label(user_frame, text="👤", font=("Segoe UI", 24),
                 bg=Tema.BG_SIDEBAR).pack()
        tk.Label(user_frame, text=self.__current_user['nama_lengkap'],
                 font=("Segoe UI", 10, "bold"),
                 bg=Tema.BG_SIDEBAR, fg=Tema.TEXT_LIGHT,
                 wraplength=170).pack()
        tk.Label(user_frame, text=f"({self.__current_user['role']})",
                 font=Tema.FONT_SMALL,
                 bg=Tema.BG_SIDEBAR, fg=Tema.TEXT_MUTED).pack()

        tk.Frame(self.sidebar, bg=Tema.ACCENT, height=1).pack(
            fill=tk.X, padx=15, pady=10)

        # Tombol navigasi
        self.sidebar_buttons = {}
        nav_items = [
            ("  Dashboard", "dashboard"),
            ("  Mahasiswa", "mahasiswa"),
            ("📚  Mata Kuliah", "mata_kuliah"),
            ("📝  KRS", "krs"),
            ("🎓  KHS / IPK", "khs"),
        ]
        for teks, key in nav_items:
            btn = tk.Button(
                self.sidebar, text=teks, font=Tema.FONT_SMALL,
                bg=Tema.BG_SIDEBAR, fg=Tema.TEXT_LIGHT,
                activebackground=Tema.ACCENT, activeforeground="white",
                relief="flat", anchor="w", padx=15, pady=10,
                cursor="hand2",
                command=lambda k=key: self._tampilkan_halaman(k)
            )
            btn.pack(fill=tk.X, padx=10, pady=2)
            self.sidebar_buttons[key] = btn

        # Tombol Logout
        tk.Frame(self.sidebar, bg=Tema.ACCENT, height=1).pack(
            fill=tk.X, padx=15, pady=20)
        btn_logout = tk.Button(
            self.sidebar, text="🚪  Logout", font=Tema.FONT_BUTTON,
            bg=Tema.DANGER, fg="white", relief="flat",
            cursor="hand2", pady=8, command=self._proses_logout
        )
        btn_logout.pack(fill=tk.X, padx=10)

        tk.Label(self.sidebar, text="© 2025 PBO Project",
                 font=("Segoe UI", 9),
                 bg=Tema.BG_SIDEBAR, fg=Tema.TEXT_MUTED).pack(
            side=tk.BOTTOM, pady=10)

    # ============================================================
    # FRAME SWITCHING
    # ============================================================
    def _buat_frame_switching(self):
        self.container = tk.Frame(self, bg=Tema.BG_MAIN)
        self.container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.__frames = {}
        for FrameClass, nama in [
            (DashboardFrame, "dashboard"),
            (MahasiswaFrame, "mahasiswa"),
            (MataKuliahFrame, "mata_kuliah"),
            (KRSFrame, "krs"),
            (KHSFrame, "khs"),
        ]:
            frame = FrameClass(self.container, self)
            self.__frames[nama] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def _tampilkan_halaman(self, nama):
        self.__frames[nama].tkraise()

        for key, btn in self.sidebar_buttons.items():
            if key == nama:
                btn.config(bg=Tema.ACCENT, fg="white")
            else:
                btn.config(bg=Tema.BG_SIDEBAR, fg=Tema.TEXT_LIGHT)

        if nama == "dashboard":
            self._refresh_dashboard()
        elif nama == "mahasiswa":
            self._refresh_mahasiswa()
        elif nama == "mata_kuliah":
            self._refresh_mata_kuliah()
        elif nama == "krs":
            self._refresh_krs()
        elif nama == "khs":
            self._siapkan_khs()

    # ============================================================
    # CRUD MAHASISWA
    # ============================================================
    def simpan_mahasiswa(self, nim, nama, jurusan, angkatan):
        try:
            self.__mhs_model.tambah(nim, nama, jurusan, angkatan)
            messagebox.showinfo("✅ Sukses",
                                f"Mahasiswa '{nama}' berhasil ditambahkan!")
            self._refresh_mahasiswa()
        except Exception as e:
            messagebox.showerror("❌ Gagal", str(e))

    def perbarui_mahasiswa(self, nim_lama, nim, nama, jurusan, angkatan):
        try:
            self.__mhs_model.perbarui(nim_lama, nim, nama, jurusan, angkatan)
            messagebox.showinfo("✅ Sukses",
                                "Data mahasiswa berhasil diperbarui!")
            self._refresh_mahasiswa()
        except Exception as e:
            messagebox.showerror("❌ Gagal", str(e))

    def hapus_mahasiswa(self, nim):
        try:
            self.__mhs_model.hapus(nim)
            messagebox.showinfo("✅ Sukses",
                                "Data mahasiswa berhasil dihapus!")
            self._refresh_mahasiswa()
        except Exception as e:
            messagebox.showerror("❌ Gagal", str(e))

    def _refresh_mahasiswa(self):
        data = self.__mhs_model.ambil_semua()
        self.__frames["mahasiswa"].muat_data(data)

    # ============================================================
    # CRUD MATA KULIAH
    # ============================================================
    def simpan_mata_kuliah(self, kode_mk, nama_mk, sks, semester):
        try:
            self.__mk_model.tambah(kode_mk, nama_mk, sks, semester)
            messagebox.showinfo("✅ Sukses",
                                f"Mata Kuliah '{nama_mk}' berhasil ditambahkan!")
            self._refresh_mata_kuliah()
        except Exception as e:
            messagebox.showerror("❌ Gagal", str(e))

    def perbarui_mata_kuliah(self, kode_lama, kode_mk, nama_mk, sks, semester):
        try:
            self.__mk_model.perbarui(kode_lama, kode_mk, nama_mk, sks, semester)
            messagebox.showinfo("✅ Sukses",
                                "Data mata kuliah berhasil diperbarui!")
            self._refresh_mata_kuliah()
        except Exception as e:
            messagebox.showerror("❌ Gagal", str(e))

    def hapus_mata_kuliah(self, kode_mk):
        try:
            self.__mk_model.hapus(kode_mk)
            messagebox.showinfo("✅ Sukses",
                                "Mata kuliah berhasil dihapus!")
            self._refresh_mata_kuliah()
        except Exception as e:
            messagebox.showerror("❌ Gagal", str(e))

    def _refresh_mata_kuliah(self):
        data = self.__mk_model.ambil_semua()
        self.__frames["mata_kuliah"].muat_data(data)

    # ============================================================
    # CRUD KRS
    # ============================================================
    def daftar_krs(self, nim, kode_mk, tahun_ajaran):
        try:
            self.__krs_model.daftar_mk(nim, kode_mk, tahun_ajaran)
            messagebox.showinfo("✅ Sukses",
                                "Mata kuliah berhasil didaftarkan!")
            self._refresh_krs()
        except Exception as e:
            messagebox.showerror("❌ Gagal", str(e))

    def hapus_krs(self, id_krs):
        try:
            self.__krs_model.hapus(id_krs)
            messagebox.showinfo("✅ Sukses",
                                "Pendaftaran dibatalkan!")
            self._refresh_krs()
        except Exception as e:
            messagebox.showerror("❌ Gagal", str(e))

    def _refresh_krs(self):
        mhs = self.__mhs_model.ambil_semua()
        mk = self.__mk_model.ambil_semua()
        daftar_nim = [f"{r['nim']} - {r['nama']}" for r in mhs]
        daftar_mk = [f"{r['kode_mk']} - {r['nama_mk']}" for r in mk]
        self.__frames["krs"].isi_combobox(daftar_nim, daftar_mk)

        # Ambil data KRS dengan SKS (dari JOIN)
        data = self.__krs_model.ambil_semua()
        formatted = [
            (r['id'], r['nim'], r['nama'], r['kode_mk'],
             r['nama_mk'], r['sks'], r['tahun_ajaran'])
            for r in data
        ]
        self.__frames["krs"].muat_data(formatted)

    # ============================================================
    # KHS
    # ============================================================
    def _siapkan_khs(self):
        mhs = [f"{r['nim']} - {r['nama']}"
               for r in self.__mhs_model.ambil_semua()]
        ta = self.__krs_model.ambil_semua_tahun_ajaran()
        self.__frames["khs"].isi_combobox(mhs, ta)

    def tampilkan_khs(self, nim, tahun_ajaran):
        data_raw = self.__krs_model.ambil_krs_mahasiswa(nim, tahun_ajaran)
        data_khs = []
        for row in data_raw:
            huruf, bobot = self.__khs_model.konversi_nilai(row['nilai'])
            data_khs.append({
                'id': row['id'],
                'kode_mk': row['kode_mk'],
                'nama_mk': row['nama_mk'],
                'sks': row['sks'],
                'nilai': row['nilai'],
                'nilai_huruf': huruf,
                'bobot': bobot
            })
        ipk, total_sks = self.__khs_model.hitung_ipk(data_khs)
        self.__frames["khs"].muat_data_khs(data_khs, ipk, total_sks)

    def update_nilai_krs(self, id_krs, nilai):
        try:
            self.__krs_model.update_nilai(id_krs, nilai)
            messagebox.showinfo("✅ Sukses", "Nilai berhasil disimpan!")
        except Exception as e:
            messagebox.showerror("❌ Gagal", str(e))

    # ============================================================
    # DASHBOARD & UTILITIES
    # ============================================================
    def _refresh_dashboard(self):
        jml_mhs = self.__mhs_model.hitung()
        jml_mk = self.__mk_model.hitung()
        jml_krs = self.__krs_model.hitung()
        self.__frames["dashboard"].perbarui_statistik(jml_mhs, jml_mk, jml_krs)

    def _tentang(self):
        messagebox.showinfo(
            "ℹ️ Tentang Aplikasi",
            "SIAKAD Mini v2.0\n\n"
            "Sistem Informasi Akademik Mini\n"
            "Python + Tkinter + SQLite\n"
            "Arsitektur: Strict MVC + OOP\n\n"
            "Fitur:\n"
            "• Autentikasi User (Login/Logout)\n"
            "• CRUD Mahasiswa\n"
            "• CRUD Mata Kuliah\n"
            "• KRS (Pendaftaran Mata Kuliah)\n"
            "• KHS (Nilai, Konversi Huruf, IPK)\n"
            "• Frame Switching Navigation\n"
            "• Exception Handling\n\n"
            "Nama Anggota Kelompok:\n"
            "1. Muhammad Syifa Prasetyo\n"
            "2. Tari Puspita\n"
            "3. Rifa Wulandari\n\n"
            "© 2025 — Proyek Akhir PBO"
        )

    def _on_closing(self):
        if messagebox.askyesno("Konfirmasi",
                               "Yakin ingin menutup aplikasi?"):
            self.__db.close()
            self.destroy()


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    app = AppController()
    app.mainloop()