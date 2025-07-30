#!/usr/bin/env python3
"""
validate_command.py - Uygulama doğrulama modülü

Bu modül `clapp validate <folder>` komutunu destekler ve
uygulama klasörlerinin doğru yapıda olup olmadığını kontrol eder.
"""

import os
import json
from pathlib import Path
from manifest_validator import validate_manifest_verbose

def validate_app_folder(folder_path):
    """Uygulama klasörünü doğrular"""
    folder = Path(folder_path)
    
    print(f"🔍 '{folder_path}' klasörü doğrulanıyor...")
    print("=" * 50)
    
    # Klasörün var olup olmadığını kontrol et
    if not folder.exists():
        print(f"❌ Klasör bulunamadı: {folder_path}")
        return False
    
    if not folder.is_dir():
        print(f"❌ Belirtilen yol bir klasör değil: {folder_path}")
        return False
    
    errors = []
    warnings = []
    
    # 1. manifest.json kontrolü
    manifest_path = folder / "manifest.json"
    if not manifest_path.exists():
        errors.append("manifest.json dosyası bulunamadı")
    else:
        print("✅ manifest.json dosyası mevcut")
        
        # Manifest içeriğini kontrol et
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_data = json.load(f)
            
            # Manifest'i doğrula
            is_valid, validation_errors = validate_manifest_verbose(manifest_data)
            
            if is_valid:
                print("✅ manifest.json geçerli")
            else:
                print("❌ manifest.json geçersiz:")
                for error in validation_errors:
                    print(f"   • {error}")
                    errors.append(f"Manifest hatası: {error}")
            
            # Giriş dosyası kontrolü
            if "entry" in manifest_data:
                entry_file = folder / manifest_data["entry"]
                if entry_file.exists():
                    print(f"✅ Giriş dosyası mevcut: {manifest_data['entry']}")
                else:
                    error_msg = f"Giriş dosyası bulunamadı: {manifest_data['entry']}"
                    print(f"❌ {error_msg}")
                    errors.append(error_msg)
            
            # Dil kontrolü
            if "language" in manifest_data:
                language = manifest_data["language"].lower()
                if language in ["python", "lua"]:
                    print(f"✅ Desteklenen dil: {language}")
                else:
                    warning_msg = f"Desteklenmeyen dil: {language}"
                    print(f"⚠️  {warning_msg}")
                    warnings.append(warning_msg)
            
        except json.JSONDecodeError as e:
            error_msg = f"manifest.json JSON formatı geçersiz: {str(e)}"
            print(f"❌ {error_msg}")
            errors.append(error_msg)
        except Exception as e:
            error_msg = f"manifest.json okunamadı: {str(e)}"
            print(f"❌ {error_msg}")
            errors.append(error_msg)
    
    # 2. Klasör içeriği kontrolü
    files = list(folder.iterdir())
    if not files:
        warnings.append("Klasör boş")
        print("⚠️  Klasör boş")
    else:
        print(f"✅ Klasör içeriği: {len(files)} öğe")
    
    # 3. Önerilen dosya yapısı kontrolü
    recommended_files = ["manifest.json", "README.md", "requirements.txt"]
    missing_recommended = []
    
    for rec_file in recommended_files:
        if not (folder / rec_file).exists():
            missing_recommended.append(rec_file)
    
    if missing_recommended:
        print("💡 Önerilen dosyalar eksik:")
        for missing in missing_recommended:
            print(f"   • {missing}")
    
    # 4. Dosya boyutu kontrolü
    try:
        total_size = 0
        file_count = 0
        
        for file_path in folder.rglob("*"):
            if file_path.is_file():
                file_count += 1
                total_size += file_path.stat().st_size
        
        print(f"📊 İstatistikler: {file_count} dosya, {format_size(total_size)}")
        
        # Büyük dosyalar için uyarı
        if total_size > 100 * 1024 * 1024:  # 100MB
            warnings.append(f"Büyük uygulama boyutu: {format_size(total_size)}")
    
    except Exception as e:
        warnings.append(f"Dosya boyutu hesaplanamadı: {str(e)}")
    
    # Sonuçları göster
    print("\n" + "=" * 50)
    print("📋 Doğrulama Sonuçları:")
    
    if not errors and not warnings:
        print("🎉 Mükemmel! Uygulama klasörü tamamen geçerli.")
        print("✅ Kurulum için hazır.")
    elif not errors:
        print("✅ Uygulama klasörü geçerli.")
        if warnings:
            print("⚠️  Bazı uyarılar var:")
            for warning in warnings:
                print(f"   • {warning}")
    else:
        print("❌ Uygulama klasörü geçersiz.")
        print("🔧 Düzeltilmesi gereken hatalar:")
        for error in errors:
            print(f"   • {error}")
        
        if warnings:
            print("⚠️  Ek uyarılar:")
            for warning in warnings:
                print(f"   • {warning}")
    
    # Öneriler
    if errors or warnings:
        print("\n💡 Öneriler:")
        if not manifest_path.exists():
            print("• manifest.json dosyası oluşturun")
            print("• Örnek: clapp init komutu ile başlayabilirsiniz")
        
        if missing_recommended:
            print("• Önerilen dosyaları ekleyin:")
            for missing in missing_recommended:
                if missing == "README.md":
                    print(f"  - {missing}: Uygulama açıklaması")
                elif missing == "requirements.txt":
                    print(f"  - {missing}: Python bağımlılıkları (Python uygulamaları için)")
        
        if warnings:
            print("• Uyarıları gözden geçirin ve gerekirse düzeltin")
    
    print(f"\n🔧 Daha fazla yardım için: clapp doctor")
    
    return len(errors) == 0

def format_size(size_bytes):
    """Dosya boyutunu formatlar"""
    if size_bytes == 0:
        return "0 B"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} TB"

def validate_multiple_folders(folder_paths):
    """Birden fazla klasörü doğrular"""
    results = []
    
    for folder_path in folder_paths:
        print(f"\n{'='*60}")
        result = validate_app_folder(folder_path)
        results.append((folder_path, result))
    
    # Özet
    print(f"\n{'='*60}")
    print("📊 Toplu Doğrulama Özeti:")
    
    valid_count = sum(1 for _, result in results if result)
    invalid_count = len(results) - valid_count
    
    print(f"✅ Geçerli: {valid_count}")
    print(f"❌ Geçersiz: {invalid_count}")
    
    if invalid_count > 0:
        print("\n❌ Geçersiz klasörler:")
        for folder_path, result in results:
            if not result:
                print(f"   • {folder_path}")
    
    return invalid_count == 0

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Kullanım: python validate_command.py <klasör_yolu>")
        print("Örnek: python validate_command.py apps/my-app")
        sys.exit(1)
    
    folder_paths = sys.argv[1:]
    
    if len(folder_paths) == 1:
        success = validate_app_folder(folder_paths[0])
        sys.exit(0 if success else 1)
    else:
        success = validate_multiple_folders(folder_paths)
        sys.exit(0 if success else 1) 