# Optimasi OpenClaw untuk Respon Lebih Cepat

Panduan ini merangkum setting yang telah kita konfigurasi untuk membuat OpenClaw lebih cepat dan efisien.

---

## 🔧 Konfigurasi yang Diubah

### 1. `maxTokens`: 300
- **Default**: ~4096 token
- **Fungsi**: Membatasi panjang output
- **Efek**: Respons lebih pendek, hemat token, lebih cepat selesai

### 2. `temperature`: 0.3
- **Default**: ~0.7
- **Fungsi**: Mengontrol "kreativitas" vs konsistensi
- **Efek**: 
  - Nilai rendah (0.1-0.3) = lebih fokus, langsung ke inti
  - Nilai tinggi (0.7-1.0) = lebih kreatif, bisa rambat

### 3. `maxIterations`: 3
- **Default**: 10+
- **Fungsi**: Membatasi jumlah putaran tool calls
- **Efek**: Loop berhenti lebih cepat, tidak berbelit-belit

### 4. `streaming`: `true`
- **Default**: `partial` atau `false`
- **Fungsi**: Mengaktifkan real-time text output
- **Efek**: Teks muncul bertahap saat diproses, terasa lebih cepat

### 5. `thinkingDefault`: `full` (opsional)
- **Pilihan**: `off`, `low`, `medium`, `full`
- **Fungsi**: Mengontrol tampilan proses berpikir
- **Catatan**: `full` menampilkan reasoning lengkap (bisa bikin lambat tapi lebih transparan)

---

## 📝 Cara Mengubah Konfigurasi

File konfigurasi ada di:
```
/root/.openclaw/openclaw.json
```

### Edit Langsung

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "openrouter/moonshotai/kimi-k2.5",
        "maxTokens": 300,
        "temperature": 0.3,
        "maxIterations": 3
      },
      "thinkingDefault": "full",
      ...
    }
  },
  "channels": {
    "telegram": {
      "streaming": true,
      ...
    }
  }
}
```

### Restart Gateway

Setelah edit, restart agar perubahan aktif:

```bash
openclaw gateway restart
# atau
pkill -USR1 openclaw
```

---

## 🧪 Verifikasi Setting

Cek status aktif dengan:
```bash
openclaw status
# atau
/session_status
```

 atau lihat langsung di file:
```bash
cat /root/.openclaw/openclaw.json | grep -A 10 '"model"'
```

---

## ⚡ Tips Tambahan

1. **Pilih Model yang Tepat**
   - Model kecil (Haiku, Flash) = lebih cepat
   - Model besar (Opus, Pro) = lebih "pintar" tapi lambat

2. **Gunakan Cache**
   - Hasil tool calls akan di-cache otomatis
   - Sebutkan `/cache` untuk melihat hit rate

3. **Batasi Context**
   - Clear history jika terlalu panjang
   - Gunakan summary untuk percakapan panjang

4. **Optimasi Tool Calling**
   - Hindari loop tool calls yang tidak perlu
   - Set `maxIterations` rendah untuk respons cepat

---

## 📊 Perbandingan Performa

| Setting | Default | Optimized (Ini) |
|---------|---------|-----------------|
| maxTokens | 4096 | 300 |
| temperature | 0.7 | 0.3 |
| maxIterations | 10+ | 3 |
| streaming | partial | true |
| Output | Panjang & rambat | Singkat & to-the-point |
| Cocok untuk | Brainstorming | Produktivitas cepat |

---

## 🔄 Balik ke Default

Kalau ingin kembalikan setting default, cukup hapus parameter custom atau ubah ke:
```json
{
  "maxTokens": null,
  "temperature": null,
  "maxIterations": null,
  "streaming": "partial",
  "thinkingDefault": "off"
}
```

---

Dibuat: 2026-03-24
Versi: OpenClaw 2026.3.11
Model: openrouter/moonshotai/kimi-k2.5
