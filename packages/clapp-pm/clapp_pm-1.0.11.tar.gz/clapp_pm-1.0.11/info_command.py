#!/usr/bin/env python3
"""
info_command.py - Uygulama bilgi görüntüleme modülü

Bu modül `clapp info <app_name>` komutunu destekler ve
yüklü uygulamaların detaylı bilgilerini gösterir.
"""

import os
import json
from pathlib import Path
from package_registry import get_manifest

def format_field(name, value, width=20):
    """Alanı formatlar"""
    if value is None or value == "":
        value = "Belirtilmemiş"
    return f"{name:<{width}}: {value}"

def format_list(items, indent=22):
    """Liste öğelerini formatlar"""
    if not items:
        return "Yok"
    
    if len(items) == 1:
        return items[0]
    
    result = items[0]
    for item in items[1:]:
        result += f"\n{' ' * indent}{item}"
    return result

def get_app_file_info(app_name):
    """Uygulama dosya bilgilerini toplar"""
    apps_dir = Path("apps")
    app_dir = apps_dir / app_name
    
    if not app_dir.exists():
        return None
    
    info = {
        "path": str(app_dir.absolute()),
        "size": 0,
        "file_count": 0,
        "files": []
    }
    
    try:
        for file_path in app_dir.rglob("*"):
            if file_path.is_file():
                info["file_count"] += 1
                info["size"] += file_path.stat().st_size
                info["files"].append(file_path.name)
    except Exception:
        pass
    
    return info

def format_size(size_bytes):
    """Dosya boyutunu formatlar"""
    if size_bytes == 0:
        return "0 B"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} TB"

def show_app_info(app_name):
    """Uygulama bilgilerini gösterir"""
    print(f"📋 {app_name} - Uygulama Bilgileri")
    print("=" * 50)
    
    # Manifest bilgilerini al
    manifest = get_manifest(app_name)
    
    if not manifest:
        print(f"❌ '{app_name}' uygulaması bulunamadı veya manifest.json eksik.")
        print()
        print("🔧 Öneriler:")
        print("• Uygulama adını kontrol edin")
        print("• apps/ dizininde uygulama klasörünün var olduğundan emin olun")
        print("• manifest.json dosyasının mevcut olduğundan emin olun")
        print("• Doğrulama için: clapp validate apps/[app_name]")
        return False
    
    # Temel bilgiler
    print("📦 Temel Bilgiler:")
    print(format_field("Ad", manifest.get("name", app_name)))
    print(format_field("Sürüm", manifest.get("version", "Belirtilmemiş")))
    print(format_field("Dil", manifest.get("language", "Belirtilmemiş")))
    print(format_field("Giriş Dosyası", manifest.get("entry", "Belirtilmemiş")))
    print()
    
    # Açıklama
    description = manifest.get("description", "")
    if description:
        print("📝 Açıklama:")
        print(f"   {description}")
        print()
    
    # Bağımlılıklar
    dependencies = manifest.get("dependencies", [])
    print("🔗 Bağımlılıklar:")
    if dependencies:
        for dep in dependencies:
            print(f"   • {dep}")
    else:
        print("   Bağımlılık yok")
    print()
    
    # Dosya bilgileri
    file_info = get_app_file_info(app_name)
    if file_info:
        print("📁 Dosya Bilgileri:")
        print(format_field("Konum", file_info["path"]))
        print(format_field("Dosya Sayısı", file_info["file_count"]))
        print(format_field("Toplam Boyut", format_size(file_info["size"])))
        print()
        
        # Dosya listesi (ilk 10 dosya)
        if file_info["files"]:
            print("📄 Dosyalar:")
            files_to_show = file_info["files"][:10]
            for file_name in files_to_show:
                print(f"   • {file_name}")
            
            if len(file_info["files"]) > 10:
                print(f"   ... ve {len(file_info['files']) - 10} dosya daha")
            print()
    
    # Ek bilgiler
    extra_fields = ["author", "license", "homepage", "repository"]
    extra_info = []
    
    for field in extra_fields:
        if field in manifest:
            extra_info.append((field.title(), manifest[field]))
    
    if extra_info:
        print("ℹ️  Ek Bilgiler:")
        for field_name, value in extra_info:
            print(format_field(field_name, value))
        print()
    
    # Çalıştırma bilgisi
    print("🚀 Çalıştırma:")
    print(f"   clapp run {app_name}")
    
    # Doğrulama önerisi
    print()
    print("🔧 Doğrulama:")
    print(f"   clapp validate apps/{app_name}")
    
    return True

def list_all_apps_info():
    """Tüm uygulamaların kısa bilgilerini listeler"""
    from package_registry import list_packages
    
    packages = list_packages()
    
    if not packages:
        print("📦 Yüklü uygulama bulunamadı.")
        return
    
    print("📋 Yüklü Uygulamalar - Özet Bilgiler")
    print("=" * 60)
    
    for package in packages:
        name = package.get("name", "Bilinmiyor")
        version = package.get("version", "?")
        language = package.get("language", "?")
        description = package.get("description", "Açıklama yok")
        
        # Açıklamayı kısalt
        if len(description) > 40:
            description = description[:37] + "..."
        
        print(f"📦 {name} (v{version})")
        print(f"   🔧 Dil: {language}")
        print(f"   📝 {description}")
        print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        app_name = sys.argv[1]
        show_app_info(app_name)
    else:
        list_all_apps_info() 