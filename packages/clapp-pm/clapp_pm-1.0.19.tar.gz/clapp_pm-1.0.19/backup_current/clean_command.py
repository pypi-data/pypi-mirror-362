#!/usr/bin/env python3
"""
clean_command.py - Geçici dosya temizleme modülü

Bu modül `clapp clean` komutunu destekler ve geçici dosyaları,
logları ve eski dosyaları temizler.
"""

import os
import shutil
import glob
from pathlib import Path

def format_size(size_bytes):
    """Dosya boyutunu formatlar"""
    if size_bytes == 0:
        return "0 B"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} TB"

def clean_temp_files():
    """Geçici dosyaları temizler"""
    temp_patterns = [
        "*.tmp",
        "*.temp",
        "*.log",
        "*.old",
        "*.bak",
        "*.backup",
        "__pycache__",
        "*.pyc",
        "*.pyo",
        ".DS_Store",
        "Thumbs.db",
        "test_write_permission.tmp"
    ]
    
    cleaned_files = []
    total_size = 0
    
    # Mevcut dizinde temizlik
    for pattern in temp_patterns:
        if pattern == "__pycache__":
            # __pycache__ dizinlerini bul ve sil
            for pycache_dir in Path(".").rglob("__pycache__"):
                if pycache_dir.is_dir():
                    try:
                        dir_size = sum(f.stat().st_size for f in pycache_dir.rglob("*") if f.is_file())
                        shutil.rmtree(pycache_dir)
                        cleaned_files.append(str(pycache_dir))
                        total_size += dir_size
                    except Exception as e:
                        print(f"⚠️  {pycache_dir} silinemedi: {e}")
        else:
            # Dosya desenlerini bul ve sil
            for file_path in Path(".").rglob(pattern):
                if file_path.is_file():
                    try:
                        file_size = file_path.stat().st_size
                        file_path.unlink()
                        cleaned_files.append(str(file_path))
                        total_size += file_size
                    except Exception as e:
                        print(f"⚠️  {file_path} silinemedi: {e}")
    
    return cleaned_files, total_size

def clean_apps_directory():
    """apps/ dizinindeki geçici dosyaları temizler"""
    apps_dir = Path("apps")
    if not apps_dir.exists():
        return [], 0
    
    cleaned_files = []
    total_size = 0
    
    # Her uygulama dizininde temizlik
    for app_dir in apps_dir.iterdir():
        if app_dir.is_dir():
            # .zip dosyalarını temizle
            for zip_file in app_dir.glob("*.zip"):
                try:
                    file_size = zip_file.stat().st_size
                    zip_file.unlink()
                    cleaned_files.append(str(zip_file))
                    total_size += file_size
                except Exception as e:
                    print(f"⚠️  {zip_file} silinemedi: {e}")
            
            # .old dosyalarını temizle
            for old_file in app_dir.glob("*.old"):
                try:
                    file_size = old_file.stat().st_size
                    old_file.unlink()
                    cleaned_files.append(str(old_file))
                    total_size += file_size
                except Exception as e:
                    print(f"⚠️  {old_file} silinemedi: {e}")
    
    return cleaned_files, total_size

def clean_clapp_config():
    """~/.clapp dizinindeki geçici dosyaları temizler"""
    home = Path.home()
    clapp_dir = home / ".clapp"
    
    if not clapp_dir.exists():
        return [], 0
    
    cleaned_files = []
    total_size = 0
    
    # temp dizini
    temp_dir = clapp_dir / "temp"
    if temp_dir.exists():
        try:
            dir_size = sum(f.stat().st_size for f in temp_dir.rglob("*") if f.is_file())
            shutil.rmtree(temp_dir)
            cleaned_files.append(str(temp_dir))
            total_size += dir_size
        except Exception as e:
            print(f"⚠️  {temp_dir} silinemedi: {e}")
    
    # logs dizini
    logs_dir = clapp_dir / "logs"
    if logs_dir.exists():
        try:
            # Sadece .log dosyalarını sil, dizini koru
            for log_file in logs_dir.glob("*.log"):
                file_size = log_file.stat().st_size
                log_file.unlink()
                cleaned_files.append(str(log_file))
                total_size += file_size
        except Exception as e:
            print(f"⚠️  Log dosyaları silinemedi: {e}")
    
    return cleaned_files, total_size

def run_clean(dry_run=False):
    """Temizleme işlemini çalıştırır"""
    print("🧹 clapp Temizleme Aracı")
    print("=" * 50)
    
    if dry_run:
        print("🔍 Kuru çalıştırma modu - Dosyalar silinmeyecek")
        print()
    
    total_cleaned = 0
    total_size = 0
    
    # 1. Geçici dosyaları temizle
    print("🗑️  Geçici dosyalar temizleniyor...")
    temp_files, temp_size = clean_temp_files()
    if temp_files:
        print(f"   ✅ {len(temp_files)} geçici dosya temizlendi")
        total_cleaned += len(temp_files)
        total_size += temp_size
    else:
        print("   ✅ Geçici dosya bulunamadı")
    
    # 2. apps/ dizinini temizle
    print("📦 apps/ dizini temizleniyor...")
    apps_files, apps_size = clean_apps_directory()
    if apps_files:
        print(f"   ✅ {len(apps_files)} dosya temizlendi")
        total_cleaned += len(apps_files)
        total_size += apps_size
    else:
        print("   ✅ Temizlenecek dosya bulunamadı")
    
    # 3. ~/.clapp dizinini temizle
    print("🏠 ~/.clapp dizini temizleniyor...")
    config_files, config_size = clean_clapp_config()
    if config_files:
        print(f"   ✅ {len(config_files)} öğe temizlendi")
        total_cleaned += len(config_files)
        total_size += config_size
    else:
        print("   ✅ Temizlenecek dosya bulunamadı")
    
    # Özet
    print("\n" + "=" * 50)
    print("📊 Temizleme Özeti:")
    print(f"🗑️  Toplam temizlenen: {total_cleaned} öğe")
    print(f"💾 Kazanılan alan: {format_size(total_size)}")
    
    if total_cleaned > 0:
        print("\n✨ Temizlik tamamlandı!")
        
        # Detaylı liste (ilk 10 dosya)
        all_files = temp_files + apps_files + config_files
        if len(all_files) > 0:
            print("\n📋 Temizlenen dosyalar:")
            for i, file_path in enumerate(all_files[:10]):
                print(f"   • {file_path}")
            
            if len(all_files) > 10:
                print(f"   ... ve {len(all_files) - 10} dosya daha")
    else:
        print("\n🎉 Sistem zaten temiz!")
        print("Temizlenecek dosya bulunamadı.")
    
    return total_cleaned > 0

if __name__ == "__main__":
    import sys
    
    dry_run = "--dry-run" in sys.argv
    run_clean(dry_run) 