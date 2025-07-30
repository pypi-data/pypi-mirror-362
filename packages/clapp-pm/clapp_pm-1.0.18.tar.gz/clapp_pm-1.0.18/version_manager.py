#!/usr/bin/env python3
"""
version_manager.py - Gelişmiş Versiyon Yönetimi Sistemi

Bu modül clapp paketlerinin versiyon yönetimini sağlar:
- Semantic versioning
- Versiyon karşılaştırma
- Otomatik versiyon artırma
- Versiyon geçmişi
- Güncelleme kontrolü
"""

import os
import json
import re
import requests
from typing import Dict, List, Tuple, Optional, Any
from packaging import version as pkg_version
from datetime import datetime, timezone

class VersionManager:
    """Gelişmiş versiyon yönetimi sınıfı"""
    
    def __init__(self, registry_url: str = "https://raw.githubusercontent.com/mburakmmm/clapp-packages/main/index.json"):
        """
        VersionManager başlatıcısı
        
        Args:
            registry_url: Paket registry URL'si
        """
        self.registry_url = registry_url
        self.cache_file = os.path.join(os.path.expanduser("~"), ".clapp", "version_cache.json")
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """Cache dizinini oluşturur"""
        cache_dir = os.path.dirname(self.cache_file)
        os.makedirs(cache_dir, exist_ok=True)
    
    def parse_version(self, version_string: str) -> pkg_version.Version:
        """
        Versiyon string'ini parse eder
        
        Args:
            version_string: Versiyon string'i (örn: "1.2.3")
            
        Returns:
            Version objesi
        """
        try:
            return pkg_version.parse(version_string)
        except pkg_version.InvalidVersion:
            raise ValueError(f"Geçersiz versiyon formatı: {version_string}")
    
    def compare_versions(self, version1: str, version2: str) -> int:
        """
        İki versiyonu karşılaştırır
        
        Args:
            version1: İlk versiyon
            version2: İkinci versiyon
            
        Returns:
            -1: version1 < version2
             0: version1 == version2
             1: version1 > version2
        """
        v1 = self.parse_version(version1)
        v2 = self.parse_version(version2)
        
        if v1 < v2:
            return -1
        elif v1 == v2:
            return 0
        else:
            return 1
    
    def increment_version(self, current_version: str, increment_type: str = "patch") -> str:
        """
        Versiyonu artırır
        
        Args:
            current_version: Mevcut versiyon
            increment_type: Artırma tipi ("major", "minor", "patch")
            
        Returns:
            Yeni versiyon
        """
        v = self.parse_version(current_version)
        
        if increment_type == "major":
            return f"{v.major + 1}.0.0"
        elif increment_type == "minor":
            return f"{v.major}.{v.minor + 1}.0"
        elif increment_type == "patch":
            return f"{v.major}.{v.minor}.{v.micro + 1}"
        else:
            raise ValueError(f"Geçersiz artırma tipi: {increment_type}")
    
    def get_latest_version(self, app_name: str) -> Optional[str]:
        """
        Uygulamanın en son versiyonunu alır
        
        Args:
            app_name: Uygulama adı
            
        Returns:
            En son versiyon veya None
        """
        try:
            # Cache'den kontrol et
            cached_data = self._load_cache()
            if app_name in cached_data:
                cache_time = cached_data[app_name].get("timestamp", 0)
                # 1 saat cache geçerli
                if datetime.now().timestamp() - cache_time < 3600:
                    return cached_data[app_name].get("latest_version")
            
            # Registry'den al
            registry_data = self._fetch_registry()
            if not registry_data:
                return None
            
            # Uygulamayı bul
            app_info = None
            for app in registry_data:
                if app.get("name") == app_name:
                    app_info = app
                    break
            
            if not app_info:
                return None
            
            latest_version = app_info.get("version", "0.0.0")
            
            # Cache'e kaydet
            self._update_cache(app_name, latest_version)
            
            return latest_version
            
        except Exception as e:
            print(f"Versiyon kontrolü hatası: {e}")
            return None
    
    def check_for_updates(self, app_name: str, current_version: str) -> Dict[str, Any]:
        """
        Uygulama güncellemelerini kontrol eder
        
        Args:
            app_name: Uygulama adı
            current_version: Mevcut versiyon
            
        Returns:
            Güncelleme bilgileri
        """
        latest_version = self.get_latest_version(app_name)
        
        if not latest_version:
            return {
                "has_update": False,
                "current_version": current_version,
                "latest_version": None,
                "update_type": None,
                "message": "Versiyon bilgisi alınamadı"
            }
        
        comparison = self.compare_versions(current_version, latest_version)
        
        if comparison < 0:
            # Güncelleme var
            update_type = self._determine_update_type(current_version, latest_version)
            return {
                "has_update": True,
                "current_version": current_version,
                "latest_version": latest_version,
                "update_type": update_type,
                "message": f"Güncelleme mevcut: {current_version} → {latest_version}"
            }
        else:
            return {
                "has_update": False,
                "current_version": current_version,
                "latest_version": latest_version,
                "update_type": None,
                "message": "En son versiyon kullanılıyor"
            }
    
    def _determine_update_type(self, current_version: str, latest_version: str) -> str:
        """Güncelleme tipini belirler"""
        current = self.parse_version(current_version)
        latest = self.parse_version(latest_version)
        
        if latest.major > current.major:
            return "major"
        elif latest.minor > current.minor:
            return "minor"
        else:
            return "patch"
    
    def get_version_history(self, app_name: str) -> List[Dict[str, Any]]:
        """
        Uygulama versiyon geçmişini alır
        
        Args:
            app_name: Uygulama adı
            
        Returns:
            Versiyon geçmişi
        """
        try:
            registry_data = self._fetch_registry()
            if not registry_data:
                return []
            
            # Uygulamayı bul
            app_info = None
            for app in registry_data:
                if app.get("name") == app_name:
                    app_info = app
                    break
            
            if not app_info:
                return []
            
            # Şimdilik sadece mevcut versiyonu döndür
            # Gelecekte GitHub releases'den alınabilir
            return [{
                "version": app_info.get("version", "0.0.0"),
                "release_date": app_info.get("release_date", "Unknown"),
                "description": app_info.get("description", ""),
                "changes": app_info.get("changelog", [])
            }]
            
        except Exception as e:
            print(f"Versiyon geçmişi hatası: {e}")
            return []
    
    def validate_version_format(self, version_string: str) -> bool:
        """
        Versiyon formatını doğrular
        
        Args:
            version_string: Versiyon string'i
            
        Returns:
            Geçerliyse True
        """
        try:
            self.parse_version(version_string)
            return True
        except ValueError:
            return False
    
    def get_version_info(self, version_string: str) -> Dict[str, Any]:
        """
        Versiyon hakkında detaylı bilgi verir
        
        Args:
            version_string: Versiyon string'i
            
        Returns:
            Versiyon bilgileri
        """
        try:
            v = self.parse_version(version_string)
            return {
                "major": v.major,
                "minor": v.minor,
                "micro": v.micro,
                "is_prerelease": v.is_prerelease,
                "is_devrelease": v.is_devrelease,
                "is_postrelease": v.is_postrelease,
                "epoch": v.epoch,
                "local": v.local,
                "public": v.public
            }
        except ValueError as e:
            return {"error": str(e)}
    
    def _fetch_registry(self) -> Optional[List[Dict]]:
        """Registry'den veri alır"""
        try:
            response = requests.get(self.registry_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Registry fetch hatası: {e}")
            return None
    
    def _load_cache(self) -> Dict:
        """Cache'i yükler"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def _update_cache(self, app_name: str, latest_version: str):
        """Cache'i günceller"""
        try:
            cache_data = self._load_cache()
            cache_data[app_name] = {
                "latest_version": latest_version,
                "timestamp": datetime.now().timestamp()
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"Cache güncelleme hatası: {e}")
    
    def clear_cache(self):
        """Cache'i temizler"""
        try:
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
                print("✅ Versiyon cache temizlendi")
        except Exception as e:
            print(f"Cache temizleme hatası: {e}")

# Yardımcı fonksiyonlar
def create_version_manager() -> VersionManager:
    """Varsayılan ayarlarla VersionManager oluşturur"""
    return VersionManager()

def check_app_updates(app_name: str, current_version: str) -> Dict[str, Any]:
    """Uygulama güncellemelerini kontrol eder"""
    vm = create_version_manager()
    return vm.check_for_updates(app_name, current_version)

def get_app_latest_version(app_name: str) -> Optional[str]:
    """Uygulamanın en son versiyonunu alır"""
    vm = create_version_manager()
    return vm.get_latest_version(app_name)

def compare_app_versions(version1: str, version2: str) -> int:
    """İki versiyonu karşılaştırır"""
    vm = create_version_manager()
    return vm.compare_versions(version1, version2)

def increment_app_version(current_version: str, increment_type: str = "patch") -> str:
    """Versiyonu artırır"""
    vm = create_version_manager()
    return vm.increment_version(current_version, increment_type)

def validate_app_version(version_string: str) -> bool:
    """Versiyon formatını doğrular"""
    vm = create_version_manager()
    return vm.validate_version_format(version_string) 