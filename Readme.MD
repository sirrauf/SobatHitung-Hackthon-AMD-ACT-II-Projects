# Release Date: July 7, 2026

---

![Logo_Sobat_Hitung](https://github.com/sirrauf/SobatHitung-Hackthon-AMD-ACT-II-Projects/blob/main-production/Logo/Logo-SobatHitung.jpg?raw=true)

# SobatHitung - AMD AI Agents Hackathon Project

**SobatHitung** is an AI-Powered Finance Company Assistant designed to help businesses automate financial operations, improve decision-making, and simplify accounting and taxation processes through intelligent AI Agents.

---

## 📌 Table of Contents

- [Features](#-features)
- [Target Users](#-target-users)
- [Vision](#-vision)
- [Technical Documentation](#%EF%B8%8F-technical-documentation)
  - [1. Project Folder Structure](#1-project-folder-structure)
  - [2. Environment Configuration (.env)](#2-environment-configuration-env)
  - [3. Python Virtual Environment Installation & Activation](#3-python-virtual-environment-installation--activation)
  - [4. Installing Dependencies (requirements.txt)](#4-installing-dependencies-requirementstxt)
  - [5. MySQL Database Setup](#5-mysql-database-setup)
  - [6. Ollama Setup (AI LLM Server)](#6-ollama-setup-ai-llm-server)
  - [7. Running the SobatHitung Project](#7-running-the-sobathitung-project)

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

## 🛠️ Technical Documentation

This section describes the technical structure of the SobatHitung project, including environment configuration, virtual environment setup, dependency installation instructions, and the commands required to run the application in a local development environment.

### 1. Project Folder Structure

The following is a visualization of the SobatHitung project directory structure along with descriptions of each component:

```text
DataSobatHitung/
│
├── static/                   # Static asset files (CSS, JS, Images)
│   ├── css/                  # CSS styling files
│   │   ├── index.css         # Styling for the main/dashboard explorer page
│   │   ├── landing.css       # Styling for the landing page
│   │   └── shared.css        # Global CSS variables, resets, and utility styles
│   └── js/                   # Client-side logic files (JavaScript/AJAX)
│       ├── auth.js           # Authentication handling (login/register/reset)
│       ├── contact.js        # Contact Us form submission logic
│       ├── index.js          # Interactive navigation for the main explorer
│       ├── landing.js        # Animations & navigation for the landing page
│       └── profile.js        # AJAX configuration for profile update settings
│
├── templates/                # Flask template files (HTML with Jinja2 rendering)
│   ├── 404.html              # 404 error page
│   ├── about.html            # Developer information & project vision
│   ├── contact.html          # Contact us form
│   ├── dashboard.html        # Main user dashboard menu
│   ├── email_reset.html      # Password reset email template
│   ├── email_verify.html     # Account registration verification email template
│   ├── forgot_password.html  # Forgot password page
│   ├── index.html            # Main application/explorer page
│   ├── landing.html          # Promotional landing page
│   ├── login.html            # Login page
│   ├── profile.html          # User profile & bio settings
│   ├── register.html         # User registration page
│   ├── reset_password.html   # New password entry page
│   └── verify.html           # Email verification success feedback page
│
├── Model_LLM/                # Local LLM (Large Language Model) directory
├── Logo/                     # SobatHitung logo assets
├── Screenshoot/              # Application screenshot documentation collection
├── uploads/                  # User file upload directory (PDF/Excel)
├── app.py                    # Flask application root (Routes, Logic, server-side validation)
├── models.py                 # Database entity schema (Pony ORM schema model)
├── .env                      # Environment variable settings (secret/sensitive)
├── requirements.txt          # Python package dependency list
├── Procfile                  # Web/WSGI server deployment configuration (Gunicorn)
└── Readme.MD                 # Project guide and technical documentation (this file)
```

**Key Component Descriptions:**

- **`app.py`**: Contains all Flask route logic, Gmail SMTP mail server configuration, relational database connection via Pony ORM, authentication control with `bcrypt` password hashing, restructured AJAX profile settings routes, and 404 error handling.
- **`models.py`**: Uses Pony ORM to define the MySQL database schema on the `tbl_user` table, including complete profile data fields, an email verification flag (`is_verified`), a verification token, and a password reset token along with its expiration time.
- **`static/` & `templates/`**: Separates the Jinja2 logic layer from the supporting resources (raw CSS and JS files).

---

### 2. Environment Configuration (`.env`)

The application uses the `python-dotenv` library to load sensitive variables from the `.env` file. To use the application, create a file named `.env` in the project root directory with the following variable structure:

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
> - `SECRETKEY` is used for Flask cookie/session encryption security.
> - `MAIL_PASSWORD` is **not your regular Gmail password**; it is a **16-character App Password** generated through your Google account security settings (2-Step Verification).
> - `OLLAMA_BASE_URL` points to the local Ollama server. Default: `http://localhost:11434`.

---

### 3. Python Virtual Environment Installation & Activation

Using a virtual environment is strongly recommended to prevent library version conflicts between the project and your computer's global environment.

#### A. Creating a Virtual Environment (If one does not already exist)

Run this command in your terminal (make sure the terminal is in the `DataSobatHitung` project directory):

```bash
python -m venv venv
```

#### B. Activating the Virtual Environment

Adjust the command according to your operating system and terminal interpreter:

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

_Once activated, you will see the `(venv)` indicator on the left side of your terminal prompt._

---

### 4. Installing Dependencies (`requirements.txt`)

After activating the Virtual Environment, install all Python packages declared in the `requirements.txt` file by running:

```bash
pip install -r requirements.txt
```

**List of Installed Dependencies (`requirements.txt`):**

- **Flask**: The primary Python web framework.
- **Flask-Mail**: SMTP server scheduler integration for email verification.
- **pony**: Pony Object Relational Mapper (ORM) for database interaction.
- **bcrypt**: A trusted hashing algorithm for user password security.
- **PyMySQL**: Python MySQL client library connected to Pony ORM.
- **python-dotenv**: A library that simplifies reading `.env` configuration files.
- **requests**: HTTP client library for communicating with the Ollama LLM API.

---

### 5. MySQL Database Setup

This application uses MySQL as its database. Before running the application, complete the following steps:

1. Start your Apache & MySQL services (e.g., using **XAMPP** or **Laragon**).
2. Open **phpMyAdmin** (`http://localhost/phpmyadmin/`) or your preferred database manager (HeidiSQL, DBeaver, etc.).
3. Create a new database named **`db_sobathitung`** (or adjust it to match the `DB_NAME` variable in your `.env` file).
4. You do not need to create the tables manually. Pony ORM, via the `db.generate_mapping(create_tables=True)` function in `app.py`, will automatically generate the following tables:
   - `tbl_user` — User data, profiles, and settings
   - `tbl_activity_log` — User activity history log
   - `tbl_chat_history` — AI conversation history
   - `tbl_uploaded_file` — Uploaded file data

---

### 6. Ollama Setup (AI LLM Server)

The SobatHitung application uses **Ollama** as a local LLM backend. Supported models include:

- **DeepSeek-R1 32B** — An advanced reasoning model for in-depth financial analysis
- **Qwen3 14B** — A fast and efficient model for instant responses

**Setup Steps:**

1. Download and install Ollama from [ollama.com](https://ollama.com).
2. Run Ollama (it automatically runs at `http://localhost:11434`).
3. Open a new terminal and download the models:
   ```bash
   ollama pull deepseek-r1:32b
   ollama pull qwen3:14b
   ```
4. Ensure Ollama remains running while using the AI features in SobatHitung.

> [!TIP]
> If your device has limited RAM, you can use just one model. Qwen3 14B is lighter and more suitable for devices with 16GB of RAM.

---

### 7. Running the SobatHitung Project

Once all of the above setup is complete (Virtual Environment activated, dependencies installed, `.env` configured, MySQL database created, and Ollama running), you can start the server with the following command:

```bash
python app.py
```

If the server starts successfully, you will see output similar to the following:

```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5100
Press CTRL+C to quit
```

Open your web browser and navigate to the address shown:

```text
http://127.0.0.1:5100/ or http://localhost:5100/
```
