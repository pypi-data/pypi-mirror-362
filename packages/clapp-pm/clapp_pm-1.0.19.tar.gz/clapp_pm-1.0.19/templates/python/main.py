#!/usr/bin/env python3
"""
Hello Python - clapp Örnek Uygulaması

Bu uygulama clapp için Python uygulaması geliştirme örneğidir.
"""

import sys
import os
from datetime import datetime

def main():
    """Ana fonksiyon"""
    print("=" * 50)
    print("🚀 Hello Python - clapp Örnek Uygulaması")
    print("=" * 50)
    
    # Temel bilgiler
    print(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python Sürümü: {sys.version}")
    print(f"📁 Çalışma Dizini: {os.getcwd()}")
    
    # Kullanıcı etkileşimi
    name = input("\n👋 Adınızı girin: ")
    if name.strip():
        print(f"Merhaba {name}! clapp'e hoş geldiniz!")
    else:
        print("Merhaba! clapp'e hoş geldiniz!")
    
    # Örnek işlemler
    print("\n🔢 Basit Hesaplama Örneği:")
    try:
        a = float(input("Birinci sayıyı girin: "))
        b = float(input("İkinci sayıyı girin: "))
        
        print(f"Toplam: {a + b}")
        print(f"Çarpım: {a * b}")
        print(f"Bölüm: {a / b if b != 0 else 'Tanımsız'}")
        
    except ValueError:
        print("❌ Geçersiz sayı girişi!")
    except ZeroDivisionError:
        print("❌ Sıfıra bölme hatası!")
    
    print("\n✅ Uygulama başarıyla tamamlandı!")
    print("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Uygulama kullanıcı tarafından sonlandırıldı.")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        sys.exit(1) 