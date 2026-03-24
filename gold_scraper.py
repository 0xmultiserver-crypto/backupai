import requests
import time
import json
from datetime import datetime

class GoldScraper:
    def __init__(self):
        self.last_price = None
        self.prices = []
        
    def get_gold_price(self):
        """Scrape harga XAUUSD dari Yahoo Finance"""
        try:
            # Yahoo Finance API for Gold
            url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()
            
            if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                result = data['chart']['result'][0]
                meta = result['meta']
                
                price = meta.get('regularMarketPrice', 0)
                prev_close = meta.get('previousClose', 0)
                change = price - prev_close
                change_pct = (change / prev_close) * 100 if prev_close else 0
                
                return {
                    'symbol': 'XAUUSD',
                    'price': round(price, 2),
                    'change': round(change, 2),
                    'change_pct': round(change_pct, 2),
                    'time': datetime.now().strftime('%H:%M:%S')
                }
            
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def analyze(self, price_data):
        """Analisis sederhana"""
        if not price_data:
            return None
            
        price = price_data['price']
        self.prices.append(price)
        
        # Keep last 50 prices
        if len(self.prices) > 50:
            self.prices = self.prices[-50:]
        
        signal = None
        
        if len(self.prices) >= 20:
            # Simple Moving Average
            ma20 = sum(self.prices[-20:]) / 20
            
            # RSI calculation (simplified)
            if len(self.prices) >= 14:
                gains = []
                losses = []
                for i in range(-14, 0):
                    change = self.prices[i] - self.prices[i-1]
                    if change > 0:
                        gains.append(change)
                    else:
                        losses.append(abs(change))
                
                avg_gain = sum(gains) / 14 if gains else 0
                avg_loss = sum(losses) / 14 if losses else 0
                
                if avg_loss == 0:
                    rsi = 100
                else:
                    rs = avg_gain / avg_loss
                    rsi = 100 - (100 / (1 + rs))
                
                # Signal logic
                if rsi < 30 and price > ma20:
                    signal = {
                        'type': 'BUY',
                        'strength': 'STRONG' if rsi < 25 else 'MODERATE',
                        'entry': price,
                        'sl': round(price - 5, 2),
                        'tp': round(price + 10, 2),
                        'reason': f'RSI Oversold ({rsi:.1f}) + Above MA20'
                    }
                elif rsi > 70 and price < ma20:
                    signal = {
                        'type': 'SELL', 
                        'strength': 'STRONG' if rsi > 75 else 'MODERATE',
                        'entry': price,
                        'sl': round(price + 5, 2),
                        'tp': round(price - 10, 2),
                        'reason': f'RSI Overbought ({rsi:.1f}) + Below MA20'
                    }
        
        return {
            'price': price_data,
            'ma20': round(ma20, 2) if len(self.prices) >= 20 else None,
            'rsi': round(rsi, 1) if len(self.prices) >= 14 else None,
            'signal': signal
        }
    
    def run(self, interval=60):
        """Jalan terus, analisis setiap interval detik"""
        print("🚀 Gold Scraper Started (XAUUSD)")
        print("=" * 50)
        
        while True:
            try:
                price_data = self.get_gold_price()
                analysis = self.analyze(price_data)
                
                if analysis:
                    p = analysis['price']
                    print(f"[{p['time']}] XAUUSD: {p['price']} ({p['change']:+.2f}, {p['change_pct']:+.2f}%)")
                    
                    if analysis['ma20']:
                        print(f"  MA20: {analysis['ma20']} | RSI: {analysis['rsi']}")
                    
                    if analysis['signal']:
                        s = analysis['signal']
                        print(f"\n🔥 SIGNAL {s['strength']} {s['type']}!")
                        print(f"   Entry: {s['entry']}")
                        print(f"   SL: {s['sl']} | TP: {s['tp']}")
                        print(f"   Reason: {s['reason']}\n")
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n✋ Stopped by user")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    scraper = GoldScraper()
    scraper.run(interval=30)  # Update setiap 30 detik
