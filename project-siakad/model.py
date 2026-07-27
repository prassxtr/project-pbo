# ============================================================
# model.py - Lapisan Data (Model)
# SIAKAD Mini - Sistem Informasi Akademik
# ============================================================

import sqlite3
import hashlib


class DatabaseManager:
    """Mengelola koneksi SQLite secara terpusat (Encapsulation)."""

    def __init__(self, db_name="siakad.db"):
        self.__db_name = db_name
        self.__conn = None
        self.__cursor = None
        self._connect()
        self._create_tables()

    def _connect(self):
        try:
            self.__conn = sqlite3.connect(self.__db_name)
            self.__conn.execute("PRAGMA foreign_keys = ON")
            self.__conn.row_factory = sqlite3.Row
            self.__cursor = self.__conn.cursor()
        except sqlite3.Error as e:
            raise Exception(f"Gagal koneksi database: {e}")

    def _create_tables(self):
        try:
            self.__cursor.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    nama_lengkap TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'admin'
                );
                CREATE TABLE IF NOT EXISTS mahasiswa (
                    nim TEXT PRIMARY KEY,
                    nama TEXT NOT NULL,
                    jurusan TEXT NOT NULL,
                    angkatan INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS mata_kuliah (
                    kode_mk TEXT PRIMARY KEY,
                    nama_mk TEXT NOT NULL,
                    sks INTEGER NOT NULL,
                    semester INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS krs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nim TEXT NOT NULL,
                    kode_mk TEXT NOT NULL,
                    nilai REAL DEFAULT NULL,
                    tahun_ajaran TEXT NOT NULL,
                    FOREIGN KEY (nim) REFERENCES mahasiswa(nim) ON DELETE CASCADE,
                    FOREIGN KEY (kode_mk) REFERENCES mata_kuliah(kode_mk) ON DELETE CASCADE,
                    UNIQUE(nim, kode_mk, tahun_ajaran)
                );
            """)

            # Buat default admin jika belum ada
            self.__cursor.execute(
                "SELECT COUNT(*) as total FROM users WHERE username = 'admin'"
            )
            if self.__cursor.fetchone()['total'] == 0:
                admin_pass = hashlib.sha256("admin123".encode()).hexdigest()
                self.__cursor.execute(
                    "INSERT INTO users (username, password, nama_lengkap, role) VALUES (?, ?, ?, ?)",
                    ('admin', admin_pass, 'Administrator Sistem', 'admin')
                )
            self.__conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Gagal membuat tabel: {e}")

    def execute(self, query, params=()):
        try:
            self.__cursor.execute(query, params)
            self.__conn.commit()
            return self.__cursor
        except sqlite3.IntegrityError as e:
            self.__conn.rollback()
            raise Exception(f"Data sudah ada / duplikat: {e}")
        except sqlite3.Error as e:
            self.__conn.rollback()
            raise Exception(f"Error SQL: {e}")

    def fetch_all(self, query, params=()):
        try:
            self.__cursor.execute(query, params)
            return self.__cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Error membaca data: {e}")

    def fetch_one(self, query, params=()):
        try:
            self.__cursor.execute(query, params)
            return self.__cursor.fetchone()
        except sqlite3.Error as e:
            raise Exception(f"Error membaca data: {e}")

    def close(self):
        if self.__conn:
            self.__conn.close()


# ============================================================
class UserModel:
    """Model untuk autentikasi user."""

    def __init__(self, db: DatabaseManager):
        self.__db = db

    def login(self, username, password):
        if not username or not password:
            raise ValueError("Username dan password wajib diisi!")
        hashed_pass = hashlib.sha256(password.encode()).hexdigest()
        user = self.__db.fetch_one(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username.strip(), hashed_pass)
        )
        if not user:
            raise ValueError("Username atau password salah!")
        return {
            'id': user['id'],
            'username': user['username'],
            'nama_lengkap': user['nama_lengkap'],
            'role': user['role']
        }


# ============================================================
class MahasiswaModel:
    """Model untuk entitas Mahasiswa."""

    def __init__(self, db: DatabaseManager):
        self.__db = db

    def tambah(self, nim, nama, jurusan, angkatan):
        self._validasi(nim, nama, jurusan, angkatan)
        self.__db.execute(
            "INSERT INTO mahasiswa (nim, nama, jurusan, angkatan) VALUES (?, ?, ?, ?)",
            (nim.strip().upper(), nama.strip(), jurusan.strip(), int(angkatan))
        )

    def perbarui(self, nim_lama, nim, nama, jurusan, angkatan):
        self._validasi(nim, nama, jurusan, angkatan)
        self.__db.execute(
            "UPDATE mahasiswa SET nim=?, nama=?, jurusan=?, angkatan=? WHERE nim=?",
            (nim.strip().upper(), nama.strip(), jurusan.strip(), int(angkatan), nim_lama)
        )

    def hapus(self, nim):
        self.__db.execute("DELETE FROM krs WHERE nim=?", (nim,))
        self.__db.execute("DELETE FROM mahasiswa WHERE nim=?", (nim,))

    def ambil_semua(self):
        return self.__db.fetch_all("SELECT nim, nama, jurusan, angkatan FROM mahasiswa ORDER BY nim")

    def hitung(self):
        rows = self.__db.fetch_all("SELECT COUNT(*) as total FROM mahasiswa")
        return rows[0]["total"] if rows else 0

    def _validasi(self, nim, nama, jurusan, angkatan):
        if not nim or not nim.strip():
            raise ValueError("NIM wajib diisi!")
        if not nama or not nama.strip():
            raise ValueError("Nama wajib diisi!")
        if not jurusan or not jurusan.strip():
            raise ValueError("Jurusan wajib diisi!")
        try:
            a = int(angkatan)
            if a < 2000 or a > 2100:
                raise ValueError("Angkatan harus antara 2000 - 2100!")
        except (TypeError, ValueError) as e:
            if "Angkatan" in str(e):
                raise
            raise ValueError("Angkatan harus berupa angka tahun!")


# ============================================================
class MataKuliahModel:
    """Model untuk entitas Mata Kuliah."""

    def __init__(self, db: DatabaseManager):
        self.__db = db

    def tambah(self, kode_mk, nama_mk, sks, semester):
        self._validasi(kode_mk, nama_mk, sks, semester)
        self.__db.execute(
            "INSERT INTO mata_kuliah (kode_mk, nama_mk, sks, semester) VALUES (?, ?, ?, ?)",
            (kode_mk.strip().upper(), nama_mk.strip(), int(sks), int(semester))
        )

    def perbarui(self, kode_lama, kode_mk, nama_mk, sks, semester):
        self._validasi(kode_mk, nama_mk, sks, semester)
        self.__db.execute(
            "UPDATE mata_kuliah SET kode_mk=?, nama_mk=?, sks=?, semester=? WHERE kode_mk=?",
            (kode_mk.strip().upper(), nama_mk.strip(), int(sks), int(semester), kode_lama)
        )

    def hapus(self, kode_mk):
        self.__db.execute("DELETE FROM krs WHERE kode_mk=?", (kode_mk,))
        self.__db.execute("DELETE FROM mata_kuliah WHERE kode_mk=?", (kode_mk,))

    def ambil_semua(self):
        return self.__db.fetch_all("SELECT kode_mk, nama_mk, sks, semester FROM mata_kuliah ORDER BY kode_mk")

    def hitung(self):
        rows = self.__db.fetch_all("SELECT COUNT(*) as total FROM mata_kuliah")
        return rows[0]["total"] if rows else 0

    def _validasi(self, kode_mk, nama_mk, sks, semester):
        if not kode_mk or not kode_mk.strip():
            raise ValueError("Kode MK wajib diisi!")
        if not nama_mk or not nama_mk.strip():
            raise ValueError("Nama MK wajib diisi!")
        try:
            s = int(sks)
            if s < 1 or s > 6:
                raise ValueError("SKS harus antara 1 - 6!")
        except (TypeError, ValueError) as e:
            if "SKS" in str(e):
                raise
            raise ValueError("SKS harus berupa angka!")
        try:
            sem = int(semester)
            if sem < 1 or sem > 8:
                raise ValueError("Semester harus antara 1 - 8!")
        except (TypeError, ValueError) as e:
            if "Semester" in str(e):
                raise
            raise ValueError("Semester harus berupa angka!")


# ============================================================
class KRSModel:
    """Model untuk entitas KRS (Kartu Rencana Studi)."""

    def __init__(self, db: DatabaseManager):
        self.__db = db

    def daftar_mk(self, nim, kode_mk, tahun_ajaran):
        if not nim or not kode_mk:
            raise ValueError("Pilih Mahasiswa dan Mata Kuliah!")
        if not tahun_ajaran or not tahun_ajaran.strip():
            raise ValueError("Tahun Ajaran wajib diisi!")
        self.__db.execute(
            "INSERT INTO krs (nim, kode_mk, tahun_ajaran) VALUES (?, ?, ?)",
            (nim, kode_mk, tahun_ajaran.strip())
        )

    def perbarui(self, id_krs, nim, kode_mk, nilai, tahun_ajaran):
        self.__db.execute(
            "UPDATE krs SET nim=?, kode_mk=?, nilai=?, tahun_ajaran=? WHERE id=?",
            (nim, kode_mk, float(nilai), tahun_ajaran.strip(), id_krs)
        )

    def update_nilai(self, id_krs, nilai):
        try:
            n = float(nilai)
            if n < 0 or n > 100:
                raise ValueError("Nilai harus antara 0 - 100!")
        except (TypeError, ValueError):
            raise ValueError("Nilai harus berupa angka 0-100!")
        self.__db.execute("UPDATE krs SET nilai = ? WHERE id = ?", (n, id_krs))

    def hapus(self, id_krs):
        self.__db.execute("DELETE FROM krs WHERE id=?", (id_krs,))

    def ambil_semua(self):
        """Ambil semua data KRS dengan SKS (untuk tabel KRS)."""
        return self.__db.fetch_all("""
            SELECT k.id, m.nim, m.nama, mk.kode_mk, mk.nama_mk, mk.sks, k.tahun_ajaran
            FROM krs k
            JOIN mahasiswa m ON k.nim = m.nim
            JOIN mata_kuliah mk ON k.kode_mk = mk.kode_mk
            ORDER BY k.tahun_ajaran DESC, m.nim
        """)

    def ambil_krs_mahasiswa(self, nim, tahun_ajaran=None):
        """Ambil KRS mahasiswa untuk KHS (dengan nilai)."""
        if tahun_ajaran:
            return self.__db.fetch_all("""
                SELECT k.id, m.nim, m.nama, mk.kode_mk, mk.nama_mk, mk.sks, k.nilai, k.tahun_ajaran
                FROM krs k
                JOIN mahasiswa m ON k.nim = m.nim
                JOIN mata_kuliah mk ON k.kode_mk = mk.kode_mk
                WHERE k.nim = ? AND k.tahun_ajaran = ?
                ORDER BY mk.kode_mk
            """, (nim, tahun_ajaran))
        return self.__db.fetch_all("""
            SELECT k.id, m.nim, m.nama, mk.kode_mk, mk.nama_mk, mk.sks, k.nilai, k.tahun_ajaran
            FROM krs k
            JOIN mahasiswa m ON k.nim = m.nim
            JOIN mata_kuliah mk ON k.kode_mk = mk.kode_mk
            WHERE k.nim = ?
            ORDER BY k.tahun_ajaran DESC, mk.kode_mk
        """, (nim,))

    def hitung(self):
        rows = self.__db.fetch_all("SELECT COUNT(*) as total FROM krs")
        return rows[0]["total"] if rows else 0

    def ambil_semua_tahun_ajaran(self):
        rows = self.__db.fetch_all("SELECT DISTINCT tahun_ajaran FROM krs ORDER BY tahun_ajaran DESC")
        return [row['tahun_ajaran'] for row in rows]


# ============================================================
class KHSModel:
    """Model untuk KHS (Kartu Hasil Studi) - Konversi Nilai & IPK."""

    @staticmethod
    def konversi_nilai(nilai_angka):
        """Konversi nilai angka ke huruf dan bobot IPK."""
        if nilai_angka is None:
            return "E", 0.0
        if nilai_angka >= 85:
            return "A", 4.0
        elif nilai_angka >= 80:
            return "B+", 3.5
        elif nilai_angka >= 75:
            return "B", 3.0
        elif nilai_angka >= 70:
            return "C+", 2.5
        elif nilai_angka >= 65:
            return "C", 2.0
        elif nilai_angka >= 60:
            return "D", 1.0
        else:
            return "E", 0.0

    def hitung_ipk(self, data_krs):
        """Hitung IPK dari data KRS."""
        total_bobot = 0
        total_sks = 0
        for mk in data_krs:
            if mk['nilai'] is not None:
                _, bobot = self.konversi_nilai(mk['nilai'])
                total_bobot += bobot * mk['sks']
                total_sks += mk['sks']
        ipk = total_bobot / total_sks if total_sks > 0 else 0.0
        return round(ipk, 2), total_sks