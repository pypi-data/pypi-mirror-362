import json
import os

def load_manifest(manifest_path):
    """
    Manifest dosyasını yükler ve parse eder.
    
    Args:
        manifest_path (str): Manifest dosyasının yolu
        
    Returns:
        dict: Parse edilmiş manifest dictionary'si
        
    Raises:
        FileNotFoundError: Dosya bulunamadığında
        json.JSONDecodeError: JSON parse hatası
    """
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"Manifest dosyası bulunamadı: {manifest_path}")
    
    with open(manifest_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_manifest(manifest):
    """
    Manifest dosyasının gerekli alanları içerip içermediğini ve tiplerinin doğru olup olmadığını kontrol eder.
    
    Args:
        manifest (dict): Doğrulanacak manifest dictionary'si
        
    Returns:
        bool: Manifest geçerliyse True, değilse False
    """
    # Gerekli alanlar
    required_fields = {
        'name': str,
        'version': str,
        'language': str,
        'entry': str
    }
    
    # Opsiyonel alanlar
    optional_fields = {
        'description': str,
        'dependencies': list,
        'author': str,
        'license': str,
        'tags': list,
        'category': str
    }
    
    # Gerekli alanları kontrol et
    for field, expected_type in required_fields.items():
        if field not in manifest:
            return False
        if not isinstance(manifest[field], expected_type):
            return False
    
    # Dil kontrolü - package_runner'dan desteklenen dilleri al
    try:
        from package_runner import get_supported_languages
        supported_languages = get_supported_languages()
        if manifest['language'] not in supported_languages:
            return False
    except ImportError:
        # Fallback: Temel diller
        if manifest['language'] not in ['python', 'lua', 'dart', 'go', 'rust', 'node', 'bash', 'perl', 'ruby', 'php']:
            return False
    
    # Opsiyonel alanları kontrol et (varsa)
    for field, expected_type in optional_fields.items():
        if field in manifest and not isinstance(manifest[field], expected_type):
            return False
    
    return True

def get_schema():
    """
    Manifest şemasını döndürür.
    
    Returns:
        dict: Manifest şeması
    """
    return {
        "required_fields": {
            "name": "string",
            "version": "string", 
            "language": "string (python or lua)",
            "entry": "string"
        },
        "optional_fields": {
            "description": "string",
            "dependencies": "list",
            "author": "string",
            "license": "string",
            "tags": "list",
            "category": "string"
        }
    } 