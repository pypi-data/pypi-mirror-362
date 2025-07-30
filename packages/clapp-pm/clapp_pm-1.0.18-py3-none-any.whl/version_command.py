#!/usr/bin/env python3
"""
version_command.py - Sürüm bilgisi modülü

Bu modül `clapp version` komutunu destekler ve
clapp'in sürüm bilgilerini gösterir.
"""

import sys
import platform
import json
from pathlib import Path

def get_version_info():
    """Sürüm bilgilerini toplar"""
    # version.py dosyasından sürüm bilgisini oku
    try:
        from version import __version__, __author__, __email__, __description__
        app_name = "clapp"
        version = __version__
        author = __author__
        email = __email__
        description = __description__
    except ImportError:
        # Fallback değerler
        app_name = "clapp"
        version = "1.0.5"
        author = "Melih Burak Memiş"
        email = "mburakmemiscy@gmail.com"
        description = "Lightweight cross-language app manager for Python and Lua"
    
    # Sistem bilgileri
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    system_info = platform.system()
    machine = platform.machine()
    
    return {
        "app_name": app_name,
        "version": version,
        "author": author,
        "python_version": python_version,
        "system": system_info,
        "machine": machine,
        "platform": f"{system_info} {platform.release()}"
    }

def print_version(format_type="default"):
    """Sürüm bilgisini yazdırır"""
    info = get_version_info()
    
    if format_type == "short":
        print(info["version"])
    elif format_type == "json":
        import json
        output = {
            "version": info["version"],
            "python": info["python_version"],
            "os": info["system"],
            "machine": info["machine"]
        }
        print(json.dumps(output, indent=2))
    else:  # default
        print(f"🚀 {info['app_name']} v{info['version']}")
        print(f"🐍 Python {info['python_version']}")
        print(f"💻 Platform: {info['platform']} ({info['machine']})")
        print(f"👨‍💻 Yazar: {info['author']}")

def print_detailed_version():
    """Detaylı sürüm bilgisini yazdırır"""
    info = get_version_info()
    
    print("📋 clapp Detaylı Sürüm Bilgileri")
    print("=" * 50)
    
    # Temel bilgiler
    print("🚀 Uygulama Bilgileri:")
    print(f"   Ad: {info['app_name']}")
    print(f"   Sürüm: {info['version']}")
    print(f"   Yazar: {info['author']}")
    print()
    
    # Python bilgileri
    print("🐍 Python Bilgileri:")
    print(f"   Sürüm: {info['python_version']}")
    print(f"   Çalıştırılabilir: {sys.executable}")
    print(f"   Prefix: {sys.prefix}")
    print()
    
    # Platform bilgileri
    print("💻 Platform Bilgileri:")
    print(f"   İşletim Sistemi: {info['system']}")
    print(f"   Sürüm: {platform.release()}")
    print(f"   Mimari: {info['machine']}")
    print(f"   İşlemci: {platform.processor()}")
    print()
    
    # Modül bilgileri
    print("📦 Modül Bilgileri:")
    try:
        import flet
        print(f"   Flet: v{flet.__version__}")
    except ImportError:
        print("   Flet: Yüklü değil")
    
    # Ek bilgiler
    print()
    print("📁 Dizin Bilgileri:")
    print(f"   Çalışma Dizini: {Path.cwd()}")
    
    # apps/ dizini kontrolü
    apps_dir = Path("apps")
    if apps_dir.exists():
        app_count = len([d for d in apps_dir.iterdir() if d.is_dir()])
        print(f"   Apps Dizini: {apps_dir.resolve()} ({app_count} uygulama)")
    else:
        print("   Apps Dizini: Bulunamadı")

def check_latest_version():
    """En son sürümü kontrol eder (placeholder)"""
    print("🔍 En son sürüm kontrol ediliyor...")
    print("⚠️  Bu özellik henüz mevcut değil.")
    print("📞 Manuel kontrol için: https://github.com/user/clapp")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--short":
            print_version("short")
        elif arg == "--json":
            print_version("json")
        elif arg == "--detailed":
            print_detailed_version()
        elif arg == "--latest":
            check_latest_version()
        else:
            print_version("default")
    else:
        print_version("default") 