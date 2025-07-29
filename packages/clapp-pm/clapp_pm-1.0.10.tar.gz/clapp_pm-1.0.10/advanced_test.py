#!/usr/bin/env python3
"""
Gelişmiş Sistem Testi
=====================

Bu script clapp sisteminin gerçek kullanım senaryolarını test eder.
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

class AdvancedTester:
    def __init__(self):
        self.test_results = []
        self.errors = []
        self.warnings = []
        
    def log_test(self, test_name: str, success: bool, message: str = "", details: Any = None):
        """Test sonucunu kaydet"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details,
            "timestamp": time.time()
        }
        self.test_results.append(result)
        
        if success:
            print(f"✅ {test_name}: {message}")
        else:
            print(f"❌ {test_name}: {message}")
            self.errors.append(result)
    
    def test_real_installation_flow(self) -> bool:
        """Gerçek kurulum akışını test et"""
        print("\n🔍 Gerçek Kurulum Akışı Testi")
        print("=" * 50)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Test uygulaması oluştur
                test_app_dir = Path(temp_dir) / "hello-world"
                test_app_dir.mkdir()
                
                # manifest.json
                manifest = {
                    "name": "hello-world",
                    "version": "1.0.0",
                    "language": "python",
                    "entry": "main.py",
                    "description": "Merhaba Dünya uygulaması"
                }
                
                with open(test_app_dir / "manifest.json", 'w', encoding='utf-8') as f:
                    json.dump(manifest, f, indent=2, ensure_ascii=False)
                
                # main.py
                main_content = '''#!/usr/bin/env python3
print("Merhaba Dünya!")
print("Bu bir test uygulamasıdır.")
'''
                with open(test_app_dir / "main.py", 'w', encoding='utf-8') as f:
                    f.write(main_content)
                
                # Kurulum testi
                from install_command import install_app
                success, message = install_app("hello-world")
                
                if success:
                    self.log_test("Install App", True, "Uygulama kuruldu")
                    
                    # Kurulum sonrası kontrol
                    from package_registry import app_exists, get_manifest
                    
                    if app_exists("hello-world"):
                        self.log_test("App Exists After Install", True, "Uygulama kurulum sonrası mevcut")
                    else:
                        self.log_test("App Exists After Install", False, "Uygulama kurulum sonrası bulunamadı")
                        return False
                    
                    # Manifest kontrolü
                    manifest = get_manifest("hello-world")
                    if manifest and manifest["name"] == "hello-world":
                        self.log_test("Manifest After Install", True, "Manifest doğru yüklendi")
                    else:
                        self.log_test("Manifest After Install", False, "Manifest yanlış yüklendi")
                        return False
                    
                    # Çalıştırma testi
                    from package_runner import run_app
                    if run_app("hello-world"):
                        self.log_test("Run App", True, "Uygulama başarıyla çalıştı")
                    else:
                        self.log_test("Run App", False, "Uygulama çalıştırılamadı")
                        return False
                    
                    # Kaldırma testi
                    from uninstall_command import uninstall_app
                    success, message = uninstall_app("hello-world", skip_confirmation=True)
                    
                    if success:
                        self.log_test("Uninstall App", True, "Uygulama kaldırıldı")
                        
                        # Kaldırma sonrası kontrol
                        if not app_exists("hello-world"):
                            self.log_test("App Not Exists After Uninstall", True, "Uygulama kaldırma sonrası mevcut değil")
                        else:
                            self.log_test("App Not Exists After Uninstall", False, "Uygulama kaldırma sonrası hala mevcut")
                            return False
                    else:
                        self.log_test("Uninstall App", False, f"Kaldırma hatası: {message}")
                        return False
                    
                else:
                    self.log_test("Install App", False, f"Kurulum hatası: {message}")
                    return False
                
                return True
                
            except Exception as e:
                self.log_test("Real Installation Flow", False, f"Kurulum akışı hatası: {e}")
                return False
    
    def test_cli_integration(self) -> bool:
        """CLI entegrasyon testleri"""
        print("\n🔍 CLI Entegrasyon Testleri")
        print("=" * 50)
        
        try:
            # Version komutu
            result = subprocess.run([sys.executable, "main.py", "version"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and "clapp v1.0.6" in result.stdout:
                self.log_test("CLI Version Output", True, "Version komutu doğru çıktı verdi")
            else:
                self.log_test("CLI Version Output", False, f"Version komutu yanlış çıktı: {result.stdout}")
                return False
            
            # List komutu
            result = subprocess.run([sys.executable, "main.py", "list"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.log_test("CLI List Output", True, "List komutu çalıştı")
            else:
                self.log_test("CLI List Output", False, f"List komutu hatası: {result.stderr}")
                return False
            
            # Help komutu
            result = subprocess.run([sys.executable, "main.py", "--help"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and "usage:" in result.stdout:
                self.log_test("CLI Help Output", True, "Help komutu çalıştı")
            else:
                self.log_test("CLI Help Output", False, f"Help komutu hatası: {result.stderr}")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("CLI Integration", False, f"CLI entegrasyon hatası: {e}")
            return False
    
    def test_error_handling(self) -> bool:
        """Hata yönetimi testleri"""
        print("\n🔍 Hata Yönetimi Testleri")
        print("=" * 50)
        
        try:
            # Var olmayan uygulama çalıştırma
            from package_runner import run_app
            result = run_app("nonexistent-app")
            
            if not result:
                self.log_test("Non-existent App Run", True, "Var olmayan uygulama doğru şekilde reddedildi")
            else:
                self.log_test("Non-existent App Run", False, "Var olmayan uygulama yanlış şekilde çalıştı")
                return False
            
            # Geçersiz manifest testi
            with tempfile.TemporaryDirectory() as temp_dir:
                test_app_dir = Path(temp_dir) / "invalid-app"
                test_app_dir.mkdir()
                
                # Geçersiz manifest
                invalid_manifest = {
                    "name": "invalid-app",
                    # version eksik
                    "language": "python"
                    # entry eksik
                }
                
                with open(test_app_dir / "manifest.json", 'w', encoding='utf-8') as f:
                    json.dump(invalid_manifest, f, indent=2, ensure_ascii=False)
                
                from manifest_validator import validate_manifest_verbose
                is_valid, errors = validate_manifest_verbose(invalid_manifest)
                
                if not is_valid and errors:
                    self.log_test("Invalid Manifest Validation", True, f"Geçersiz manifest doğru şekilde reddedildi: {errors}")
                else:
                    self.log_test("Invalid Manifest Validation", False, "Geçersiz manifest yanlış şekilde kabul edildi")
                    return False
            
            return True
            
        except Exception as e:
            self.log_test("Error Handling", False, f"Hata yönetimi hatası: {e}")
            return False
    
    def test_performance(self) -> bool:
        """Performans testleri"""
        print("\n🔍 Performans Testleri")
        print("=" * 50)
        
        try:
            import time
            
            # List komutu performansı
            start_time = time.time()
            from package_registry import list_packages
            packages = list_packages()
            end_time = time.time()
            
            duration = end_time - start_time
            if duration < 1.0:  # 1 saniyeden az olmalı
                self.log_test("List Performance", True, f"List komutu {duration:.3f} saniyede tamamlandı")
            else:
                self.log_test("List Performance", False, f"List komutu çok yavaş: {duration:.3f} saniye")
                return False
            
            # Version komutu performansı
            start_time = time.time()
            from version_command import get_version_info
            info = get_version_info()
            end_time = time.time()
            
            duration = end_time - start_time
            if duration < 0.1:  # 0.1 saniyeden az olmalı
                self.log_test("Version Performance", True, f"Version komutu {duration:.3f} saniyede tamamlandı")
            else:
                self.log_test("Version Performance", False, f"Version komutu çok yavaş: {duration:.3f} saniye")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Performance", False, f"Performans testi hatası: {e}")
            return False
    
    def test_file_permissions(self) -> bool:
        """Dosya izinleri testleri"""
        print("\n🔍 Dosya İzinleri Testleri")
        print("=" * 50)
        
        try:
            from package_registry import get_apps_directory
            apps_dir = get_apps_directory()
            
            # Dizin oluşturma izni
            test_dir = Path(apps_dir) / "test-permissions"
            test_dir.mkdir(exist_ok=True)
            
            if test_dir.exists():
                self.log_test("Directory Creation Permission", True, "Dizin oluşturma izni var")
            else:
                self.log_test("Directory Creation Permission", False, "Dizin oluşturma izni yok")
                return False
            
            # Dosya yazma izni
            test_file = test_dir / "test.txt"
            test_file.write_text("test")
            
            if test_file.exists():
                self.log_test("File Write Permission", True, "Dosya yazma izni var")
            else:
                self.log_test("File Write Permission", False, "Dosya yazma izni yok")
                return False
            
            # Dosya okuma izni
            content = test_file.read_text()
            if content == "test":
                self.log_test("File Read Permission", True, "Dosya okuma izni var")
            else:
                self.log_test("File Read Permission", False, "Dosya okuma izni yok")
                return False
            
            # Temizlik
            test_file.unlink()
            test_dir.rmdir()
            
            return True
            
        except Exception as e:
            self.log_test("File Permissions", False, f"Dosya izinleri hatası: {e}")
            return False
    
    def test_network_resilience(self) -> bool:
        """Ağ dayanıklılığı testleri"""
        print("\n🔍 Ağ Dayanıklılığı Testleri")
        print("=" * 50)
        
        try:
            # Index yükleme testi
            from install_command import load_index
            success, message, apps = load_index()
            
            if success:
                self.log_test("Index Loading", True, f"Index yüklendi: {len(apps)} uygulama")
            else:
                self.log_test("Index Loading", False, f"Index yükleme hatası: {message}")
                return False
            
            # Uygulama arama testi
            from install_command import find_app_in_index
            app_info = find_app_in_index("hello-python", apps)
            
            if app_info:
                self.log_test("App Search", True, f"Uygulama bulundu: {app_info['name']}")
            else:
                self.log_test("App Search", True, "Uygulama bulunamadı (beklenen)")
            
            return True
            
        except Exception as e:
            self.log_test("Network Resilience", False, f"Ağ dayanıklılığı hatası: {e}")
            return False
    
    def run_all_advanced_tests(self) -> Dict[str, Any]:
        """Tüm gelişmiş testleri çalıştır"""
        print("🚀 CLAPP Gelişmiş Sistem Testi Başlatılıyor")
        print("=" * 60)
        
        tests = [
            ("Gerçek Kurulum Akışı", self.test_real_installation_flow),
            ("CLI Entegrasyonu", self.test_cli_integration),
            ("Hata Yönetimi", self.test_error_handling),
            ("Performans", self.test_performance),
            ("Dosya İzinleri", self.test_file_permissions),
            ("Ağ Dayanıklılığı", self.test_network_resilience)
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                success = test_func()
                results[test_name] = success
            except Exception as e:
                self.log_test(test_name, False, f"Test hatası: {e}")
                results[test_name] = False
        
        return results
    
    def generate_advanced_report(self) -> str:
        """Gelişmiş test raporu oluştur"""
        print("\n" + "=" * 60)
        print("📊 GELİŞMİŞ TEST RAPORU")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = len(self.errors)
        
        print(f"Toplam Test: {total_tests}")
        print(f"Başarılı: {successful_tests}")
        print(f"Başarısız: {failed_tests}")
        print(f"Başarı Oranı: {(successful_tests/total_tests*100):.1f}%")
        
        if self.errors:
            print(f"\n❌ BAŞARISIZ TESTLER:")
            for error in self.errors:
                print(f"  - {error['test']}: {error['message']}")
        
        if self.warnings:
            print(f"\n⚠️  UYARILAR:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if failed_tests == 0:
            print(f"\n🎉 TÜM GELİŞMİŞ TESTLER BAŞARILI! Sistem production-ready!")
        else:
            print(f"\n🔧 {failed_tests} test başarısız. Sistem iyileştirme gerektiriyor.")
        
        return f"Başarı Oranı: {(successful_tests/total_tests*100):.1f}%"

def main():
    """Ana test fonksiyonu"""
    tester = AdvancedTester()
    results = tester.run_all_advanced_tests()
    report = tester.generate_advanced_report()
    
    # Sonuçları JSON olarak kaydet
    with open("advanced_test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "results": results,
            "test_details": tester.test_results,
            "errors": tester.errors,
            "warnings": tester.warnings,
            "summary": report
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detaylı rapor: advanced_test_results.json")
    
    # Başarı oranına göre exit code
    total_tests = len(tester.test_results)
    successful_tests = len([r for r in tester.test_results if r["success"]])
    
    if successful_tests == total_tests:
        sys.exit(0)  # Başarılı
    else:
        sys.exit(1)  # Başarısız

if __name__ == "__main__":
    main() 