#!/usr/bin/env python3
"""
where_command.py - Uygulama konum bulma modülü

Bu modül `clapp where <app_name>` komutunu destekler ve
yüklü uygulamaların dosya sistemi konumlarını gösterir.
"""

import os
import json
from pathlib import Path

def locate_app_path(app_name, check_entry=False):
    """Uygulama konumunu bulur"""
    print(f"📍 '{app_name}' uygulaması aranıyor...")
    print("=" * 50)
    
    # Varsayılan uygulama dizini
    apps_dir = Path("apps")
    app_dir = apps_dir / app_name
    
    if not app_dir.exists():
        print(f"❌ '{app_name}' uygulaması bulunamadı.")
        print()
        print("🔍 Öneriler:")
        print("• Uygulama adını kontrol edin")
        print("• Yüklü uygulamaları görmek için: clapp list")
        print("• Uygulama yüklemek için: clapp install <kaynak>")
        return False
    
    if not app_dir.is_dir():
        print(f"❌ '{app_name}' bir dizin değil.")
        return False
    
    # Temel bilgiler
    abs_path = app_dir.resolve()
    print(f"📂 Uygulama konumu:")
    print(f"   {abs_path}")
    print()
    
    # Dizin içeriği
    try:
        contents = list(app_dir.iterdir())
        print(f"📋 Dizin içeriği ({len(contents)} öğe):")
        
        for item in contents:
            if item.is_file():
                size = item.stat().st_size
                print(f"   📄 {item.name} ({format_size(size)})")
            elif item.is_dir():
                print(f"   📁 {item.name}/")
        print()
    except Exception as e:
        print(f"⚠️  Dizin içeriği okunamadı: {e}")
        print()
    
    # Manifest kontrolü
    manifest_path = app_dir / "manifest.json"
    if manifest_path.exists():
        print("✅ manifest.json mevcut")
        
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            # Temel manifest bilgileri
            print(f"   📝 Ad: {manifest.get('name', 'Belirtilmemiş')}")
            print(f"   🔢 Sürüm: {manifest.get('version', 'Belirtilmemiş')}")
            print(f"   🔧 Dil: {manifest.get('language', 'Belirtilmemiş')}")
            print(f"   🚀 Giriş: {manifest.get('entry', 'Belirtilmemiş')}")
            
            # Giriş dosyası kontrolü
            if check_entry and "entry" in manifest:
                entry_file = app_dir / manifest["entry"]
                print()
                print("🔍 Giriş dosyası kontrolü:")
                if entry_file.exists():
                    size = entry_file.stat().st_size
                    print(f"   ✅ {manifest['entry']} mevcut ({format_size(size)})")
                    print(f"   📍 Tam yol: {entry_file.resolve()}")
                else:
                    print(f"   ❌ {manifest['entry']} bulunamadı")
            
        except json.JSONDecodeError:
            print("   ❌ manifest.json geçersiz JSON formatında")
        except Exception as e:
            print(f"   ❌ manifest.json okunamadı: {e}")
    else:
        print("❌ manifest.json bulunamadı")
    
    print()
    
    # Kullanım örnekleri
    print("🚀 Kullanım:")
    print(f"   clapp run {app_name}")
    print(f"   clapp info {app_name}")
    print(f"   clapp validate {app_dir}")
    
    return True

def format_size(size_bytes):
    """Dosya boyutunu formatlar"""
    if size_bytes == 0:
        return "0 B"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} TB"

def list_all_app_locations():
    """Tüm uygulamaların konumlarını listeler"""
    print("📍 Tüm Uygulama Konumları")
    print("=" * 60)
    
    apps_dir = Path("apps")
    if not apps_dir.exists():
        print("❌ apps/ dizini bulunamadı")
        return False
    
    app_dirs = [d for d in apps_dir.iterdir() if d.is_dir()]
    
    if not app_dirs:
        print("📦 Yüklü uygulama bulunamadı")
        return True
    
    print(f"📂 Toplam {len(app_dirs)} uygulama bulundu:\n")
    
    for app_dir in sorted(app_dirs):
        app_name = app_dir.name
        abs_path = app_dir.resolve()
        
        # Manifest kontrolü
        manifest_path = app_dir / "manifest.json"
        version = "?"
        language = "?"
        
        if manifest_path.exists():
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                version = manifest.get('version', '?')
                language = manifest.get('language', '?')
            except:
                pass
        
        # Dizin boyutu
        try:
            total_size = sum(f.stat().st_size for f in app_dir.rglob("*") if f.is_file())
            size_str = format_size(total_size)
        except:
            size_str = "?"
        
        print(f"📦 {app_name} (v{version}, {language})")
        print(f"   📍 {abs_path}")
        print(f"   📊 {size_str}")
        print()
    
    return True

def open_app_location(app_name):
    """Uygulama konumunu dosya yöneticisinde açar"""
    apps_dir = Path("apps")
    app_dir = apps_dir / app_name
    
    if not app_dir.exists():
        print(f"❌ '{app_name}' uygulaması bulunamadı.")
        return False
    
    abs_path = app_dir.resolve()
    
    try:
        import platform
        system = platform.system()
        
        if system == "Windows":
            os.startfile(abs_path)
        elif system == "Darwin":  # macOS
            os.system(f"open '{abs_path}'")
        else:  # Linux
            os.system(f"xdg-open '{abs_path}'")
        
        print(f"📂 '{app_name}' konumu dosya yöneticisinde açıldı")
        print(f"📍 {abs_path}")
        return True
        
    except Exception as e:
        print(f"❌ Dosya yöneticisi açılamadı: {e}")
        print(f"📍 Manuel olarak açın: {abs_path}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        list_all_app_locations()
    else:
        app_name = sys.argv[1]
        check_entry = "--check-entry" in sys.argv
        open_flag = "--open" in sys.argv
        
        if open_flag:
            open_app_location(app_name)
        else:
            locate_app_path(app_name, check_entry) 