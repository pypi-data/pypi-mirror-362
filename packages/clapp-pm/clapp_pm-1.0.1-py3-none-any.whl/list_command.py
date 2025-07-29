#!/usr/bin/env python3
"""
list_command.py - clapp List Command

Bu modül 'clapp list' komutunu uygular.
Kurulu uygulamaları farklı formatlarda listeler.
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

def get_apps_directory() -> str:
    """Uygulamaların kurulu olduğu dizini döndürür"""
    # Kullanıcının home dizininde .clapp klasörü
    home_dir = Path.home()
    clapp_dir = home_dir / ".clapp"
    apps_dir = clapp_dir / "apps"
    
    return str(apps_dir)

def load_app_manifest(app_path: str) -> Optional[Dict[str, Any]]:
    """Uygulama manifest'ini yükler"""
    manifest_path = os.path.join(app_path, "manifest.json")
    
    if not os.path.exists(manifest_path):
        return None
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def get_installed_apps_with_info() -> List[Dict[str, Any]]:
    """Kurulu uygulamaların detaylı bilgilerini döndürür"""
    apps_dir = get_apps_directory()
    apps = []
    
    if not os.path.exists(apps_dir):
        return apps
    
    for item in os.listdir(apps_dir):
        item_path = os.path.join(apps_dir, item)
        
        if not os.path.isdir(item_path) or item.startswith('.'):
            continue
        
        manifest = load_app_manifest(item_path)
        
        if manifest:
            app_info = {
                'name': manifest.get('name', item),
                'version': manifest.get('version', '?'),
                'language': manifest.get('language', '?'),
                'description': manifest.get('description', 'Açıklama yok'),
                'entry': manifest.get('entry', '?'),
                'dependencies': manifest.get('dependencies', []),
                'folder': item,
                'path': item_path
            }
        else:
            app_info = {
                'name': item,
                'version': '?',
                'language': '?',
                'description': 'Manifest bulunamadı',
                'entry': '?',
                'dependencies': [],
                'folder': item,
                'path': item_path
            }
        
        apps.append(app_info)
    
    return apps

def format_table_output(apps: List[Dict[str, Any]]) -> str:
    """Uygulamaları tablo formatında formatlar"""
    if not apps:
        return "📭 Hiç uygulama kurulu değil."
    
    # Başlık
    output = []
    output.append(f"📦 Kurulu Uygulamalar ({len(apps)})")
    output.append("=" * 80)
    
    # Sütun başlıkları
    output.append(f"{'Ad':<20} {'Sürüm':<10} {'Dil':<10} {'Açıklama':<30}")
    output.append("-" * 80)
    
    # Uygulamalar
    for app in sorted(apps, key=lambda x: x['name'].lower()):
        name = app['name'][:19]
        version = app['version'][:9]
        language = app['language'][:9]
        description = app['description'][:29]
        
        output.append(f"{name:<20} {version:<10} {language:<10} {description:<30}")
    
    return "\n".join(output)

def format_simple_output(apps: List[Dict[str, Any]]) -> str:
    """Uygulamaları basit liste formatında formatlar"""
    if not apps:
        return "📭 Hiç uygulama kurulu değil."
    
    output = []
    output.append(f"📦 Kurulu Uygulamalar ({len(apps)}):")
    
    for app in sorted(apps, key=lambda x: x['name'].lower()):
        name = app['name']
        version = app['version']
        language = app['language']
        output.append(f"  • {name} (v{version}) - {language}")
    
    return "\n".join(output)

def format_json_output(apps: List[Dict[str, Any]]) -> str:
    """Uygulamaları JSON formatında formatlar"""
    return json.dumps(apps, indent=2, ensure_ascii=False)

def format_detailed_output(apps: List[Dict[str, Any]]) -> str:
    """Uygulamaları detaylı formatda formatlar"""
    if not apps:
        return "📭 Hiç uygulama kurulu değil."
    
    output = []
    output.append(f"📦 Kurulu Uygulamalar ({len(apps)})")
    output.append("=" * 60)
    
    for i, app in enumerate(sorted(apps, key=lambda x: x['name'].lower()), 1):
        output.append(f"\n{i}. {app['name']}")
        output.append(f"   Sürüm: {app['version']}")
        output.append(f"   Dil: {app['language']}")
        output.append(f"   Açıklama: {app['description']}")
        output.append(f"   Entry: {app['entry']}")
        output.append(f"   Klasör: {app['folder']}")
        output.append(f"   Yol: {app['path']}")
        
        if app['dependencies']:
            output.append(f"   Bağımlılıklar: {', '.join(app['dependencies'])}")
        else:
            output.append(f"   Bağımlılıklar: Yok")
    
    return "\n".join(output)

def filter_apps_by_language(apps: List[Dict[str, Any]], language: str) -> List[Dict[str, Any]]:
    """Uygulamaları dile göre filtreler"""
    return [app for app in apps if app['language'].lower() == language.lower()]

def filter_apps_by_name(apps: List[Dict[str, Any]], search_term: str) -> List[Dict[str, Any]]:
    """Uygulamaları isme göre filtreler"""
    search_term = search_term.lower()
    return [app for app in apps if search_term in app['name'].lower() or search_term in app['description'].lower()]

def list_apps(format_type: str = "table", language_filter: str = None, search_term: str = None) -> str:
    """
    Ana list fonksiyonu
    
    Args:
        format_type: Çıktı formatı (table, simple, json, detailed)
        language_filter: Dil filtresi (python, lua, vb.)
        search_term: Arama terimi
        
    Returns:
        Formatlanmış çıktı
    """
    apps = get_installed_apps_with_info()
    
    # Filtreleri uygula
    if language_filter:
        apps = filter_apps_by_language(apps, language_filter)
    
    if search_term:
        apps = filter_apps_by_name(apps, search_term)
    
    # Formatı uygula
    if format_type == "json":
        return format_json_output(apps)
    elif format_type == "simple":
        return format_simple_output(apps)
    elif format_type == "detailed":
        return format_detailed_output(apps)
    else:  # table (default)
        return format_table_output(apps)

def show_help():
    """Yardım mesajını gösterir"""
    help_text = """
clapp list - Kurulu uygulamaları listeler

Kullanım:
    python list_command.py [seçenekler]

Seçenekler:
    --format FORMAT     Çıktı formatı (table, simple, json, detailed)
    --language LANG     Dil filtresi (python, lua, vb.)
    --search TERM       Arama terimi (ad veya açıklamada)
    --help             Bu yardım mesajını göster

Örnekler:
    python list_command.py
    python list_command.py --format json
    python list_command.py --format simple
    python list_command.py --format detailed
    python list_command.py --language python
    python list_command.py --search calculator
    python list_command.py --language python --format detailed
    """
    print(help_text.strip())

def main():
    """CLI entry point"""
    # Komut satırı argümanlarını parse et
    args = sys.argv[1:]
    
    if "--help" in args or "-h" in args:
        show_help()
        sys.exit(0)
    
    format_type = "table"
    language_filter = None
    search_term = None
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg == "--format" and i + 1 < len(args):
            format_type = args[i + 1]
            i += 2
        elif arg == "--language" and i + 1 < len(args):
            language_filter = args[i + 1]
            i += 2
        elif arg == "--search" and i + 1 < len(args):
            search_term = args[i + 1]
            i += 2
        else:
            print(f"❌ Bilinmeyen argüman: {arg}")
            print("Yardım için: python list_command.py --help")
            sys.exit(1)
    
    # Format kontrolü
    valid_formats = ["table", "simple", "json", "detailed"]
    if format_type not in valid_formats:
        print(f"❌ Geçersiz format: {format_type}")
        print(f"Geçerli formatlar: {', '.join(valid_formats)}")
        sys.exit(1)
    
    # Uygulamaları listele
    try:
        output = list_apps(format_type, language_filter, search_term)
        print(output)
    except Exception as e:
        print(f"❌ Hata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 