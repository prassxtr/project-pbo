# ============================================================
# view.py - Lapisan Antarmuka (View)
# SIAKAD Mini - Sistem Informasi Akademik
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
# TEMA (MERAH MAROON)
# ============================================================
class Tema:
    BG_DARK = "#2d0a0a"
    BG_SIDEBAR = "#3d0c0c"
    BG_MAIN = "#f8f9fa"
    BG_CARD = "#ffffff"
    ACCENT = "#8b0000"
    ACCENT_LIGHT = "#a52a2a"
    SUCCESS = "#27ae60"
    WARNING = "#f39c12"
    DANGER = "#c0392b"
    INFO = "#8b0000"
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
# LOGIN FRAME
# ============================================================
class LoginFrame(tk.Frame):
    """Frame untuk login user."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=Tema.BG_DARK)
        self.controller = controller

        container = tk.Frame(self, bg=Tema.BG_CARD, padx=50, pady=50)
        container.place(relx=0.5, rely=0.5, anchor="center", width=420)

        tk.Label(container, text="🎓", font=("Segoe UI", 56),
                 bg=Tema.BG_CARD).pack(pady=(0, 10))
        tk.Label(container, text="SIAKAD Mini",
                 font=("Segoe UI", 26, "bold"),
                 bg=Tema.BG_CARD, fg=Tema.ACCENT).pack(pady=(0, 5))
        tk.Label(container, text="Sistem Informasi Akademik",
                 font=Tema.FONT_SMALL,
                 bg=Tema.BG_CARD, fg=Tema.TEXT_MUTED).pack(pady=(0, 30))

        form_frame = tk.Frame(container, bg=Tema.BG_CARD)
        form_frame.pack(fill=tk.X)

        tk.Label(form_frame, text="Username", font=Tema.FONT_BODY,
                 bg=Tema.BG_CARD, fg=Tema.TEXT_DARK, anchor="w").pack(fill=tk.X, pady=(0, 5))
        self.ent_username = tk.Entry(form_frame, font=Tema.FONT_BODY,
                                      relief="solid", bd=1)
        self.ent_username.pack(fill=tk.X, pady=(0, 15))
        self.ent_username.bind("<Return>", lambda e: self._do_login())

        tk.Label(form_frame, text="Password", font=Tema.FONT_BODY,
                 bg=Tema.BG_CARD, fg=Tema.TEXT_DARK, anchor="w").pack(fill=tk.X, pady=(0, 5))
        self.ent_password = tk.Entry(form_frame, font=Tema.FONT_BODY,
                                      show="•", relief="solid", bd=1)
        self.ent_password.pack(fill=tk.X, pady=(0, 20))
        self.ent_password.bind("<Return>", lambda e: self._do_login())

        btn_login = tk.Button(form_frame, text="🔐 Login", font=Tema.FONT_BUTTON,
                              bg=Tema.ACCENT, fg="white", relief="flat",
                              cursor="hand2", padx=20, pady=12,
                              command=self._do_login)
        btn_login.pack(fill=tk.X)
        btn_login.bind("<Enter>", lambda e: btn_login.config(bg=Tema.ACCENT_LIGHT))
        btn_login.bind("<Leave>", lambda e: btn_login.config(bg=Tema.ACCENT))

        tk.Label(container, text="\nDefault Login:\nUsername: admin | Password: admin123",
                 font=("Segoe UI", 8),
                 bg=Tema.BG_CARD, fg=Tema.TEXT_MUTED).pack(pady=(20, 0))

        tk.Label(self, text="© 2025 SIAKAD Mini - PBO Project",
                 font=("Segoe UI", 9),
                 bg=Tema.BG_DARK, fg=Tema.TEXT_MUTED).place(relx=0.5, rely=0.95, anchor="center")

    def _do_login(self):
        self.controller.proses_login(self.ent_username.get(), self.ent_password.get())

    def clear_form(self):
        self.ent_username.delete(0, tk.END)
        self.ent_password.delete(0, tk.END)
        self.ent_username.focus()


# ============================================================
# BASE FRAME (INHERITANCE)
# ============================================================
class BaseFrame(tk.Frame):
    """Kelas dasar semua halaman."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=Tema.BG_MAIN)

    def buat_header(self, judul, subjudul=""):
        header = tk.Frame(self, bg=Tema.ACCENT, pady=18, padx=25)
        header.pack(fill=tk.X)
        tk.Label(header, text=judul, font=Tema.FONT_TITLE,
                 bg=Tema.ACCENT, fg=Tema.TEXT_LIGHT).pack(anchor="w")
        if subjudul:
            tk.Label(header, text=subjudul, font=Tema.FONT_SMALL,
                     bg=Tema.ACCENT, fg="#f5c6cb").pack(anchor="w", pady=(4, 0))

    def buat_card(self, parent_frame, title=""):
        outer = tk.Frame(parent_frame, bg=Tema.BORDER, padx=1, pady=1)
        outer.pack(fill=tk.X, padx=25, pady=(15, 5))
        card = tk.Frame(outer, bg=Tema.BG_CARD, padx=20, pady=15)
        card.pack(fill=tk.X)
        card.grid_columnconfigure(1, weight=1)
        if title:
            tk.Label(card, text=title, font=("Segoe UI", 11, "bold"),
                     bg=Tema.BG_CARD, fg=Tema.ACCENT).grid(row=0, column=0,
                     columnspan=2, sticky="w", pady=(0, 10))
        return card

    def buat_tombol(self, parent_frame, teks, warna, command):
        btn = tk.Button(parent_frame, text=teks, font=Tema.FONT_BUTTON,
                        bg=warna, fg="white", relief="flat", cursor="hand2",
                        padx=14, pady=6, command=command)
        btn.pack(side=tk.LEFT, padx=4)
        return btn

    def buat_entry(self, parent_frame, label_text, row, default=""):
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
# DASHBOARD
# ============================================================
class DashboardFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.buat_header(" Dashboard", "Sistem Informasi Akademik Mini")

        self.frame_cards = tk.Frame(self, bg=Tema.BG_MAIN)
        self.frame_cards.pack(fill=tk.X, padx=25, pady=25)
        self.frame_cards.grid_columnconfigure((0, 1, 2), weight=1)

        self.card_mhs = self._buat_stat_card(self.frame_cards, 0, "👥", "Mahasiswa", Tema.ACCENT)
        self.card_mk = self._buat_stat_card(self.frame_cards, 1, "📚", "Mata Kuliah", Tema.ACCENT_LIGHT)
        self.card_krs = self._buat_stat_card(self.frame_cards, 2, "📝", "Entri KRS", Tema.SUCCESS)

    def _buat_stat_card(self, parent, col, icon, label, warna):
        outer = tk.Frame(parent, bg=Tema.BORDER, padx=1, pady=1)
        outer.grid(row=0, column=col, padx=8, pady=5, sticky="nsew")
        card = tk.Frame(outer, bg=Tema.BG_CARD, padx=20, pady=20)
        card.pack(fill=tk.BOTH, expand=True)
        tk.Label(card, text=icon, font=("Segoe UI", 32), bg=Tema.BG_CARD).pack()
        lbl = tk.Label(card, text="0", font=("Segoe UI", 28, "bold"),
                       bg=Tema.BG_CARD, fg=warna)
        lbl.pack(pady=(5, 2))
        tk.Label(card, text=label, font=Tema.FONT_SMALL,
                 bg=Tema.BG_CARD, fg=Tema.TEXT_MUTED).pack()
        return lbl

    def perbarui_statistik(self, mhs, mk, krs):
        self.card_mhs.config(text=str(mhs))
        self.card_mk.config(text=str(mk))
        self.card_krs.config(text=str(krs))


# ============================================================
# MAHASISWA
# ============================================================
class MahasiswaFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.buat_header("👥 Data Mahasiswa", "Kelola data mahasiswa")
        self.__editing_nim = None

        card = self.buat_card(self, "Form Input")
        self.ent_nim = self.buat_entry(card, "NIM", 0)
        self.ent_nama = self.buat_entry(card, "Nama", 1)
        self.ent_jurusan = self.buat_entry(card, "Jurusan", 2)
        self.ent_angkatan = self.buat_entry(card, "Angkatan", 3)

        frm_btn = tk.Frame(card, bg=Tema.BG_CARD)
        frm_btn.grid(row=4, column=0, columnspan=2, pady=(15, 0))
        self.buat_tombol(frm_btn, "💾 Simpan", Tema.SUCCESS, self._simpan)
        self.buat_tombol(frm_btn, "✏️ Update", Tema.ACCENT, self._update)
        self.buat_tombol(frm_btn, "🗑️ Hapus", Tema.DANGER, self._hapus)
        self.buat_tombol(frm_btn, "🔄 Reset", Tema.TEXT_MUTED, self._reset)
        self._buat_tabel()

    def _buat_tabel(self):
        frm = tk.Frame(self, bg=Tema.BG_MAIN)
        frm.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)
        self.tree = ttk.Treeview(frm, columns=("nim", "nama", "jurusan", "angkatan"),
                                  show="headings", height=8)
        for col, w in [("nim", 100), ("nama", 200), ("jurusan", 150), ("angkatan", 80)]:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=w)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _simpan(self):
        try:
            self.controller.simpan_mahasiswa(self.ent_nim.get(), self.ent_nama.get(),
                                              self.ent_jurusan.get(), self.ent_angkatan.get())
            self._reset()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _update(self):
        if not self.__editing_nim:
            messagebox.showwarning("Peringatan", "Pilih data dulu!"); return
        try:
            self.controller.perbarui_mahasiswa(self.__editing_nim, self.ent_nim.get(),
                                                self.ent_nama.get(), self.ent_jurusan.get(),
                                                self.ent_angkatan.get())
            self._reset()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _hapus(self):
        sel = self.tree.selection()
        if not sel: return
        nim = self.tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Konfirmasi", f"Hapus NIM {nim}?"):
            self.controller.hapus_mahasiswa(nim)

    def _reset(self):
        for ent in [self.ent_nim, self.ent_nama, self.ent_jurusan, self.ent_angkatan]:
            ent.delete(0, tk.END)
        self.ent_nim.config(state="normal")
        self.__editing_nim = None

    def _on_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0])["values"]
        self.ent_nim.config(state="normal")
        self.ent_nim.delete(0, tk.END); self.ent_nim.insert(0, vals[0])
        self.ent_nim.config(state="disabled")
        self.ent_nama.delete(0, tk.END); self.ent_nama.insert(0, vals[1])
        self.ent_jurusan.delete(0, tk.END); self.ent_jurusan.insert(0, vals[2])
        self.ent_angkatan.delete(0, tk.END); self.ent_angkatan.insert(0, vals[3])
        self.__editing_nim = vals[0]

    def muat_data(self, data):
        for row in self.tree.get_children(): self.tree.delete(row)
        for row in data: self.tree.insert("", tk.END, values=tuple(row))


# ============================================================
# MATA KULIAH
# ============================================================
class MataKuliahFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.buat_header("📚 Mata Kuliah", "Kelola mata kuliah")
        self.__editing_kode = None

        card = self.buat_card(self, "Form Input")
        self.ent_kode = self.buat_entry(card, "Kode MK", 0)
        self.ent_nama = self.buat_entry(card, "Nama MK", 1)
        self.ent_sks = self.buat_entry(card, "SKS", 2)
        self.ent_semester = self.buat_entry(card, "Semester", 3)

        frm_btn = tk.Frame(card, bg=Tema.BG_CARD)
        frm_btn.grid(row=4, column=0, columnspan=2, pady=(15, 0))
        self.buat_tombol(frm_btn, "💾 Simpan", Tema.SUCCESS, self._simpan)
        self.buat_tombol(frm_btn, "✏️ Update", Tema.ACCENT, self._update)
        self.buat_tombol(frm_btn, "🗑️ Hapus", Tema.DANGER, self._hapus)
        self.buat_tombol(frm_btn, "🔄 Reset", Tema.TEXT_MUTED, self._reset)
        self._buat_tabel()

    def _buat_tabel(self):
        frm = tk.Frame(self, bg=Tema.BG_MAIN)
        frm.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)
        self.tree = ttk.Treeview(frm, columns=("kode_mk", "nama_mk", "sks", "semester"),
                                  show="headings", height=8)
        for col, w in [("kode_mk", 100), ("nama_mk", 250), ("sks", 50), ("semester", 80)]:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=w)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _simpan(self):
        try:
            self.controller.simpan_mata_kuliah(self.ent_kode.get(), self.ent_nama.get(),
                                                self.ent_sks.get(), self.ent_semester.get())
            self._reset()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _update(self):
        if not self.__editing_kode:
            messagebox.showwarning("Peringatan", "Pilih data dulu!"); return
        try:
            self.controller.perbarui_mata_kuliah(self.__editing_kode, self.ent_kode.get(),
                                                  self.ent_nama.get(), self.ent_sks.get(),
                                                  self.ent_semester.get())
            self._reset()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _hapus(self):
        sel = self.tree.selection()
        if not sel: return
        kode = self.tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Konfirmasi", f"Hapus MK {kode}?"):
            self.controller.hapus_mata_kuliah(kode)

    def _reset(self):
        for ent in [self.ent_kode, self.ent_nama, self.ent_sks, self.ent_semester]:
            ent.delete(0, tk.END)
        self.ent_kode.config(state="normal")
        self.__editing_kode = None

    def _on_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0])["values"]
        self.ent_kode.config(state="normal")
        self.ent_kode.delete(0, tk.END); self.ent_kode.insert(0, vals[0])
        self.ent_kode.config(state="disabled")
        self.ent_nama.delete(0, tk.END); self.ent_nama.insert(0, vals[1])
        self.ent_sks.delete(0, tk.END); self.ent_sks.insert(0, vals[2])
        self.ent_semester.delete(0, tk.END); self.ent_semester.insert(0, vals[3])
        self.__editing_kode = vals[0]

    def muat_data(self, data):
        for row in self.tree.get_children(): self.tree.delete(row)
        for row in data: self.tree.insert("", tk.END, values=tuple(row))


# ============================================================
# KRS (Kartu Rencana Studi)
# ============================================================
class KRSFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.buat_header("📝 KRS (Kartu Rencana Studi)", "Pendaftaran Mata Kuliah")

        card = self.buat_card(self, "Form Pendaftaran")
        tk.Label(card, text="Mahasiswa", font=Tema.FONT_SMALL,
                 bg=Tema.BG_CARD, width=14, anchor="w").grid(row=1, column=0,
                 padx=(0, 10), pady=6, sticky="w")
        self.cbo_nim = ttk.Combobox(card, state="readonly")
        self.cbo_nim.grid(row=1, column=1, padx=5, pady=6, sticky="ew")

        tk.Label(card, text="Mata Kuliah", font=Tema.FONT_SMALL,
                 bg=Tema.BG_CARD, width=14, anchor="w").grid(row=2, column=0,
                 padx=(0, 10), pady=6, sticky="w")
        self.cbo_mk = ttk.Combobox(card, state="readonly")
        self.cbo_mk.grid(row=2, column=1, padx=5, pady=6, sticky="ew")

        tk.Label(card, text="Tahun Ajaran", font=Tema.FONT_SMALL,
                 bg=Tema.BG_CARD, width=14, anchor="w").grid(row=3, column=0,
                 padx=(0, 10), pady=6, sticky="w")
        self.ent_ta = tk.Entry(card, relief="solid", bd=1)
        self.ent_ta.insert(0, "2025/2026")
        self.ent_ta.grid(row=3, column=1, padx=5, pady=6, sticky="ew")

        frm_btn = tk.Frame(card, bg=Tema.BG_CARD)
        frm_btn.grid(row=4, column=0, columnspan=2, pady=(15, 0))
        self.buat_tombol(frm_btn, "💾 Daftarkan", Tema.SUCCESS, self._simpan)
        self.buat_tombol(frm_btn, "🗑️ Batalkan", Tema.DANGER, self._hapus)
        self.buat_tombol(frm_btn, "🔄 Reset", Tema.TEXT_MUTED, self._reset)
        self._buat_tabel()

    def _buat_tabel(self):
        frm = tk.Frame(self, bg=Tema.BG_MAIN)
        frm.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)
        self.tree = ttk.Treeview(frm, columns=("id", "nim", "nama", "kode_mk", "nama_mk", "sks", "ta"),
                                  show="headings", height=8)
        for col, w in [("id", 30), ("nim", 80), ("nama", 120), ("kode_mk", 70),
                        ("nama_mk", 150), ("sks", 50), ("ta", 80)]:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=w)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def isi_combobox(self, nim, mk):
        self.cbo_nim["values"] = nim
        self.cbo_mk["values"] = mk

    def _simpan(self):
        try:
            n = self.cbo_nim.get().split(" - ")[0] if self.cbo_nim.get() else ""
            m = self.cbo_mk.get().split(" - ")[0] if self.cbo_mk.get() else ""
            self.controller.daftar_krs(n, m, self.ent_ta.get())
            self._reset()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _hapus(self):
        sel = self.tree.selection()
        if not sel: return
        id_krs = self.tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Konfirmasi", "Batalkan pendaftaran ini?"):
            self.controller.hapus_krs(id_krs)

    def _reset(self):
        self.cbo_nim.set(""); self.cbo_mk.set("")
        self.ent_ta.delete(0, tk.END); self.ent_ta.insert(0, "2025/2026")

    def muat_data(self, data):
        for row in self.tree.get_children(): self.tree.delete(row)
        for row in data: self.tree.insert("", tk.END, values=tuple(row))


# ============================================================
# KHS (Kartu Hasil Studi)
# ============================================================
class KHSFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.buat_header("🎓 KHS (Kartu Hasil Studi)", "Lihat Nilai & Hitung IPK")

        card_filter = self.buat_card(self, "Filter Data")
        tk.Label(card_filter, text="Mahasiswa", font=Tema.FONT_SMALL,
                 bg=Tema.BG_CARD, width=14, anchor="w").grid(row=1, column=0,
                 padx=(0, 10), pady=6, sticky="w")
        self.cbo_nim = ttk.Combobox(card_filter, state="readonly")
        self.cbo_nim.grid(row=1, column=1, padx=5, pady=6, sticky="ew")

        tk.Label(card_filter, text="Tahun Ajaran", font=Tema.FONT_SMALL,
                 bg=Tema.BG_CARD, width=14, anchor="w").grid(row=2, column=0,
                 padx=(0, 10), pady=6, sticky="w")
        self.cbo_ta = ttk.Combobox(card_filter, state="readonly")
        self.cbo_ta.grid(row=2, column=1, padx=5, pady=6, sticky="ew")

        frm_btn = tk.Frame(card_filter, bg=Tema.BG_CARD)
        frm_btn.grid(row=3, column=0, columnspan=2, pady=(15, 0))
        self.buat_tombol(frm_btn, "🔍 Tampilkan KHS", Tema.ACCENT, self._tampilkan)

        card_nilai = self.buat_card(self, "Input / Update Nilai")
        tk.Label(card_nilai, text="ID KRS (Pilih di tabel)", font=Tema.FONT_SMALL,
                 bg=Tema.BG_CARD, width=14, anchor="w").grid(row=1, column=0,
                 padx=(0, 10), pady=6, sticky="w")
        self.ent_id = tk.Entry(card_nilai, relief="solid", bd=1, state="readonly")
        self.ent_id.grid(row=1, column=1, padx=5, pady=6, sticky="ew")

        tk.Label(card_nilai, text="Nilai (0-100)", font=Tema.FONT_SMALL,
                 bg=Tema.BG_CARD, width=14, anchor="w").grid(row=2, column=0,
                 padx=(0, 10), pady=6, sticky="w")
        self.ent_nilai = tk.Entry(card_nilai, relief="solid", bd=1)
        self.ent_nilai.grid(row=2, column=1, padx=5, pady=6, sticky="ew")

        frm_btn2 = tk.Frame(card_nilai, bg=Tema.BG_CARD)
        frm_btn2.grid(row=3, column=0, columnspan=2, pady=(15, 0))
        self.buat_tombol(frm_btn2, "💾 Simpan Nilai", Tema.SUCCESS, self._simpan_nilai)

        self._buat_tabel()

        self.frm_summary = tk.Frame(self, bg=Tema.BG_CARD, padx=20, pady=15)
        self.frm_summary.pack(fill=tk.X, padx=25, pady=(0, 15))
        self.lbl_ipk = tk.Label(self.frm_summary,
                                text="Total SKS: 0 | IP Semester: 0.00",
                                font=("Segoe UI", 14, "bold"),
                                bg=Tema.BG_CARD, fg=Tema.ACCENT)
        self.lbl_ipk.pack(anchor="w")

    def _buat_tabel(self):
        frm = tk.Frame(self, bg=Tema.BG_MAIN)
        frm.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)
        self.tree = ttk.Treeview(frm, columns=("id", "kode_mk", "nama_mk", "sks",
                                                "nilai", "huruf", "bobot"),
                                  show="headings", height=6)
        for col, w in [("id", 30), ("kode_mk", 70), ("nama_mk", 200), ("sks", 50),
                        ("nilai", 60), ("huruf", 50), ("bobot", 60)]:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=w)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def isi_combobox(self, nim, ta):
        self.cbo_nim["values"] = nim
        self.cbo_ta["values"] = ta

    def _tampilkan(self):
        nim_val = self.cbo_nim.get().split(" - ")[0] if self.cbo_nim.get() else ""
        ta_val = self.cbo_ta.get() if self.cbo_ta.get() else None
        if not nim_val:
            messagebox.showwarning("Peringatan", "Pilih mahasiswa!"); return
        self.controller.tampilkan_khs(nim_val, ta_val)

    def _simpan_nilai(self):
        id_krs = self.ent_id.get()
        nilai = self.ent_nilai.get()
        if not id_krs:
            messagebox.showwarning("Peringatan", "Pilih mata kuliah di tabel!"); return
        try:
            self.controller.update_nilai_krs(int(id_krs), nilai)
            self._tampilkan()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _on_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0])["values"]
        self.ent_id.config(state="normal")
        self.ent_id.delete(0, tk.END); self.ent_id.insert(0, vals[0])
        self.ent_id.config(state="readonly")
        self.ent_nilai.delete(0, tk.END)
        if vals[4] != "-":
            self.ent_nilai.insert(0, vals[4])

    def muat_data_khs(self, data_khs, ipk, total_sks):
        for row in self.tree.get_children(): self.tree.delete(row)
        for row in data_khs:
            nilai_tampil = row['nilai'] if row['nilai'] is not None else "-"
            self.tree.insert("", tk.END, values=(
                row['id'], row['kode_mk'], row['nama_mk'], row['sks'],
                nilai_tampil, row['nilai_huruf'], row['bobot']
            ))
        self.lbl_ipk.config(text=f"Total SKS: {total_sks}  |  IP Semester: {ipk:.2f}")