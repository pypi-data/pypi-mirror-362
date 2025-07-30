#!/usr/bin/env python3
"""
Hello Python - Basit Python merhaba dünya uygulaması
clapp paket yöneticisi için örnek uygulama
"""

import sys
import os
from datetime import datetime

def main():
    """Ana fonksiyon"""
    print("🐍 Merhaba Python Dünyası!")
    print("=" * 40)
    
    # Uygulama bilgileri
    print(f"📦 Uygulama: hello-python")
    print(f"🔢 Sürüm: 1.0.0")
    print(f"💻 Dil: Python {sys.version.split()[0]}")
    print(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Sistem bilgileri
    print(f"\n🖥️  Sistem Bilgileri:")
    print(f"   İşletim Sistemi: {os.name}")
    print(f"   Python Sürümü: {sys.version}")
    print(f"   Çalışma Dizini: {os.getcwd()}")
    
    # Basit hesaplama
    print(f"\n🧮 Basit Hesaplama:")
    a, b = 15, 25
    print(f"   {a} + {b} = {a + b}")
    print(f"   {a} * {b} = {a * b}")
    
    # Dosya listesi
    print(f"\n📁 Mevcut Dizin İçeriği:")
    try:
        files = os.listdir('.')
        for i, file in enumerate(files[:5], 1):
            print(f"   {i}. {file}")
        if len(files) > 5:
            print(f"   ... ve {len(files) - 5} dosya daha")
    except Exception as e:
        print(f"   Dosya listesi alınamadı: {e}")
    
    print(f"\n✅ hello-python uygulaması başarıyla çalıştı!")
    print("🎉 clapp paket yöneticisine hoş geldiniz!")

if __name__ == "__main__":
    main() 