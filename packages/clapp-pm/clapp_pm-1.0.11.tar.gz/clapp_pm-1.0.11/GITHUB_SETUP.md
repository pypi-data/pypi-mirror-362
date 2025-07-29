# GitHub Repository Kurulum Talimatları

Bu dosya, clapp projesi için GitHub repository'lerinin nasıl kurulacağını açıklar.

## 1. Ana clapp Repository'si

### Adres: https://github.com/mburakmmm/clapp

### Kurulum Adımları:

1. **Repository'yi oluştur:**
   - GitHub'da yeni repository oluştur: `clapp`
   - Public olarak ayarla
   - README.md dosyası ekle

2. **Dosyaları yükle:**
   ```bash
   # Mevcut dizinde git init
   git init
   git add .
   git commit -m "Initial commit - clapp package manager"
   git branch -M main
   git remote add origin https://github.com/mburakmmm/clapp.git
   git push -u origin main
   ```

3. **Yüklenmesi gereken dosyalar:**
   - Tüm Python dosyaları (main.py, gui_*.py, package_*.py, vs.)
   - requirements.txt
   - setup.py
   - README.md (güncellenmiş)
   - LICENSE
   - .gitignore

## 2. clapp-packages Repository'si

### Adres: https://github.com/mburakmmm/clapp-packages

### Kurulum Adımları:

1. **Repository'yi oluştur:**
   - GitHub'da yeni repository oluştur: `clapp-packages`
   - Public olarak ayarla

2. **Dosyaları yükle:**
   ```bash
   # packages-repo-files klasöründeki dosyaları yükle
   cd packages-repo-files
   git init
   git add .
   git commit -m "Initial commit - clapp packages repository"
   git branch -M main
   git remote add origin https://github.com/mburakmmm/clapp-packages.git
   git push -u origin main
   ```

3. **Yüklenmesi gereken dosyalar:**
   - README.md
   - packages.json
   - hello-world/ klasörü (manifest.json, main.py, README.md)

## 3. GitHub Releases Oluşturma

### hello-world paketi için:

1. **Paket dosyasını oluştur:**
   ```bash
   cd packages-repo-files/hello-world
   zip -r hello-world.clapp.zip . -x "*.git*"
   ```

2. **GitHub Release oluştur:**
   - GitHub'da clapp-packages repository'sine git
   - "Releases" sekmesine tıkla
   - "Create a new release" tıkla
   - Tag version: `v1.0.0`
   - Release title: `Hello World v1.0.0`
   - Description: "İlk demo paket - Hello World uygulaması"
   - `hello-world.clapp.zip` dosyasını yükle
   - "Publish release" tıkla

## 4. Doğrulama

### Test etmek için:

1. **GUI'yi çalıştır:**
   ```bash
   python main.py gui
   ```

2. **App Store sekmesine git**
   - Paketler GitHub'dan yüklenmeli
   - hello-world paketi görünmeli
   - Paket detayları açılabilmeli

3. **CLI ile test et:**
   ```bash
   python main.py remote
   ```

## 5. Ek Paketler

Daha fazla paket eklemek için:

1. Yeni paket klasörü oluştur
2. manifest.json, main.py, README.md ekle
3. .clapp.zip dosyası oluştur
4. GitHub Release olarak yükle
5. packages.json dosyasını güncelle

## 6. Güncelleme Süreci

Paket güncellemesi için:

1. Paket sürümünü artır (manifest.json)
2. Yeni .clapp.zip oluştur
3. Yeni GitHub Release oluştur
4. packages.json dosyasını güncelle
5. Git commit ve push

## 7. Önemli Notlar

- ✅ Repository'ler public olmalı
- ✅ packages.json dosyası main branch'te olmalı
- ✅ Release tag'leri semantic versioning kullanmalı (v1.0.0)
- ✅ .clapp.zip dosyaları GitHub Releases'te olmalı
- ✅ Download URL'leri packages.json'da doğru olmalı

## 8. Sorun Giderme

### Yaygın sorunlar:

1. **404 Error**: Repository public değil veya dosya yok
2. **JSON Parse Error**: packages.json formatı hatalı
3. **Download Error**: Release dosyası bulunamıyor
4. **Timeout Error**: İnternet bağlantısı yavaş

### Çözümler:

1. Repository'lerin public olduğundan emin ol
2. JSON formatını doğrula
3. Release URL'lerini kontrol et
4. Timeout süresini artır (gui_store.py) 