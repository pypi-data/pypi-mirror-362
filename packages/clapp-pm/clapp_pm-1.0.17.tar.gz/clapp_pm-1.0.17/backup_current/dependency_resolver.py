import os
from package_registry import get_manifest, app_exists

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

if __name__ == "__main__":
    # Test için örnek kullanım
    print("Sistem bağımlılık raporu:")
    print(get_system_dependency_report()) 