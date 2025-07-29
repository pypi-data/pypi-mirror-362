import os
import sys
import json
import subprocess
import importlib
from pathlib import Path
from package_registry import get_manifest, app_exists, get_apps_directory

def check_dependencies(manifest):
    """
    Manifest'te belirtilen bağımlılıkları kontrol eder.
    
    Args:
        manifest (dict): Kontrol edilecek manifest
        
    Returns:
        list: Eksik bağımlılıkların listesi
    """
    missing_dependencies = []
    
    # Bağımlılık listesini al
    dependencies = manifest.get('dependencies', [])
    
    if not dependencies:
        return missing_dependencies
    
    # Her bağımlılığı kontrol et
    for dependency in dependencies:
        if not app_exists(dependency):
            missing_dependencies.append(dependency)
    
    return missing_dependencies

def check_app_dependencies(app_name):
    """
    Belirtilen uygulamanın bağımlılıklarını kontrol eder.
    
    Args:
        app_name (str): Kontrol edilecek uygulama adı
        
    Returns:
        tuple: (missing_dependencies: list, dependency_info: dict)
    """
    # Uygulama manifest'ini al
    manifest = get_manifest(app_name)
    
    if not manifest:
        return [], {"error": f"Uygulama '{app_name}' bulunamadı"}
    
    # Bağımlılıkları kontrol et
    missing_dependencies = check_dependencies(manifest)
    
    # Bağımlılık bilgilerini topla
    dependency_info = {
        "app_name": app_name,
        "total_dependencies": len(manifest.get('dependencies', [])),
        "missing_count": len(missing_dependencies),
        "satisfied_count": len(manifest.get('dependencies', [])) - len(missing_dependencies),
        "dependencies": manifest.get('dependencies', []),
        "missing_dependencies": missing_dependencies
    }
    
    return missing_dependencies, dependency_info

def get_dependency_tree(app_name, visited=None):
    """
    Uygulamanın bağımlılık ağacını oluşturur.
    
    Args:
        app_name (str): Uygulama adı
        visited (set): Ziyaret edilen uygulamalar (döngüsel bağımlılık kontrolü için)
        
    Returns:
        dict: Bağımlılık ağacı
    """
    if visited is None:
        visited = set()
    
    # Döngüsel bağımlılık kontrolü
    if app_name in visited:
        return {"error": f"Döngüsel bağımlılık tespit edildi: {app_name}"}
    
    visited.add(app_name)
    
    # Uygulama manifest'ini al
    manifest = get_manifest(app_name)
    
    if not manifest:
        return {"error": f"Uygulama '{app_name}' bulunamadı"}
    
    # Bağımlılık ağacını oluştur
    tree = {
        "name": app_name,
        "version": manifest.get('version', '0.0.0'),
        "language": manifest.get('language', 'unknown'),
        "dependencies": [],
        "missing_dependencies": []
    }
    
    dependencies = manifest.get('dependencies', [])
    
    for dep in dependencies:
        if app_exists(dep):
            # Bağımlılığın kendi ağacını al
            dep_tree = get_dependency_tree(dep, visited.copy())
            tree["dependencies"].append(dep_tree)
        else:
            tree["missing_dependencies"].append(dep)
    
    return tree

def resolve_all_dependencies(app_name):
    """
    Uygulamanın tüm bağımlılıklarını çözümler (derin analiz).
    
    Args:
        app_name (str): Uygulama adı
        
    Returns:
        dict: Çözümleme sonuçları
    """
    result = {
        "app_name": app_name,
        "status": "unknown",
        "all_dependencies": set(),
        "missing_dependencies": set(),
        "dependency_tree": None,
        "circular_dependencies": [],
        "resolution_order": []
    }
    
    # Bağımlılık ağacını al
    tree = get_dependency_tree(app_name)
    result["dependency_tree"] = tree
    
    if "error" in tree:
        result["status"] = "error"
        return result
    
    # Tüm bağımlılıkları topla
    def collect_dependencies(node, all_deps, missing_deps):
        if "dependencies" in node:
            for dep in node["dependencies"]:
                all_deps.add(dep["name"])
                collect_dependencies(dep, all_deps, missing_deps)
        
        if "missing_dependencies" in node:
            for missing in node["missing_dependencies"]:
                missing_deps.add(missing)
    
    collect_dependencies(tree, result["all_dependencies"], result["missing_dependencies"])
    
    # Durum belirleme
    if result["missing_dependencies"]:
        result["status"] = "missing_dependencies"
    else:
        result["status"] = "resolved"
    
    # Çözümleme sırası (topological sort benzeri)
    result["resolution_order"] = list(result["all_dependencies"])
    
    return result

def get_dependency_report(app_name):
    """
    Bağımlılık raporu oluşturur.
    
    Args:
        app_name (str): Uygulama adı
        
    Returns:
        str: Formatlanmış bağımlılık raporu
    """
    missing_deps, dep_info = check_app_dependencies(app_name)
    
    if "error" in dep_info:
        return f"❌ Hata: {dep_info['error']}"
    
    report = f"📦 {app_name} Bağımlılık Raporu\n"
    report += "=" * 40 + "\n"
    
    if dep_info["total_dependencies"] == 0:
        report += "✅ Bu uygulama hiçbir bağımlılığa sahip değil.\n"
        return report
    
    report += f"📊 Toplam Bağımlılık: {dep_info['total_dependencies']}\n"
    report += f"✅ Karşılanan: {dep_info['satisfied_count']}\n"
    report += f"❌ Eksik: {dep_info['missing_count']}\n\n"
    
    if missing_deps:
        report += "🚨 Eksik Bağımlılıklar:\n"
        for dep in missing_deps:
            report += f"  - {dep}\n"
        report += "\n"
    
    if dep_info["satisfied_count"] > 0:
        satisfied_deps = [dep for dep in dep_info["dependencies"] if dep not in missing_deps]
        report += "✅ Karşılanan Bağımlılıklar:\n"
        for dep in satisfied_deps:
            dep_manifest = get_manifest(dep)
            version = dep_manifest.get('version', '0.0.0') if dep_manifest else 'bilinmiyor'
            report += f"  - {dep} (v{version})\n"
        report += "\n"
    
    return report

def check_system_dependencies():
    """
    Sistemdeki tüm uygulamaların bağımlılıklarını kontrol eder.
    
    Returns:
        dict: Sistem geneli bağımlılık durumu
    """
    from package_registry import list_packages
    
    packages = list_packages()
    system_report = {
        "total_apps": len(packages),
        "apps_with_dependencies": 0,
        "apps_with_missing_dependencies": 0,
        "total_dependencies": 0,
        "total_missing": 0,
        "problematic_apps": []
    }
    
    for package in packages:
        app_name = package['name']
        missing_deps, dep_info = check_app_dependencies(app_name)
        
        if dep_info["total_dependencies"] > 0:
            system_report["apps_with_dependencies"] += 1
            system_report["total_dependencies"] += dep_info["total_dependencies"]
        
        if missing_deps:
            system_report["apps_with_missing_dependencies"] += 1
            system_report["total_missing"] += len(missing_deps)
            system_report["problematic_apps"].append({
                "name": app_name,
                "missing_dependencies": missing_deps
            })
    
    return system_report

def get_system_dependency_report():
    """
    Sistem geneli bağımlılık raporu oluşturur.
    
    Returns:
        str: Formatlanmış sistem raporu
    """
    report_data = check_system_dependencies()
    
    report = "🏢 Sistem Bağımlılık Raporu\n"
    report += "=" * 40 + "\n"
    
    report += f"📱 Toplam Uygulama: {report_data['total_apps']}\n"
    report += f"🔗 Bağımlılığa Sahip: {report_data['apps_with_dependencies']}\n"
    report += f"⚠️  Eksik Bağımlılığa Sahip: {report_data['apps_with_missing_dependencies']}\n"
    report += f"📊 Toplam Bağımlılık: {report_data['total_dependencies']}\n"
    report += f"❌ Toplam Eksik: {report_data['total_missing']}\n\n"
    
    if report_data['problematic_apps']:
        report += "🚨 Sorunlu Uygulamalar:\n"
        for app in report_data['problematic_apps']:
            report += f"  📦 {app['name']}:\n"
            for dep in app['missing_dependencies']:
                report += f"    - {dep}\n"
        report += "\n"
    else:
        report += "✅ Tüm bağımlılıklar karşılanmış!\n"
    
    return report

def check_and_install_python_dependencies(app_path):
    """
    Python uygulamasının bağımlılıklarını kontrol eder ve eksik olanları kurar.
    
    Args:
        app_path (str): Uygulama dizini
        
    Returns:
        tuple: (success: bool, message: str, missing_packages: list)
    """
    missing_packages = []
    
    # Manifest dosyasını kontrol et
    manifest_path = Path(app_path) / "manifest.json"
    if not manifest_path.exists():
        return False, "Manifest dosyası bulunamadı", []
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except Exception as e:
        return False, f"Manifest dosyası okunamadı: {e}", []
    
    # Sadece Python uygulamaları için
    if manifest.get('language') != 'python':
        return True, "Python uygulaması değil", []
    
    # 1. İlk olarak inline dependencies kontrol et
    dependencies = manifest.get('dependencies', [])
    for pkg in dependencies:
        try:
            importlib.import_module(pkg)
        except ImportError:
            missing_packages.append(pkg)
            try:
                print(f"📦 {pkg} kuruluyor...")
                result = subprocess.run([sys.executable, "-m", "pip", "install", pkg], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    print(f"✅ {pkg} başarıyla kuruldu")
                else:
                    print(f"❌ {pkg} kurulumu başarısız: {result.stderr}")
            except Exception as e:
                print(f"❌ {pkg} kurulum hatası: {e}")
    
    # 2. requirements.txt dosyasını kontrol et (fallback)
    req_txt_path = Path(app_path) / "requirements.txt"
    if req_txt_path.exists() and missing_packages:
        try:
            print(f"📦 requirements.txt dosyasından bağımlılıklar kuruluyor...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_txt_path)], 
                                  capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                print("✅ requirements.txt bağımlılıkları kuruldu")
            else:
                print(f"❌ requirements.txt kurulum hatası: {result.stderr}")
        except Exception as e:
            print(f"❌ requirements.txt kurulum hatası: {e}")
    
    if missing_packages:
        return True, f"{len(missing_packages)} bağımlılık kuruldu", missing_packages
    else:
        return True, "Tüm bağımlılıklar zaten kurulu", []

def check_and_install_lua_dependencies(app_path):
    """
    Lua uygulamasının bağımlılıklarını kontrol eder ve eksik olanları kurar.
    
    Args:
        app_path (str): Uygulama dizini
        
    Returns:
        tuple: (success: bool, message: str, missing_packages: list)
    """
    missing_packages = []
    
    # Manifest dosyasını kontrol et
    manifest_path = Path(app_path) / "manifest.json"
    if not manifest_path.exists():
        return False, "Manifest dosyası bulunamadı", []
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except Exception as e:
        return False, f"Manifest dosyası okunamadı: {e}", []
    
    # Sadece Lua uygulamaları için
    if manifest.get('language') != 'lua':
        return True, "Lua uygulaması değil", []
    
    # Lua bağımlılıklarını kontrol et
    dependencies = manifest.get('dependencies', [])
    for pkg in dependencies:
        try:
            result = subprocess.run(["luarocks", "show", pkg], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                missing_packages.append(pkg)
                try:
                    print(f"🪨 {pkg} kuruluyor...")
                    result = subprocess.run(["luarocks", "install", pkg], 
                                          capture_output=True, text=True, timeout=60)
                    if result.returncode == 0:
                        print(f"✅ {pkg} başarıyla kuruldu")
                    else:
                        print(f"❌ {pkg} kurulumu başarısız: {result.stderr}")
                except Exception as e:
                    print(f"❌ {pkg} kurulum hatası: {e}")
        except Exception as e:
            print(f"❌ {pkg} kontrol hatası: {e}")
    
    if missing_packages:
        return True, f"{len(missing_packages)} Lua bağımlılığı kuruldu", missing_packages
    else:
        return True, "Tüm Lua bağımlılıkları zaten kurulu", []

def check_engine_availability(app_path):
    """
    Uygulamanın gerekli motor/framework'ünün kurulu olup olmadığını kontrol eder.
    
    Args:
        app_path (str): Uygulama dizini
        
    Returns:
        tuple: (available: bool, message: str, engine_info: dict)
    """
    # Manifest dosyasını kontrol et
    manifest_path = Path(app_path) / "manifest.json"
    if not manifest_path.exists():
        return False, "Manifest dosyası bulunamadı", {}
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except Exception as e:
        return False, f"Manifest dosyası okunamadı: {e}", {}
    
    # Engine bilgisi yoksa
    if "engine" not in manifest:
        return True, "Engine gereksinimi yok", {}
    
    engine = manifest["engine"]
    language = manifest.get("language", "unknown")
    
    engine_info = {
        "name": engine,
        "language": language,
        "required": True
    }
    
    if language == "python":
        try:
            importlib.import_module(engine)
            engine_info["available"] = True
            return True, f"Python motoru '{engine}' kurulu", engine_info
        except ImportError:
            engine_info["available"] = False
            return False, f"Python motoru '{engine}' eksik", engine_info
    
    elif language == "lua":
        try:
            result = subprocess.run(["luarocks", "show", engine], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                engine_info["available"] = True
                return True, f"Lua modülü '{engine}' kurulu", engine_info
            else:
                engine_info["available"] = False
                return False, f"Lua modülü '{engine}' eksik", engine_info
        except Exception as e:
            engine_info["available"] = False
            return False, f"Lua modülü '{engine}' kontrol edilemedi: {e}", engine_info
    
    return True, "Bilinmeyen dil türü", engine_info

def get_enhanced_system_dependency_report():
    """
    Gelişmiş sistem bağımlılık raporu oluşturur.
    
    Returns:
        str: Gelişmiş sistem raporu
    """
    report = "🔍 Gelişmiş Sistem Bağımlılık Raporu\n"
    report += "=" * 50 + "\n"
    
    # Python sürümü
    report += f"🐍 Python Sürümü: {sys.version}\n"
    
    # Pip durumu
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            report += f"📦 Pip: {result.stdout.strip()}\n"
        else:
            report += "❌ Pip: Kurulu değil\n"
    except Exception:
        report += "❌ Pip: Erişilemiyor\n"
    
    # Lua/Luarocks durumu
    try:
        result = subprocess.run(["lua", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            report += f"🌙 Lua: {result.stdout.strip()}\n"
        else:
            report += "❌ Lua: Kurulu değil\n"
    except Exception:
        report += "❌ Lua: Erişilemiyor\n"
    
    try:
        result = subprocess.run(["luarocks", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            report += f"🪨 Luarocks: {result.stdout.strip()}\n"
        else:
            report += "❌ Luarocks: Kurulu değil\n"
    except Exception:
        report += "❌ Luarocks: Erişilemiyor\n"
    
    return report

if __name__ == "__main__":
    # Test için örnek kullanım
    print("Sistem bağımlılık raporu:")
    print(get_system_dependency_report()) 