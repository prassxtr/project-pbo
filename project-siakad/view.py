# ============================================================
# view.py - Lapisan Antarmuka (View)
# SIAKAD Mini - Sistem Informasi Akademik
# Tugas: HANYA berisi komponen visual Tkinter
# DILARANG berisi sqlite3 atau logika bisnis
# Menerapkan INHERITANCE: semua frame mewarisi BaseFrame
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
# KONSTANTA TEMA (DRY: satu tempat untuk semua warna/font)
# ============================================================
class Tema:
    BG_DARK = "#1a1a2e"
    BG_SIDEBAR = "#16213e"
    BG_MAIN = "#f8f9fa"
    BG_CARD = "#ffffff"
    ACCENT = "#0f3460"
    ACCENT_LIGHT = "#533483"
    SUCCESS = "#27ae60"
    WARNING = "#f39c12"
    DANGER = "#e74c3c"
    INFO = "#3498db"
    TEXT_DARK = "#2c3e50"
    TEXT_LIGHT = "#ecf0f1"
    TEXT_MUTED = "#7f8c8d"
    BORDER = "#dee2e6"
    FONT_TITLE = ("Segoe UI", 18, "bold")
    FONT_SUBTITLE = ("Segoe UI", 12)
    FONT_BODY = ("Segoe UI", 11)
    FONT_SMALL = ("Segoe UI", 10)
    FONT_BUTTON = ("Segoe UI", 10, "bold")


# ============================================================
# BASE FRAME (INHERITANCE: parent class untuk semua halaman)
# ============================================================
class BaseFrame(tk.Frame):
    """Kelas dasar semua halaman. Menerapkan Inheritance."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=Tema.BG_MAIN)

    def buat_header(self, judul, subjudul=""):
        """Header halaman dengan gradient-style (DRY)."""
        header = tk.Frame(self, bg=Tema.ACCENT, pady=18, padx=25)
        header.pack(fill=tk.X)

        tk.Label(header, text=judul, font=Tema.FONT_TITLE,
                 bg=Tema.ACCENT, fg=Tema.TEXT_LIGHT).pack(anchor="w")
        if subjudul:
            tk.Label(header, text=subjudul, font=Tema.FONT_SMALL,
                     bg=Tema.ACCENT, fg="#a8d8ea").pack(anchor="w", pady=(4, 0))

    def buat_card(self, parent_frame, title=""):
        """Membuat card container dengan shadow effect (REVISI - konsisten grid)."""
        outer = tk.Frame(parent_frame, bg=Tema.BORDER, padx=1, pady=1)
        outer.pack(fill=tk.X, padx=25, pady=(15, 5))

        card = tk.Frame(outer, bg=Tema.BG_CARD, padx=20, pady=15)
        card.pack(fill=tk.X)
        
        # Setup grid configuration untuk card
        card.grid_columnconfigure(1, weight=1)

        if title:
            # Gunakan grid untuk title juga agar konsisten
            tk.Label(card, text=title, font=("Segoe UI", 11, "bold"),
                    bg=Tema.BG_CARD, fg=Tema.ACCENT).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
            # Return card dengan row offset sudah di-set
            card._current_row = 2
        else:
            card._current_row = 0

        return card

    def buat_tombol(self, parent_frame, teks, warna, command):
        """Tombol berwarna konsisten (DRY + POLYMORPHISM)."""
        btn = tk.Button(
            parent_frame, text=teks, font=Tema.FONT_BUTTON,
            bg=warna, fg="white", activebackground=warna,
            activeforeground="white", relief="flat", cursor="hand2",
            padx=14, pady=6, command=command
        )
        btn.pack(side=tk.LEFT, padx=4)
        # Hover effect
        btn.bind("<Enter>", lambda e, b=btn, c=warna: b.config(bg=self._darken(c)))
        btn.bind("<Leave>", lambda e, b=btn, c=warna: b.config(bg=c))
        return btn

    def _darken(self, hex_color):
        """Gelapkan warna untuk hover effect."""
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r, g, b = max(0, r - 30), max(0, g - 30), max(0, b - 30)
        return f"#{r:02x}{g:02x}{b:02x}"

    def buat_entry(self, parent_frame, label_text, row, default=""):
        """Entry field dengan label (auto-increment row)."""
        tk.Label(parent_frame, text=label_text, font=Tema.FONT_SMALL,
                bg=Tema.BG_CARD, fg=Tema.TEXT_DARK, width=14, anchor="w"
                ).grid(row=row, column=0, padx=(0, 10), pady=6, sticky="w")
        ent = tk.Entry(parent_frame, font=Tema.FONT_BODY, width=32,
                relief="solid", bd=1)
        ent.grid(row=row, column=1, padx=5, pady=6, sticky="ew")
        if default:
            ent.insert(0, default)
        return ent


# ============================================================
# HALAMAN DASHBOARD
# ============================================================
class DashboardFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.buat_header("📊  Dashboard", "Sistem Informasi Akademik Mini")

        # Container untuk 3 kartu statistik
        self.frame_cards = tk.Frame(self, bg=Tema.BG_MAIN)
        self.frame_cards.pack(fill=tk.X, padx=25, pady=25)
        self.frame_cards.grid_columnconfigure((0, 1, 2), weight=1)

        self.card_mhs = self._buat_stat_card(self.frame_cards, 0, "👥", "Mahasiswa", Tema.INFO)
        self.card_mk = self._buat_stat_card(self.frame_cards, 1, "📚", "Mata Kuliah", Tema.ACCENT_LIGHT)
        self.card_krs = self._buat_stat_card(self.frame_cards, 2, "📝", "Entri KRS", Tema.SUCCESS)

        # Welcome text
        welcome_frame = tk.Frame(self, bg=Tema.BG_MAIN)
        welcome_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

        tk.Label(welcome_frame,
                 text="Selamat datang di SIAKAD Mini!\n"
                      "Gunakan menu 'Navigasi' di atas untuk mengelola data.",
                 font=Tema.FONT_SUBTITLE, bg=Tema.BG_MAIN,
                 fg=Tema.TEXT_MUTED, justify="center").pack(pady=30)

    def _buat_stat_card(self, parent, col, icon, label, warna):
        """Membuat satu kartu statistik."""
        outer = tk.Frame(parent, bg=Tema.BORDER, padx=1, pady=1)
        outer.grid(row=0, column=col, padx=8, pady=5, sticky="nsew")

        card = tk.Frame(outer, bg=Tema.BG_CARD, padx=20, pady=20)
        card.pack(fill=tk.BOTH, expand=True)

        tk.Label(card, text=icon, font=("Segoe UI", 32),
                 bg=Tema.BG_CARD).pack()
        lbl_count = tk.Label(card, text="0", font=("Segoe UI", 28, "bold"),
                             bg=Tema.BG_CARD, fg=warna)
        lbl_count.pack(pady=(5, 2))
        tk.Label(card, text=label, font=Tema.FONT_SMALL,
                 bg=Tema.BG_CARD, fg=Tema.TEXT_MUTED).pack()
        return lbl_count

    def perbarui_statistik(self, jml_mhs, jml_mk, jml_krs):
        self.card_mhs.config(text=str(jml_mhs))
        self.card_mk.config(text=str(jml_mk))
        self.card_krs.config(text=str(jml_krs))


# ============================================================
# HALAMAN MAHASISWA (CRUD)
# ============================================================
class MahasiswaFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.buat_header("👥  Data Mahasiswa", "Kelola data mahasiswa aktif")
        self.__editing_nim = None

        # Form Card
        card = self.buat_card(self, "Form Input")
        card.grid_columnconfigure(1, weight=1)

        self.ent_nim = self.buat_entry(card, "NIM", 0)
        self.ent_nama = self.buat_entry(card, "Nama Lengkap", 1)
        self.ent_jurusan = self.buat_entry(card, "Jurusan", 2)
        self.ent_angkatan = self.buat_entry(card, "Angkatan", 3)

        # Tombol
        frm_btn = tk.Frame(card, bg=Tema.BG_CARD)
        frm_btn.grid(row=4, column=0, columnspan=2, pady=(15, 0))
        self.buat_tombol(frm_btn, "💾  Simpan", Tema.SUCCESS, self._aksi_simpan)
        self.buat_tombol(frm_btn, "✏️  Update", Tema.INFO, self._aksi_update)
        self.buat_tombol(frm_btn, "🗑️  Hapus", Tema.DANGER, self._aksi_hapus)
        self.buat_tombol(frm_btn, "🔄  Reset", Tema.TEXT_MUTED, self._aksi_reset)

        # Tabel
        self._buat_tabel()

    def _buat_tabel(self):
        frm_tree = tk.Frame(self, bg=Tema.BG_MAIN)
        frm_tree.pack(fill=tk.BOTH, expand=True, padx=25, pady=(10, 15))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=Tema.FONT_SMALL, rowheight=30,
                        background=Tema.BG_CARD, fieldbackground=Tema.BG_CARD)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background=Tema.ACCENT, foreground="white")
        style.map("Treeview", background=[("selected", Tema.INFO)])

        self.tree = ttk.Treeview(frm_tree,
                                columns=("nim", "nama", "jurusan", "angkatan"),
                                show="headings", height=8)
        for col, w, anc in [("nim", 110, "w"), ("nama", 220, "w"),
                            ("jurusan", 160, "w"), ("angkatan", 90, "center")]:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=w, anchor=anc)

        scrollbar = ttk.Scrollbar(frm_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _aksi_simpan(self):
        try:
            self.controller.simpan_mahasiswa(
                nim=self.ent_nim.get(),
                nama=self.ent_nama.get(),
                jurusan=self.ent_jurusan.get(),
                angkatan=self.ent_angkatan.get()
            )
            self._aksi_reset()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _aksi_update(self):
        if not self.__editing_nim:
            messagebox.showwarning("Peringatan", "Pilih data di tabel terlebih dahulu!")
            return
        try:
            self.controller.perbarui_mahasiswa(
                nim_lama=self.__editing_nim,
                nim=self.ent_nim.get(),
                nama=self.ent_nama.get(),
                jurusan=self.ent_jurusan.get(),
                angkatan=self.ent_angkatan.get()
            )
            self._aksi_reset()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _aksi_hapus(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus!")
            return
        nim = self.tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Konfirmasi Hapus", f"Hapus mahasiswa NIM {nim}?\n(Semua data KRS terkait juga akan dihapus)"):
            self.controller.hapus_mahasiswa(nim)

    def _aksi_reset(self):
        self.ent_nim.config(state="normal")
        for ent in [self.ent_nim, self.ent_nama, self.ent_jurusan, self.ent_angkatan]:
            ent.delete(0, tk.END)
        self.__editing_nim = None
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)

    def _on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        self.ent_nim.config(state="normal")
        self.ent_nim.delete(0, tk.END)
        self.ent_nim.insert(0, vals[0])
        self.ent_nim.config(state="disabled")
        self.ent_nama.delete(0, tk.END)
        self.ent_nama.insert(0, vals[1])
        self.ent_jurusan.delete(0, tk.END)
        self.ent_jurusan.insert(0, vals[2])
        self.ent_angkatan.delete(0, tk.END)
        self.ent_angkatan.insert(0, vals[3])
        self.__editing_nim = vals[0]

    def muat_data(self, data):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in data:
            self.tree.insert("", tk.END, values=tuple(row))


# ============================================================
# HALAMAN MATA KULIAH (CRUD)
# ============================================================
class MataKuliahFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.buat_header("📚  Data Mata Kuliah", "Kelola katalog mata kuliah")
        self.__editing_kode = None

        card = self.buat_card(self, "Form Input")
        card.grid_columnconfigure(1, weight=1)

        self.ent_kode = self.buat_entry(card, "Kode MK", 0)
        self.ent_nama = self.buat_entry(card, "Nama MK", 1)
        self.ent_sks = self.buat_entry(card, "SKS (1-6)", 2)
        self.ent_semester = self.buat_entry(card, "Semester (1-8)", 3)

        frm_btn = tk.Frame(card, bg=Tema.BG_CARD)
        frm_btn.grid(row=4, column=0, columnspan=2, pady=(15, 0))
        self.buat_tombol(frm_btn, "💾  Simpan", Tema.SUCCESS, self._aksi_simpan)
        self.buat_tombol(frm_btn, "✏️  Update", Tema.INFO, self._aksi_update)
        self.buat_tombol(frm_btn, "🗑️  Hapus", Tema.DANGER, self._aksi_hapus)
        self.buat_tombol(frm_btn, "🔄  Reset", Tema.TEXT_MUTED, self._aksi_reset)

        self._buat_tabel()

    def _buat_tabel(self):
        frm_tree = tk.Frame(self, bg=Tema.BG_MAIN)
        frm_tree.pack(fill=tk.BOTH, expand=True, padx=25, pady=(10, 15))

        self.tree = ttk.Treeview(frm_tree,
                                  columns=("kode_mk", "nama_mk", "sks", "semester"),
                                  show="headings", height=8)
        for col, w, anc in [("kode_mk", 100, "w"), ("nama_mk", 280, "w"),
                             ("sks", 70, "center"), ("semester", 100, "center")]:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=w, anchor=anc)

        scrollbar = ttk.Scrollbar(frm_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _aksi_simpan(self):
        try:
            self.controller.simpan_mata_kuliah(
                kode_mk=self.ent_kode.get(),
                nama_mk=self.ent_nama.get(),
                sks=self.ent_sks.get(),
                semester=self.ent_semester.get()
            )
            self._aksi_reset()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _aksi_update(self):
        if not self.__editing_kode:
            messagebox.showwarning("Peringatan", "Pilih data di tabel terlebih dahulu!")
            return
        try:
            self.controller.perbarui_mata_kuliah(
                kode_lama=self.__editing_kode,
                kode_mk=self.ent_kode.get(),
                nama_mk=self.ent_nama.get(),
                sks=self.ent_sks.get(),
                semester=self.ent_semester.get()
            )
            self._aksi_reset()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _aksi_hapus(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus!")
            return
        kode = self.tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Konfirmasi Hapus", f"Hapus Mata Kuliah {kode}?"):
            self.controller.hapus_mata_kuliah(kode)

    def _aksi_reset(self):
        self.ent_kode.config(state="normal")
        for ent in [self.ent_kode, self.ent_nama, self.ent_sks, self.ent_semester]:
            ent.delete(0, tk.END)
        self.__editing_kode = None
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)

    def _on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        self.ent_kode.config(state="normal")
        self.ent_kode.delete(0, tk.END)
        self.ent_kode.insert(0, vals[0])
        self.ent_kode.config(state="disabled")
        self.ent_nama.delete(0, tk.END)
        self.ent_nama.insert(0, vals[1])
        self.ent_sks.delete(0, tk.END)
        self.ent_sks.insert(0, vals[2])
        self.ent_semester.delete(0, tk.END)
        self.ent_semester.insert(0, vals[3])
        self.__editing_kode = vals[0]

    def muat_data(self, data):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in data:
            self.tree.insert("", tk.END, values=tuple(row))


# ============================================================
# HALAMAN KRS (CRUD)
# ============================================================
class KRSFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.buat_header("📝  KRS / Transkrip Nilai", "Pengisian dan pengelolaan nilai mahasiswa")
        self.__editing_id = None

        # Form container - gunakan grid yang konsisten
        frm_form = tk.Frame(self, bg=Tema.BG_CARD, padx=20, pady=15)
        frm_form.pack(fill=tk.X, padx=25, pady=15)
        frm_form.grid_columnconfigure(1, weight=1)  # Kolom 1 expand

        # Judul form
        tk.Label(frm_form, text="Form Input KRS", font=("Segoe UI", 11, "bold"),
                 bg=Tema.BG_CARD, fg=Tema.ACCENT).grid(row=0, column=0, 
                                                        columnspan=2, 
                                                        sticky="w", 
                                                        pady=(0, 10))
        ttk.Separator(frm_form, orient="horizontal").grid(row=1, column=0, 
                                                           columnspan=2, 
                                                           sticky="ew", 
                                                           pady=(0, 10))

        # NIM Combobox
        tk.Label(frm_form, text="Mahasiswa", font=Tema.FONT_SMALL,
                 bg=Tema.BG_CARD, fg=Tema.TEXT_DARK, width=14, anchor="w"
                 ).grid(row=2, column=0, padx=(0, 10), pady=6, sticky="w")
        self.cbo_nim = ttk.Combobox(frm_form, state="readonly", font=Tema.FONT_SMALL)
        self.cbo_nim.grid(row=2, column=1, padx=5, pady=6, sticky="ew")

        # MK Combobox
        tk.Label(frm_form, text="Mata Kuliah", font=Tema.FONT_SMALL,
                 bg=Tema.BG_CARD, fg=Tema.TEXT_DARK, width=14, anchor="w"
                 ).grid(row=3, column=0, padx=(0, 10), pady=6, sticky="w")
        self.cbo_mk = ttk.Combobox(frm_form, state="readonly", font=Tema.FONT_SMALL)
        self.cbo_mk.grid(row=3, column=1, padx=5, pady=6, sticky="ew")

        # Nilai
        tk.Label(frm_form, text="Nilai (0-100)", font=Tema.FONT_SMALL,
                 bg=Tema.BG_CARD, fg=Tema.TEXT_DARK, width=14, anchor="w"
                 ).grid(row=4, column=0, padx=(0, 10), pady=6, sticky="w")
        self.ent_nilai = tk.Entry(frm_form, font=Tema.FONT_BODY, width=32,
                                   relief="solid", bd=1, highlightthickness=2,
                                   highlightcolor=Tema.INFO, highlightbackground=Tema.BORDER)
        self.ent_nilai.grid(row=4, column=1, padx=5, pady=6, sticky="ew")

        # Tahun Ajaran
        tk.Label(frm_form, text="Tahun Ajaran", font=Tema.FONT_SMALL,
                 bg=Tema.BG_CARD, fg=Tema.TEXT_DARK, width=14, anchor="w"
                 ).grid(row=5, column=0, padx=(0, 10), pady=6, sticky="w")
        self.ent_ta = tk.Entry(frm_form, font=Tema.FONT_BODY, width=32,
                                relief="solid", bd=1, highlightthickness=2,
                                highlightcolor=Tema.INFO, highlightbackground=Tema.BORDER)
        self.ent_ta.insert(0, "2025/2026")
        self.ent_ta.grid(row=5, column=1, padx=5, pady=6, sticky="ew")

        # Tombol
        frm_btn = tk.Frame(frm_form, bg=Tema.BG_CARD)
        frm_btn.grid(row=6, column=0, columnspan=2, pady=(15, 0))
        self.buat_tombol(frm_btn, "💾  Simpan", Tema.SUCCESS, self._aksi_simpan)
        self.buat_tombol(frm_btn, "✏️  Update", Tema.INFO, self._aksi_update)
        self.buat_tombol(frm_btn, "🗑️  Hapus", Tema.DANGER, self._aksi_hapus)
        self.buat_tombol(frm_btn, "🔄  Reset", Tema.TEXT_MUTED, self._aksi_reset)

        # Tabel
        self._buat_tabel()

    def _buat_tabel(self):
        frm_tree = tk.Frame(self, bg=Tema.BG_MAIN)
        frm_tree.pack(fill=tk.BOTH, expand=True, padx=25, pady=(10, 15))

        self.tree = ttk.Treeview(frm_tree,
                                  columns=("id", "nim", "nama", "kode_mk", "nama_mk", "nilai", "ta"),
                                  show="headings", height=7)
        cols = [("id", 35, "center"), ("nim", 90, "w"), ("nama", 140, "w"),
                ("kode_mk", 75, "w"), ("nama_mk", 170, "w"), ("nilai", 55, "center"), ("ta", 95, "center")]
        for col, w, anc in cols:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=w, anchor=anc)

        scrollbar = ttk.Scrollbar(frm_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def isi_combobox(self, daftar_nim, daftar_mk):
        self.cbo_nim["values"] = daftar_nim
        self.cbo_mk["values"] = daftar_mk

    def _aksi_simpan(self):
        try:
            nim_val = self.cbo_nim.get().split(" - ")[0] if self.cbo_nim.get() else ""
            mk_val = self.cbo_mk.get().split(" - ")[0] if self.cbo_mk.get() else ""
            self.controller.simpan_krs(
                nim=nim_val, kode_mk=mk_val,
                nilai=self.ent_nilai.get(), tahun_ajaran=self.ent_ta.get()
            )
            self._aksi_reset()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _aksi_update(self):
        if not self.__editing_id:
            messagebox.showwarning("Peringatan", "Pilih data di tabel terlebih dahulu!")
            return
        try:
            nim_val = self.cbo_nim.get().split(" - ")[0] if self.cbo_nim.get() else ""
            mk_val = self.cbo_mk.get().split(" - ")[0] if self.cbo_mk.get() else ""
            self.controller.perbarui_krs(
                id_krs=self.__editing_id, nim=nim_val, kode_mk=mk_val,
                nilai=self.ent_nilai.get(), tahun_ajaran=self.ent_ta.get()
            )
            self._aksi_reset()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _aksi_hapus(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus!")
            return
        id_krs = self.tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Konfirmasi Hapus", "Hapus entri KRS ini?"):
            self.controller.hapus_krs(id_krs)

    def _aksi_reset(self):
        self.cbo_nim.set("")
        self.cbo_mk.set("")
        self.ent_nilai.delete(0, tk.END)
        self.ent_ta.delete(0, tk.END)
        self.ent_ta.insert(0, "2025/2026")
        self.__editing_id = None
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)

    def _on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        self.__editing_id = vals[0]
        self.cbo_nim.set(f"{vals[1]} - {vals[2]}")
        self.cbo_mk.set(f"{vals[3]} - {vals[4]}")
        self.ent_nilai.delete(0, tk.END)
        self.ent_nilai.insert(0, vals[5])
        self.ent_ta.delete(0, tk.END)
        self.ent_ta.insert(0, vals[6])

    def muat_data(self, data):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in data:
            self.tree.insert("", tk.END, values=tuple(row))