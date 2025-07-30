import os
import argparse
from remote_registry import get_package_info, list_remote_packages, search_packages
from installer import install_package, uninstall_package, create_package_from_directory
from package_registry import list_packages, get_manifest
from dependency_resolver import get_dependency_report, get_system_dependency_report
from manifest_validator import validate_manifest_file, get_validation_summary

# Yeni komut modüllerini import et
from publish_command import publish_app
from install_command import install_app
from uninstall_command import uninstall_app
from list_command import list_apps

def install_from_remote(app_name, force=False):
    """
    Uzak paket deposundan uygulama yükler.
    
    Args:
        app_name (str): Yüklenecek uygulama adı
        force (bool): Mevcut uygulamanın üzerine yazılmasına izin ver
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Yeni install_command modülünü kullan
    return install_app(app_name)

def install_from_remote_legacy(app_name, force=False):
    """
    Uzak paket deposundan uygulama yükler (eski sistem).
    
    Args:
        app_name (str): Yüklenecek uygulama adı
        force (bool): Mevcut uygulamanın üzerine yazılmasına izin ver
        
    Returns:
        tuple: (success: bool, message: str)
    """
    print(f"'{app_name}' uzak paket deposunda aranıyor...")
    
    # Uzak paket bilgilerini al
    package_info = get_package_info(app_name)
    
    if not package_info:
        return False, f"'{app_name}' uzak paket deposunda bulunamadı"
    
    # İndirme URL'sini al
    download_url = package_info.get('download_url')
    if not download_url:
        return False, f"'{app_name}' için indirme URL'si bulunamadı"
    
    print(f"📦 {app_name} v{package_info.get('version', '0.0.0')}")
    print(f"📝 {package_info.get('description', 'Açıklama yok')}")
    print(f"💻 Dil: {package_info.get('language', 'Bilinmiyor')}")
    
    # Bağımlılıkları göster
    dependencies = package_info.get('dependencies', [])
    if dependencies:
        print(f"🔗 Bağımlılıklar: {', '.join(dependencies)}")
    
    print(f"⬇️  İndiriliyor: {download_url}")
    
    # Paketi yükle
    success, message = install_package(download_url, force)
    
    if success:
        print(f"✅ {message}")
        
        # Bağımlılık kontrolü
        print("\n🔍 Bağımlılıklar kontrol ediliyor...")
        dep_report = get_dependency_report(app_name)
        print(dep_report)
        
    else:
        print(f"❌ {message}")
    
    return success, message

def uninstall_from_local(app_name, skip_confirmation=False):
    """
    Yerel uygulamayı kaldırır.
    
    Args:
        app_name (str): Kaldırılacak uygulama adı
        skip_confirmation (bool): Onay sorma
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Yeni uninstall_command modülünü kullan
    return uninstall_app(app_name, skip_confirmation)

def publish_to_repository(app_path):
    """
    Uygulamayı repository'e publish eder.
    
    Args:
        app_path (str): Uygulama dizini
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Yeni publish_command modülünü kullan
    return publish_app(app_path)

def list_installed_apps(format_type="table", language_filter=None, search_term=None):
    """
    Kurulu uygulamaları listeler.
    
    Args:
        format_type (str): Çıktı formatı (table, simple, json, detailed)
        language_filter (str): Dil filtresi
        search_term (str): Arama terimi
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        output = list_apps(format_type, language_filter, search_term)
        print(output)
        return True, "Liste gösterildi"
    except Exception as e:
        return False, f"Liste hatası: {e}"

def upgrade_package(app_name):
    """
    Uygulamayı günceller.
    
    Args:
        app_name (str): Güncellenecek uygulama adı
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Yerel sürümü kontrol et
    local_manifest = get_manifest(app_name)
    if not local_manifest:
        return False, f"'{app_name}' yerel olarak yüklü değil"
    
    local_version = local_manifest.get('version', '0.0.0')
    
    # Uzak sürümü kontrol et
    remote_package = get_package_info(app_name)
    if not remote_package:
        return False, f"'{app_name}' uzak paket deposunda bulunamadı"
    
    remote_version = remote_package.get('version', '0.0.0')
    
    print(f"📦 {app_name}")
    print(f"📱 Yerel sürüm: {local_version}")
    print(f"🌐 Uzak sürüm: {remote_version}")
    
    # Sürüm karşılaştırması (basit string karşılaştırması)
    if local_version == remote_version:
        return True, f"'{app_name}' zaten güncel (v{local_version})"
    
    print(f"🔄 Güncelleme mevcut: {local_version} → {remote_version}")
    
    # Güncelleme için yeniden yükle
    return install_from_remote(app_name, force=True)

def publish_package(app_path):
    """
    Uygulama paketini yayınlamak için hazırlar.
    
    Args:
        app_path (str): Uygulama dizini
        
    Returns:
        tuple: (success: bool, message: str)
    """
    if not os.path.exists(app_path):
        return False, f"Dizin bulunamadı: {app_path}"
    
    if not os.path.isdir(app_path):
        return False, f"'{app_path}' bir dizin değil"
    
    print(f"📁 Paket hazırlanıyor: {app_path}")
    
    # Manifest doğrulama
    manifest_path = os.path.join(app_path, "manifest.json")
    is_valid, errors = validate_manifest_file(manifest_path)
    
    print("🔍 Manifest doğrulanıyor...")
    print(get_validation_summary(errors))
    
    if not is_valid:
        return False, "Manifest doğrulama başarısız"
    
    # Paketi oluştur
    success, message, output_file = create_package_from_directory(app_path)
    
    if success:
        print(f"✅ {message}")
        print("\n📋 Yayınlama talimatları:")
        print("1. Oluşturulan .clapp.zip dosyasını GitHub'a yükleyin")
        print("2. packages.json dosyasını güncelleyin")
        print("3. Pull request oluşturun")
        print(f"\n📁 Paket dosyası: {output_file}")
        
    else:
        print(f"❌ {message}")
    
    return success, message

def search_remote_packages(query):
    """
    Uzak paket deposunda arama yapar.
    
    Args:
        query (str): Arama terimi
        
    Returns:
        tuple: (success: bool, message: str)
    """
    print(f"🔍 Arama yapılıyor: '{query}'")
    
    results = search_packages(query)
    
    if not results:
        return False, f"'{query}' için sonuç bulunamadı"
    
    print(f"✅ {len(results)} sonuç bulundu:\n")
    
    for package in results:
        name = package.get('name', 'Bilinmiyor')
        version = package.get('version', '0.0.0')
        description = package.get('description', 'Açıklama yok')
        language = package.get('language', 'Bilinmiyor')
        
        print(f"📦 {name} (v{version})")
        print(f"   💻 Dil: {language}")
        print(f"   📝 {description}")
        print()
    
    return True, f"{len(results)} paket bulundu"

def show_package_info(app_name, remote=False):
    """
    Paket bilgilerini gösterir.
    
    Args:
        app_name (str): Uygulama adı
        remote (bool): Uzak paket deposundan bilgi al
        
    Returns:
        tuple: (success: bool, message: str)
    """
    if remote:
        # Uzak paket bilgisi
        package = get_package_info(app_name)
        if not package:
            return False, f"'{app_name}' uzak paket deposunda bulunamadı"
        
        print(f"🌐 Uzak Paket Bilgisi: {app_name}")
        print("=" * 40)
        
    else:
        # Yerel paket bilgisi
        package = get_manifest(app_name)
        if not package:
            return False, f"'{app_name}' yerel olarak yüklü değil"
        
        print(f"📱 Yerel Paket Bilgisi: {app_name}")
        print("=" * 40)
    
    # Paket bilgilerini göster
    print(f"📦 Ad: {package.get('name', 'Bilinmiyor')}")
    print(f"🔢 Sürüm: {package.get('version', '0.0.0')}")
    print(f"💻 Dil: {package.get('language', 'Bilinmiyor')}")
    print(f"📝 Açıklama: {package.get('description', 'Açıklama yok')}")
    print(f"🚀 Giriş: {package.get('entry', 'Bilinmiyor')}")
    
    # Bağımlılıklar
    dependencies = package.get('dependencies', [])
    if dependencies:
        print(f"🔗 Bağımlılıklar: {', '.join(dependencies)}")
    else:
        print("🔗 Bağımlılık yok")
    
    # Uzak paket için ek bilgiler
    if remote and 'download_url' in package:
        print(f"⬇️  İndirme: {package['download_url']}")
    
    # Yerel paket için bağımlılık raporu
    if not remote:
        print("\n" + get_dependency_report(app_name))
    
    return True, "Bilgi gösterildi"

def list_all_packages():
    """
    Hem yerel hem uzak paketleri listeler.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    print("📱 Yerel Paketler:")
    print("=" * 30)
    
    # Yerel paketler - yeni list_command kullan
    success, message = list_installed_apps("simple")
    
    print(f"\n🌐 Uzak Paketler:")
    print("=" * 30)
    
    # Uzak paketler
    remote_list = list_remote_packages()
    print(remote_list)
    
    return True, "Paket listesi gösterildi"

def check_system_health():
    """
    Sistem sağlığını kontrol eder.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    print("🏥 Sistem Sağlık Kontrolü")
    print("=" * 40)
    
    # Bağımlılık kontrolü
    print("🔍 Bağımlılıklar kontrol ediliyor...")
    dep_report = get_system_dependency_report()
    print(dep_report)
    
    # Uzak bağlantı kontrolü
    print("🌐 Uzak bağlantı kontrol ediliyor...")
    from remote_registry import check_remote_connectivity
    
    if check_remote_connectivity():
        print("✅ Uzak paket deposuna bağlantı başarılı")
    else:
        print("❌ Uzak paket deposuna bağlantı kurulamadı")
    
    # Manifest doğrulama
    print("\n🔍 Tüm manifest'ler doğrulanıyor...")
    local_packages = list_packages()
    invalid_count = 0
    
    for package in local_packages:
        app_name = package['name']
        app_path = os.path.join("apps", app_name)
        manifest_path = os.path.join(app_path, "manifest.json")
        
        is_valid, errors = validate_manifest_file(manifest_path)
        if not is_valid:
            print(f"❌ {app_name}: Geçersiz manifest")
            invalid_count += 1
    
    if invalid_count == 0:
        print("✅ Tüm manifest'ler geçerli")
    else:
        print(f"❌ {invalid_count} geçersiz manifest bulundu")
    
    return True, "Sistem sağlık kontrolü tamamlandı"

# Yeni komut fonksiyonları
def handle_publish_command(args):
    """Publish komutunu işler"""
    if not args.folder:
        print("❌ Hata: Publish edilecek klasör belirtilmedi")
        print("Kullanım: clapp publish <folder>")
        return False, "Klasör belirtilmedi"
    
    return publish_to_repository(args.folder)

def handle_install_command(args):
    """Install komutunu işler"""
    if not args.app_name:
        print("❌ Hata: Kurulacak uygulama adı belirtilmedi")
        print("Kullanım: clapp install <app_name>")
        return False, "Uygulama adı belirtilmedi"
    
    return install_from_remote(args.app_name)

def handle_uninstall_command(args):
    """Uninstall komutunu işler"""
    if not args.app_name:
        print("❌ Hata: Kaldırılacak uygulama adı belirtilmedi")
        print("Kullanım: clapp uninstall <app_name>")
        return False, "Uygulama adı belirtilmedi"
    
    return uninstall_from_local(args.app_name, args.yes)

def handle_list_command(args):
    """List komutunu işler"""
    format_type = getattr(args, 'format', 'table')
    language_filter = getattr(args, 'language', None)
    search_term = getattr(args, 'search', None)
    
    return list_installed_apps(format_type, language_filter, search_term)

if __name__ == "__main__":
    # Test için örnek kullanım
    print("CLI Commands Test")
    print("=" * 30)
    
    # Sistem sağlığını kontrol et
    check_system_health()
    
    print("\nTest tamamlandı.") 