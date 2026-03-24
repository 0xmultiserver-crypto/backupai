import requests
import time
import json
import os
from datetime import datetime

class XauMonitor:
    def __init__(self):
        self.last_price = None
        self.prices = []
        self.high = None
        self.low = None
        
        # Load token dari file .env (jangan hardcode!)
        self.bot_token = self.load_token()
        self.chat_id = "1160205666"  # Chat ID lo
        
    def load_token(self):
        """Load token dari file .env (AMAN)"""
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('BOT_TOKEN='):
                        return line.strip().split('=', 1)[1]
        except:
            pass
        return None
    
    def send_telegram(self, message):
        """Kirim alert ke Telegram"""
        if not self.bot_token:
            print("⚠️ Token belum di-set! Buat file .env isi: BOT_TOKEN=token_lo")
            return
            
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            print(f"Telegram error: {e}")
    
    def get_xau_price(self):
        """Ambil harga XAU/USD real-time"""
        try:
            url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            resp = requests.get(url, headers=headers, timeout=10)
            data = resp.json()
            
            if 'chart' in data and data['chart']['result']:
                result = data['chart']['result'][0]
                meta = result['meta']
                
                price = meta.get('regularMarketPrice', 0)
                prev = meta.get('previousClose', 0)
                high = meta.get('regularMarketDayHigh', price)
                low = meta.get('regularMarketDayLow', price)
                
                return {
                    'price': round(price, 2),
                    'prev': round(prev, 2),
                    'high': round(high, 2),
                    'low': round(low, 2),
                    'change': round(price - prev, 2),
                    'change_pct': round(((price - prev) / prev) * 100, 2) if prev else 0,
                    'time': datetime.now().strftime('%H:%M:%S')
                }
        except Exception as e:
            print(f"Error fetch: {e}")
        return None
    
    def calculate_indicators(self):
        """Hitung RSI & Moving Averages"""
        if len(self.prices) < 14:
            return None
            
        # RSI
        gains = []
        losses = []
        for i in range(-14, 0):
            change = self.prices[i] - self.prices[i-1]
            if change > 0:
                gains.append(change)
            else:
                losses.append(abs(change))
        
        avg_gain = sum(gains) / 14 if gains else 0.001
        avg_loss = sum(losses) / 14 if losses else 0.001
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        # Moving Averages
        ma10 = sum(self.prices[-10:]) / 10 if len(self.prices) >= 10 else None
        ma20 = sum(self.prices[-20:]) / 20 if len(self.prices) >= 20 else None
        ma50 = sum(self.prices[-50:]) / 50 if len(self.prices) >= 50 else None
        
        return {
            'rsi': round(rsi, 1),
            'ma10': round(ma10, 2) if ma10 else None,
            'ma20': round(ma20, 2) if ma20 else None,
            'ma50': round(ma50, 2) if ma50 else None
        }
    
    def check_signals(self, price_data, indi):
        """Cek sinyal trading"""
        if not indi or not price_data:
            return None
            
        price = price_data['price']
        rsi = indi['rsi']
        ma20 = indi['ma20']
        
        signals = []
        
        # Signal 1: RSI Oversold/Overbought
        if rsi < 30:
            signals.append({
                'type': '🟢 BUY',
                'strength': 'STRONG' if rsi < 25 else 'MODERATE',
                'reason': f'RSI Oversold ({rsi})',
                'entry': price,
                'sl': round(price - 8, 2),
                'tp1': round(price + 15, 2),
                'tp2': round(price + 25, 2)
            })
        elif rsi > 70:
            signals.append({
                'type': '🔴 SELL',
                'strength': 'STRONG' if rsi > 75 else 'MODERATE',
                'reason': f'RSI Overbought ({rsi})',
                'entry': price,
                'sl': round(price + 8, 2),
                'tp1': round(price - 15, 2),
                'tp2': round(price - 25, 2)
            })
        
        # Signal 2: MA Cross (Price vs MA20)
        if ma20:
            if price > ma20 * 1.002 and rsi > 50:
                signals.append({
                    'type': '🟢 BUY',
                    'strength': 'WEAK',
                    'reason': f'Price above MA20 ({ma20})',
                    'entry': price,
                    'sl': round(ma20 - 5, 2),
                    'tp1': round(price + 10, 2),
                    'tp2': None
                })
            elif price < ma20 * 0.998 and rsi < 50:
                signals.append({
                    'type': '🔴 SELL',
                    'strength': 'WEAK',
                    'reason': f'Price below MA20 ({ma20})',
                    'entry': price,
                    'sl': round(ma20 + 5, 2),
                    'tp1': round(price - 10, 2),
                    'tp2': None
                })
        
        return signals
    
    def run(self):
        """Monitor 24/7"""
        print("🚀 XAU/USD 24/7 Monitor Started")
        print("=" * 50)
        print("⚠️  Jangan lupa buat file .env isi BOT_TOKEN=token_lo")
        print("=" * 50)
        
        last_signal_time = 0
        
        while True:
            try:
                # Get price
                data = self.get_xau_price()
                if not data:
                    time.sleep(5)
                    continue
                
                # Store price
                self.prices.append(data['price'])
                if len(self.prices) > 100:
                    self.prices = self.prices[-100:]
                
                # Calculate indicators
                indi = self.calculate_indicators()
                
                # Print status
                print(f"[{data['time']}] XAU: {data['price']} ({data['change']:+.2f}, {data['change_pct']:+.2f}%)")
                
                if indi:
                    print(f"  RSI: {indi['rsi']} | MA20: {indi['ma20']} | Range: {data['low']} - {data['high']}")
                
                # Check signals (max 1 per 5 menit biar gak spam)
                current_time = time.time()
                if indi and (current_time - last_signal_time) > 300:
                    signals = self.check_signals(data, indi)
                    
                    if signals:
                        for sig in signals:
                            msg = f"""
🔥 *SIGNAL {sig['strength']} {sig['type']}*

💰 Entry: `{sig['entry']}`
🛑 SL: `{sig['sl']}`
🎯 TP1: `{sig['tp1']}`
{f"🎯 TP2: `{sig['tp2']}`" if sig['tp2'] else ""}

📊 {sig['reason']}
RSI: {indi['rsi']} | MA20: {indi['ma20']}

⏰ {data['time']} UTC
"""
                            print(f"\n🚨 SIGNAL: {sig['type']} @ {sig['entry']}\n")
                            self.send_telegram(msg)
                            last_signal_time = current_time
                
                # Check user's position (if you want to track P/L)
                # Add code here to check if price hits SL/TP for existing positions
                
                time.sleep(30)  # Update setiap 30 detik
                
            except KeyboardInterrupt:
                print("\n✋ Stopped")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(10)

if __name__ == "__main__":
    monitor = XauMonitor()
    monitor.run()
