import os
import json
from manifest_schema import validate_manifest

def get_apps_directory():
    """Uygulamaların kurulacağı dizini döndürür"""
    from pathlib import Path
    # Kullanıcının home dizininde .clapp klasörü oluştur
    home_dir = Path.home()
    clapp_dir = home_dir / ".clapp"
    apps_dir = clapp_dir / "apps"
    
    # Klasörleri oluştur
    apps_dir.mkdir(parents=True, exist_ok=True)
    
    return str(apps_dir)

def list_packages():
    """
    Yüklü paketlerin listesini döndürür.
    
    Returns:
        list: Yüklü paketlerin listesi (dict formatında)
    """
    packages = []
    apps_dir = get_apps_directory()
    
    # apps dizinindeki her klasörü kontrol et
    for app_name in os.listdir(apps_dir):
        app_path = os.path.join(apps_dir, app_name)
        
        # Sadece dizinleri kontrol et
        if os.path.isdir(app_path):
            manifest_path = os.path.join(app_path, "manifest.json")
            
            # Manifest dosyası varsa
            if os.path.exists(manifest_path):
                try:
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        manifest = json.load(f)
                    
                    # Manifest geçerliyse listeye ekle
                    if validate_manifest(manifest):
                        packages.append({
                            'name': manifest['name'],
                            'version': manifest.get('version', '0.0.0'),
                            'language': manifest.get('language', 'unknown'),
                            'description': manifest.get('description', 'Açıklama yok'),
                            'entry': manifest.get('entry', 'main.py'),
                            'dependencies': manifest.get('dependencies', [])
                        })
                except (json.JSONDecodeError, KeyError):
                    # Geçersiz manifest dosyası, atla
                    continue
    
    return packages

def get_manifest(app_name):
    """
    Belirtilen uygulamanın manifest bilgilerini döndürür.
    
    Args:
        app_name (str): Uygulama adı
        
    Returns:
        dict or None: Manifest bilgileri veya None (bulunamazsa)
    """
    apps_dir = get_apps_directory()
    app_path = os.path.join(apps_dir, app_name)
    manifest_path = os.path.join(app_path, "manifest.json")
    
    if not os.path.exists(manifest_path):
        return None
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # Manifest geçerliyse döndür
        if validate_manifest(manifest):
            return manifest
        else:
            return None
            
    except (json.JSONDecodeError, FileNotFoundError):
        return None

def app_exists(app_name):
    """
    Belirtilen uygulamanın yüklü olup olmadığını kontrol eder.
    
    Args:
        app_name (str): Uygulama adı
        
    Returns:
        bool: Uygulama yüklüyse True, değilse False
    """
    return get_manifest(app_name) is not None

def list_app_names():
    """
    Yüklü uygulamaların sadece isimlerini döndürür.
    
    Returns:
        list: Uygulama isimlerinin listesi (string formatında)
    """
    app_names = []
    apps_dir = get_apps_directory()
    
    # apps dizinindeki her klasörü kontrol et
    for app_name in os.listdir(apps_dir):
        app_path = os.path.join(apps_dir, app_name)
        
        # Sadece dizinleri kontrol et
        if os.path.isdir(app_path):
            manifest_path = os.path.join(app_path, "manifest.json")
            
            # Manifest dosyası varsa
            if os.path.exists(manifest_path):
                try:
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        manifest = json.load(f)
                    
                    # Manifest geçerliyse listeye ekle
                    if validate_manifest(manifest):
                        app_names.append(app_name)
                except (json.JSONDecodeError, KeyError):
                    # Geçersiz manifest dosyası, atla
                    continue
    
    return app_names 