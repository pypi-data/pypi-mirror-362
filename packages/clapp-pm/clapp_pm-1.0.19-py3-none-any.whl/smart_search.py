#!/usr/bin/env python3
"""
smart_search.py - Akıllı Arama Sistemi

Bu modül clapp paketlerinde gelişmiş arama özellikleri sağlar:
- Fuzzy search (bulanık arama)
- Arama geçmişi
- Kategori bazlı arama
- Dil bazlı filtreleme
- Popülerlik sıralaması
- Otomatik tamamlama
"""

import os
import json
import re
import difflib
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
import pickle

class SmartSearch:
    """Akıllı arama motoru"""
    
    def __init__(self, history_file: Optional[str] = None):
        """
        SmartSearch başlatıcısı
        
        Args:
            history_file: Arama geçmişi dosyası
        """
        if history_file is None:
            history_file = os.path.join(os.path.expanduser("~"), ".clapp", "search_history.json")
        
        self.history_file = Path(history_file)
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Arama geçmişi
        self.search_history = self._load_history()
        
        # Kategori tanımları
        self.categories = {
            "cli": ["command", "terminal", "console", "cli", "command-line"],
            "gui": ["gui", "interface", "window", "desktop", "graphical"],
            "utility": ["utility", "tool", "helper", "assistant"],
            "development": ["dev", "development", "programming", "code", "script"],
            "game": ["game", "play", "entertainment", "fun"],
            "productivity": ["productivity", "work", "office", "business"],
            "education": ["education", "learn", "study", "tutorial"],
            "multimedia": ["media", "video", "audio", "image", "photo"]
        }
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """Arama geçmişini yükler"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return []
    
    def _save_history(self):
        """Arama geçmişini kaydeder"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.search_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Arama geçmişi kaydetme hatası: {e}")
    
    def add_to_history(self, query: str, results_count: int = 0):
        """Arama geçmişine ekler"""
        # Eski kayıtları temizle (30 günden eski)
        cutoff_date = datetime.now() - timedelta(days=30)
        self.search_history = [
            record for record in self.search_history
            if datetime.fromisoformat(record["timestamp"]) > cutoff_date
        ]
        
        # Yeni kayıt ekle
        record = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "results_count": results_count
        }
        
        # Aynı sorgu varsa güncelle
        for existing in self.search_history:
            if existing["query"] == query:
                existing["timestamp"] = record["timestamp"]
                existing["results_count"] = results_count
                self._save_history()
                return
        
        self.search_history.append(record)
        self._save_history()
    
    def get_search_history(self, limit: int = 10) -> List[str]:
        """Arama geçmişini döndürür"""
        # En son kullanılan sorguları döndür
        sorted_history = sorted(
            self.search_history,
            key=lambda x: datetime.fromisoformat(x["timestamp"]),
            reverse=True
        )
        
        return [record["query"] for record in sorted_history[:limit]]
    
    def get_popular_searches(self, limit: int = 5) -> List[Tuple[str, int]]:
        """Popüler aramaları döndürür"""
        # Sorgu frekansını hesapla
        query_counts = {}
        for record in self.search_history:
            query = record["query"]
            query_counts[query] = query_counts.get(query, 0) + 1
        
        # En popüler olanları döndür
        sorted_queries = sorted(query_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_queries[:limit]
    
    def fuzzy_search(self, query: str, packages: List[Dict[str, Any]], threshold: float = 0.6) -> List[Dict[str, Any]]:
        """
        Bulanık arama yapar
        
        Args:
            query: Arama sorgusu
            packages: Paket listesi
            threshold: Eşleşme eşiği (0.0 - 1.0)
            
        Returns:
            Eşleşen paketler (skor ile)
        """
        results = []
        query_lower = query.lower()
        
        for package in packages:
            score = 0.0
            name = package.get("name", "").lower()
            description = package.get("description", "").lower()
            language = package.get("language", "").lower()
            
            # Tam eşleşme kontrolü
            if query_lower == name:
                score = 1.0
            elif query_lower in name:
                score = 0.9
            elif query_lower in description:
                score = 0.7
            elif query_lower == language:
                score = 0.6
            else:
                # Fuzzy matching
                name_ratio = difflib.SequenceMatcher(None, query_lower, name).ratio()
                desc_ratio = difflib.SequenceMatcher(None, query_lower, description).ratio()
                
                score = max(name_ratio, desc_ratio * 0.5)
            
            if score >= threshold:
                results.append({
                    **package,
                    "search_score": score
                })
        
        # Skora göre sırala
        results.sort(key=lambda x: x["search_score"], reverse=True)
        return results
    
    def search_by_category(self, category: str, packages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Kategoriye göre arama yapar
        
        Args:
            category: Kategori adı
            packages: Paket listesi
            
        Returns:
            Kategoriye uygun paketler
        """
        if category not in self.categories:
            return []
        
        category_keywords = self.categories[category]
        results = []
        
        for package in packages:
            name = package.get("name", "").lower()
            description = package.get("description", "").lower()
            
            # Kategori anahtar kelimelerini kontrol et
            for keyword in category_keywords:
                if keyword in name or keyword in description:
                    results.append(package)
                    break
        
        return results
    
    def search_by_language(self, language: str, packages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Dile göre filtreleme yapar
        
        Args:
            language: Dil adı (python, lua, vb.)
            packages: Paket listesi
            
        Returns:
            Dile uygun paketler
        """
        language_lower = language.lower()
        return [
            package for package in packages
            if package.get("language", "").lower() == language_lower
        ]
    
    def advanced_search(self, query: str, packages: List[Dict[str, Any]], 
                       filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Gelişmiş arama yapar
        
        Args:
            query: Arama sorgusu
            packages: Paket listesi
            filters: Filtreler (language, category, min_version, vb.)
            
        Returns:
            Filtrelenmiş ve sıralanmış paketler
        """
        if filters is None:
            filters = {}
        
        # Başlangıçta tüm paketler
        results = packages
        
        # Dil filtresi
        if "language" in filters:
            results = self.search_by_language(filters["language"], results)
        
        # Kategori filtresi
        if "category" in filters:
            results = self.search_by_category(filters["category"], results)
        
        # Versiyon filtresi
        if "min_version" in filters:
            results = self._filter_by_version(results, filters["min_version"], "min")
        
        if "max_version" in filters:
            results = self._filter_by_version(results, filters["max_version"], "max")
        
        # Fuzzy search
        if query:
            results = self.fuzzy_search(query, results)
        
        # Sıralama
        sort_by = filters.get("sort_by", "relevance")
        if sort_by == "name":
            results.sort(key=lambda x: x.get("name", "").lower())
        elif sort_by == "version":
            results.sort(key=lambda x: x.get("version", "0.0.0"), reverse=True)
        elif sort_by == "language":
            results.sort(key=lambda x: x.get("language", "").lower())
        
        return results
    
    def _filter_by_version(self, packages: List[Dict[str, Any]], version: str, filter_type: str) -> List[Dict[str, Any]]:
        """Versiyona göre filtreleme"""
        try:
            from packaging import version as pkg_version
            target_version = pkg_version.parse(version)
            
            filtered_packages = []
            for package in packages:
                package_version = pkg_version.parse(package.get("version", "0.0.0"))
                
                if filter_type == "min" and package_version >= target_version:
                    filtered_packages.append(package)
                elif filter_type == "max" and package_version <= target_version:
                    filtered_packages.append(package)
            
            return filtered_packages
        except Exception:
            return packages
    
    def get_search_suggestions(self, partial_query: str, packages: List[Dict[str, Any]], limit: int = 5) -> List[str]:
        """
        Arama önerileri verir
        
        Args:
            partial_query: Kısmi sorgu
            packages: Paket listesi
            limit: Maksimum öneri sayısı
            
        Returns:
            Öneri listesi
        """
        suggestions = set()
        partial_lower = partial_query.lower()
        
        # Paket isimlerinden öneriler
        for package in packages:
            name = package.get("name", "")
            if partial_lower in name.lower():
                suggestions.add(name)
        
        # Arama geçmişinden öneriler
        for record in self.search_history:
            query = record["query"]
            if partial_lower in query.lower():
                suggestions.add(query)
        
        # Kategori önerileri
        for category in self.categories.keys():
            if partial_lower in category.lower():
                suggestions.add(f"category:{category}")
        
        # Dil önerileri
        languages = set(package.get("language", "") for package in packages)
        for language in languages:
            if partial_lower in language.lower():
                suggestions.add(f"language:{language}")
        
        return list(suggestions)[:limit]
    
    def get_search_analytics(self) -> Dict[str, Any]:
        """Arama analitiklerini döndürür"""
        if not self.search_history:
            return {
                "total_searches": 0,
                "unique_queries": 0,
                "most_popular": [],
                "recent_searches": [],
                "search_trends": {}
            }
        
        # Toplam arama sayısı
        total_searches = len(self.search_history)
        
        # Benzersiz sorgu sayısı
        unique_queries = len(set(record["query"] for record in self.search_history))
        
        # En popüler aramalar
        popular_searches = self.get_popular_searches(5)
        
        # Son aramalar
        recent_searches = self.get_search_history(5)
        
        # Arama trendleri (son 7 gün)
        trends = {}
        cutoff_date = datetime.now() - timedelta(days=7)
        
        for record in self.search_history:
            record_date = datetime.fromisoformat(record["timestamp"])
            if record_date > cutoff_date:
                date_str = record_date.strftime("%Y-%m-%d")
                trends[date_str] = trends.get(date_str, 0) + 1
        
        return {
            "total_searches": total_searches,
            "unique_queries": unique_queries,
            "most_popular": popular_searches,
            "recent_searches": recent_searches,
            "search_trends": trends
        }

class SearchIndex:
    """Arama indeksi oluşturucu"""
    
    def __init__(self):
        """SearchIndex başlatıcısı"""
        self.index = {}
    
    def build_index(self, packages: List[Dict[str, Any]]):
        """Paketlerden arama indeksi oluşturur"""
        self.index = {}
        
        for package in packages:
            name = package.get("name", "").lower()
            description = package.get("description", "").lower()
            language = package.get("language", "").lower()
            
            # Kelimeleri ayır
            words = set()
            words.update(name.split())
            words.update(description.split())
            words.add(language)
            
            # İndekse ekle
            for word in words:
                if len(word) >= 2:  # En az 2 karakter
                    if word not in self.index:
                        self.index[word] = []
                    self.index[word].append(package)
    
    def search_index(self, query: str) -> List[Dict[str, Any]]:
        """İndeksten arama yapar"""
        query_words = query.lower().split()
        results = {}
        
        for word in query_words:
            if word in self.index:
                for package in self.index[word]:
                    package_id = package.get("name", "")
                    if package_id not in results:
                        results[package_id] = package
                        results[package_id]["match_count"] = 0
                    results[package_id]["match_count"] += 1
        
        # Eşleşme sayısına göre sırala
        sorted_results = sorted(
            results.values(),
            key=lambda x: x["match_count"],
            reverse=True
        )
        
        return sorted_results

# Yardımcı fonksiyonlar
def create_smart_search() -> SmartSearch:
    """Varsayılan ayarlarla SmartSearch oluşturur"""
    return SmartSearch()

def create_search_index() -> SearchIndex:
    """SearchIndex oluşturur"""
    return SearchIndex()

def search_packages(query: str, packages: List[Dict[str, Any]], 
                   filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Paketlerde arama yapar"""
    searcher = create_smart_search()
    results = searcher.advanced_search(query, packages, filters)
    
    # Arama geçmişine ekle
    searcher.add_to_history(query, len(results))
    
    return results

def get_search_suggestions(partial_query: str, packages: List[Dict[str, Any]]) -> List[str]:
    """Arama önerileri alır"""
    searcher = create_smart_search()
    return searcher.get_search_suggestions(partial_query, packages)

def get_search_analytics() -> Dict[str, Any]:
    """Arama analitiklerini alır"""
    searcher = create_smart_search()
    return searcher.get_search_analytics()

def clear_search_history():
    """Arama geçmişini temizler"""
    searcher = create_smart_search()
    searcher.search_history = []
    searcher._save_history()
    print("✅ Arama geçmişi temizlendi") 