from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_mail import Mail, Message
from pony.orm import db_session, commit
from models import db, User, ActivityLog, ChatHistory, UploadedFile
from functools import wraps
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import bcrypt
import uuid
import os
import json
import requests

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRETKEY', 'default-secret-key')

# --- Upload config ---
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Ollama config ---
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
AVAILABLE_MODELS = {
    'deepseek-r1:32b': {
        'name': 'DeepSeek-R1 32B',
        'desc': 'Model reasoning canggih untuk analisis keuangan mendalam'
    },
    'qwen3:14b': {
        'name': 'Qwen3 14B',
        'desc': 'Model cepat dan efisien untuk respons instan'
    }
}

# --- Mail config (Gmail) ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME', '')

mail = Mail(app)

# --- Database (PyMySQL) ---
db.bind(
    provider='mysql',
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    passwd=os.getenv('DB_PASSWORD', ''),
    db=os.getenv('DB_NAME', 'db_sobathitung')
)
db.generate_mapping(create_tables=True)


# ==================== HELPERS ====================

def raw_query_ids(sql, params=None):
    """Execute raw SQL and return list of id values.
    Bypasses Pony ORM's broken query machinery on Python 3.12+/3.14."""
    cursor = db.execute(sql, params or {})
    return [row[0] for row in cursor.fetchall()]

FINANCE_SYSTEM_PROMPT = """Kamu adalah SobatHitung AI Finance Assistant — asisten keuangan cerdas berbahasa Indonesia.

Keahlianmu mencakup:
1. **AI Finance Assistant**: Memahami konteks bisnis pengguna, menjawab pertanyaan tentang data keuangan, akuntansi, cash flow, dan memberikan rekomendasi strategis dalam bahasa natural.
2. **Pembukuan Otomatis**: Membantu mencatat dan mengkategorikan transaksi secara otomatis, memproses data invoice.
3. **Laporan Instan**: Membantu generate laporan laba rugi, neraca, dan arus kas.
4. **Analitik Bisnis**: Memberikan rekomendasi berbasis AI untuk meningkatkan profitabilitas dan efisiensi.
5. **Pajak Cerdas**: Perhitungan pajak otomatis dan monitoring kepatuhan perpajakan Indonesia.
6. **Peramalan Arus Kas**: Prediksi tren arus kas masa depan untuk keputusan yang lebih baik.

Selalu jawab dalam bahasa Indonesia yang profesional dan mudah dipahami. Berikan contoh angka jika relevan. Gunakan format yang rapi dengan bullet points dan penjelasan yang sistematis."""


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def hash_password(plain):
    return bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(plain, hashed):
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def log_activity(user_id, action, detail=''):
    """Log user activity to database"""
    with db_session:
        user = User[user_id]
        ActivityLog(user=user, action=action, detail=detail)
        commit()


# ==================== PUBLIC PAGES ====================

@app.route('/')
def home():
    return redirect(url_for('landing'))


@app.route('/landing')
def landing():
    return render_template('landing.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/explorer')
def explorer():
    return render_template('index.html')


# ==================== REGISTER ====================

@app.route('/register', methods=['GET', 'POST'])
@db_session
def register():
    if request.method == 'POST':
        nama = request.form.get('nama', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')

        # Validasi server-side
        if len(nama) < 2:
            flash('Nama minimal 2 karakter.', 'danger')
            return redirect(url_for('register'))
        if not email or '@' not in email:
            flash('Format email tidak valid.', 'danger')
            return redirect(url_for('register'))
        if len(password) < 8:
            flash('Password minimal 8 karakter.', 'danger')
            return redirect(url_for('register'))
        if password != password_confirm:
            flash('Password dan konfirmasi tidak cocok.', 'danger')
            return redirect(url_for('register'))

        # Cek email sudah terdaftar
        existing = User.get(email=email)
        if existing:
            flash('Email sudah terdaftar. Silakan gunakan email lain.', 'danger')
            return redirect(url_for('register'))

        # Buat user baru dengan password hashed bcrypt
        token = uuid.uuid4().hex
        new_user = User(
            nama=nama,
            email=email,
            password=hash_password(password),
            is_verified=False,
            verification_token=token
        )
        commit()

        # Log activity
        ActivityLog(user=new_user, action='Mendaftar ke SobatHitung', detail=f'Email: {email}')
        commit()

        # Kirim email verifikasi via Gmail
        try:
            verify_url = url_for('verify_email', token=token, _external=True)
            msg = Message(
                'Verifikasi Email - SobatHitung',
                recipients=[email]
            )
            msg.html = render_template('email_verify.html', nama=nama, verify_url=verify_url)
            mail.send(msg)
            flash('Registrasi berhasil! Silakan cek email Anda untuk verifikasi.', 'success')
        except Exception as e:
            print(f"[MAIL ERROR] {e}")
            flash('Registrasi berhasil! Namun gagal mengirim email verifikasi. Hubungi admin.', 'warning')

        return redirect(url_for('login'))

    return render_template('register.html')


# ==================== EMAIL VERIFICATION ====================

@app.route('/verify/<token>')
@db_session
def verify_email(token):
    user = User.get(verification_token=token)
    if user:
        user.is_verified = True
        user.verification_token = ''
        commit()
        ActivityLog(user=user, action='Email berhasil diverifikasi')
        commit()
        flash('Email berhasil diverifikasi! Silakan login.', 'success')
    else:
        flash('Token verifikasi tidak valid atau sudah digunakan.', 'danger')
    return render_template('verify.html')


# ==================== LOGIN ====================

@app.route('/login', methods=['GET', 'POST'])
@db_session
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.get(email=email)
        if user and check_password(password, user.password):
            if not user.is_verified:
                flash('Silakan verifikasi email Anda terlebih dahulu.', 'warning')
                return redirect(url_for('login'))
            session['user_id'] = user.id
            session['user_nama'] = user.nama
            ActivityLog(user=user, action='Login ke SobatHitung')
            commit()
            flash(f'Selamat datang, {user.nama}!', 'success')
            return redirect(url_for('dashboard'))
        flash('Email atau password salah.', 'danger')

    return render_template('login.html')


# ==================== LOGOUT ====================

@app.route('/logout')
def logout():
    uid = session.get('user_id')
    if uid:
        try:
            log_activity(uid, 'Logout dari SobatHitung')
        except Exception:
            pass
    session.pop('user_id', None)
    session.pop('user_nama', None)
    flash('Logout berhasil.', 'info')
    return redirect(url_for('landing'))


# ==================== FORGOT PASSWORD ====================

@app.route('/forgot-password', methods=['GET', 'POST'])
@db_session
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user = User.get(email=email)

        if user:
            token = uuid.uuid4().hex
            user.reset_token = token
            user.reset_token_expiry = datetime.now() + timedelta(hours=1)
            commit()

            try:
                reset_url = url_for('reset_password', token=token, _external=True)
                msg = Message(
                    'Reset Password - SobatHitung',
                    recipients=[email]
                )
                msg.html = render_template('email_reset.html', nama=user.nama, reset_url=reset_url)
                mail.send(msg)
            except Exception as e:
                print(f"[MAIL ERROR] {e}")

        # Selalu tampilkan pesan yang sama untuk keamanan
        flash('Jika email terdaftar, link reset password sudah dikirim. Silakan cek inbox Anda.', 'success')
        return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
@db_session
def reset_password(token):
    user = User.get(reset_token=token)

    if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.now():
        flash('Link reset password tidak valid atau sudah expired.', 'danger')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')

        if len(password) < 8:
            flash('Password minimal 8 karakter.', 'danger')
            return redirect(url_for('reset_password', token=token))
        if password != password_confirm:
            flash('Password dan konfirmasi tidak cocok.', 'danger')
            return redirect(url_for('reset_password', token=token))

        user.password = hash_password(password)
        user.reset_token = ''
        user.reset_token_expiry = None
        commit()

        ActivityLog(user=user, action='Reset password berhasil')
        commit()

        flash('Password berhasil direset! Silakan login.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html', token=token)


# ==================== DASHBOARD ====================

@app.route('/dashboard')
@login_required
@db_session
def dashboard():
    user = User[session['user_id']]
    ids = raw_query_ids(
        'SELECT id FROM tbl_chat_history WHERE user = $uid ORDER BY created_at DESC LIMIT 50',
        {'uid': user.id}
    )
    chat_history = [ChatHistory[i] for i in ids]
    return render_template('dashboard.html', user=user, chat_history=chat_history, models=AVAILABLE_MODELS)


# ==================== AI CHAT (Ollama) ====================

def get_ollama_installed_models():
    """Ambil daftar model yang sudah ter-install di Ollama.
    Return dict: {model_name: True} atau {} jika Ollama tidak berjalan."""
    try:
        resp = requests.get(f'{OLLAMA_BASE_URL}/api/tags', timeout=5)
        resp.raise_for_status()
        data = resp.json()
        # data.models adalah list of {"name": "deepseek-r1:32b", ...}
        return {m['name']: True for m in data.get('models', [])}
    except Exception:
        return None  # None = Ollama tidak berjalan


@app.route('/api/ollama-status', methods=['GET'])
@login_required
def api_ollama_status():
    """Cek status Ollama dan model mana yang sudah ter-install."""
    installed = get_ollama_installed_models()
    if installed is None:
        return jsonify({
            'ollama_running': False,
            'models': {}
        })

    # Cek tiap model yang didefinisikan di AVAILABLE_MODELS
    model_status = {}
    for model_key in AVAILABLE_MODELS:
        # Cek exact match atau prefix match (misal deepseek-r1:32b bisa muncul
        # sebagai deepseek-r1:32b-q4_K_M di ollama list)
        is_installed = any(
            name == model_key or name.startswith(model_key.split(':')[0] + ':')
            for name in installed
        )
        # Cari exact name yang cocok untuk dipakai saat generate
        exact_name = next(
            (name for name in installed if name == model_key),
            next(
                (name for name in installed
                 if name.startswith(model_key.split(':')[0] + ':')),
                None
            )
        )
        model_status[model_key] = {
            'installed': is_installed,
            'exact_name': exact_name,
        }

    return jsonify({
        'ollama_running': True,
        'models': model_status,
        'all_installed': [name for name in installed]
    })


@app.route('/api/chat', methods=['POST'])
@login_required
@db_session
def api_chat():
    user = User[session['user_id']]
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    model = data.get('model', 'deepseek-r1:32b')
    is_error_response = False

    if not prompt:
        return jsonify({'error': 'Prompt tidak boleh kosong'}), 400

    if model not in AVAILABLE_MODELS:
        return jsonify({'error': 'Model tidak valid'}), 400

    # Tentukan nama model yang tepat di Ollama (bisa berbeda dari key)
    model_to_use = model
    installed = get_ollama_installed_models()
    if installed is not None:
        # Cari exact match dulu, lalu prefix match
        if model not in installed:
            prefix = model.split(':')[0] + ':'
            alt = next((n for n in installed if n.startswith(prefix)), None)
            if alt:
                model_to_use = alt  # pakai versi yang tersedia (misal quantized)

    try:
        # Call Ollama API /api/generate
        ollama_response = requests.post(
            f'{OLLAMA_BASE_URL}/api/generate',
            json={
                'model': model_to_use,
                'prompt': f"{FINANCE_SYSTEM_PROMPT}\n\nPertanyaan pengguna: {prompt}",
                'stream': False
            },
            timeout=300
        )

        # Tangani 404 secara spesifik: model belum di-pull
        if ollama_response.status_code == 404:
            is_error_response = True
            ai_response = (
                f"🔴 **Model `{model}` belum diinstall di Ollama.**\n\n"
                f"Jalankan perintah berikut di terminal untuk mengunduh model:\n\n"
                f"```\nollama pull {model}\n```\n\n"
                f"⏳ Proses download mungkin membutuhkan waktu beberapa menit tergantung kecepatan internet.\n\n"
                f"Setelah selesai, refresh halaman dan coba lagi."
            )
        else:
            ollama_response.raise_for_status()
            result = ollama_response.json()
            ai_response = result.get('response', 'Maaf, tidak ada respons dari AI.')

    except requests.exceptions.ConnectionError:
        is_error_response = True
        ai_response = (
            "⚠️ **Ollama tidak berjalan atau tidak terdeteksi.**\n\n"
            "Pastikan Ollama sudah terinstal dan aktif di komputer Anda.\n\n"
            "**Cara setup:**\n"
            "1. Download Ollama dari [ollama.com](https://ollama.com)\n"
            "2. Install dan jalankan Ollama\n"
            "3. Buka terminal, jalankan:\n"
            f"   `ollama pull {model}`\n"
            "4. Refresh halaman dan coba lagi"
        )
    except requests.exceptions.Timeout:
        is_error_response = True
        ai_response = (
            f"⏳ **Request timeout setelah 5 menit.**\n\n"
            f"Model `{model}` sangat besar dan membutuhkan waktu lama. "
            f"Coba pertanyaan yang lebih singkat, atau gunakan **Qwen3 14B** yang lebih cepat."
        )
    except Exception as e:
        is_error_response = True
        ai_response = f"❌ **Error tidak terduga:** {str(e)}"

    # Simpan ke history hanya jika BUKAN pesan error dan user mengaktifkan save_history
    if user.save_history and not is_error_response:
        ChatHistory(
            user=user,
            model_name=model,
            prompt=prompt,
            response=ai_response
        )
        commit()

    # Log activity (selalu dicatat)
    ActivityLog(
        user=user,
        action='Menggunakan AI Chat',
        detail=f'Model: {AVAILABLE_MODELS[model]["name"]} | Status: {"Error" if is_error_response else "OK"}'
    )
    commit()

    return jsonify({
        'response': ai_response,
        'model': AVAILABLE_MODELS[model]['name'],
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'is_error': is_error_response
    })


# ==================== FILE UPLOAD ====================

@app.route('/api/upload', methods=['POST'])
@login_required
@db_session
def api_upload():
    user = User[session['user_id']]

    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang dikirim'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Tidak ada file yang dipilih'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Format file tidak diizinkan. Hanya PDF dan Excel (.xlsx, .xls)'}), 400

    original_name = secure_filename(file.filename)
    ext = original_name.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
    file.save(file_path)
    file_size = os.path.getsize(file_path)

    # Save to DB
    uploaded = UploadedFile(
        user=user,
        filename=unique_name,
        original_name=original_name,
        file_type=ext,
        file_size=file_size
    )
    commit()

    # Log activity
    ActivityLog(
        user=user,
        action='Mengupload file',
        detail=f'File: {original_name} ({ext.upper()}, {file_size // 1024} KB)'
    )
    commit()

    return jsonify({
        'status': 'ok',
        'file': {
            'id': uploaded.id,
            'name': original_name,
            'type': ext.upper(),
            'size': f'{file_size // 1024} KB'
        }
    })


@app.route('/api/files', methods=['GET'])
@login_required
@db_session
def api_files():
    user = User[session['user_id']]
    ids = raw_query_ids(
        'SELECT id FROM tbl_uploaded_file WHERE user = $uid ORDER BY created_at DESC LIMIT 20',
        {'uid': user.id}
    )
    files = [UploadedFile[i] for i in ids]
    return jsonify({
        'files': [{
            'id': f.id,
            'name': f.original_name,
            'type': f.file_type.upper(),
            'size': f'{f.file_size // 1024} KB',
            'date': f.created_at.strftime('%d/%m/%Y %H:%M')
        } for f in files]
    })


@app.route('/api/files/<int:file_id>/delete', methods=['POST'])
@login_required
@db_session
def api_delete_file(file_id):
    user = User[session['user_id']]
    f = UploadedFile.get(id=file_id, user=user)
    if not f:
        return jsonify({'error': 'File tidak ditemukan'}), 404

    # Delete physical file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    name = f.original_name
    f.delete()
    commit()

    ActivityLog(user=user, action='Menghapus file', detail=f'File: {name}')
    commit()

    return jsonify({'status': 'ok'})


# ==================== ACTIVITY HISTORY ====================

@app.route('/api/activities', methods=['GET'])
@login_required
@db_session
def api_activities():
    user = User[session['user_id']]
    ids = raw_query_ids(
        'SELECT id FROM tbl_activity_log WHERE user = $uid ORDER BY created_at DESC LIMIT 50',
        {'uid': user.id}
    )
    activities = [ActivityLog[i] for i in ids]
    return jsonify({
        'activities': [{
            'action': a.action,
            'detail': a.detail,
            'time': a.created_at.strftime('%d/%m/%Y %H:%M')
        } for a in activities]
    })


# ==================== CHAT HISTORY ====================

@app.route('/api/chat-history', methods=['GET'])
@login_required
@db_session
def api_chat_history():
    user = User[session['user_id']]
    ids = raw_query_ids(
        'SELECT id FROM tbl_chat_history WHERE user = $uid ORDER BY created_at DESC LIMIT 50',
        {'uid': user.id}
    )
    chats = [ChatHistory[i] for i in ids]
    return jsonify({
        'chats': [{
            'id': c.id,
            'model': c.model_name,
            'prompt': c.prompt[:100],
            'response': c.response[:200],
            'time': c.created_at.strftime('%d/%m/%Y %H:%M')
        } for c in chats]
    })


@app.route('/api/chat-history/<int:chat_id>/delete', methods=['POST'])
@login_required
@db_session
def api_delete_chat(chat_id):
    user = User[session['user_id']]
    c = ChatHistory.get(id=chat_id, user=user)
    if not c:
        return jsonify({'error': 'Chat tidak ditemukan'}), 404
    c.delete()
    commit()
    return jsonify({'status': 'ok'})


# ==================== PROFILE ====================

@app.route('/profile', methods=['GET', 'POST'])
@login_required
@db_session
def profile():
    user = User[session['user_id']]
    ids = raw_query_ids(
        'SELECT id FROM tbl_activity_log WHERE user = $uid ORDER BY created_at DESC LIMIT 10',
        {'uid': user.id}
    )
    activities = [ActivityLog[i] for i in ids]

    if request.method == 'POST':
        old_nama = user.nama
        old_email = user.email
        old_phone = user.phone
        old_location = user.location
        old_bio = user.bio

        user.nama = request.form.get('nama', user.nama).strip()
        new_email = request.form.get('email', user.email).strip().lower()

        # Cek jika email berubah dan sudah dipakai user lain
        if new_email != user.email:
            existing = User.get(email=new_email)
            if existing:
                flash('Email sudah digunakan oleh akun lain.', 'danger')
                return redirect(url_for('profile'))
            user.email = new_email

        user.phone = request.form.get('phone', '').strip()
        user.location = request.form.get('location', '').strip()
        user.bio = request.form.get('bio', '').strip()
        commit()

        # Log perubahan detail
        changes = []
        if old_nama != user.nama:
            changes.append(f'Nama: {old_nama} → {user.nama}')
        if old_email != user.email:
            changes.append(f'Email: {old_email} → {user.email}')
        if old_phone != user.phone:
            changes.append(f'Telepon diperbarui')
        if old_location != user.location:
            changes.append(f'Lokasi diperbarui')
        if old_bio != user.bio:
            changes.append(f'Bio diperbarui')

        if changes:
            ActivityLog(
                user=user,
                action='Mengubah data profil',
                detail='; '.join(changes)
            )
            commit()

        session['user_nama'] = user.nama
        flash('Profil berhasil disimpan!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user, activities=activities)


# ==================== PROFILE SETTINGS (AJAX) ====================

@app.route('/profile/settings', methods=['POST'])
@login_required
@db_session
def profile_settings():
    user = User[session['user_id']]
    data = request.get_json()

    changes = []

    if 'notif_email' in data:
        old_val = user.notif_email
        user.notif_email = bool(data['notif_email'])
        if old_val != user.notif_email:
            changes.append(f"Notifikasi Email: {'Aktif' if user.notif_email else 'Non-aktif'}")

    if 'dark_mode' in data:
        old_val = user.dark_mode
        user.dark_mode = bool(data['dark_mode'])
        if old_val != user.dark_mode:
            changes.append(f"Mode Gelap: {'Aktif' if user.dark_mode else 'Non-aktif'}")

    if 'save_history' in data:
        old_val = user.save_history
        user.save_history = bool(data['save_history'])
        if old_val != user.save_history:
            changes.append(f"Simpan Riwayat: {'Aktif' if user.save_history else 'Non-aktif'}")

    commit()

    if changes:
        ActivityLog(
            user=user,
            action='Mengubah pengaturan',
            detail='; '.join(changes)
        )
        commit()

    return jsonify({'status': 'ok', 'dark_mode': user.dark_mode})


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# ==================== RUN ====================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5100))
    app.run(debug=True, host='0.0.0.0', port=port)
