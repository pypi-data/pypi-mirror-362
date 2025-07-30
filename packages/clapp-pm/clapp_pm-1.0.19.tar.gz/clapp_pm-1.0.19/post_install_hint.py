#!/usr/bin/env python3
"""
post_install_hint.py - Kurulum sonrası yardım ipuçları

Bu modül kullanıcıya clapp kurulumu sonrasında PATH ve ortam
sorunları hakkında bilgi verir.
"""

import os
import sys
import shutil
import platform
from pathlib import Path

def get_platform_type():
    """Platform türünü döndürür"""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    else:
        return "linux"

def get_onboarded_flag_path():
    """Onboarding flag dosyasının yolunu döndürür"""
    home = Path.home()
    clapp_dir = home / ".clapp"
    return clapp_dir / ".onboarded"

def is_onboarded():
    """Kullanıcının daha önce onboarding gördüğünü kontrol eder"""
    return get_onboarded_flag_path().exists()

def mark_as_onboarded():
    """Kullanıcıyı onboarded olarak işaretler"""
    flag_path = get_onboarded_flag_path()
    flag_path.parent.mkdir(exist_ok=True)
    flag_path.write_text("onboarded")

def get_path_suggestions():
    """Platform'a göre PATH önerilerini döndürür"""
    platform_type = get_platform_type()
    
    if platform_type == "windows":
        return [
            "Windows PATH'e eklemek için:",
            "1. Sistem Özellikleri > Gelişmiş > Ortam Değişkenleri",
            "2. PATH değişkenine Python Scripts klasörünü ekleyin",
            "3. Örnek: C:\\Python39\\Scripts",
            "",
            "Veya PowerShell'de:",
            '$env:PATH += ";C:\\Python39\\Scripts"'
        ]
    elif platform_type == "macos":
        return [
            "macOS PATH'e eklemek için:",
            "~/.zshrc veya ~/.bash_profile dosyasına ekleyin:",
            'export PATH="$PATH:$HOME/.local/bin"',
            "",
            "Sonra terminali yeniden başlatın veya:",
            "source ~/.zshrc"
        ]
    else:  # linux
        return [
            "Linux PATH'e eklemek için:",
            "~/.bashrc veya ~/.profile dosyasına ekleyin:",
            'export PATH="$PATH:$HOME/.local/bin"',
            "",
            "Sonra terminali yeniden başlatın veya:",
            "source ~/.bashrc"
        ]

def show_post_install_hint():
    """Kurulum sonrası ipuçlarını gösterir"""
    # Eğer zaten onboarded ise gösterme
    if is_onboarded():
        return
    
    # clapp PATH'te var mı kontrol et
    clapp_in_path = shutil.which("clapp") is not None
    
    if not clapp_in_path:
        print("🚀 clapp'e Hoş Geldiniz!")
        print("=" * 50)
        print("⚠️  clapp komutu sistem PATH'inde bulunamadı.")
        print("Bu, 'clapp' komutunu her yerden çalıştıramamanız anlamına gelir.")
        print()
        
        # Platform'a göre öneriler
        suggestions = get_path_suggestions()
        for suggestion in suggestions:
            print(suggestion)
        
        print()
        print("🔧 Alternatif olarak:")
        print("• Python -m clapp [komut] şeklinde çalıştırabilirsiniz")
        print("• Veya python main.py [komut] şeklinde çalıştırabilirsiniz")
        print()
        print("📋 Sistem kontrolü için: clapp check-env")
        print("🩺 Detaylı tanılama için: clapp doctor")
        print()
        print("Bu mesajı bir daha görmek istemiyorsanız:")
        print("clapp doctor komutunu çalıştırın ve sorunları düzeltin.")
        print("=" * 50)
    else:
        print("✅ clapp başarıyla kuruldu ve PATH'te mevcut!")
        print("🎉 Başlamak için: clapp list")
        
        # Onboarded olarak işaretle
        mark_as_onboarded()

def show_welcome_message():
    """Hoş geldin mesajını gösterir"""
    print("🎉 clapp - Hafif Çoklu Dil Uygulama Yöneticisi")
    print()
    print("📚 Temel komutlar:")
    print("  clapp list              - Yüklü uygulamaları listele")
    print("  clapp run <app>         - Uygulama çalıştır")
    print("  clapp info <app>        - Uygulama bilgilerini göster")
    print("  clapp gui               - Grafik arayüzü başlat")
    print("  clapp check-env         - Sistem kontrolü")
    print("  clapp doctor            - Detaylı tanılama")
    print()
    print("🔧 Yönetim komutları:")
    print("  clapp install <source>  - Uygulama yükle")
    print("  clapp uninstall <app>   - Uygulama kaldır")
    print("  clapp upgrade <app>     - Uygulama güncelle")
    print("  clapp validate <folder> - Uygulama klasörünü doğrula")
    print("  clapp clean             - Geçici dosyaları temizle")
    print()
    print("📖 Daha fazla yardım için: clapp --help")

def check_first_run():
    """İlk çalıştırma kontrolü yapar"""
    if not is_onboarded():
        show_welcome_message()
        print()
        show_post_install_hint()
        return True
    return False

if __name__ == "__main__":
    show_post_install_hint() 