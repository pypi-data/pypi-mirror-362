#!/usr/bin/env python3
"""
Bağımlılık Yönetimi Komutu
==========================

Bu modül bağımlılık yönetimi için CLI komutlarını sağlar.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

from dependency_resolver import (
    check_and_install_python_dependencies,
    check_and_install_lua_dependencies,
    check_engine_availability,
    get_dependency_report,
    get_system_dependency_report,
    get_enhanced_system_dependency_report,
    resolve_all_dependencies
)
from package_registry import get_apps_directory, list_packages, get_manifest

def handle_dependency_check(args):
    """Bağımlılık kontrolü komutunu işler"""
    app_name = args.app_name
    
    if app_name:
        # Belirli bir uygulama için bağımlılık kontrolü
        print(f"🔍 {app_name} bağımlılık kontrolü...")
        print("=" * 50)
        
        # Bağımlılık raporu
        report = get_dependency_report(app_name)
        print(report)
        
        # Detaylı çözümleme
        resolution = resolve_all_dependencies(app_name)
        if resolution["status"] == "resolved":
            print("✅ Tüm bağımlılıklar çözümlenmiş!")
        elif resolution["status"] == "missing_dependencies":
            print("❌ Eksik bağımlılıklar var!")
        else:
            print(f"⚠️  Durum: {resolution['status']}")
        
    else:
        # Sistem geneli bağımlılık kontrolü
        print("🔍 Sistem geneli bağımlılık kontrolü...")
        print("=" * 50)
        
        report = get_system_dependency_report()
        print(report)
        
        # Gelişmiş sistem raporu
        enhanced_report = get_enhanced_system_dependency_report()
        print("\n" + enhanced_report)

def handle_dependency_install(args):
    """Bağımlılık kurulumu komutunu işler"""
    app_name = args.app_name
    force = args.force
    
    if not app_name:
        print("❌ Uygulama adı belirtilmelidir!")
        return False, "Uygulama adı eksik"
    
    apps_dir = get_apps_directory()
    app_path = os.path.join(apps_dir, app_name)
    
    if not os.path.exists(app_path):
        return False, f"Uygulama bulunamadı: {app_name}"
    
    print(f"🔧 {app_name} bağımlılıkları kuruluyor...")
    print("=" * 50)
    
    # Manifest'i oku
    manifest_path = os.path.join(app_path, "manifest.json")
    if not os.path.exists(manifest_path):
        return False, "Manifest dosyası bulunamadı"
    
    try:
        import json
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except Exception as e:
        return False, f"Manifest okuma hatası: {e}"
    
    language = manifest.get('language', 'unknown')
    
    if language == 'python':
        success, message, missing_packages = check_and_install_python_dependencies(app_path)
        if success:
            if missing_packages:
                print(f"✅ {message}")
                print(f"📦 Kurulan paketler: {', '.join(missing_packages)}")
            else:
                print("✅ Tüm Python bağımlılıkları zaten kurulu")
            return True, message
        else:
            return False, message
    
    elif language == 'lua':
        success, message, missing_packages = check_and_install_lua_dependencies(app_path)
        if success:
            if missing_packages:
                print(f"✅ {message}")
                print(f"🪨 Kurulan paketler: {', '.join(missing_packages)}")
            else:
                print("✅ Tüm Lua bağımlılıkları zaten kurulu")
            return True, message
        else:
            return False, message
    
    else:
        return False, f"Desteklenmeyen dil: {language}"

def handle_engine_check(args):
    """Engine kontrolü komutunu işler"""
    app_name = args.app_name
    
    if app_name:
        # Belirli bir uygulama için engine kontrolü
        apps_dir = get_apps_directory()
        app_path = os.path.join(apps_dir, app_name)
        
        if not os.path.exists(app_path):
            return False, f"Uygulama bulunamadı: {app_name}"
        
        print(f"🔧 {app_name} engine kontrolü...")
        print("=" * 50)
        
        available, message, engine_info = check_engine_availability(app_path)
        
        if available:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
        
        if engine_info:
            print(f"📊 Engine Bilgileri:")
            print(f"  - Ad: {engine_info.get('name', 'Bilinmiyor')}")
            print(f"  - Dil: {engine_info.get('language', 'Bilinmiyor')}")
            print(f"  - Gerekli: {engine_info.get('required', False)}")
            print(f"  - Mevcut: {engine_info.get('available', False)}")
        
        return available, message
    
    else:
        # Tüm uygulamalar için engine kontrolü
        print("🔧 Sistem geneli engine kontrolü...")
        print("=" * 50)
        
        packages = list_packages()
        engine_report = {
            "total_apps": len(packages),
            "apps_with_engines": 0,
            "apps_with_missing_engines": 0,
            "engine_details": []
        }
        
        for package in packages:
            app_name = package['name']
            apps_dir = get_apps_directory()
            app_path = os.path.join(apps_dir, app_name)
            
            available, message, engine_info = check_engine_availability(app_path)
            
            if engine_info:
                engine_report["apps_with_engines"] += 1
                if not available:
                    engine_report["apps_with_missing_engines"] += 1
                
                engine_report["engine_details"].append({
                    "app": app_name,
                    "engine": engine_info.get('name', 'Bilinmiyor'),
                    "language": engine_info.get('language', 'Bilinmiyor'),
                    "available": available,
                    "message": message
                })
        
        # Raporu yazdır
        print(f"📊 Engine Raporu:")
        print(f"  - Toplam Uygulama: {engine_report['total_apps']}")
        print(f"  - Engine Gereksinimi: {engine_report['apps_with_engines']}")
        print(f"  - Eksik Engine: {engine_report['apps_with_missing_engines']}")
        print()
        
        if engine_report["engine_details"]:
            print("🔍 Detaylı Engine Durumu:")
            for detail in engine_report["engine_details"]:
                status = "✅" if detail["available"] else "❌"
                print(f"  {status} {detail['app']}: {detail['engine']} ({detail['language']})")
        
        return True, "Engine kontrolü tamamlandı"

def handle_dependency_tree(args):
    """Bağımlılık ağacı komutunu işler"""
    app_name = args.app_name
    
    if not app_name:
        print("❌ Uygulama adı belirtilmelidir!")
        return False, "Uygulama adı eksik"
    
    print(f"🌳 {app_name} bağımlılık ağacı...")
    print("=" * 50)
    
    resolution = resolve_all_dependencies(app_name)
    
    if resolution["status"] == "error":
        print(f"❌ Hata: {resolution.get('dependency_tree', {}).get('error', 'Bilinmeyen hata')}")
        return False, "Bağımlılık ağacı oluşturulamadı"
    
    tree = resolution["dependency_tree"]
    
    def print_tree(node, level=0):
        indent = "  " * level
        status = "✅" if node.get("missing_dependencies") == [] else "❌"
        print(f"{indent}{status} {node['name']} (v{node['version']}) [{node['language']}]")
        
        if node.get("missing_dependencies"):
            for missing in node["missing_dependencies"]:
                print(f"{indent}  ❌ Eksik: {missing}")
        
        for dep in node.get("dependencies", []):
            print_tree(dep, level + 1)
    
    print_tree(tree)
    
    print(f"\n📊 Özet:")
    print(f"  - Durum: {resolution['status']}")
    print(f"  - Toplam Bağımlılık: {len(resolution['all_dependencies'])}")
    print(f"  - Eksik: {len(resolution['missing_dependencies'])}")
    
    return True, "Bağımlılık ağacı gösterildi"

def main():
    """Ana CLI fonksiyonu"""
    parser = argparse.ArgumentParser(
        description="CLAPP Bağımlılık Yönetimi",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  clapp dependency check hello-python     # Belirli uygulama bağımlılık kontrolü
  clapp dependency check                  # Sistem geneli bağımlılık kontrolü
  clapp dependency install hello-python   # Bağımlılıkları kur
  clapp dependency engine hello-python    # Engine kontrolü
  clapp dependency tree hello-python      # Bağımlılık ağacı
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Alt komutlar')
    
    # Check komutu
    check_parser = subparsers.add_parser('check', help='Bağımlılık kontrolü')
    check_parser.add_argument('app_name', nargs='?', help='Uygulama adı (opsiyonel)')
    
    # Install komutu
    install_parser = subparsers.add_parser('install', help='Bağımlılık kurulumu')
    install_parser.add_argument('app_name', help='Uygulama adı')
    install_parser.add_argument('--force', '-f', action='store_true', help='Zorla kurulum')
    
    # Engine komutu
    engine_parser = subparsers.add_parser('engine', help='Engine kontrolü')
    engine_parser.add_argument('app_name', nargs='?', help='Uygulama adı (opsiyonel)')
    
    # Tree komutu
    tree_parser = subparsers.add_parser('tree', help='Bağımlılık ağacı')
    tree_parser.add_argument('app_name', help='Uygulama adı')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'check':
            handle_dependency_check(args)
        elif args.command == 'install':
            success, message = handle_dependency_install(args)
            if not success:
                print(f"❌ {message}")
                sys.exit(1)
        elif args.command == 'engine':
            success, message = handle_engine_check(args)
            if not success:
                print(f"❌ {message}")
                sys.exit(1)
        elif args.command == 'tree':
            success, message = handle_dependency_tree(args)
            if not success:
                print(f"❌ {message}")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⚠️  İşlem iptal edildi")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 