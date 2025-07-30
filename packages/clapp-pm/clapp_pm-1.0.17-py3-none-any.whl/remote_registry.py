import json
import urllib.request
import urllib.parse
from typing import List, Dict, Optional

# Uzak paket deposu URL'si
REMOTE_PACKAGES_URL = "https://raw.githubusercontent.com/mburakmmm/clapp-packages/main/packages.json"

def fetch_remote_packages() -> List[Dict]:
    """
    Uzak paket deposundan paket listesini indirir.
    
    Returns:
        list: Paket listesi (dict formatında)
    """
    try:
        print("Uzak paket deposu kontrol ediliyor...")
        
        # HTTP isteği gönder
        with urllib.request.urlopen(REMOTE_PACKAGES_URL) as response:
            data = response.read().decode('utf-8')
        
        # JSON'u parse et
        packages = json.loads(data)
        
        print(f"✅ {len(packages)} paket bulundu")
        return packages
        
    except urllib.error.URLError as e:
        print(f"❌ Ağ hatası: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse hatası: {e}")
        return []
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        return []

def get_package_info(app_name: str) -> Optional[Dict]:
    """
    Belirtilen uygulama için uzak paket bilgilerini döndürür.
    
    Args:
        app_name (str): Uygulama adı
        
    Returns:
        dict or None: Paket bilgileri veya None
    """
    packages = fetch_remote_packages()
    
    for package in packages:
        if package.get('name') == app_name:
            return package
    
    return None

def search_packages(query: str) -> List[Dict]:
    """
    Paket deposunda arama yapar.
    
    Args:
        query (str): Arama terimi
        
    Returns:
        list: Eşleşen paketler
    """
    packages = fetch_remote_packages()
    results = []
    
    query_lower = query.lower()
    
    for package in packages:
        # İsim, açıklama ve dilde arama yap
        name = package.get('name', '').lower()
        description = package.get('description', '').lower()
        language = package.get('language', '').lower()
        
        if (query_lower in name or 
            query_lower in description or 
            query_lower in language):
            results.append(package)
    
    return results

def get_packages_by_language(language: str) -> List[Dict]:
    """
    Belirtilen dildeki paketleri döndürür.
    
    Args:
        language (str): Programlama dili
        
    Returns:
        list: Belirtilen dildeki paketler
    """
    packages = fetch_remote_packages()
    filtered_packages = []
    
    for package in packages:
        if package.get('language', '').lower() == language.lower():
            filtered_packages.append(package)
    
    return filtered_packages

def list_remote_packages(show_details=False) -> str:
    """
    Uzak paket deposundaki paketleri listeler.
    
    Args:
        show_details (bool): Detayları göster
        
    Returns:
        str: Formatlanmış paket listesi
    """
    packages = fetch_remote_packages()
    
    if not packages:
        return "❌ Uzak paket deposuna erişilemedi veya paket bulunamadı"
    
    output = f"🌐 Uzak Paket Deposu ({len(packages)} paket)\n"
    output += "=" * 50 + "\n"
    
    # Dillere göre grupla
    by_language = {}
    for package in packages:
        language = package.get('language', 'unknown')
        if language not in by_language:
            by_language[language] = []
        by_language[language].append(package)
    
    for language, lang_packages in sorted(by_language.items()):
        output += f"\n📚 {language.upper()} ({len(lang_packages)} paket):\n"
        
        for package in sorted(lang_packages, key=lambda x: x.get('name', '')):
            name = package.get('name', 'Bilinmiyor')
            version = package.get('version', '0.0.0')
            description = package.get('description', 'Açıklama yok')
            
            output += f"  📦 {name} (v{version})\n"
            
            if show_details:
                output += f"      Açıklama: {description}\n"
                output += f"      İndirme: {package.get('download_url', 'Yok')}\n"
                
                if package.get('dependencies'):
                    deps = ', '.join(package['dependencies'])
                    output += f"      Bağımlılıklar: {deps}\n"
    
    return output

def validate_package_url(url: str) -> bool:
    """
    Paket URL'sinin geçerli olup olmadığını kontrol eder.
    
    Args:
        url (str): Kontrol edilecek URL
        
    Returns:
        bool: Geçerliyse True
    """
    try:
        # URL formatını kontrol et
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False
        
        # HTTP HEAD isteği gönder
        request = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(request) as response:
            return response.status == 200
            
    except Exception:
        return False

def get_package_statistics() -> Dict:
    """
    Paket deposu istatistiklerini döndürür.
    
    Returns:
        dict: İstatistik bilgileri
    """
    packages = fetch_remote_packages()
    
    stats = {
        "total_packages": len(packages),
        "languages": {},
        "with_dependencies": 0,
        "without_dependencies": 0,
        "total_dependencies": 0
    }
    
    for package in packages:
        # Dil istatistikleri
        language = package.get('language', 'unknown')
        stats["languages"][language] = stats["languages"].get(language, 0) + 1
        
        # Bağımlılık istatistikleri
        dependencies = package.get('dependencies', [])
        if dependencies:
            stats["with_dependencies"] += 1
            stats["total_dependencies"] += len(dependencies)
        else:
            stats["without_dependencies"] += 1
    
    return stats

def get_statistics_report() -> str:
    """
    İstatistik raporunu döndürür.
    
    Returns:
        str: Formatlanmış istatistik raporu
    """
    stats = get_package_statistics()
    
    if stats["total_packages"] == 0:
        return "❌ Paket deposu verisi alınamadı"
    
    report = "📊 Paket Deposu İstatistikleri\n"
    report += "=" * 40 + "\n"
    
    report += f"📦 Toplam Paket: {stats['total_packages']}\n"
    report += f"🔗 Bağımlılığa Sahip: {stats['with_dependencies']}\n"
    report += f"🆓 Bağımlılıksız: {stats['without_dependencies']}\n"
    report += f"📊 Toplam Bağımlılık: {stats['total_dependencies']}\n\n"
    
    # Dil dağılımı
    report += "💻 Dil Dağılımı:\n"
    for language, count in sorted(stats["languages"].items()):
        percentage = (count / stats["total_packages"]) * 100
        report += f"  {language}: {count} paket (%{percentage:.1f})\n"
    
    return report

def check_remote_connectivity() -> bool:
    """
    Uzak paket deposuna bağlantıyı kontrol eder.
    
    Returns:
        bool: Bağlantı varsa True
    """
    try:
        request = urllib.request.Request(REMOTE_PACKAGES_URL, method='HEAD')
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status == 200
    except Exception:
        return False

def get_package_versions(app_name: str) -> List[str]:
    """
    Paketin mevcut sürümlerini döndürür (şu an sadece mevcut sürüm).
    
    Args:
        app_name (str): Uygulama adı
        
    Returns:
        list: Sürüm listesi
    """
    package = get_package_info(app_name)
    
    if package:
        return [package.get('version', '0.0.0')]
    
    return []

if __name__ == "__main__":
    # Test için örnek kullanım
    print("Remote Registry Test")
    print("=" * 30)
    
    # Bağlantı testi
    if check_remote_connectivity():
        print("✅ Uzak paket deposuna bağlantı başarılı")
        
        # Paket listesi
        print("\nPaket listesi:")
        print(list_remote_packages())
        
        # İstatistikler
        print("\nİstatistikler:")
        print(get_statistics_report())
        
    else:
        print("❌ Uzak paket deposuna bağlantı kurulamadı")
    
    print("\nTest tamamlandı.") 