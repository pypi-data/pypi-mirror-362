#!/usr/bin/env python3
"""
cache_manager.py - Performans Optimizasyonu ve Önbellekleme Sistemi

Bu modül clapp'in performansını artırmak için:
- Paket meta verilerini önbellekleme
- Registry verilerini önbellekleme
- Dosya checksum'larını önbellekleme
- Akıllı cache yönetimi
- Paralel indirme desteği
"""

import os
import json
import hashlib
import pickle
import threading
import time
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
import concurrent.futures
import requests
from functools import wraps

class CacheManager:
    """Akıllı önbellekleme yöneticisi"""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        CacheManager başlatıcısı
        
        Args:
            cache_dir: Cache dizini (varsayılan: ~/.clapp/cache)
        """
        if cache_dir is None:
            cache_dir = os.path.join(os.path.expanduser("~"), ".clapp", "cache")
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache türleri
        self.metadata_cache = self.cache_dir / "metadata"
        self.registry_cache = self.cache_dir / "registry"
        self.checksum_cache = self.cache_dir / "checksums"
        self.download_cache = self.cache_dir / "downloads"
        
        # Cache dizinlerini oluştur
        for cache_path in [self.metadata_cache, self.registry_cache, 
                          self.checksum_cache, self.download_cache]:
            cache_path.mkdir(exist_ok=True)
        
        # Cache istatistikleri
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "size": 0
        }
        
        # Thread-safe cache
        self._lock = threading.Lock()
    
    def _get_cache_key(self, key: str, cache_type: str = "metadata") -> Path:
        """Cache anahtarı için dosya yolu oluşturur"""
        if cache_type == "metadata":
            return self.metadata_cache / f"{key}.json"
        elif cache_type == "registry":
            return self.registry_cache / f"{key}.json"
        elif cache_type == "checksum":
            return self.checksum_cache / f"{key}.txt"
        elif cache_type == "download":
            return self.download_cache / f"{key}.zip"
        else:
            raise ValueError(f"Geçersiz cache türü: {cache_type}")
    
    def get(self, key: str, cache_type: str = "metadata", max_age: int = 3600) -> Optional[Any]:
        """
        Cache'den veri alır
        
        Args:
            key: Cache anahtarı
            cache_type: Cache türü
            max_age: Maksimum yaş (saniye)
            
        Returns:
            Cache'lenmiş veri veya None
        """
        cache_file = self._get_cache_key(key, cache_type)
        
        if not cache_file.exists():
            self.stats["misses"] += 1
            return None
        
        # Dosya yaşını kontrol et
        file_age = time.time() - cache_file.stat().st_mtime
        if file_age > max_age:
            cache_file.unlink()
            self.stats["misses"] += 1
            return None
        
        try:
            with self._lock:
                if cache_type in ["metadata", "registry"]:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                elif cache_type == "checksum":
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        data = f.read().strip()
                else:
                    # Binary dosyalar için pickle kullan
                    with open(cache_file, 'rb') as f:
                        data = pickle.load(f)
            
            self.stats["hits"] += 1
            return data
            
        except Exception as e:
            print(f"Cache okuma hatası: {e}")
            cache_file.unlink()
            self.stats["misses"] += 1
            return None
    
    def set(self, key: str, data: Any, cache_type: str = "metadata") -> bool:
        """
        Cache'e veri kaydeder
        
        Args:
            key: Cache anahtarı
            data: Kaydedilecek veri
            cache_type: Cache türü
            
        Returns:
            Başarılıysa True
        """
        cache_file = self._get_cache_key(key, cache_type)
        
        try:
            with self._lock:
                if cache_type in ["metadata", "registry"]:
                    with open(cache_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                elif cache_type == "checksum":
                    with open(cache_file, 'w', encoding='utf-8') as f:
                        f.write(str(data))
                else:
                    # Binary dosyalar için pickle kullan
                    with open(cache_file, 'wb') as f:
                        pickle.dump(data, f)
            
            return True
            
        except Exception as e:
            print(f"Cache yazma hatası: {e}")
            return False
    
    def delete(self, key: str, cache_type: str = "metadata") -> bool:
        """Cache'den veri siler"""
        cache_file = self._get_cache_key(key, cache_type)
        
        try:
            if cache_file.exists():
                cache_file.unlink()
                return True
            return False
        except Exception:
            return False
    
    def clear(self, cache_type: Optional[str] = None) -> int:
        """
        Cache'i temizler
        
        Args:
            cache_type: Temizlenecek cache türü (None ise tümü)
            
        Returns:
            Silinen dosya sayısı
        """
        deleted_count = 0
        
        if cache_type:
            cache_path = self._get_cache_key("", cache_type).parent
            if cache_path.exists():
                for file in cache_path.iterdir():
                    if file.is_file():
                        file.unlink()
                        deleted_count += 1
        else:
            # Tüm cache'leri temizle
            for cache_path in [self.metadata_cache, self.registry_cache, 
                              self.checksum_cache, self.download_cache]:
                if cache_path.exists():
                    for file in cache_path.iterdir():
                        if file.is_file():
                            file.unlink()
                            deleted_count += 1
        
        return deleted_count
    
    def get_stats(self) -> Dict[str, Any]:
        """Cache istatistiklerini döndürür"""
        total_size = 0
        
        # Cache boyutunu hesapla
        for cache_path in [self.metadata_cache, self.registry_cache, 
                          self.checksum_cache, self.download_cache]:
            if cache_path.exists():
                for file in cache_path.iterdir():
                    if file.is_file():
                        total_size += file.stat().st_size
        
        return {
            **self.stats,
            "size_bytes": total_size,
            "size_mb": round(total_size / (1024 * 1024), 2),
            "hit_rate": round(self.stats["hits"] / max(1, self.stats["hits"] + self.stats["misses"]) * 100, 2)
        }
    
    def calculate_checksum(self, file_path: str) -> str:
        """Dosyanın SHA-256 checksum'unu hesaplar ve cache'ler"""
        cache_key = hashlib.md5(file_path.encode()).hexdigest()
        cached_checksum = self.get(cache_key, "checksum", max_age=86400)  # 24 saat
        
        if cached_checksum:
            return cached_checksum
        
        # Checksum hesapla
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        
        checksum = sha256_hash.hexdigest()
        self.set(cache_key, checksum, "checksum")
        
        return checksum
    
    def cache_package_metadata(self, package_path: str, metadata: Dict[str, Any]) -> bool:
        """Paket meta verilerini cache'ler"""
        cache_key = hashlib.md5(package_path.encode()).hexdigest()
        return self.set(cache_key, metadata, "metadata")
    
    def get_cached_package_metadata(self, package_path: str) -> Optional[Dict[str, Any]]:
        """Cache'lenmiş paket meta verilerini alır"""
        cache_key = hashlib.md5(package_path.encode()).hexdigest()
        return self.get(cache_key, "metadata", max_age=3600)  # 1 saat
    
    def cache_registry_data(self, registry_url: str, data: List[Dict[str, Any]]) -> bool:
        """Registry verilerini cache'ler"""
        cache_key = hashlib.md5(registry_url.encode()).hexdigest()
        return self.set(cache_key, data, "registry")
    
    def get_cached_registry_data(self, registry_url: str) -> Optional[List[Dict[str, Any]]]:
        """Cache'lenmiş registry verilerini alır"""
        cache_key = hashlib.md5(registry_url.encode()).hexdigest()
        return self.get(cache_key, "registry", max_age=1800)  # 30 dakika

class ParallelDownloader:
    """Paralel indirme yöneticisi"""
    
    def __init__(self, max_workers: int = 4):
        """
        ParallelDownloader başlatıcısı
        
        Args:
            max_workers: Maksimum paralel işçi sayısı
        """
        self.max_workers = max_workers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'clapp-package-manager/1.0'
        })
    
    def download_file(self, url: str, destination: str) -> Tuple[bool, str]:
        """Tek dosya indirir"""
        try:
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True, f"Dosya indirildi: {destination}"
            
        except Exception as e:
            return False, f"İndirme hatası: {str(e)}"
    
    def download_files_parallel(self, download_tasks: List[Tuple[str, str]]) -> List[Tuple[bool, str]]:
        """
        Birden fazla dosyayı paralel indirir
        
        Args:
            download_tasks: [(url, destination), ...] listesi
            
        Returns:
            [(success, message), ...] listesi
        """
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # İndirme görevlerini başlat
            future_to_task = {
                executor.submit(self.download_file, url, dest): (url, dest)
                for url, dest in download_tasks
            }
            
            # Sonuçları topla
            for future in concurrent.futures.as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append((False, f"İndirme hatası: {str(e)}"))
        
        return results

# Cache decorator
def cached(max_age: int = 3600, cache_type: str = "metadata"):
    """Cache decorator'ı"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Cache anahtarı oluştur
            cache_key = f"{func.__name__}_{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Cache manager oluştur
            cache_manager = CacheManager()
            
            # Cache'den kontrol et
            cached_result = cache_manager.get(cache_key, cache_type, max_age)
            if cached_result is not None:
                return cached_result
            
            # Fonksiyonu çalıştır
            result = func(*args, **kwargs)
            
            # Sonucu cache'le
            cache_manager.set(cache_key, result, cache_type)
            
            return result
        return wrapper
    return decorator

# Yardımcı fonksiyonlar
def create_cache_manager() -> CacheManager:
    """Varsayılan ayarlarla CacheManager oluşturur"""
    return CacheManager()

def create_parallel_downloader(max_workers: int = 4) -> ParallelDownloader:
    """ParallelDownloader oluşturur"""
    return ParallelDownloader(max_workers)

def get_cache_stats() -> Dict[str, Any]:
    """Cache istatistiklerini alır"""
    cache_manager = create_cache_manager()
    return cache_manager.get_stats()

def clear_all_caches() -> int:
    """Tüm cache'leri temizler"""
    cache_manager = create_cache_manager()
    return cache_manager.clear()

def download_packages_parallel(package_urls: List[str], destination_dir: str) -> List[Tuple[bool, str]]:
    """Paketleri paralel indirir"""
    downloader = create_parallel_downloader()
    
    # İndirme görevlerini hazırla
    download_tasks = []
    for url in package_urls:
        filename = os.path.basename(url)
        destination = os.path.join(destination_dir, filename)
        download_tasks.append((url, destination))
    
    return downloader.download_files_parallel(download_tasks) 