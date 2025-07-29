# PyPI Upload Talimatları

Bu dosya clapp paketini PyPI'ya yükleme sürecini açıklar.

## 1. Gerekli Araçları Yükle

```bash
pip install --upgrade pip
pip install --upgrade build
pip install --upgrade twine
```

## 2. Paket Build Et

```bash
# Önceki build dosyalarını temizle
rm -rf dist/ build/ *.egg-info/

# Yeni build oluştur
python -m build --sdist --wheel
```

## 3. Build Kontrolü

```bash
# Build edilen dosyaları kontrol et
ls -la dist/

# Paket içeriğini kontrol et
python -m twine check dist/*
```

## 4. Test PyPI'ya Yükle (Opsiyonel)

```bash
# Test PyPI hesabı oluştur: https://test.pypi.org/account/register/
# API token oluştur: https://test.pypi.org/manage/account/token/

# Test PyPI'ya yükle
python -m twine upload --repository testpypi dist/*

# Test PyPI'dan yükle ve test et
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ clapp
```

## 5. Gerçek PyPI'ya Yükle

```bash
# PyPI hesabı oluştur: https://pypi.org/account/register/
# API token oluştur: https://pypi.org/manage/account/token/

# Gerçek PyPI'ya yükle
python -m twine upload dist/*
```

## 6. PyPI Konfigürasyonu

### ~/.pypirc dosyası oluştur:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR_API_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TEST_API_TOKEN_HERE
```

## 7. Güvenlik Notları

- ✅ API token kullan, şifre kullanma
- ✅ Token'ları güvenli yerde sakla
- ✅ Token'lara sadece gerekli izinleri ver
- ✅ .pypirc dosyasını .gitignore'a ekle

## 8. Yükleme Sonrası Test

```bash
# Yeni bir virtual environment oluştur
python -m venv test_env
source test_env/bin/activate  # Linux/Mac
# test_env\Scripts\activate  # Windows

# PyPI'dan yükle
pip install clapp

# Test et
clapp --version
clapp list
clapp gui
```

## 9. Güncelleme Süreci

```bash
# Version'u güncelle
# version.py ve version.json dosyalarını güncelle

# Yeni build oluştur
python -m build --sdist --wheel

# PyPI'ya yükle
python -m twine upload dist/*
```

## 10. Yaygın Sorunlar ve Çözümleri

### Build Hataları:
- `pip install --upgrade setuptools wheel build`
- `rm -rf dist/ build/ *.egg-info/`
- Yeniden build et

### Upload Hataları:
- API token'ı kontrol et
- Paket adının mevcut olup olmadığını kontrol et
- Version numarasının benzersiz olduğunu kontrol et

### Test Hataları:
- Dependency'lerin doğru yüklendiğini kontrol et
- Entry point'lerin çalıştığını kontrol et
- Import hatalarını kontrol et

## 11. Monitoring

PyPI'da paket sayfasını kontrol et:
- https://pypi.org/project/clapp/
- İndirme istatistikleri
- Kullanıcı geri bildirimleri
- Issue'lar ve bug raporları

## 12. Otomasyonlar

### GitHub Actions ile otomatik PyPI upload:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        twine upload dist/*
```

## 13. Başarı Kontrolü

✅ Paket PyPI'da görünüyor
✅ `pip install clapp` çalışıyor
✅ `clapp --version` çalışıyor
✅ `clapp gui` çalışıyor
✅ Tüm komutlar çalışıyor
✅ Dependencies doğru yükleniyor 