#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

def send_screenshot(image_path):
    """Kirim screenshot ke Telegram"""
    
    # Load token dari file
    env_path = '/root/.openclaw/workspace/.env.telegram'
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    token = os.getenv('BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID', '1160205666')
    
    if not token:
        print("❌ Token gak ketemu! Cek .env.telegram")
        return
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    
    try:
        with open(image_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': chat_id, 'caption': '📸 Screenshot VNC Desktop'}
            
            response = requests.post(url, files=files, data=data, timeout=30)
            
            if response.status_code == 200:
                print(f"✅ Screenshot terkirim ke Telegram!")
            else:
                print(f"❌ Gagal: {response.text}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        send_screenshot(sys.argv[1])
    else:
        # Default screenshot desktop
        send_screenshot('/root/.openclaw/workspace/vnc_desktop.png')
