# 🛰️ py-telecast

A lightweight and plug-and-play **broadcast module** for Python Telegram Bots using `python-telegram-bot` v20+. Developed by **Manji Devs**, this module supports:
- JSON (default)
- SQLite
- MongoDB

> Simple. Powerful. Flexible.


## ✨ Features
- 📣 Broadcast any message (text, media, buttons, hyperlinks)
- 📥 Supports reply-to-message for broadcasting
- 👤 User database with JSON / SQLite / MongoDB backends
- 🧠 Smart message formatting (Markdown & buttons preserved)
- 🛡️ Sudo-only broadcasting
- 📊 Stats report after broadcast


## 🔧 Installation
```bash
pip install py-telecast
```


**Requirements**: Python 3.10+ and python-telegram-bot>=20.6


## 🚀 Quick Start

### 1. Basic Setup (`main.py`)
```python
from telegram.ext import Application
from pytelecast import init_broadcast

app = Application.builder().token("YOUR_BOT_TOKEN").build()

init_broadcast(
    app,
    sudo_users=[123456789],  # required
    db_type="json",          # json (default) | sqlite | mongo
    db_url=None              # optional for mongo: "mongodb+srv://..."
)

app.run_polling()
```

### 2. Broadcasting
1. Reply to any message with:
   ```
   /broadcast
   ```
2. Bot will show a preview with confirmation buttons
3. After confirmation, sends to all users with stats:
   ```
   ✅ Broadcast completed.
   ◇ Total Users: 10
   ◇ Successful: 9
   ◇ Blocked Users: 1
   ◇ Deleted Accounts: 0
   ◇ Unsuccessful: 0
   ```


## 🛠️ Supported DB Backends
| Type   | Configuration |
|--------|---------------|
| JSON   | Default (no config needed) |
| SQLite | `db_type="sqlite"` |
| MongoDB | `db_type="mongo"`, `db_url="mongodb+srv://..."` |


## 📁 Requirements
Core Dependencies:
- `python-telegram-bot>=20.6`

Optional (for MongoDB):
- `pymongo>=4.6.3`


## 🧩 Integration Tips
1. Works seamlessly with existing PTB bots
2. Automatic database structure creation
3. Logs indicate active backend during startup
4. All broadcast attempts are logged with timestamps
5. Supports both polling and webhook setups

## 🌐 Links
- GitHub: [github.com/your-org/py-telecast](https://github.com/manjidevs/py-telecast)
- PyPI: [pypi.org/project/py-telecast](https://pypi.org/project/py-telecast)
- Python-Telegram-Bot Docs: [docs.python-telegram-bot.org](https://docs.python-telegram-bot.org)

## 📄 License
MIT License © 2023 Manji Devs
