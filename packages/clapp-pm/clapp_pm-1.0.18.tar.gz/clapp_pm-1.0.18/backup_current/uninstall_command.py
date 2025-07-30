#!/usr/bin/env python3
"""
uninstall_command.py - clapp Uninstall Command

Bu modül 'clapp uninstall <app_name>' komutunu uygular.
Kurulu uygulamaları güvenli bir şekilde kaldırır.
"""

import os
import shutil
import sys
from pathlib import Path
from typing import Tuple, List

def get_apps_directory() -> str:
    """Uygulamaların kurulu olduğu dizini döndürür"""
    # Kullanıcının home dizininde .clapp klasörü
    home_dir = Path.home()
    clapp_dir = home_dir / ".clapp"
    apps_dir = clapp_dir / "apps"
    
    return str(apps_dir)

def get_installed_apps() -> List[str]:
    """Kurulu uygulamaların listesini döndürür"""
    apps_dir = get_apps_directory()
    
    if not os.path.exists(apps_dir):
        return []
    
    apps = []
    for item in os.listdir(apps_dir):
        item_path = os.path.join(apps_dir, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            # manifest.json varlığını kontrol et
            manifest_path = os.path.join(item_path, "manifest.json")
            if os.path.exists(manifest_path):
                apps.append(item)
    
    return apps

def is_app_installed(app_name: str) -> bool:
    """Uygulamanın kurulu olup olmadığını kontrol eder"""
    apps_dir = get_apps_directory()
    app_path = os.path.join(apps_dir, app_name)
    
    if not os.path.exists(app_path):
        return False
    
    if not os.path.isdir(app_path):
        return False
    
    # manifest.json varlığını kontrol et
    manifest_path = os.path.join(app_path, "manifest.json")
    return os.path.exists(manifest_path)

def get_app_info(app_name: str) -> Tuple[bool, str, dict]:
    """Uygulamanın bilgilerini getirir"""
    apps_dir = get_apps_directory()
    app_path = os.path.join(apps_dir, app_name)
    manifest_path = os.path.join(app_path, "manifest.json")
    
    try:
        import json
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        return True, "Bilgiler alındı", manifest
    except Exception as e:
        return False, f"Manifest okunamadı: {e}", {}

def confirm_uninstall(app_name: str, app_info: dict, skip_confirmation: bool = False) -> bool:
    """Kullanıcıdan kaldırma onayı alır"""
    if skip_confirmation:
        return True
    
    print(f"\n📋 Kaldırılacak uygulama:")
    print(f"   Ad: {app_info.get('name', app_name)}")
    print(f"   Sürüm: {app_info.get('version', 'Bilinmiyor')}")
    print(f"   Dil: {app_info.get('language', 'Bilinmiyor')}")
    print(f"   Açıklama: {app_info.get('description', 'Yok')}")
    
    while True:
        response = input(f"\n❓ '{app_name}' uygulamasını kaldırmak istediğinizden emin misiniz? (e/h): ").lower().strip()
        if response in ['e', 'evet', 'y', 'yes']:
            return True
        elif response in ['h', 'hayır', 'n', 'no']:
            return False
        else:
            print("Lütfen 'e' (evet) veya 'h' (hayır) giriniz.")

def remove_app_directory(app_name: str) -> Tuple[bool, str]:
    """Uygulama klasörünü güvenli şekilde kaldırır"""
    try:
        apps_dir = get_apps_directory()
        app_path = os.path.join(apps_dir, app_name)
        
        # Güvenlik kontrolü - sadece .clapp/apps altındaki klasörleri sil
        if not app_path.startswith(apps_dir):
            return False, "Güvenlik hatası: Geçersiz klasör yolu"
        
        if not os.path.exists(app_path):
            return False, "Uygulama klasörü bulunamadı"
        
        # Klasörü sil
        shutil.rmtree(app_path)
        
        return True, f"Uygulama klasörü kaldırıldı: {app_path}"
        
    except PermissionError:
        return False, "İzin hatası: Klasör kaldırılamadı"
    except Exception as e:
        return False, f"Kaldırma hatası: {e}"

def uninstall_app(app_name: str, skip_confirmation: bool = False) -> Tuple[bool, str]:
    """
    Ana uninstall fonksiyonu
    
    Args:
        app_name: Kaldırılacak uygulamanın adı
        skip_confirmation: Onay sorma (--yes flag için)
        
    Returns:
        (success, message)
    """
    print(f"🗑️  Kaldırma başlatılıyor: {app_name}")
    print("=" * 50)
    
    # 1. Uygulama kurulu mu kontrol et
    print("1️⃣ Uygulama kontrol ediliyor...")
    
    if not is_app_installed(app_name):
        installed_apps = get_installed_apps()
        if installed_apps:
            return False, f"Uygulama kurulu değil: {app_name}\nKurulu uygulamalar: {', '.join(installed_apps)}"
        else:
            return False, f"Uygulama kurulu değil: {app_name}\nHiç uygulama kurulu değil."
    
    print(f"✅ {app_name} kurulu")
    
    # 2. Uygulama bilgilerini al
    print("2️⃣ Uygulama bilgileri alınıyor...")
    info_success, info_message, app_info = get_app_info(app_name)
    
    if not info_success:
        print(f"⚠️  {info_message}")
        app_info = {'name': app_name}
    
    # 3. Kullanıcı onayı
    if not skip_confirmation:
        print("3️⃣ Kullanıcı onayı bekleniyor...")
        if not confirm_uninstall(app_name, app_info, skip_confirmation):
            return False, "Kaldırma işlemi iptal edildi"
    
    # 4. Uygulamayı kaldır
    print("4️⃣ Uygulama kaldırılıyor...")
    remove_success, remove_message = remove_app_directory(app_name)
    
    if not remove_success:
        return False, remove_message
    
    return True, f"🎉 '{app_name}' başarıyla kaldırıldı!"

def list_installed_apps():
    """Kurulu uygulamaları listeler"""
    apps = get_installed_apps()
    
    if not apps:
        print("📭 Hiç uygulama kurulu değil.")
        return
    
    print(f"📦 Kurulu uygulamalar ({len(apps)}):")
    print("-" * 30)
    
    for app_name in sorted(apps):
        info_success, _, app_info = get_app_info(app_name)
        if info_success:
            version = app_info.get('version', '?')
            language = app_info.get('language', '?')
            print(f"  • {app_name} (v{version}) - {language}")
        else:
            print(f"  • {app_name} - bilgi alınamadı")

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Kullanım: python uninstall_command.py <app_name> [--yes]")
        print("         python uninstall_command.py --list")
        print()
        print("Örnekler:")
        print("  python uninstall_command.py hello-python")
        print("  python uninstall_command.py hello-python --yes")
        print("  python uninstall_command.py --list")
        sys.exit(1)
    
    # --list flag kontrolü
    if sys.argv[1] == "--list":
        list_installed_apps()
        sys.exit(0)
    
    app_name = sys.argv[1]
    skip_confirmation = "--yes" in sys.argv
    
    success, message = uninstall_app(app_name, skip_confirmation)
    
    print("\n" + "=" * 50)
    if success:
        print(f"✅ {message}")
        sys.exit(0)
    else:
        print(f"❌ {message}")
        sys.exit(1)

if __name__ == "__main__":
    main() 