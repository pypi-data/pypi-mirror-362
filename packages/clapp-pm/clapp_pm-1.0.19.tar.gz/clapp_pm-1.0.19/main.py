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

# Yeni güvenlik ve performans modülleri
from package_signing import check_package_security
from version_manager import check_app_updates, get_app_latest_version, increment_app_version
from cache_manager import get_cache_stats, clear_all_caches, download_packages_parallel
from smart_search import search_packages, get_search_suggestions, get_search_analytics, clear_search_history

# Yeni publish.cursorrules komutları
from publish_command import publish_app
from install_command import install_app
from uninstall_command import uninstall_app
from list_command import list_apps as list_apps_new

# Dependency yönetimi komutları
from dependency_resolver import (
    handle_dependency_check,
    handle_dependency_install,
    handle_engine_check,
    handle_dependency_tree
)

# Yeni uygulama oluşturma komutu
from new_command import handle_new_command

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
  clapp new python my-app       # Yeni Python uygulaması oluştur

🔧 Yönetim Komutları:
  clapp install app.zip         # ZIP dosyasından uygulama yükle
  clapp uninstall hello-python  # Uygulamayı kaldır
  clapp upgrade hello-python    # Uygulamayı güncelle
  clapp validate ./my-app       # Uygulama klasörünü doğrula
  clapp publish ./my-app        # Uygulama yayınla

🔗 Bağımlılık Komutları:
  clapp dependency check        # Sistem geneli bağımlılık kontrolü
  clapp dependency check app    # Belirli uygulama bağımlılık kontrolü
  clapp dependency install app  # Uygulama bağımlılıklarını kur
  clapp dependency engine app   # Engine kontrolü
  clapp dependency tree app     # Bağımlılık ağacı

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
    
    # Güvenlik komutları
    security_parser = subparsers.add_parser('security', help='Paket güvenlik işlemleri')
    security_parser.add_argument('action', choices=['sign', 'verify', 'check'], help='Güvenlik işlemi')
    security_parser.add_argument('package_path', help='Paket dosyası yolu')
    security_parser.add_argument('--signature', help='İmza dosyası yolu (verify için)')
    
    # Versiyon yönetimi komutları
    update_parser = subparsers.add_parser('update', help='Versiyon yönetimi')
    update_parser.add_argument('action', choices=['check', 'increment'], help='İşlem türü')
    update_parser.add_argument('--app', help='Uygulama adı')
    update_parser.add_argument('--type', choices=['major', 'minor', 'patch'], default='patch', help='Artırma tipi')
    
    # Cache yönetimi komutları
    cache_parser = subparsers.add_parser('cache', help='Cache yönetimi')
    cache_parser.add_argument('action', choices=['stats', 'clear', 'download'], help='Cache işlemi')
    cache_parser.add_argument('--urls', nargs='+', help='İndirilecek URL\'ler (download için)')
    cache_parser.add_argument('--dest', help='Hedef dizin (download için)')
    
    # Akıllı arama komutları
    search_parser = subparsers.add_parser('search', help='Akıllı arama')
    search_parser.add_argument('query', nargs='?', help='Arama sorgusu')
    search_parser.add_argument('--suggestions', action='store_true', help='Arama önerileri')
    search_parser.add_argument('--analytics', action='store_true', help='Arama analitikleri')
    search_parser.add_argument('--clear-history', action='store_true', help='Arama geçmişini temizle')
    search_parser.add_argument('--language', help='Dil filtresi')
    search_parser.add_argument('--category', help='Kategori filtresi')
    search_parser.add_argument('--sort', choices=['relevance', 'name', 'version', 'language'], default='relevance', help='Sıralama')
    
    # dependency komutu (yeni)
    dependency_parser = subparsers.add_parser('dependency', help='Bağımlılık yönetimi')
    dependency_subparsers = dependency_parser.add_subparsers(dest='dependency_command', help='Bağımlılık alt komutları')
    
    # dependency check
    dep_check_parser = dependency_subparsers.add_parser('check', help='Bağımlılık kontrolü')
    dep_check_parser.add_argument('app_name', nargs='?', help='Uygulama adı (opsiyonel)')
    
    # dependency install
    dep_install_parser = dependency_subparsers.add_parser('install', help='Bağımlılık kurulumu')
    dep_install_parser.add_argument('app_name', help='Uygulama adı')
    dep_install_parser.add_argument('--force', '-f', action='store_true', help='Zorla kurulum')
    
    # dependency engine
    dep_engine_parser = dependency_subparsers.add_parser('engine', help='Engine kontrolü')
    dep_engine_parser.add_argument('app_name', nargs='?', help='Uygulama adı (opsiyonel)')
    
    # dependency tree
    dep_tree_parser = dependency_subparsers.add_parser('tree', help='Bağımlılık ağacı')
    dep_tree_parser.add_argument('app_name', help='Uygulama adı')
    
    # new komutu (yeni)
    new_parser = subparsers.add_parser('new', help='Yeni uygulama oluştur')
    new_parser.add_argument('language', nargs='?', help='Programlama dili')
    new_parser.add_argument('app_name', nargs='?', help='Uygulama adı')
    new_parser.add_argument('--list', action='store_true', help='Mevcut şablonları listele')
    new_parser.add_argument('--target-dir', help='Hedef dizin (opsiyonel)')
    
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
        
        elif args.command == 'dependency':
            # Dependency komutlarını işle
            if args.dependency_command == 'check':
                handle_dependency_check(args)
            elif args.dependency_command == 'install':
                success, message = handle_dependency_install(args)
                if not success:
                    print(f"❌ {message}")
                    sys.exit(1)
            elif args.dependency_command == 'engine':
                success, message = handle_engine_check(args)
                if not success:
                    print(f"❌ {message}")
                    sys.exit(1)
            elif args.dependency_command == 'tree':
                success, message = handle_dependency_tree(args)
                if not success:
                    print(f"❌ {message}")
                    sys.exit(1)
            else:
                print("❌ Geçersiz dependency komutu")
                sys.exit(1)
        
        elif args.command == 'new':
            # Yeni uygulama oluşturma komutu
            success, message = handle_new_command(args)
            if success:
                print(message)
            else:
                print(f"❌ {message}")
                sys.exit(1)
        
        elif args.command == 'security':
            if args.action == 'check':
                results = check_package_security(args.package_path)
                print("🔒 Paket Güvenlik Kontrolü")
                print("=" * 40)
                print(f"Bütünlük: {'✅' if results['integrity'] else '❌'}")
                print(f"İmza: {'✅' if results['signature'] else '❌'}")
                print(f"Checksum: {results['checksum']}")
                if results['warnings']:
                    print("\n⚠️  Uyarılar:")
                    for warning in results['warnings']:
                        print(f"  - {warning}")
            else:
                print("❌ İmzalama özelliği geçici olarak devre dışı")
                sys.exit(1)
        
        elif args.command == 'update':
            if args.action == 'check':
                if not args.app:
                    print("❌ --app parametresi gerekli")
                    sys.exit(1)
                
                from package_registry import get_manifest
                manifest = get_manifest(args.app)
                if not manifest:
                    print(f"❌ {args.app} uygulaması bulunamadı")
                    sys.exit(1)
                
                current_version = manifest.get('version', '0.0.0')
                update_info = check_app_updates(args.app, current_version)
                
                print(f"📦 {args.app} Güncelleme Kontrolü")
                print("=" * 40)
                print(f"Mevcut: {update_info['current_version']}")
                print(f"En son: {update_info['latest_version'] or 'Bilinmiyor'}")
                print(f"Durum: {update_info['message']}")
                
                if update_info['has_update']:
                    print(f"Güncelleme tipi: {update_info['update_type']}")
            
            elif args.action == 'increment':
                if not args.app:
                    print("❌ --app parametresi gerekli")
                    sys.exit(1)
                
                from package_registry import get_manifest
                manifest = get_manifest(args.app)
                if not manifest:
                    print(f"❌ {args.app} uygulaması bulunamadı")
                    sys.exit(1)
                
                current_version = manifest.get('version', '0.0.0')
                new_version = increment_app_version(current_version, args.type)
                print(f"📦 {args.app} versiyonu artırıldı")
                print(f"Eski: {current_version} → Yeni: {new_version}")
        
        elif args.command == 'cache':
            if args.action == 'stats':
                stats = get_cache_stats()
                print("📊 Cache İstatistikleri")
                print("=" * 30)
                print(f"Hit: {stats['hits']}")
                print(f"Miss: {stats['misses']}")
                print(f"Hit Rate: {stats['hit_rate']}%")
                print(f"Boyut: {stats['size_mb']} MB")
            
            elif args.action == 'clear':
                deleted_count = clear_all_caches()
                print(f"✅ {deleted_count} cache dosyası silindi")
            
            elif args.action == 'download':
                if not args.urls or not args.dest:
                    print("❌ --urls ve --dest parametreleri gerekli")
                    sys.exit(1)
                
                os.makedirs(args.dest, exist_ok=True)
                results = download_packages_parallel(args.urls, args.dest)
                
                print("📥 Paralel İndirme Sonuçları")
                print("=" * 40)
                for success, message in results:
                    print(f"{'✅' if success else '❌'} {message}")
        
        elif args.command == 'search':
            if args.suggestions:
                from package_registry import list_packages
                packages = list_packages()
                suggestions = get_search_suggestions(args.query or "", packages)
                print("💡 Arama Önerileri")
                print("=" * 20)
                for suggestion in suggestions:
                    print(f"  • {suggestion}")
            
            elif args.analytics:
                analytics = get_search_analytics()
                print("📈 Arama Analitikleri")
                print("=" * 25)
                print(f"Toplam arama: {analytics['total_searches']}")
                print(f"Benzersiz sorgu: {analytics['unique_queries']}")
                print(f"Hit rate: {round(analytics['total_searches'] / max(1, analytics['unique_queries']) * 100, 1)}%")
                
                if analytics['most_popular']:
                    print("\n🔥 Popüler Aramalar:")
                    for query, count in analytics['most_popular']:
                        print(f"  • {query} ({count} kez)")
            
            elif args.clear_history:
                clear_search_history()
            
            elif args.query:
                from package_registry import list_packages
                packages = list_packages()
                
                filters = {}
                if args.language:
                    filters['language'] = args.language
                if args.category:
                    filters['category'] = args.category
                if args.sort:
                    filters['sort_by'] = args.sort
                
                results = search_packages(args.query, packages, filters)
                
                print(f"🔍 '{args.query}' için {len(results)} sonuç bulundu")
                print("=" * 50)
                
                for package in results:
                    score = package.get('search_score', 0)
                    print(f"📦 {package['name']} v{package['version']} ({package['language']})")
                    print(f"   {package['description']}")
                    if score > 0:
                        print(f"   Skor: {score:.2f}")
                    print()
            
            else:
                print("❌ Arama sorgusu gerekli veya --suggestions/--analytics kullanın")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n❌ İşlem iptal edildi")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 