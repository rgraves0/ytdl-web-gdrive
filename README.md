# yt-dlp Web UI with rclone

ဤသည်မှာ yt-dlp ကို အသုံးပြု၍ ဗီဒီယိုဒေါင်းလုပ်နိုင်သော Flask အခြေပြု Web UI တစ်ခုဖြစ်သည်။ ၎င်းတွင် username/password ဖြင့် လော့ဂ်အင်စနစ်ပါရှိပြီး၊ ဒေါင်းလုပ်ထားသော ဖိုင်များကို rclone သုံးပြီး Google Drive သို့မဟုတ် OneDrive for Business တွင် သိမ်းဆည်းနိုင်သည်။ ဤ repository ကို Railway.app တွင် deploy လုပ်ရန် ဒီဇိုင်းပြုလုပ်ထားသည်။

## စတင်ပုံ

### လိုအပ်ချက်များ
- Python 3.8+
- Railway.app အကောင့်
- Google Drive သို့မဟုတ် OneDrive for Business အတွက် rclone config
- GitHub အကောင့်

### တပ်ဆင်နည်းလမ်းများ

1. **Repository ကို Fork လုပ်ပါ**:
   - ဤ repository ကို သင့် GitHub အကောင့်သို့ fork လုပ်ပါ။

2. **rclone Config ပြင်ဆင်ပါ**:
   - သင့်ကွန်ပြူတာတွင် rclone ကို ထည့်သွင်းပါ (`rclone config` ဖြင့် Google Drive နှင့် OneDrive အတွက် remote များ ဖန်တီးပါ)။
   - Google Drive remote အမည်ကို `gdrive` ဟု သတ်မှတ်ပါ။
   - OneDrive remote အမည်ကို `onedrive` ဟု သတ်မှတ်ပါ။
   - rclone.conf ဖိုင်ထဲမှ အကြောင်းအရာကို ကူးယူပါ။

3. **Username နှင့် Password Hash များ ဖန်တီးပါ**:
   - Python ကို သုံးပြီး သင်လိုချင်သော username နှင့် password ၏ SHA256 hash များကို ဖန်တီးပါ။
     ```python
     import hashlib
     print(hashlib.sha256("your_username".encode()).hexdigest())
     print(hashlib.sha256("your_password".encode()).hexdigest())
     ```
   - ရလာသော hash များကို မှတ်ထားပါ။

4. **Railway.app တွင် Deploy လုပ်ပါ**:
   - Railway.app သို့ ဝင်ပါ။
   - "New Project" > "GitHub Repo" ကို ရွေးပြီး သင် fork လုပ်ထားသော repository ကို ချိတ်ဆက်ပါ�。
   - Environment variables များကို အောက်ပါအတိုင်း ထည့်သွင်းပါ:
     ```
     FLASK_SECRET_KEY=သင့်လျှို့ဝှက်ကီး (ဥပမာ: randomstring123)
     USERNAME_HASH=သင့် username ၏ SHA256 hash
     PASSWORD_HASH=သင့် password ၏ SHA256 hash
     RCLONE_CONFIG=သင့် rclone.conf ဖိုင်ထဲမှ အကြောင်းအရာတစ်ခုလုံး
     PORT=5000
     ```
   - Deploy လုပ်ပြီးသည်နှင့် Railway.app က ပေးသော URL တွင် Web UI ကို ဝင်ကြည့်နိုင်ပါသည်။

### အသုံးပြုနည်း
1. Web UI သို့ ဝင်ပါ (Railway.app မှ ပေးသော URL)။
2. သင်သတ်မှတ်ထားသော username နှင့် password ဖြင့် လော့ဂ်အင်ဝင်ပါ။
3. ဒေါင်းလုပ်လိုသော ဗီဒီယို URL ထည့်ပါ။
4. Google Drive သို့မဟုတ် OneDrive တွင် သိမ်းမည့်နေရာကို ရွေးပါ။
5. "ဒေါင်းလုပ်ရန်" ခလုတ်ကို နှိပ်ပါ။
6. ဖိုင်သည် သင်ရွေးချယ်ထားသော cloud storage သို့ အပ်လုပ်သွားပါမည်။

### မှတ်ချက်များ
- rclone သည် Railway.app ၏ container ထဲတွင် ဖိုင်များကို cloud သို့ တင်ပြီးနောက် local ဖိုင်များကို ဖျက်ပါသည်။
- လုံခြုံရေးအတွက် FLASK_SECRET_KEY နှင့် rclone config ကို မည်သူမျှ မမျှဝေပါနှင့်။
- yt-dlp သည် YouTube နှင့် အခြားဝဘ်ဆိုဒ်များစွာကို ထောက်ပံ့ပေးသည်။

### ပြဿနာဖြေရှင်းနည်း
- အကယ်၍ deploy မအောင်မြင်ပါက Railway.app ၏ logs ကို စစ်ဆေးပါ။
- rclone config မမှန်ကန်ပါက `rclone config` ဖြင့် ပြန်လည်စစ်ဆေးပါ။

## လိုင်စင်
MIT License
