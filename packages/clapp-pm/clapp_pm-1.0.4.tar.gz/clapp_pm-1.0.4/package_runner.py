import os
import json
import subprocess
from package_registry import get_manifest

def run_app(app_name):
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
    app_path = os.path.join("apps", app_name)
    entry_file = manifest['entry']
    entry_path = os.path.join(app_path, entry_file)
    
    # Giriş dosyasının varlığını kontrol et
    if not os.path.exists(entry_path):
        print(f"Hata: Giriş dosyası '{entry_file}' bulunamadı.")
        return False
    
    # Dile göre çalıştır
    language = manifest['language'].lower()
    
    try:
        if language == 'python':
            # Python uygulamasını çalıştır
            result = subprocess.run(['python', entry_file], 
                                  cwd=app_path, 
                                  capture_output=False)
            return result.returncode == 0
            
        elif language == 'lua':
            # Lua uygulamasını çalıştır
            result = subprocess.run(['lua', entry_file], 
                                  cwd=app_path, 
                                  capture_output=False)
            return result.returncode == 0
            
        else:
            print(f"Hata: Desteklenmeyen dil '{language}'. Desteklenen diller: python, lua")
            return False
            
    except FileNotFoundError as e:
        if language == 'python':
            print("Hata: Python yüklü değil veya PATH'te bulunamadı.")
        elif language == 'lua':
            print("Hata: Lua yüklü değil veya PATH'te bulunamadı.")
        return False
        
    except Exception as e:
        print(f"Hata: Uygulama çalıştırılırken bir hata oluştu: {e}")
        return False

def get_supported_languages():
    """
    Desteklenen programlama dillerinin listesini döndürür.
    
    Returns:
        list: Desteklenen diller listesi
    """
    return ['python', 'lua']

def check_language_support(language):
    """
    Belirtilen dilin desteklenip desteklenmediğini kontrol eder.
    
    Args:
        language (str): Kontrol edilecek dil
        
    Returns:
        bool: Dil destekleniyorsa True, değilse False
    """
    return language.lower() in get_supported_languages() 