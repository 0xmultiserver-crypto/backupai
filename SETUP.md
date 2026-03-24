# Setup Kira di VPS Baru

Panduan setup Kira (AI Assistant) dengan personality & memory lengkap.

---

## 🚀 Quick Start

### 1. Install OpenClaw

```bash
# Via npm
npm install -g openclaw

# Atau download binary dari GitHub releases
```

### 2. Clone Workspace

```bash
# Buat direktori workspace
mkdir -p ~/.openclaw

# Clone dari GitHub
git clone https://github.com/0xmultiserver-crypto/backupai.git ~/.openclaw/workspace

# Masuk ke workspace
cd ~/.openclaw/workspace
```

### 3. Install Dependencies (Opsional)

```bash
# Kalo butuh Playwright untuk otomasi browser
npm install
npx playwright install chromium
npx playwright install-deps chromium
```

### 4. Setup Environment

```bash
# Setup API keys (sesuaikan provider)
export OPENROUTER_API_KEY="your_key_here"
export ANTHROPIC_API_KEY="your_key_here"

# Atau edit ~/.bashrc biar permanen
echo 'export OPENROUTER_API_KEY="your_key_here"' >> ~/.bashrc
```

### 5. Start Gateway

```bash
openclaw gateway start

# Atau kalo udah pernah di-setup
openclaw gateway restart
```

---

## ✅ Verifikasi

Setelah restart, cek personality udah apply:

1. Chat ke bot Telegram lo
2. Kira harusnya jawab pake gaya: "woy", "gue", "lu", "bro"
3. Respons singkat & to the point

Kalo masih formal, restart lagi:
```bash
openclaw gateway restart
```

---

## 📁 File Penting

File ini wajib ada biar Kira jadi "diri sendiri":

| File | Fungsi |
|------|--------|
| `SOUL.md` | Personality (gue, lu, woy, casual) |
| `MEMORY.md` | User preferences & long-term memory |
| `USER.md` | Data tentang user |
| `AGENTS.md` | Rules & guidelines |
| `HEARTBEAT.md` | Task periodic |
| `memory/` | Daily logs |

---

## 🔧 Backup & Restore

### Backup (dari VPS lama)
```bash
cd ~/.openclaw/workspace
./kira-backup.sh backup
```

### Restore (di VPS baru)
```bash
./kira-backup.sh restore
```

---

## 🐛 Troubleshooting

### Gateway gak mau start
```bash
# Cek error
openclaw gateway status

# Atau start manual
cd ~/.openclaw/workspace
openclaw gateway start --foreground
```

### Personality masih formal
- Pastikan `SOUL.md` ada di workspace
- Restart gateway: `openclaw gateway restart`
- Clear session: `/new` atau `/reset`

### Missing API Key
- Set environment variable
- Atau edit `openclaw.json`

---

## 📞 Support

Repo: https://github.com/0xmultiserver-crypto/backupai

Last updated: 24 Maret 2026
