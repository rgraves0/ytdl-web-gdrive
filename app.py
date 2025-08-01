```python
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import yt_dlp
import os
import subprocess
import hashlib
import json
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-here')

# Flask-Login စတင်ပြင်ဆင်ခြင်း
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Flask-Login အတွက် User အမျိုးအစား
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# User ကို ပြန်လည်ဖွင့်ရန်
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Environment မှ credentials များကို ဖတ်ရန်
USERNAME_HASH = os.environ.get('USERNAME_HASH')
PASSWORD_HASH = os.environ.get('PASSWORD_HASH')
RCLONE_CONFIG = os.environ.get('RCLONE_CONFIG')

# rclone config ကို ဖိုင်ထဲသို့ ရေးရန်
if RCLONE_CONFIG:
    with open('/app/rclone.conf', 'w') as f:
        f.write(RCLONE_CONFIG)

# ဒေါင်းလုပ်ဖိုင်များသိမ်းရန်နေရာ
DOWNLOAD_DIR = '/app/downloads'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Admin အတွက်သာ ဝင်ခွင့်ပြုရန်
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') != 'admin':
            flash('ဝင်ခွင့်မရှိပါ။', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        username_hash = hashlib.sha256(username.encode()).hexdigest()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if username_hash == USERNAME_HASH and password_hash == PASSWORD_HASH:
            user = User('admin')
            login_user(user)
            session['user_id'] = 'admin'
            return redirect(url_for('index'))
        else:
            flash('အသုံးပြုသူအမည် သို့မဟုတ် စကားဝှက် မမှန်ကန်ပါ။', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    flash('အောင်မြင်စွာ ထွက်လိုက်ပါပြီ။', 'success')
    return redirect(url_for('login'))

@app.route('/download', methods=['POST'])
@login_required
@admin_required
def download():
    url = request.form['url']
    destination = request.form['destination']
    try:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        # rclone ဖြင့် cloud သို့ အပ်လုပ်ရန်
        if destination in ['gdrive', 'onedrive']:
            rclone_cmd = [
                'rclone', 'copy', filename,
                f'{destination}:/Downloads/',
                '--config', '/app/rclone.conf'
            ]
            result = subprocess.run(rclone_cmd, capture_output=True, text=True)
            if result.returncode == 0:
                flash(f'ဖိုင်ကို {destination} သို့ အပ်လုပ်ပြီးပါပြီ။', 'success')
            else:
                flash(f'rclone error: {result.stderr}', 'error')
            
            # ဒေါင်းလုပ်ထားသောဖိုင်ကို ဖျက်ရန်
            os.remove(filename)
        else:
            flash('မမှန်ကန်သော destination ရွေးချယ်မှု။', 'error')
        
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'ဒေါင်းလုပ်မှု မအောင်မြင်ပါ: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```