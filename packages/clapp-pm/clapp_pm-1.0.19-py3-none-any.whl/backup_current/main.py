#!/usr/bin/env python3
"""
main.py - clapp Ana CLI Giriş Noktası

Bu dosya clapp'in ana komut satırı arayüzüdür.
Tüm komutları yönlendirir ve kullanıcı deneyimini yönetir.
"""

import argparse
import sys
import os
from pathlib import Path

# Mevcut modülleri import et
from clapp_core import list_apps, run_app
from cli_commands import (
    install_from_remote, upgrade_package, publish_package,
    search_remote_packages, show_package_info, list_all_packages,
    check_system_health, handle_publish_command, handle_install_command,
    handle_uninstall_command, handle_list_command, publish_to_repository
)
from installer import install_package, uninstall_package, install_from_directory
from remote_registry import list_remote_packages

# Yeni komut modüllerini import et
from post_install_hint import check_first_run, show_post_install_hint
from check_env import run_environment_check
from info_command import show_app_info
from validate_command import validate_app_folder
from doctor_command import run_doctor
from clean_command import run_clean
from where_command import locate_app_path, list_all_app_locations
from version_command import print_version, print_detailed_version

# Yeni publish.cursorrules komutları
from publish_command import publish_app
from install_command import install_app
from uninstall_command import uninstall_app
from list_command import list_apps as list_apps_new

def main():
    """Ana CLI fonksiyonu"""
    
    # İlk çalıştırma kontrolü
    first_run = check_first_run()
    if first_run:
        print()  # Boş satır ekle
    
    parser = argparse.ArgumentParser(
        prog='clapp',
        description='🚀 clapp - Hafif Çoklu Dil Uygulama Yöneticisi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
📚 Temel Komutlar:
  clapp list                    # Yüklü uygulamaları listele
  clapp run hello-python        # hello-python uygulamasını çalıştır
  clapp info hello-python       # Uygulama bilgilerini göster

🔧 Yönetim Komutları:
  clapp install app.zip         # ZIP dosyasından uygulama yükle
  clapp uninstall hello-python  # Uygulamayı kaldır
  clapp upgrade hello-python    # Uygulamayı güncelle
  clapp validate ./my-app       # Uygulama klasörünü doğrula
  clapp publish ./my-app        # Uygulama yayınla

🛠️  Sistem Komutları:
  clapp check-env               # Ortam kontrolü
  clapp doctor                  # Kapsamlı sistem tanılaması
  clapp clean                   # Geçici dosyaları temizle
  clapp where hello-python      # Uygulama konumunu göster
  clapp version                 # Sürüm bilgilerini göster

🌐 Uzak Komutlar:
  clapp search calculator       # Uzak depoda ara
  clapp remote list             # Uzak depo listesi
  clapp health                  # Sistem sağlık kontrolü

📖 Daha fazla bilgi için: https://github.com/mburakmmm/clapp
        """
    )
    
    # Alt komutlar
    subparsers = parser.add_subparsers(dest='command', help='Mevcut komutlar')
    
    # run komutu
    run_parser = subparsers.add_parser('run', help='Yüklü bir uygulamayı çalıştır')
    run_parser.add_argument('app_name', help='Çalıştırılacak uygulamanın adı')
    
    # list komutu
    list_parser = subparsers.add_parser('list', help='Yüklü uygulamaları listele')
    list_parser.add_argument('--all', action='store_true', help='Hem yerel hem uzak paketleri listele')
    list_parser.add_argument('--format', choices=['table', 'simple', 'json', 'detailed'], 
                           default='table', help='Çıktı formatı')
    list_parser.add_argument('--language', help='Dil filtresi (python, lua, vb.)')
    list_parser.add_argument('--search', help='Arama terimi (ad veya açıklamada)')
    
    # install komutu
    install_parser = subparsers.add_parser('install', help='Uygulama yükle')
    install_parser.add_argument('source', help='Uygulama adı, zip dosyası veya URL')
    install_parser.add_argument('--force', action='store_true', help='Mevcut uygulamanın üzerine yaz')
    install_parser.add_argument('--local', action='store_true', help='Yerel dizinden yükle')
    
    # uninstall komutu
    uninstall_parser = subparsers.add_parser('uninstall', help='Uygulama kaldır')
    uninstall_parser.add_argument('app_name', help='Kaldırılacak uygulamanın adı')
    uninstall_parser.add_argument('--yes', action='store_true', help='Onay sorma')
    
    # upgrade komutu
    upgrade_parser = subparsers.add_parser('upgrade', help='Uygulamayı güncelle')
    upgrade_parser.add_argument('app_name', help='Güncellenecek uygulamanın adı')
    
    # search komutu
    search_parser = subparsers.add_parser('search', help='Paket ara')
    search_parser.add_argument('query', help='Arama terimi')
    
    # info komutu (yeni)
    info_parser = subparsers.add_parser('info', help='Uygulama bilgilerini detaylı göster')
    info_parser.add_argument('app_name', help='Bilgisi gösterilecek uygulamanın adı')
    info_parser.add_argument('--remote', action='store_true', help='Uzak paket bilgisini göster')
    
    # validate komutu (yeni)
    validate_parser = subparsers.add_parser('validate', help='Uygulama klasörünü doğrula')
    validate_parser.add_argument('folder', help='Doğrulanacak klasör yolu')
    
    # publish komutu
    publish_parser = subparsers.add_parser('publish', help='Paket yayınla')
    publish_parser.add_argument('app_path', help='Yayınlanacak uygulama dizini')
    publish_parser.add_argument('--push', action='store_true', help='clapp-packages reposuna otomatik push et')
    
    # remote komutu
    remote_parser = subparsers.add_parser('remote', help='Uzak paket deposunu listele')
    remote_parser.add_argument('--details', action='store_true', help='Detayları göster')
    
    # health komutu
    health_parser = subparsers.add_parser('health', help='Sistem sağlığını kontrol et')
    
    # check-env komutu (yeni)
    check_env_parser = subparsers.add_parser('check-env', help='Ortam kontrolü yap')
    
    # doctor komutu (yeni)
    doctor_parser = subparsers.add_parser('doctor', help='Kapsamlı sistem tanılaması')
    
    # clean komutu (yeni)
    clean_parser = subparsers.add_parser('clean', help='Geçici dosyaları temizle')
    clean_parser.add_argument('--dry-run', action='store_true', help='Sadece göster, silme')
    
    # where komutu (yeni)
    where_parser = subparsers.add_parser('where', help='Uygulama konumunu göster')
    where_parser.add_argument('app_name', nargs='?', help='Konumu gösterilecek uygulamanın adı')
    where_parser.add_argument('--check-entry', action='store_true', help='Giriş dosyasını da kontrol et')
    where_parser.add_argument('--open', action='store_true', help='Dosya yöneticisinde aç')
    

    
    # version komutu (yeni)
    version_parser = subparsers.add_parser('version', help='Sürüm bilgisini göster')
    version_parser.add_argument('--short', action='store_true', help='Sadece sürüm numarası')
    version_parser.add_argument('--json', action='store_true', help='JSON formatında')
    version_parser.add_argument('--detailed', action='store_true', help='Detaylı bilgi')
    
    # Argümanları parse et
    args = parser.parse_args()
    
    # Komut yoksa help göster
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Komutları işle
        if args.command == 'run':
            success = run_app(args.app_name)
            sys.exit(0 if success else 1)
        
        elif args.command == 'list':
            if args.all:
                list_all_packages()
            else:
                # Yeni gelişmiş list komutu
                try:
                    output = list_apps_new(args.format, args.language, args.search)
                    print(output)
                except Exception as e:
                    print(f"❌ Liste hatası: {e}")
                    sys.exit(1)
        
        elif args.command == 'install':
            if args.local:
                # Yerel dizinden yükle
                success, message = install_from_directory(args.source, args.force)
            elif args.source.endswith('.zip') or '/' in args.source:
                # Zip dosyası veya URL
                success, message = install_package(args.source, args.force)
            else:
                # Yeni install komutu (GitHub'dan index.json ile)
                success, message = install_app(args.source)
            
            if not success:
                print(f"❌ {message}")
                sys.exit(1)
        
        elif args.command == 'uninstall':
            # Yeni uninstall komutu
            success, message = uninstall_app(args.app_name, args.yes)
            print(message)
            sys.exit(0 if success else 1)
        
        elif args.command == 'upgrade':
            success, message = upgrade_package(args.app_name)
            if not success:
                print(f"❌ {message}")
                sys.exit(1)
        
        elif args.command == 'search':
            success, message = search_remote_packages(args.query)
            if not success:
                print(f"❌ {message}")
                sys.exit(1)
        
        elif args.command == 'info':
            if args.remote:
                # Eski remote info fonksiyonu
                success, message = show_package_info(args.app_name, args.remote)
                if not success:
                    print(f"❌ {message}")
                    sys.exit(1)
            else:
                # Yeni detaylı info komutu
                success = show_app_info(args.app_name)
                sys.exit(0 if success else 1)
        
        elif args.command == 'validate':
            success = validate_app_folder(args.folder)
            sys.exit(0 if success else 1)
        
        elif args.command == 'publish':
            # Yeni publish komutu
            success, message = publish_app(args.app_path, push_to_github=args.push)
            if not success:
                print(f"❌ {message}")
                sys.exit(1)
        
        elif args.command == 'remote':
            output = list_remote_packages(args.details)
            print(output)
        
        elif args.command == 'health':
            check_system_health()
        
        elif args.command == 'check-env':
            success = run_environment_check()
            sys.exit(0 if success else 1)
        
        elif args.command == 'doctor':
            success = run_doctor()
            sys.exit(0 if success else 1)
        
        elif args.command == 'clean':
            success = run_clean(args.dry_run)
            sys.exit(0 if success else 1)
        
        elif args.command == 'where':
            if args.app_name:
                if args.open:
                    from where_command import open_app_location
                    success = open_app_location(args.app_name)
                else:
                    success = locate_app_path(args.app_name, args.check_entry)
                sys.exit(0 if success else 1)
            else:
                success = list_all_app_locations()
                sys.exit(0 if success else 1)
        

        
        elif args.command == 'version':
            if args.short:
                print_version("short")
            elif args.json:
                print_version("json")
            elif args.detailed:
                print_detailed_version()
            else:
                print_version("default")
    
    except KeyboardInterrupt:
        print("\n❌ İşlem iptal edildi")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 