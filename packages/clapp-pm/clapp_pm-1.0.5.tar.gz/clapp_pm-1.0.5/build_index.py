#!/usr/bin/env python3
"""
build_index.py - clapp Index Builder Script

Bu script packages/ klasörünü tarayarak tüm uygulamaların metadata'sını
index.json dosyasına toplar. Publish işlemlerinden sonra otomatik çalışır.
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

def load_manifest(app_path: str) -> Dict[str, Any]:
    """Uygulama klasöründen manifest.json yükler"""
    manifest_path = os.path.join(app_path, "manifest.json")
    
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"manifest.json bulunamadı: {manifest_path}")
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Geçersiz JSON formatı {manifest_path}: {e}")

def validate_manifest(manifest: Dict[str, Any], app_name: str) -> bool:
    """Manifest'in gerekli alanları içerip içermediğini kontrol eder"""
    required_fields = ['name', 'version', 'language', 'description', 'entry']
    
    for field in required_fields:
        if field not in manifest:
            print(f"⚠️  {app_name}: Eksik alan '{field}'")
            return False
    
    return True

def scan_packages_directory(packages_dir: str = "./packages") -> List[Dict[str, Any]]:
    """packages klasörünü tarayarak tüm uygulamaları bulur"""
    apps = []
    
    if not os.path.exists(packages_dir):
        print(f"⚠️  packages klasörü bulunamadı: {packages_dir}")
        return apps
    
    for app_name in os.listdir(packages_dir):
        app_path = os.path.join(packages_dir, app_name)
        
        # Sadece klasörleri işle
        if not os.path.isdir(app_path):
            continue
            
        # Gizli klasörleri atla
        if app_name.startswith('.'):
            continue
        
        try:
            manifest = load_manifest(app_path)
            
            # Manifest'i doğrula
            if not validate_manifest(manifest, app_name):
                continue
            
            # Index için gerekli alanları çıkar
            app_info = {
                'name': manifest['name'],
                'version': manifest['version'],
                'language': manifest['language'],
                'description': manifest['description'],
                'entry': manifest['entry'],
                'dependencies': manifest.get('dependencies', []),
                'folder': app_name,
                'repo_url': f"https://github.com/mburakmmm/clapp-packages",
                'subdir': app_name
            }
            
            apps.append(app_info)
            print(f"✅ {app_name} (v{manifest['version']}) eklendi")
            
        except Exception as e:
            print(f"❌ {app_name}: {e}")
            continue
    
    return apps

def generate_index(output_file: str = "index.json") -> bool:
    """Index.json dosyasını oluşturur"""
    try:
        print("🔄 packages/ klasörü taranıyor...")
        apps = scan_packages_directory()
        
        if not apps:
            print("⚠️  Hiç geçerli uygulama bulunamadı!")
            return False
        
        # Alfabetik sıralama
        apps.sort(key=lambda x: x['name'].lower())
        
        # Index.json'u yaz
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(apps, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {output_file} başarıyla oluşturuldu ({len(apps)} uygulama)")
        return True
        
    except Exception as e:
        print(f"❌ Index oluşturulurken hata: {e}")
        return False

def main():
    """Ana fonksiyon"""
    print("🚀 clapp Index Builder v1.0.0")
    print("=" * 40)
    
    # Komut satırı argümanları
    output_file = "index.json"
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    
    # Index oluştur
    success = generate_index(output_file)
    
    if success:
        print("\n🎉 Index başarıyla güncellendi!")
        sys.exit(0)
    else:
        print("\n💥 Index güncellenemedi!")
        sys.exit(1)

if __name__ == "__main__":
    main() 