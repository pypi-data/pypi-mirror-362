from manifest_schema import validate_manifest, get_schema

def validate_manifest_verbose(manifest):
    """
    Manifest dosyasını doğrular ve detaylı hata mesajları döndürür.
    
    Args:
        manifest (dict): Doğrulanacak manifest dictionary'si
        
    Returns:
        tuple: (is_valid: bool, errors: list of strings)
    """
    errors = []
    
    if not isinstance(manifest, dict):
        return False, ["Manifest geçerli bir JSON objesi değil"]
    
    # Şema bilgilerini al
    schema = get_schema()
    required_fields = schema["required_fields"]
    
    # Gerekli alanları kontrol et
    for field, field_type in required_fields.items():
        if field not in manifest:
            errors.append(f"Gerekli alan eksik: '{field}'")
            continue
        
        # Tip kontrolü
        value = manifest[field]
        
        if field == "name":
            if not isinstance(value, str) or not value.strip():
                errors.append(f"'{field}' alanı boş olmayan bir string olmalı")
        elif field == "version":
            if not isinstance(value, str) or not value.strip():
                errors.append(f"'{field}' alanı boş olmayan bir string olmalı")
            elif not is_valid_version(value):
                errors.append(f"'{field}' alanı geçerli bir sürüm formatında olmalı (örn: 1.0.0)")
        elif field == "language":
            if not isinstance(value, str):
                errors.append(f"'{field}' alanı string olmalı")
            elif value.lower() not in ["python", "lua", "dart", "go", "rust", "node", "bash", "perl", "ruby", "php"]:
                errors.append(f"'{field}' alanı desteklenen bir dil olmalı, '{value}' geçersiz")
        elif field == "entry":
            if not isinstance(value, str) or not value.strip():
                errors.append(f"'{field}' alanı boş olmayan bir string olmalı")
            elif not is_valid_filename(value):
                errors.append(f"'{field}' alanı geçerli bir dosya adı olmalı")
    
    # Opsiyonel alanları kontrol et
    if "description" in manifest:
        if not isinstance(manifest["description"], str):
            errors.append("'description' alanı string olmalı")
    
    if "dependencies" in manifest:
        if not isinstance(manifest["dependencies"], list):
            errors.append("'dependencies' alanı liste olmalı")
        else:
            for i, dep in enumerate(manifest["dependencies"]):
                if not isinstance(dep, str) or not dep.strip():
                    errors.append(f"'dependencies[{i}]' boş olmayan bir string olmalı")
    
    # Bilinmeyen alanları kontrol et
    known_fields = set(required_fields.keys()) | {"description", "dependencies", "author", "license", "tags", "category"}
    for field in manifest.keys():
        if field not in known_fields:
            errors.append(f"Bilinmeyen alan: '{field}' (göz ardı edilecek)")
    
    return len(errors) == 0, errors

def is_valid_version(version_string):
    """
    Sürüm string'inin geçerli olup olmadığını kontrol eder.
    
    Args:
        version_string (str): Sürüm string'i
        
    Returns:
        bool: Geçerliyse True
    """
    try:
        # Basit sürüm formatı kontrolü (x.y.z veya x.y)
        parts = version_string.split('.')
        if len(parts) < 2 or len(parts) > 3:
            return False
        
        for part in parts:
            if not part.isdigit():
                return False
        
        return True
    except:
        return False

def is_valid_filename(filename):
    """
    Dosya adının geçerli olup olmadığını kontrol eder.
    
    Args:
        filename (str): Dosya adı
        
    Returns:
        bool: Geçerliyse True
    """
    import os
    
    # Boş string kontrolü
    if not filename or not filename.strip():
        return False
    
    # Geçersiz karakterler
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '\0']
    for char in invalid_chars:
        if char in filename:
            return False
    
    # Sistem dosya adları (Windows)
    reserved_names = [
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    ]
    
    name_without_ext = os.path.splitext(filename)[0].upper()
    if name_without_ext in reserved_names:
        return False
    
    return True

def validate_manifest_file(manifest_path):
    """
    Manifest dosyasını doğrular.
    
    Args:
        manifest_path (str): Manifest dosyasının yolu
        
    Returns:
        tuple: (is_valid: bool, errors: list of strings)
    """
    import json
    import os
    
    # Dosya varlığını kontrol et
    if not os.path.exists(manifest_path):
        return False, [f"Manifest dosyası bulunamadı: {manifest_path}"]
    
    # JSON dosyasını yüklemeye çalış
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"JSON formatı hatalı: {e}"]
    except Exception as e:
        return False, [f"Dosya okuma hatası: {e}"]
    
    # Manifest içeriğini doğrula
    return validate_manifest_verbose(manifest)

def get_validation_summary(errors):
    """
    Doğrulama hatalarının özetini döndürür.
    
    Args:
        errors (list): Hata mesajları listesi
        
    Returns:
        str: Hata özeti
    """
    if not errors:
        return "✅ Manifest dosyası geçerli"
    
    summary = f"❌ {len(errors)} hata bulundu:\n"
    for i, error in enumerate(errors, 1):
        summary += f"{i}. {error}\n"
    
    return summary

def suggest_fixes(errors):
    """
    Hatalara göre düzeltme önerileri sunar.
    
    Args:
        errors (list): Hata mesajları listesi
        
    Returns:
        list: Düzeltme önerileri
    """
    suggestions = []
    
    for error in errors:
        if "Gerekli alan eksik" in error:
            field = error.split("'")[1]
            if field == "name":
                suggestions.append("Uygulama adını 'name' alanına ekleyin")
            elif field == "version":
                suggestions.append("Sürüm bilgisini 'version' alanına ekleyin (örn: '1.0.0')")
            elif field == "language":
                suggestions.append("Programlama dilini 'language' alanına ekleyin ('python' veya 'lua')")
            elif field == "entry":
                suggestions.append("Giriş dosyasını 'entry' alanına ekleyin (örn: 'main.py')")
        
        elif "geçerli bir sürüm formatında olmalı" in error:
            suggestions.append("Sürüm formatını düzeltin (örn: '1.0.0', '2.1.5')")
        
        elif "python' veya 'lua' olmalı" in error:
            suggestions.append("Desteklenen dil kullanın: 'python' veya 'lua'")
        
        elif "geçerli bir dosya adı olmalı" in error:
            suggestions.append("Giriş dosyası adını düzeltin (geçersiz karakterler içermemeli)")
    
    return suggestions

if __name__ == "__main__":
    # Test için örnek manifest'ler
    
    # Geçerli manifest
    valid_manifest = {
        "name": "test-app",
        "version": "1.0.0",
        "language": "python",
        "entry": "main.py",
        "description": "Test uygulaması"
    }
    
    # Geçersiz manifest
    invalid_manifest = {
        "name": "",
        "version": "abc",
        "language": "javascript",
        "entry": "main.py",
        "unknown_field": "value"
    }
    
    print("Geçerli manifest testi:")
    is_valid, errors = validate_manifest_verbose(valid_manifest)
    print(get_validation_summary(errors))
    
    print("\nGeçersiz manifest testi:")
    is_valid, errors = validate_manifest_verbose(invalid_manifest)
    print(get_validation_summary(errors))
    
    print("\nDüzeltme önerileri:")
    suggestions = suggest_fixes(errors)
    for suggestion in suggestions:
        print(f"- {suggestion}") 