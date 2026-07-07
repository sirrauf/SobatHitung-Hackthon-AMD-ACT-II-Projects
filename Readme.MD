# Release date: 07 July 2026

---

![Logo_Sobat_Hitung](https://github.com/sirrauf/SobatHitung-Hackthon-AMD-ACT-II-Projects/blob/main-production/Logo/Logo-SobatHitung.jpg?raw=true)

# SobatHitung - AMD AI Agents Hackathon Project

**SobatHitung** is an AI-Powered Finance Company Assistant designed to help businesses automate financial operations, improve decision-making, and simplify accounting and taxation processes through intelligent AI Agents.

---

## 📌 Table of Contents

- [Features](#-features)
- [Target Users](#-target-users)
- [Vision](#-vision)
- [Dokumentasi Teknis](#%EF%B8%8F-dokumentasi-teknis)
  - [1. Struktur Arsitektur Folder](#1-struktur-arsitektur-folder)
  - [2. Konfigurasi Environment (.env)](#2-konfigurasi-environment-env)
  - [3. Instalasi dan Aktivasi Python Virtual Environment (venv)](#3-instalasi-dan-aktivasi-python-virtual-environment-venv)
  - [4. Instalasi Dependensi (requirements.txt)](#4-instalasi-dependensi-requirementstxt)
  - [5. Persiapan Database MySQL](#5-persiapan-database-mysql)
  - [6. Setup Ollama (AI LLM Server)](#6-setup-ollama-ai-llm-server)
  - [7. Cara Menjalankan Proyek SobatHitung](#7-cara-menjalankan-proyek-sobathitung)

---

## 🤖 Features

### 🤖 AI Finance Assistant

An intelligent conversational assistant that helps users understand financial data, answer accounting questions, and provide real-time financial insights.

### 📊 Automated Accounting

Automatically records, categorizes, and manages financial transactions, reducing manual bookkeeping effort and minimizing human errors.

### 💰 Financial Reporting

Generate financial reports such as Profit & Loss Statements, Balance Sheets, Cash Flow Reports, and Business Performance Summaries instantly.

### 📈 Business Analytics & Insights

Analyze company financial performance and provide AI-driven recommendations to improve profitability, cash flow, and operational efficiency.

### 🧾 Smart Tax Management

Assist businesses in calculating, organizing, and preparing tax-related information to ensure compliance and reduce tax reporting complexity.

### 🔍 Financial Health Monitoring

Monitor business financial conditions continuously and detect unusual spending patterns, cash flow risks, and potential financial issues.

### 📅 Cash Flow Forecasting

Predict future cash flow trends using AI-powered analysis to help businesses make better financial decisions.

### 📂 Intelligent Document Processing

Extract and process financial information from invoices, receipts, and financial documents automatically using AI.

### ⚡ Real-Time Decision Support

Provide actionable recommendations for budgeting, expense optimization, investment planning, and financial strategy.

### 🔒 Secure Financial Data Management

Ensure business financial information remains protected with secure data handling and privacy-focused architecture.

## 👥 Target Users

- Small and Medium Enterprises (SMEs)
- Startups
- Finance Teams
- Accountants
- Business Owners
- Tax Consultants

## 💡 Vision

Empowering businesses with AI Agents that transform complex financial operations into simple, intelligent, and automated workflows.

---

## 🛠️ Dokumentasi Teknis

Bagian ini menjelaskan struktur teknis dari proyek SobatHitung, konfigurasi environment, setup virtual environment, cara instalasi dependensi, hingga perintah untuk menjalankan aplikasi di lingkungan lokal.

### 1. Struktur Arsitektur Folder

Berikut adalah visualisasi struktur direktori proyek SobatHitung beserta penjelasannya:

```text
DataSobatHitung/
│
├── static/                   # File aset statis (CSS, JS, Gambar)
│   ├── css/                  # File-file styling CSS
│   │   ├── index.css         # Styling halaman utama/dashboard explorer
│   │   ├── landing.css       # Styling halaman landing
│   │   └── shared.css        # Variabel CSS global, reset, dan utility styling
│   └── js/                   # File-file backend logic sisi klien (JavaScript/AJAX)
│       ├── auth.js           # Penanganan autentikasi (login/register/reset)
│       ├── contact.js        # Logika submit contact us
│       ├── index.js          # Sederet interaktif navigasi main explorer
│       ├── landing.js        # Animasi & navigasi di halaman landing
│       └── profile.js        # Konfigurasi AJAX profile update settings
│
├── templates/                # File template Flask (HTML dengan rendering Jinja2)
│   ├── 404.html              # Halaman error 404
│   ├── about.html            # Informasi pengembang & visi misi
│   ├── contact.html          # Form hubungi kami
│   ├── dashboard.html        # Menu dashboard utama pengguna
│   ├── email_reset.html      # Template email reset kata sandi
│   ├── email_verify.html     # Template email verifikasi akun pendaftaran
│   ├── forgot_password.html  # Halaman lupa kata sandi
│   ├── index.html            # Halaman utama aplikasi / explorer
│   ├── landing.html          # Landing page promosi
│   ├── login.html            # Halaman masuk (login)
│   ├── profile.html          # Pengaturan biodata & profil user
│   ├── register.html         # Halaman pendaftaran user
│   ├── reset_password.html   # Halaman memasukkan password baru
│   └── verify.html           # Feedback verifikasi email berhasil
│
├── Model_LLM/                # Direktori model LLM (Large Language Model) lokal
├── Logo/                     # Aset logo SobatHitung
├── Screenshoot/              # Kumpulan dokumentasi tangkapan layar aplikasi
├── uploads/                  # Direktori upload file user (PDF/Excel)
├── app.py                    # Root aplikasi Flask (Rute, Logic, validasi server-side)
├── models.py                 # Skema entity database (Pony ORM schema model)
├── .env                      # Pengaturan variabel environment (rahasia/sensitif)
├── requirements.txt          # Daftar package python dependencies
├── Procfile                  # Konfigurasi deploy Web / WSGI server (Gunicorn)
└── Readme.MD                 # Panduan dan dokumentasi teknis (file ini)
```

**Penjelasan Komponen Utama:**

- **`app.py`**: Berisi keseluruhan logika routes untuk Flask, konfigurasi mail server (Gmail SMTP), koneksi relational database dengan Pony ORM, pengontrolan autentikasi bersertifikat password hashing dengan `bcrypt`, restrukturasi rute AJAX profile settings, serta penanganan error 404.
- **`models.py`**: Menggunakan Pony ORM untuk merelasikan schema database MySQL pada table `tbl_user`, menyertakan field data profil lengkap, penanda verifikasi email (`is_verified`), token penunjuk verifikasi, dan token reset password beserta masa berlakunya.
- **`static/` & `templates/`**: Memisahkan antarmuka logic (Jinja2) dengan resources pendukung (raw CSS dan JS).

---

### 2. Konfigurasi Environment (`.env`)

Aplikasi menggunakan library `python-dotenv` untuk memuat variabel sensitif dari file `.env`. Untuk menggunakan aplikasi, buat file bernama `.env` di root direktori dengan struktur variabel berikut:

```ini
# Flask configuration
SECRETKEY=@Viti412
PORT=5100

# Database Configuration (MySQL)
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=db_sobathitung

# SMTP Configuration (Gmail)
MAIL_USERNAME=anandatechnologysolution@gmail.com
MAIL_PASSWORD=afuc rjrg jmzr oesh

# Ollama LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
```

> [!IMPORTANT]
>
> - `SECRETKEY` digunakan untuk keamanan enkripsi cookie/session Flask.
> - `MAIL_PASSWORD` **bukanlah password Gmail biasa**, melainkan **App Password** 16 karakter yang dibuat melalui menu keamanan akun Google Anda (2-Step Verification).
> - `OLLAMA_BASE_URL` menunjuk ke server Ollama lokal. Default: `http://localhost:11434`.

---

### 3. Instalasi dan Aktivasi Python Virtual Environment (`venv`)

Menggunakan virtual environment sangat direkomendasikan agar versi library di proyek tidak bertabrakan dengan environment global komputer Anda.

#### A. Membuat Virtual Environment (Jika belum ada)

Jalankan perintah ini di terminal (Pastikan terminal berada di direktori proyek `DataSobatHitung`):

```bash
python -m venv venv
```

#### B. Mengaktifkan Virtual Environment

Sesuaikan perintah dengan Sistem Operasi dan interpreter terminal yang Anda gunakan:

- **Windows (PowerShell):**
  ```powershell
  venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  venv\Scripts\activate.bat
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

_Setelah aktif, Anda akan melihat tanda `(venv)` di sebelah kiri prompt terminal Anda._

---

### 4. Instalasi Dependensi (`requirements.txt`)

Setelah mengaktifkan Virtual Environment, Anda harus menginstal seluruh package Python yang dideklarasikan di file `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Daftar Dependency yang Dipasang (`requirements.txt`):**

- **Flask**: Framework web Python utama.
- **Flask-Mail**: Integrasi scheduler SMTP server untuk email verifikasi.
- **pony**: Pony Object Relational Mapper (ORM) untuk interaksi database.
- **bcrypt**: Algoritma hashing terpercaya untuk pengamanan password user.
- **PyMySQL**: Python MySQL client library yang dihubungkan ke Pony ORM.
- **python-dotenv**: Library untuk mempermudah pembacaan file konfigurasi `.env`.
- **requests**: HTTP client library untuk komunikasi dengan Ollama LLM API.

---

### 5. Persiapan Database MySQL

Aplikasi ini menggunakan MySQL sebagai database. Sebelum menjalankan aplikasi, lakukan langkah berikut:

1. Aktifkan service Apache & MySQL Anda (misal menggunakan **XAMPP / Laragon**).
2. Buka **phpMyAdmin** (`http://localhost/phpmyadmin/`) atau database manager pilihan Anda (HeidiSQL, DBeaver, dll.).
3. Buat database baru bernama **`db_sobathitung`** (atau sesuaikan dengan konfigurasi variabel `DB_NAME` di file `.env`).
4. Anda tidak perlu membuat tabel secara manual. Pony ORM melalui fungsi `db.generate_mapping(create_tables=True)` di file `app.py` akan otomatis me-generate tabel berikut:
   - `tbl_user` — Data pengguna, profil, dan pengaturan
   - `tbl_activity_log` — Log riwayat aktivitas user
   - `tbl_chat_history` — Riwayat percakapan AI
   - `tbl_uploaded_file` — Data file yang diupload

---

### 6. Setup Ollama (AI LLM Server)

Aplikasi SobatHitung menggunakan **Ollama** sebagai backend LLM lokal. Model yang didukung:

- **DeepSeek-R1 32B** — Model reasoning canggih untuk analisis keuangan mendalam
- **Qwen3 14B** — Model cepat dan efisien untuk respons instan

**Langkah Setup:**

1. Download dan install Ollama dari [ollama.com](https://ollama.com)
2. Jalankan Ollama (otomatis berjalan di `http://localhost:11434`)
3. Buka terminal baru, lalu download model:
   ```bash
   ollama pull deepseek-r1:32b
   ollama pull qwen3:14b
   ```
4. Pastikan Ollama tetap berjalan saat menggunakan fitur AI di SobatHitung.

> [!TIP]
> Jika perangkat Anda memiliki RAM terbatas, Anda bisa menggunakan salah satu model saja. Qwen3 14B lebih ringan dan cocok untuk perangkat dengan RAM 16GB.

---

### 7. Cara Menjalankan Proyek SobatHitung

Setelah semua setup di atas selesai (Virtual Environment aktif, dependensi terinstal, `.env` terkonfigurasi, database MySQL telah dibuat, dan Ollama berjalan), Anda dapat menjalankan server dengan langkah berikut:

```bash
python app.py
```

Jika server berhasil berjalan, Anda akan melihat output serupa:

```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5100
Press CTRL+C to quit
```

Buka peramban (browser) Anda dan akses alamat tersebut:

```text
http://127.0.0.1:5100/ atau http://localhost:5100/
```
