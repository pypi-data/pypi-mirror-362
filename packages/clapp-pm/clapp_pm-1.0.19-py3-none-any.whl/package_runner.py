import os
import json
import subprocess
from typing import Dict, Callable, Optional, Tuple
from package_registry import get_manifest

class LanguageRunner:
    """Dil çalıştırıcıları için temel sınıf"""
    
    def __init__(self, name: str, command: str, file_extension: str = ""):
        self.name = name
        self.command = command
        self.file_extension = file_extension
    
    def run(self, entry_file: str, app_path: str) -> Tuple[bool, str]:
        """
        Uygulamayı çalıştırır
        
        Args:
            entry_file: Giriş dosyası
            app_path: Uygulama dizini
            
        Returns:
            (success, error_message)
        """
        try:
            result = subprocess.run([self.command, entry_file], 
                                  cwd=app_path, 
                                  capture_output=False)
            return result.returncode == 0, ""
        except FileNotFoundError:
            return False, f"{self.name} yüklü değil veya PATH'te bulunamadı."
        except Exception as e:
            return False, f"Çalıştırma hatası: {str(e)}"
    
    def check_availability(self) -> bool:
        """Dil çalıştırıcısının sistemde mevcut olup olmadığını kontrol eder"""
        try:
            result = subprocess.run([self.command, "--version"], 
                                  capture_output=True, 
                                  text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False

# Desteklenen diller için runner'lar
LANGUAGE_RUNNERS: Dict[str, LanguageRunner] = {
    'python': LanguageRunner('Python', 'python', '.py'),
    'lua': LanguageRunner('Lua', 'lua', '.lua'),
    'dart': LanguageRunner('Dart', 'dart', '.dart'),
    'go': LanguageRunner('Go', 'go', '.go'),
    'rust': LanguageRunner('Rust', 'cargo', '.rs'),
    'node': LanguageRunner('Node.js', 'node', '.js'),
    'bash': LanguageRunner('Bash', 'bash', '.sh'),
    'perl': LanguageRunner('Perl', 'perl', '.pl'),
    'ruby': LanguageRunner('Ruby', 'ruby', '.rb'),
    'php': LanguageRunner('PHP', 'php', '.php')
}

def get_runner_for_language(language: str) -> Optional[LanguageRunner]:
    """
    Dile göre runner döndürür
    
    Args:
        language: Programlama dili
        
    Returns:
        LanguageRunner veya None
    """
    return LANGUAGE_RUNNERS.get(language.lower())

def add_language_support(name: str, command: str, file_extension: str = "") -> bool:
    """
    Yeni dil desteği ekler
    
    Args:
        name: Dil adı
        command: Çalıştırma komutu
        file_extension: Dosya uzantısı
        
    Returns:
        Başarılı ise True
    """
    try:
        LANGUAGE_RUNNERS[name.lower()] = LanguageRunner(name, command, file_extension)
        return True
    except Exception:
        return False

def run_app(app_name: str) -> bool:
    """
    Belirtilen uygulamayı çalıştırır.
    
    Args:
        app_name (str): Çalıştırılacak uygulamanın adı
        
    Returns:
        bool: Uygulama başarıyla çalıştırıldıysa True, değilse False
    """
    # Manifest bilgilerini al
    manifest = get_manifest(app_name)
    
    if not manifest:
        print(f"Hata: '{app_name}' uygulaması bulunamadı veya geçersiz manifest dosyası.")
        return False
    
    # Uygulama dizini ve giriş dosyası
    from package_registry import get_apps_directory
    apps_dir = get_apps_directory()
    app_path = os.path.join(apps_dir, app_name)
    entry_file = manifest['entry']
    entry_path = os.path.join(app_path, entry_file)
    
    # Giriş dosyasının varlığını kontrol et
    if not os.path.exists(entry_path):
        print(f"Hata: Giriş dosyası '{entry_file}' bulunamadı.")
        return False
    
    # Dile göre runner al
    language = manifest['language'].lower()
    runner = get_runner_for_language(language)
    
    if not runner:
        supported = ', '.join(LANGUAGE_RUNNERS.keys())
        print(f"Hata: Desteklenmeyen dil '{language}'. Desteklenen diller: {supported}")
        return False
    
    # Uygulamayı çalıştır
    success, error_msg = runner.run(entry_file, app_path)
    
    if not success and error_msg:
        print(f"Hata: {error_msg}")
    
    return success

def get_supported_languages() -> list:
    """
    Desteklenen programlama dillerinin listesini döndürür.
    
    Returns:
        list: Desteklenen diller listesi
    """
    return list(LANGUAGE_RUNNERS.keys())

def check_language_support(language: str) -> bool:
    """
    Belirtilen dilin desteklenip desteklenmediğini kontrol eder.
    
    Args:
        language (str): Kontrol edilecek dil
        
    Returns:
        bool: Dil destekleniyorsa True, değilse False
    """
    return language.lower() in LANGUAGE_RUNNERS

def check_language_availability(language: str) -> bool:
    """
    Belirtilen dilin sistemde mevcut olup olmadığını kontrol eder.
    
    Args:
        language (str): Kontrol edilecek dil
        
    Returns:
        bool: Dil mevcutsa True, değilse False
    """
    runner = get_runner_for_language(language)
    if not runner:
        return False
    return runner.check_availability()

def get_language_status_report() -> str:
    """
    Tüm desteklenen dillerin durum raporunu döndürür.
    
    Returns:
        str: Formatlanmış durum raporu
    """
    report = "🌐 Desteklenen Diller Durumu\n"
    report += "=" * 40 + "\n\n"
    
    for lang_name, runner in LANGUAGE_RUNNERS.items():
        available = runner.check_availability()
        status = "✅ Mevcut" if available else "❌ Mevcut Değil"
        report += f"{lang_name.title():<12} : {status}\n"
    
    return report 