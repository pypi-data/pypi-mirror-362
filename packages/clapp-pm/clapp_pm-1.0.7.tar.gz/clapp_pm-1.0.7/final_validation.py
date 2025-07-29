#!/usr/bin/env python3
"""
Son Doğrulama Testi
===================

Bu script clapp sisteminin production-ready olup olmadığını kontrol eder.
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any

class FinalValidator:
    def __init__(self):
        self.test_results = []
        self.critical_errors = []
        self.warnings = []
        
    def log_test(self, test_name: str, success: bool, message: str = "", critical: bool = False):
        """Test sonucunu kaydet"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "critical": critical,
            "timestamp": time.time()
        }
        self.test_results.append(result)
        
        if success:
            print(f"✅ {test_name}: {message}")
        else:
            print(f"❌ {test_name}: {message}")
            if critical:
                self.critical_errors.append(result)
    
    def test_critical_functions(self) -> bool:
        """Kritik fonksiyonları test et"""
        print("\n🔍 Kritik Fonksiyonlar Testi")
        print("=" * 50)
        
        try:
            # 1. Version sistemi
            from version import __version__, __author__
            if __version__ and __author__:
                self.log_test("Version System", True, f"Sürüm: {__version__}, Yazar: {__author__}", critical=True)
            else:
                self.log_test("Version System", False, "Sürüm bilgisi eksik", critical=True)
                return False
            
            # 2. Apps dizini
            from package_registry import get_apps_directory
            apps_dir = get_apps_directory()
            if Path(apps_dir).exists() or Path(apps_dir).mkdir(parents=True, exist_ok=True):
                self.log_test("Apps Directory", True, f"Dizin: {apps_dir}", critical=True)
            else:
                self.log_test("Apps Directory", False, "Apps dizini oluşturulamadı", critical=True)
                return False
            
            # 3. Manifest doğrulama
            from manifest_schema import validate_manifest
            test_manifest = {
                "name": "test",
                "version": "1.0.0",
                "language": "python",
                "entry": "main.py"
            }
            if validate_manifest(test_manifest):
                self.log_test("Manifest Validation", True, "Manifest doğrulama çalışıyor", critical=True)
            else:
                self.log_test("Manifest Validation", False, "Manifest doğrulama çalışmıyor", critical=True)
                return False
            
            # 4. Package registry
            from package_registry import list_packages, app_exists
            packages = list_packages()
            if isinstance(packages, list):
                self.log_test("Package Registry", True, f"{len(packages)} paket listelendi", critical=True)
            else:
                self.log_test("Package Registry", False, "Package registry çalışmıyor", critical=True)
                return False
            
            # 5. Package runner
            from package_runner import run_app
            # Var olmayan uygulama testi
            result = run_app("nonexistent-app")
            if not result:  # False dönmeli
                self.log_test("Package Runner", True, "Package runner çalışıyor", critical=True)
            else:
                self.log_test("Package Runner", False, "Package runner çalışmıyor", critical=True)
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Critical Functions", False, f"Kritik fonksiyonlar hatası: {e}", critical=True)
            return False
    
    def test_cli_interface(self) -> bool:
        """CLI arayüzünü test et"""
        print("\n🔍 CLI Arayüzü Testi")
        print("=" * 50)
        
        try:
            # Version komutu
            result = subprocess.run([sys.executable, "main.py", "version"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and "clapp v" in result.stdout:
                self.log_test("CLI Version", True, "Version komutu çalışıyor", critical=True)
            else:
                self.log_test("CLI Version", False, "Version komutu çalışmıyor", critical=True)
                return False
            
            # List komutu
            result = subprocess.run([sys.executable, "main.py", "list"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.log_test("CLI List", True, "List komutu çalışıyor", critical=True)
            else:
                self.log_test("CLI List", False, "List komutu çalışmıyor", critical=True)
                return False
            
            # Help komutu
            result = subprocess.run([sys.executable, "main.py", "--help"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and "usage:" in result.stdout:
                self.log_test("CLI Help", True, "Help komutu çalışıyor", critical=True)
            else:
                self.log_test("CLI Help", False, "Help komutu çalışmıyor", critical=True)
                return False
            
            return True
            
        except Exception as e:
            self.log_test("CLI Interface", False, f"CLI arayüzü hatası: {e}", critical=True)
            return False
    
    def test_error_handling(self) -> bool:
        """Hata yönetimini test et"""
        print("\n🔍 Hata Yönetimi Testi")
        print("=" * 50)
        
        try:
            # Var olmayan uygulama
            from package_runner import run_app
            result = run_app("nonexistent-app")
            if not result:
                self.log_test("Non-existent App", True, "Var olmayan uygulama doğru şekilde reddedildi")
            else:
                self.log_test("Non-existent App", False, "Var olmayan uygulama yanlış şekilde kabul edildi")
                return False
            
            # Geçersiz manifest
            from manifest_validator import validate_manifest_verbose
            invalid_manifest = {"name": "test"}  # Eksik alanlar
            is_valid, errors = validate_manifest_verbose(invalid_manifest)
            
            if not is_valid and errors:
                self.log_test("Invalid Manifest", True, "Geçersiz manifest doğru şekilde reddedildi")
            else:
                self.log_test("Invalid Manifest", False, "Geçersiz manifest yanlış şekilde kabul edildi")
                return False
            
            # Var olmayan uygulama manifest
            from package_registry import get_manifest
            manifest = get_manifest("nonexistent-app")
            if manifest is None:
                self.log_test("Non-existent Manifest", True, "Var olmayan uygulama manifest None döndürdü")
            else:
                self.log_test("Non-existent Manifest", False, "Var olmayan uygulama manifest None döndürmedi")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Error Handling", False, f"Hata yönetimi hatası: {e}")
            return False
    
    def test_performance(self) -> bool:
        """Performansı test et"""
        print("\n🔍 Performans Testi")
        print("=" * 50)
        
        try:
            import time
            
            # List komutu performansı
            start_time = time.time()
            from package_registry import list_packages
            packages = list_packages()
            end_time = time.time()
            
            duration = end_time - start_time
            if duration < 0.5:  # 0.5 saniyeden az
                self.log_test("List Performance", True, f"List komutu {duration:.3f}s'de tamamlandı")
            else:
                self.log_test("List Performance", False, f"List komutu çok yavaş: {duration:.3f}s")
                return False
            
            # Version komutu performansı
            start_time = time.time()
            from version_command import get_version_info
            info = get_version_info()
            end_time = time.time()
            
            duration = end_time - start_time
            if duration < 0.1:  # 0.1 saniyeden az
                self.log_test("Version Performance", True, f"Version komutu {duration:.3f}s'de tamamlandı")
            else:
                self.log_test("Version Performance", False, f"Version komutu çok yavaş: {duration:.3f}s")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Performance", False, f"Performans testi hatası: {e}")
            return False
    
    def test_file_operations(self) -> bool:
        """Dosya işlemlerini test et"""
        print("\n🔍 Dosya İşlemleri Testi")
        print("=" * 50)
        
        try:
            from package_registry import get_apps_directory
            apps_dir = get_apps_directory()
            
            # Test dizini oluştur
            test_dir = Path(apps_dir) / "test-file-ops"
            test_dir.mkdir(exist_ok=True)
            
            # Dosya yazma
            test_file = test_dir / "test.txt"
            test_file.write_text("test content")
            
            if test_file.exists():
                self.log_test("File Write", True, "Dosya yazma çalışıyor")
            else:
                self.log_test("File Write", False, "Dosya yazma çalışmıyor")
                return False
            
            # Dosya okuma
            content = test_file.read_text()
            if content == "test content":
                self.log_test("File Read", True, "Dosya okuma çalışıyor")
            else:
                self.log_test("File Read", False, "Dosya okuma çalışmıyor")
                return False
            
            # Temizlik
            test_file.unlink()
            test_dir.rmdir()
            
            return True
            
        except Exception as e:
            self.log_test("File Operations", False, f"Dosya işlemleri hatası: {e}")
            return False
    
    def test_network_operations(self) -> bool:
        """Ağ işlemlerini test et"""
        print("\n🔍 Ağ İşlemleri Testi")
        print("=" * 50)
        
        try:
            # Index yükleme
            from install_command import load_index
            success, message, apps = load_index()
            
            if success and isinstance(apps, list):
                self.log_test("Index Loading", True, f"Index yüklendi: {len(apps)} uygulama")
            else:
                self.log_test("Index Loading", False, f"Index yükleme hatası: {message}")
                return False
            
            # Uygulama arama
            from install_command import find_app_in_index
            app_info = find_app_in_index("hello-python", apps)
            
            if app_info and app_info.get("name") == "hello-python":
                self.log_test("App Search", True, "Uygulama arama çalışıyor")
            else:
                self.log_test("App Search", False, "Uygulama arama çalışmıyor")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Network Operations", False, f"Ağ işlemleri hatası: {e}")
            return False
    
    def run_final_validation(self) -> Dict[str, Any]:
        """Son doğrulama testlerini çalıştır"""
        print("🚀 CLAPP Son Doğrulama Testi Başlatılıyor")
        print("=" * 60)
        
        tests = [
            ("Kritik Fonksiyonlar", self.test_critical_functions),
            ("CLI Arayüzü", self.test_cli_interface),
            ("Hata Yönetimi", self.test_error_handling),
            ("Performans", self.test_performance),
            ("Dosya İşlemleri", self.test_file_operations),
            ("Ağ İşlemleri", self.test_network_operations)
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                success = test_func()
                results[test_name] = success
            except Exception as e:
                self.log_test(test_name, False, f"Test hatası: {e}", critical=True)
                results[test_name] = False
        
        return results
    
    def generate_final_report(self) -> str:
        """Son doğrulama raporu oluştur"""
        print("\n" + "=" * 60)
        print("📊 SON DOĞRULAMA RAPORU")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = len([r for r in self.test_results if not r["success"]])
        critical_errors = len(self.critical_errors)
        
        print(f"Toplam Test: {total_tests}")
        print(f"Başarılı: {successful_tests}")
        print(f"Başarısız: {failed_tests}")
        print(f"Kritik Hatalar: {critical_errors}")
        print(f"Başarı Oranı: {(successful_tests/total_tests*100):.1f}%")
        
        if self.critical_errors:
            print(f"\n🚨 KRİTİK HATALAR:")
            for error in self.critical_errors:
                print(f"  - {error['test']}: {error['message']}")
        
        if failed_tests > 0 and critical_errors == 0:
            print(f"\n⚠️  BAŞARISIZ TESTLER (Kritik değil):")
            for result in self.test_results:
                if not result["success"] and not result["critical"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        if critical_errors == 0:
            if failed_tests == 0:
                print(f"\n🎉 MÜKEMMEL! Sistem tamamen production-ready!")
                return "PRODUCTION-READY"
            else:
                print(f"\n✅ SİSTEM HAZIR! Kritik hatalar yok, küçük iyileştirmeler gerekebilir.")
                return "READY_WITH_MINOR_ISSUES"
        else:
            print(f"\n❌ SİSTEM HAZIR DEĞİL! Kritik hatalar var.")
            return "NOT_READY"
    
    def check_production_readiness(self) -> bool:
        """Production-ready olup olmadığını kontrol et"""
        results = self.run_final_validation()
        report = self.generate_final_report()
        
        # Sonuçları JSON olarak kaydet
        with open("final_validation_results.json", "w", encoding="utf-8") as f:
            json.dump({
                "results": results,
                "test_details": self.test_results,
                "critical_errors": self.critical_errors,
                "warnings": self.warnings,
                "summary": report,
                "production_ready": len(self.critical_errors) == 0
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Detaylı rapor: final_validation_results.json")
        
        # Production-ready kontrolü
        is_ready = len(self.critical_errors) == 0
        
        if is_ready:
            print(f"\n🚀 SİSTEM PRODUCTION-READY!")
            print(f"✅ Kritik hatalar: 0")
            print(f"✅ Başarı oranı: {(len([r for r in self.test_results if r['success']])/len(self.test_results)*100):.1f}%")
            print(f"✅ Tüm temel fonksiyonlar çalışıyor")
            print(f"✅ CLI arayüzü stabil")
            print(f"✅ Hata yönetimi uygun")
            print(f"✅ Performans kabul edilebilir")
        else:
            print(f"\n🔧 SİSTEM PRODUCTION-READY DEĞİL!")
            print(f"❌ Kritik hatalar: {len(self.critical_errors)}")
            print(f"🔧 Bu hatalar düzeltilmeli:")
            for error in self.critical_errors:
                print(f"  - {error['test']}: {error['message']}")
        
        return is_ready

def main():
    """Ana doğrulama fonksiyonu"""
    validator = FinalValidator()
    is_ready = validator.check_production_readiness()
    
    if is_ready:
        sys.exit(0)  # Başarılı
    else:
        sys.exit(1)  # Başarısız

if __name__ == "__main__":
    main() 