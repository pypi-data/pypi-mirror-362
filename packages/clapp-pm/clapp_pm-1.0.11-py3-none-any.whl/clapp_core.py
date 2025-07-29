import os
import json
import argparse
from package_registry import list_packages
from package_runner import run_app

def main():
    """
    clapp CLI'sinin ana giriş noktası. Komut satırı argümanlarını işler ve uygun fonksiyonları çağırır.
    """
    parser = argparse.ArgumentParser(
        description='clapp - Basit paket yöneticisi',
        prog='clapp'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Mevcut komutlar')
    
    # run komutu
    run_parser = subparsers.add_parser('run', help='Yüklü bir uygulamayı çalıştır')
    run_parser.add_argument('app_name', help='Çalıştırılacak uygulamanın adı')
    
    # list komutu
    list_parser = subparsers.add_parser('list', help='Yüklü uygulamaları listele')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        success = run_app(args.app_name)
        if not success:
            exit(1)
    
    elif args.command == 'list':
        list_apps()
    
    else:
        parser.print_help()

def list_apps():
    """
    Yüklü uygulamaları listeler ve konsola yazdırır.
    """
    packages = list_packages()
    
    if not packages:
        print("Yüklü uygulama bulunamadı.")
        print("Uygulamaları 'apps/' dizinine yerleştirin.")
        return
    
    print(f"Yüklü Uygulamalar ({len(packages)} adet):")
    print("-" * 50)
    
    for package in packages:
        print(f"📦 {package['name']} (v{package['version']})")
        print(f"   Dil: {package['language']}")
        print(f"   Açıklama: {package['description']}")
        if package['dependencies']:
            print(f"   Bağımlılıklar: {', '.join(package['dependencies'])}")
        print()

if __name__ == '__main__':
    main() 