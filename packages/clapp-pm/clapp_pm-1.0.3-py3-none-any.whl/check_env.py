#!/usr/bin/env python3
"""
check_env.py - Sistem ortam kontrolü modülü

Bu modül `clapp check-env` komutunu destekler ve kullanıcının
sisteminin clapp çalıştırmak için uygun olup olmadığını kontrol eder.
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path

def check_python_version():
    """Python sürümünü kontrol eder (>= 3.8 gerekli)"""
    version = sys.version_info
    required_major, required_minor = 3, 8
    
    if version.major >= required_major and version.minor >= required_minor:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    else:
        return False, f"Python {version.major}.{version.minor}.{version.micro} (>= {required_major}.{required_minor} gerekli)"

def check_clapp_in_path():
    """clapp komutunun PATH'te olup olmadığını kontrol eder"""
    clapp_path = shutil.which("clapp")
    if clapp_path:
        return True, f"clapp komutu bulundu: {clapp_path}"
    else:
        return False, "clapp komutu PATH'te bulunamadı"

def check_platform_info():
    """Platform bilgilerini toplar"""
    system = platform.system()
    release = platform.release()
    machine = platform.machine()
    
    return True, f"{system} {release} ({machine})"

def check_python_executable():
    """Python çalıştırılabilir dosyasının konumunu kontrol eder"""
    python_path = sys.executable
    return True, f"Python çalıştırılabilir: {python_path}"

def check_working_directory():
    """Mevcut çalışma dizinini kontrol eder"""
    cwd = os.getcwd()
    return True, f"Çalışma dizini: {cwd}"

def check_apps_directory():
    """apps/ dizininin var olup olmadığını kontrol eder"""
    apps_dir = Path("apps")
    if apps_dir.exists() and apps_dir.is_dir():
        app_count = len([d for d in apps_dir.iterdir() if d.is_dir()])
        return True, f"apps/ dizini mevcut ({app_count} uygulama)"
    else:
        return False, "apps/ dizini bulunamadı"

def check_permissions():
    """Yazma izinlerini kontrol eder"""
    try:
        # Mevcut dizinde yazma izni kontrolü
        test_file = Path("test_write_permission.tmp")
        test_file.write_text("test")
        test_file.unlink()
        
        return True, "Yazma izinleri: OK"
    except PermissionError:
        return False, "Yazma izinleri: Yetersiz izin"
    except Exception as e:
        return False, f"Yazma izinleri: Hata - {str(e)}"

def check_flet_installation():
    """Flet kurulumunu kontrol eder"""
    try:
        import flet
        return True, f"Flet kurulu: v{flet.__version__}"
    except ImportError:
        return False, "Flet kurulu değil (pip install flet)"

def run_environment_check():
    """Tüm ortam kontrollerini çalıştırır ve sonuçları yazdırır"""
    print("🔍 clapp Ortam Kontrolü")
    print("=" * 50)
    
    checks = [
        ("Python Sürümü", check_python_version),
        ("Platform Bilgisi", check_platform_info),
        ("Python Çalıştırılabilir", check_python_executable),
        ("Çalışma Dizini", check_working_directory),
        ("clapp PATH Kontrolü", check_clapp_in_path),
        ("apps/ Dizini", check_apps_directory),
        ("Yazma İzinleri", check_permissions),
        ("Flet Kurulumu", check_flet_installation),
    ]
    
    passed = 0
    failed = 0
    warnings = 0
    
    for check_name, check_func in checks:
        try:
            success, message = check_func()
            if success:
                print(f"✅ {check_name}: {message}")
                passed += 1
            else:
                print(f"❌ {check_name}: {message}")
                failed += 1
        except Exception as e:
            print(f"⚠️  {check_name}: Hata - {str(e)}")
            warnings += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Özet: {passed} başarılı, {failed} başarısız, {warnings} uyarı")
    
    if failed > 0:
        print("\n🔧 Öneriler:")
        if not shutil.which("clapp"):
            print("• clapp'i PATH'e ekleyin veya pip install ile kurun")
        if not Path("apps").exists():
            print("• apps/ dizini oluşturun: mkdir apps")
        
        print("• Daha fazla yardım için: clapp doctor")
    
    print("\n✨ Sorun yaşıyorsanız 'clapp doctor' komutunu çalıştırın!")
    
    return failed == 0

if __name__ == "__main__":
    run_environment_check() 