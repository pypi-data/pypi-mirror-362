#!/usr/bin/env python3
"""
new_command.py - Yeni Uygulama Oluşturma Komutu

Bu modül clapp için yeni uygulama şablonları oluşturur.
"""

import os
import shutil
import json
from pathlib import Path
from package_runner import get_supported_languages

def create_new_app(language: str, app_name: str, target_dir: str | None = None) -> tuple[bool, str]:
    """
    Yeni bir clapp uygulaması oluşturur
    
    Args:
        language: Programlama dili
        app_name: Uygulama adı
        target_dir: Hedef dizin (opsiyonel)
        
    Returns:
        (success, message)
    """
    try:
        # Dil kontrolü
        if language.lower() not in get_supported_languages():
            supported = ', '.join(get_supported_languages())
            return False, f"Desteklenmeyen dil: {language}. Desteklenen diller: {supported}"
        
        # Uygulama adı kontrolü
        if not app_name or not app_name.strip():
            return False, "Uygulama adı boş olamaz"
        
        app_name = app_name.strip().lower()
        
        # Geçersiz karakter kontrolü
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            if char in app_name:
                return False, f"Uygulama adında geçersiz karakter: {char}"
        
        # Hedef dizin belirleme
        if target_dir:
            target_path = Path(target_dir) / app_name
        else:
            target_path = Path.cwd() / app_name
        
        # Dizin zaten var mı kontrol et
        if target_path.exists():
            return False, f"Dizin zaten mevcut: {target_path}"
        
        # Şablon dizini
        template_dir = Path(__file__).parent / "templates" / language.lower()
        
        if not template_dir.exists():
            return False, f"Şablon bulunamadı: {language}"
        
        # Dizini oluştur
        target_path.mkdir(parents=True, exist_ok=True)
        
        # Şablon dosyalarını kopyala
        for item in template_dir.iterdir():
            if item.is_file():
                # Dosya adını uygulama adına göre güncelle
                if item.name == "manifest.json":
                    update_manifest(item, target_path / item.name, app_name, language)
                else:
                    shutil.copy2(item, target_path / item.name)
            elif item.is_dir():
                # Alt dizinleri kopyala
                shutil.copytree(item, target_path / item.name)
        
        # Başarı mesajı
        success_message = f"""
✅ Yeni {language} uygulaması oluşturuldu!

📁 Dizin: {target_path}
🚀 Çalıştırmak için:
   cd {app_name}
   clapp validate .
   clapp install .
   clapp run {app_name}

📖 Geliştirme için docs/developer_guide.md dosyasını inceleyin.
        """.strip()
        
        return True, success_message
        
    except Exception as e:
        return False, f"Uygulama oluşturma hatası: {str(e)}"

def update_manifest(template_path: Path, target_path: Path, app_name: str, language: str):
    """
    Manifest dosyasını uygulama adına göre günceller
    
    Args:
        template_path: Şablon manifest dosyası
        target_path: Hedef manifest dosyası
        app_name: Uygulama adı
        language: Programlama dili
    """
    try:
        # Şablon manifest'i oku
        with open(template_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # Uygulama adını güncelle
        manifest['name'] = app_name
        
        # Açıklamayı güncelle
        if 'description' in manifest:
            manifest['description'] = manifest['description'].replace(
                'hello-' + language.lower(), app_name
            )
        
        # Hedef dosyaya yaz
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"⚠️  Manifest güncelleme hatası: {e}")

def list_available_templates() -> str:
    """
    Mevcut şablonları listeler
    
    Returns:
        Formatlanmış şablon listesi
    """
    templates_dir = Path(__file__).parent / "templates"
    
    if not templates_dir.exists():
        return "❌ Şablon dizini bulunamadı"
    
    result = "📋 Mevcut Şablonlar:\n"
    result += "=" * 30 + "\n\n"
    
    for template in sorted(templates_dir.iterdir()):
        if template.is_dir():
            # Şablon bilgilerini oku
            manifest_path = template / "manifest.json"
            if manifest_path.exists():
                try:
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        manifest = json.load(f)
                    
                    name = manifest.get('name', template.name)
                    description = manifest.get('description', 'Açıklama yok')
                    language = manifest.get('language', 'unknown')
                    
                    result += f"🌐 {language.upper()}\n"
                    result += f"   📝 {description}\n"
                    result += f"   📁 Şablon: {template.name}\n\n"
                    
                except Exception:
                    result += f"🌐 {template.name.upper()}\n"
                    result += f"   📁 Şablon: {template.name}\n\n"
    
    result += "💡 Kullanım: clapp new <dil> <uygulama-adı>"
    
    return result

def handle_new_command(args) -> tuple[bool, str]:
    """
    new komutunu işler
    
    Args:
        args: Argümanlar
        
    Returns:
        (success, message)
    """
    if args.list:
        return True, list_available_templates()
    
    if not args.language or not args.app_name:
        return False, "Dil ve uygulama adı gerekli. Örnek: clapp new python my-app"
    
    return create_new_app(args.language, args.app_name, args.target_dir) 