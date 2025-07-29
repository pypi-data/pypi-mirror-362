#!/usr/bin/env python3
"""
doctor_command.py - Kapsamlı sistem tanılaması modülü

Bu modül `clapp doctor` komutunu destekler ve sistemin
clapp için uygun olup olmadığını kapsamlı şekilde kontrol eder.
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path
from check_env import (
    check_python_version,
    check_clapp_in_path,
    check_platform_info,
    check_python_executable,
    check_working_directory,
    check_apps_directory,
    check_permissions,
)

def check_clapp_config():
    """clapp konfigürasyon dizinini kontrol eder"""
    home = Path.home()
    clapp_config_dir = home / ".clapp"
    
    if clapp_config_dir.exists():
        return True, f"Konfigürasyon dizini mevcut: {clapp_config_dir}"
    else:
        return False, "Konfigürasyon dizini bulunamadı (~/.clapp)"

def check_path_environment():
    """PATH ortam değişkenini detaylı kontrol eder"""
    path_env = os.environ.get("PATH", "")
    path_dirs = path_env.split(os.pathsep)
    
    # Önemli dizinleri kontrol et
    important_dirs = []
    
    # Platform'a göre önemli dizinler
    system = platform.system().lower()
    if system == "windows":
        important_dirs = [
            os.path.join(os.environ.get("APPDATA", ""), "Python", "Scripts"),
            os.path.join(sys.prefix, "Scripts"),
        ]
    else:
        home = Path.home()
        important_dirs = [
            str(home / ".local" / "bin"),
            "/usr/local/bin",
            "/usr/bin",
        ]
    
    found_dirs = []
    missing_dirs = []
    
    for imp_dir in important_dirs:
        if imp_dir in path_dirs:
            found_dirs.append(imp_dir)
        else:
            missing_dirs.append(imp_dir)
    
    if missing_dirs:
        return False, f"PATH'te eksik dizinler: {', '.join(missing_dirs)}"
    else:
        return True, f"PATH uygun ({len(found_dirs)} önemli dizin mevcut)"

def check_dependencies():
    """Bağımlılıkları kontrol eder"""
    dependencies = ["python", "pip"]
    
    missing = []
    found = []
    
    for dep in dependencies:
        if shutil.which(dep):
            found.append(dep)
        else:
            missing.append(dep)
    
    if missing:
        return False, f"Eksik bağımlılıklar: {', '.join(missing)}"
    else:
        return True, f"Tüm bağımlılıklar mevcut: {', '.join(found)}"

def check_disk_space():
    """Disk alanını kontrol eder"""
    try:
        cwd = Path.cwd()
        stat = shutil.disk_usage(cwd)
        
        # GB'ye çevir
        free_gb = stat.free / (1024**3)
        total_gb = stat.total / (1024**3)
        
        if free_gb < 0.5:  # 500MB'den az
            return False, f"Yetersiz disk alanı: {free_gb:.1f}GB boş"
        else:
            return True, f"Disk alanı uygun: {free_gb:.1f}GB / {total_gb:.1f}GB"
    
    except Exception as e:
        return False, f"Disk alanı kontrol edilemedi: {str(e)}"

def check_network_access():
    """Ağ erişimini kontrol eder"""
    try:
        # Basit bir ping testi
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True, "Ağ erişimi mevcut"
    except:
        return False, "Ağ erişimi yok veya sınırlı"

def check_installed_apps():
    """Yüklü uygulamaları kontrol eder"""
    try:
        from package_registry import list_packages
        packages = list_packages()
        
        if not packages:
            return True, "Yüklü uygulama yok (normal)"
        
        # Bozuk uygulamaları kontrol et
        broken_apps = []
        for package in packages:
            if not package.get("name") or not package.get("entry"):
                broken_apps.append(package.get("name", "Bilinmiyor"))
        
        if broken_apps:
            return False, f"Bozuk uygulamalar: {', '.join(broken_apps)}"
        else:
            return True, f"{len(packages)} uygulama yüklü (tümü geçerli)"
    
    except Exception as e:
        return False, f"Uygulama listesi kontrol edilemedi: {str(e)}"

def check_python_modules():
    """Gerekli Python modüllerini kontrol eder"""
    required_modules = [
        ("json", "JSON desteği"),
        ("os", "İşletim sistemi arayüzü"),
        ("sys", "Sistem arayüzü"),
        ("pathlib", "Dosya yolu işlemleri"),
        ("subprocess", "Alt süreç yönetimi"),
        ("argparse", "Komut satırı ayrıştırma"),
    ]
    
    missing = []
    found = []
    
    for module_name, description in required_modules:
        try:
            __import__(module_name)
            found.append(module_name)
        except ImportError:
            missing.append(f"{module_name} ({description})")
    
    if missing:
        return False, f"Eksik Python modülleri: {', '.join(missing)}"
    else:
        return True, f"Tüm gerekli modüller mevcut ({len(found)} modül)"

def check_apps_directory():
    """apps/ dizinini kontrol eder, yoksa otomatik oluşturur veya bilgi verir"""
    apps_dir = Path("apps")
    if apps_dir.exists():
        return True, "apps/ dizini mevcut"
    else:
        try:
            apps_dir.mkdir(parents=True, exist_ok=True)
            return True, "apps/ dizini yoktu, otomatik oluşturuldu (ilk kurulum için normal)"
        except Exception as e:
            return False, f"apps/ dizini oluşturulamadı: {e}"


def run_doctor():
    """Kapsamlı sistem tanılaması yapar"""
    print("🩺 clapp Sistem Tanılaması")
    print("=" * 60)
    print("Sisteminiz clapp için uygun mu kontrol ediliyor...")
    print()
    # Tüm kontroller
    checks = [
        ("Python Sürümü", check_python_version),
        ("Platform Bilgisi", check_platform_info),
        ("Python Çalıştırılabilir", check_python_executable),
        ("Çalışma Dizini", check_working_directory),
        ("clapp PATH Kontrolü", check_clapp_in_path),
        ("PATH Ortam Değişkeni", check_path_environment),
        ("Sistem Bağımlılıkları", check_dependencies),
        ("Python Modülleri", check_python_modules),
        ("apps/ Dizini", check_apps_directory),
        ("Yüklü Uygulamalar", check_installed_apps),
        ("Yazma İzinleri", check_permissions),
        ("Disk Alanı", check_disk_space),
        ("Ağ Erişimi", check_network_access),
        ("clapp Konfigürasyonu", check_clapp_config),
    ]
    passed = 0
    failed = 0
    warnings = 0
    results = []
    for check_name, check_func in checks:
        try:
            ok, msg = check_func()
            if ok:
                print(f"✅ {check_name}: {msg}")
                passed += 1
            else:
                print(f"❌ {check_name}: {msg}")
                failed += 1
            results.append((check_name, ok, msg))
        except Exception as e:
            print(f"❌ {check_name}: Kontrol sırasında hata: {e}")
            failed += 1
            results.append((check_name, False, str(e)))
    print("\n" + "=" * 60)
    print(f"📊 Tanılama Özeti:")
    print(f"✅ Başarılı: {passed}")
    print(f"❌ Başarısız: {failed}")
    print(f"⚠️  Uyarı: {warnings}")
    if failed > 0:
        print("\n🔧 Dikkat! Bazı sorunlar bulundu.")
        print("❌ Aşağıdaki sorunları çözmeniz önerilir:")
        for name, ok, msg in results:
            if not ok:
                print(f"\n🔧 {name}:\n   Sorun: {msg}")
    else:
        print("\n🚀 Her şey yolunda! clapp sorunsuz çalışabilir.")
    print("\n📞 Yardım:")
    print("• GitHub: https://github.com/user/clapp")
    print("• Dokümantasyon: README.md dosyasını okuyun")

if __name__ == "__main__":
    run_doctor() 