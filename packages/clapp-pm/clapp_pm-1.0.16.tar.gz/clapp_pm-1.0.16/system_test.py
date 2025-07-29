#!/usr/bin/env python3
"""
Sistem Entegrasyon Testi
========================

Bu script clapp sisteminin tüm bileşenlerinin doğru çalışıp çalışmadığını test eder.
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Any

class SystemTester:
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
            "details": details
        }
        self.test_results.append(result)
        
        if success:
            print(f"✅ {test_name}: {message}")
        else:
            print(f"❌ {test_name}: {message}")
            self.errors.append(result)
    
    def log_warning(self, warning: str):
        """Uyarı kaydet"""
        self.warnings.append(warning)
        print(f"⚠️  {warning}")
    
    def test_imports(self) -> bool:
        """Tüm modüllerin import edilebilirliğini test et"""
        print("\n🔍 Modül Import Testleri")
        print("=" * 50)
        
        modules = [
            "main", "clapp_core", "package_registry", "package_runner",
            "manifest_schema", "manifest_validator", "install_command",
            "list_command", "version_command", "info_command", "doctor_command",
            "clean_command", "where_command", "validate_command", "uninstall_command",
            "publish_command", "remote_registry", "dependency_resolver",
            "installer", "cli_commands", "check_env", "post_install_hint"
        ]
        
        all_success = True
        for module in modules:
            try:
                __import__(module)
                self.log_test(f"Import {module}", True, "Başarılı")
            except ImportError as e:
                self.log_test(f"Import {module}", False, f"Import hatası: {e}")
                all_success = False
            except Exception as e:
                self.log_test(f"Import {module}", False, f"Beklenmeyen hata: {e}")
                all_success = False
        
        return all_success
    
    def test_version_system(self) -> bool:
        """Sürüm sistemi testleri"""
        print("\n🔍 Sürüm Sistemi Testleri")
        print("=" * 50)
        
        try:
            from version import __version__, __author__, __email__
            
            # Sürüm formatı kontrolü
            if not __version__ or __version__ == "0.0.0":
                self.log_test("Version Format", False, "Geçersiz sürüm numarası")
                return False
            
            self.log_test("Version Import", True, f"Sürüm: {__version__}")
            self.log_test("Author Import", True, f"Yazar: {__author__}")
            self.log_test("Email Import", True, f"Email: {__email__}")
            
            # version_command.py testi
            try:
                from version_command import get_version_info
                info = get_version_info()
                
                if info["version"] == __version__:
                    self.log_test("Version Command Integration", True, "Sürüm bilgisi eşleşiyor")
                else:
                    self.log_test("Version Command Integration", False, 
                                f"Sürüm uyumsuzluğu: {info['version']} != {__version__}")
                    return False
                    
            except Exception as e:
                self.log_test("Version Command Integration", False, f"Hata: {e}")
                return False
                
            return True
            
        except Exception as e:
            self.log_test("Version System", False, f"Sürüm sistemi hatası: {e}")
            return False
    
    def test_directory_structure(self) -> bool:
        """Dizin yapısı testleri"""
        print("\n🔍 Dizin Yapısı Testleri")
        print("=" * 50)
        
        # package_registry.py'deki get_apps_directory() testi
        try:
            from package_registry import get_apps_directory
            apps_dir = get_apps_directory()
            
            # Dizin oluşturulabilir mi?
            Path(apps_dir).mkdir(parents=True, exist_ok=True)
            self.log_test("Apps Directory Creation", True, f"Dizin: {apps_dir}")
            
            # Dizin yazılabilir mi?
            test_file = Path(apps_dir) / "test.txt"
            test_file.write_text("test")
            test_file.unlink()
            self.log_test("Apps Directory Write", True, "Yazma testi başarılı")
            
            return True
            
        except Exception as e:
            self.log_test("Directory Structure", False, f"Dizin yapısı hatası: {e}")
            return False
    
    def test_manifest_system(self) -> bool:
        """Manifest sistemi testleri"""
        print("\n🔍 Manifest Sistemi Testleri")
        print("=" * 50)
        
        # Geçerli manifest örneği
        valid_manifest = {
            "name": "test-app",
            "version": "1.0.0",
            "language": "python",
            "entry": "main.py",
            "description": "Test uygulaması"
        }
        
        # Geçersiz manifest örneği
        invalid_manifest = {
            "name": "test-app",
            # version eksik
            "language": "python"
            # entry eksik
        }
        
        try:
            from manifest_schema import validate_manifest
            from manifest_validator import validate_manifest_verbose
            
            # Geçerli manifest testi
            is_valid = validate_manifest(valid_manifest)
            if is_valid:
                self.log_test("Valid Manifest Schema", True, "Geçerli manifest doğrulandı")
            else:
                self.log_test("Valid Manifest Schema", False, "Geçerli manifest reddedildi")
                return False
            
            # Geçersiz manifest testi
            is_valid = validate_manifest(invalid_manifest)
            if not is_valid:
                self.log_test("Invalid Manifest Schema", True, "Geçersiz manifest reddedildi")
            else:
                self.log_test("Invalid Manifest Schema", False, "Geçersiz manifest kabul edildi")
                return False
            
            # Detaylı doğrulama testi
            is_valid, errors = validate_manifest_verbose(valid_manifest)
            if is_valid and not errors:
                self.log_test("Detailed Validation", True, "Detaylı doğrulama başarılı")
            else:
                self.log_test("Detailed Validation", False, f"Doğrulama hataları: {errors}")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Manifest System", False, f"Manifest sistemi hatası: {e}")
            return False
    
    def test_package_registry(self) -> bool:
        """Paket kayıt sistemi testleri"""
        print("\n🔍 Paket Kayıt Sistemi Testleri")
        print("=" * 50)
        
        try:
            from package_registry import list_packages, get_manifest, app_exists, get_apps_directory
            
            apps_dir = get_apps_directory()
            
            # Boş liste testi
            packages = list_packages()
            if isinstance(packages, list):
                self.log_test("List Packages Type", True, f"{len(packages)} paket bulundu")
            else:
                self.log_test("List Packages Type", False, f"Yanlış tip: {type(packages)}")
                return False
            
            # Var olmayan uygulama testi
            manifest = get_manifest("nonexistent-app")
            if manifest is None:
                self.log_test("Non-existent App", True, "Var olmayan uygulama None döndürdü")
            else:
                self.log_test("Non-existent App", False, "Var olmayan uygulama None döndürmedi")
                return False
            
            # app_exists testi
            exists = app_exists("nonexistent-app")
            if not exists:
                self.log_test("App Exists Check", True, "Var olmayan uygulama False döndürdü")
            else:
                self.log_test("App Exists Check", False, "Var olmayan uygulama True döndürdü")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Package Registry", False, f"Paket kayıt sistemi hatası: {e}")
            return False
    
    def test_cli_commands(self) -> bool:
        """CLI komutları testleri"""
        print("\n🔍 CLI Komutları Testleri")
        print("=" * 50)
        
        try:
            from cli_commands import handle_version_command, handle_list_command
            
            # Version komutu testi
            try:
                # Mock args objesi oluştur
                class MockArgs:
                    def __init__(self):
                        self.format = 'default'
                
                args = MockArgs()
                handle_version_command(args)
                self.log_test("Version Command", True, "Version komutu çalıştı")
            except Exception as e:
                self.log_test("Version Command", False, f"Version komutu hatası: {e}")
                return False
            
            # List komutu testi
            try:
                # Mock args objesi oluştur
                class MockArgs:
                    def __init__(self):
                        self.format = 'table'
                        self.language = None
                        self.search = None
                
                args = MockArgs()
                handle_list_command(args)
                self.log_test("List Command", True, "List komutu çalıştı")
            except Exception as e:
                self.log_test("List Command", False, f"List komutu hatası: {e}")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("CLI Commands", False, f"CLI komutları hatası: {e}")
            return False
    
    def test_integration(self) -> bool:
        """Entegrasyon testleri"""
        print("\n🔍 Entegrasyon Testleri")
        print("=" * 50)
        
        # Test uygulaması oluştur
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Test uygulaması dizini
                test_app_dir = Path(temp_dir) / "test-app"
                test_app_dir.mkdir()
                
                # Test manifest.json
                manifest = {
                    "name": "test-app",
                    "version": "1.0.0",
                    "language": "python",
                    "entry": "main.py",
                    "description": "Test uygulaması"
                }
                
                manifest_file = test_app_dir / "manifest.json"
                with open(manifest_file, 'w', encoding='utf-8') as f:
                    json.dump(manifest, f, indent=2, ensure_ascii=False)
                
                # Test main.py
                main_file = test_app_dir / "main.py"
                main_file.write_text('print("Hello from test app!")')
                
                # package_registry entegrasyonu
                from package_registry import get_apps_directory
                apps_dir = get_apps_directory()
                target_dir = Path(apps_dir) / "test-app"
                
                # Kopyala
                if target_dir.exists():
                    shutil.rmtree(target_dir)
                shutil.copytree(test_app_dir, target_dir)
                
                # Manifest doğrulama
                from manifest_validator import validate_manifest_verbose
                with open(target_dir / "manifest.json", 'r', encoding='utf-8') as f:
                    loaded_manifest = json.load(f)
                
                is_valid, errors = validate_manifest_verbose(loaded_manifest)
                if is_valid:
                    self.log_test("Integration Manifest Validation", True, "Manifest doğrulandı")
                else:
                    self.log_test("Integration Manifest Validation", False, f"Doğrulama hataları: {errors}")
                    return False
                
                # package_registry entegrasyonu
                from package_registry import get_manifest, app_exists
                manifest = get_manifest("test-app")
                if manifest and manifest["name"] == "test-app":
                    self.log_test("Integration Package Registry", True, "Paket kayıt sistemi çalışıyor")
                else:
                    self.log_test("Integration Package Registry", False, "Paket kayıt sistemi hatası")
                    return False
                
                # app_exists testi
                if app_exists("test-app"):
                    self.log_test("Integration App Exists", True, "Uygulama varlık kontrolü çalışıyor")
                else:
                    self.log_test("Integration App Exists", False, "Uygulama varlık kontrolü hatası")
                    return False
                
                # Temizlik
                if target_dir.exists():
                    shutil.rmtree(target_dir)
                
                return True
                
            except Exception as e:
                self.log_test("Integration Test", False, f"Entegrasyon testi hatası: {e}")
                return False
    
    def test_cli_execution(self) -> bool:
        """CLI çalıştırma testleri"""
        print("\n🔍 CLI Çalıştırma Testleri")
        print("=" * 50)
        
        try:
            # Version komutu
            result = subprocess.run([sys.executable, "main.py", "version"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.log_test("CLI Version Execution", True, "Version komutu başarıyla çalıştı")
            else:
                self.log_test("CLI Version Execution", False, f"Version komutu hatası: {result.stderr}")
                return False
            
            # List komutu
            result = subprocess.run([sys.executable, "main.py", "list"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.log_test("CLI List Execution", True, "List komutu başarıyla çalıştı")
            else:
                self.log_test("CLI List Execution", False, f"List komutu hatası: {result.stderr}")
                return False
            
            return True
            
        except subprocess.TimeoutExpired:
            self.log_test("CLI Execution", False, "CLI komutları zaman aşımı")
            return False
        except Exception as e:
            self.log_test("CLI Execution", False, f"CLI çalıştırma hatası: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Tüm testleri çalıştır"""
        print("🚀 CLAPP Sistem Entegrasyon Testi Başlatılıyor")
        print("=" * 60)
        
        tests = [
            ("Modül Importları", self.test_imports),
            ("Sürüm Sistemi", self.test_version_system),
            ("Dizin Yapısı", self.test_directory_structure),
            ("Manifest Sistemi", self.test_manifest_system),
            ("Paket Kayıt Sistemi", self.test_package_registry),
            ("CLI Komutları", self.test_cli_commands),
            ("Entegrasyon", self.test_integration),
            ("CLI Çalıştırma", self.test_cli_execution)
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
    
    def generate_report(self) -> str:
        """Test raporu oluştur"""
        print("\n" + "=" * 60)
        print("📊 TEST RAPORU")
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
            print(f"\n🎉 TÜM TESTLER BAŞARILI! Sistem tam entegre çalışıyor.")
        else:
            print(f"\n🔧 {failed_tests} test başarısız. Sistem entegrasyonunda sorunlar var.")
        
        return f"Başarı Oranı: {(successful_tests/total_tests*100):.1f}%"

def main():
    """Ana test fonksiyonu"""
    tester = SystemTester()
    results = tester.run_all_tests()
    report = tester.generate_report()
    
    # Sonuçları JSON olarak kaydet
    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "results": results,
            "test_details": tester.test_results,
            "errors": tester.errors,
            "warnings": tester.warnings,
            "summary": report
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detaylı rapor: test_results.json")
    
    # Başarı oranına göre exit code
    total_tests = len(tester.test_results)
    successful_tests = len([r for r in tester.test_results if r["success"]])
    
    if successful_tests == total_tests:
        sys.exit(0)  # Başarılı
    else:
        sys.exit(1)  # Başarısız

if __name__ == "__main__":
    main() 