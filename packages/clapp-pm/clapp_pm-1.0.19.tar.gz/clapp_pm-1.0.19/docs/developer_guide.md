# clapp Geliştirici Rehberi

Bu rehber, clapp için uygulama geliştirmek isteyen geliştiriciler için hazırlanmıştır.

## 📋 İçindekiler

1. [Başlangıç](#başlangıç)
2. [Manifest Dosyası](#manifest-dosyası)
3. [Desteklenen Diller](#desteklenen-diller)
4. [Uygulama Yapısı](#uygulama-yapısı)
5. [Bağımlılık Yönetimi](#bağımlılık-yönetimi)
6. [Test ve Doğrulama](#test-ve-doğrulama)
7. [Yayınlama](#yayınlama)
8. [En İyi Uygulamalar](#en-iyi-uygulamalar)

## 🚀 Başlangıç

### Yeni Uygulama Oluşturma

Yeni bir clapp uygulaması oluşturmak için:

```bash
# Python uygulaması oluştur
clapp new python my-app

# Lua uygulaması oluştur
clapp new lua my-lua-app

# Diğer diller için
clapp new dart my-dart-app
clapp new go my-go-app
clapp new rust my-rust-app
```

### Manuel Oluşturma

Eğer `clapp new` komutu henüz mevcut değilse, manuel olarak oluşturabilirsiniz:

1. Yeni bir klasör oluşturun
2. `manifest.json` dosyası ekleyin
3. Giriş dosyanızı oluşturun
4. Gerekli dosyaları ekleyin

## 📄 Manifest Dosyası

Her clapp uygulaması bir `manifest.json` dosyasına sahip olmalıdır.

### Zorunlu Alanlar

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "language": "python",
  "entry": "main.py"
}
```

### Opsiyonel Alanlar

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "language": "python",
  "entry": "main.py",
  "description": "Uygulama açıklaması",
  "author": "Geliştirici Adı",
  "license": "MIT",
  "dependencies": ["other-app"],
  "tags": ["utility", "tool"],
  "category": "productivity"
}
```

### Alan Açıklamaları

- **name**: Uygulama adı (benzersiz olmalı)
- **version**: Sürüm numarası (semantic versioning önerilir)
- **language**: Programlama dili (python, lua, dart, go, rust, vb.)
- **entry**: Giriş dosyası (uygulamanın başlangıç noktası)
- **description**: Uygulama açıklaması
- **author**: Geliştirici bilgisi
- **license**: Lisans bilgisi
- **dependencies**: Bağımlılık listesi (diğer clapp uygulamaları)
- **tags**: Etiketler (arama için)
- **category**: Kategori (store, productivity, game, vb.)

## 🌐 Desteklenen Diller

### Python
- **Dosya uzantısı**: `.py`
- **Giriş noktası**: `python main.py`
- **Örnek**: `main.py`

### Lua
- **Dosya uzantısı**: `.lua`
- **Giriş noktası**: `lua main.lua`
- **Örnek**: `main.lua`

### Dart
- **Dosya uzantısı**: `.dart`
- **Giriş noktası**: `dart main.dart`
- **Örnek**: `main.dart`

### Go
- **Dosya uzantısı**: `.go`
- **Giriş noktası**: `go run main.go`
- **Örnek**: `main.go`

### Rust
- **Dosya uzantısı**: `.rs`
- **Giriş noktası**: `cargo run`
- **Örnek**: `Cargo.toml` + `src/main.rs`

### Node.js
- **Dosya uzantısı**: `.js`
- **Giriş noktası**: `node main.js`
- **Örnek**: `main.js`

### Bash
- **Dosya uzantısı**: `.sh`
- **Giriş noktası**: `bash main.sh`
- **Örnek**: `main.sh`

### Perl
- **Dosya uzantısı**: `.pl`
- **Giriş noktası**: `perl main.pl`
- **Örnek**: `main.pl`

### Ruby
- **Dosya uzantısı**: `.rb`
- **Giriş noktası**: `ruby main.rb`
- **Örnek**: `main.rb`

### PHP
- **Dosya uzantısı**: `.php`
- **Giriş noktası**: `php main.php`
- **Örnek**: `main.php`

## 📁 Uygulama Yapısı

### Temel Yapı

```
my-app/
├── manifest.json      # Zorunlu
├── main.py           # Giriş dosyası (manifest'te belirtilen)
├── README.md         # Opsiyonel
├── requirements.txt  # Python bağımlılıkları (opsiyonel)
└── assets/           # Statik dosyalar (opsiyonel)
    ├── images/
    └── data/
```

### Örnek Python Uygulaması

**manifest.json:**
```json
{
  "name": "hello-world",
  "version": "1.0.0",
  "language": "python",
  "entry": "main.py",
  "description": "Basit bir Hello World uygulaması",
  "author": "Geliştirici",
  "tags": ["example", "hello"]
}
```

**main.py:**
```python
#!/usr/bin/env python3

def main():
    print("Merhaba Dünya!")
    print("Bu bir clapp uygulamasıdır.")

if __name__ == "__main__":
    main()
```

### Örnek Lua Uygulaması

**manifest.json:**
```json
{
  "name": "lua-calculator",
  "version": "1.0.0",
  "language": "lua",
  "entry": "main.lua",
  "description": "Basit hesap makinesi",
  "tags": ["calculator", "math"]
}
```

**main.lua:**
```lua
#!/usr/bin/env lua

function main()
    print("Lua Hesap Makinesi")
    print("2 + 2 = " .. (2 + 2))
end

main()
```

## 🔗 Bağımlılık Yönetimi

### clapp Bağımlılıkları

Manifest dosyasında diğer clapp uygulamalarını bağımlılık olarak belirtebilirsiniz:

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "language": "python",
  "entry": "main.py",
  "dependencies": ["database-app", "auth-app"]
}
```

### Sistem Bağımlılıkları

Her dil için sistem bağımlılıkları farklı şekilde yönetilir:

#### Python
- `requirements.txt` dosyası kullanın
- `pip install -r requirements.txt` otomatik çalışır

#### Node.js
- `package.json` dosyası kullanın
- `npm install` otomatik çalışır

#### Rust
- `Cargo.toml` dosyası kullanın
- `cargo build` otomatik çalışır

### Bağımlılık Kontrolü

```bash
# Uygulama bağımlılıklarını kontrol et
clapp dependency check my-app

# Bağımlılık ağacını göster
clapp dependency tree my-app
```

## 🧪 Test ve Doğrulama

### Uygulama Doğrulama

```bash
# Uygulama klasörünü doğrula
clapp validate ./my-app
```

### Test Çalıştırma

```bash
# Uygulamayı test et
clapp run my-app
```

### Bağımlılık Testi

```bash
# Bağımlılıkları test et
clapp dependency check my-app
```

## 📦 Yayınlama

### Yerel Test

```bash
# Uygulamayı yerel olarak test et
clapp install ./my-app
clapp run my-app
```

### Paket Oluşturma

```bash
# Paket oluştur
clapp publish ./my-app
```

### GitHub'a Yükleme

```bash
# GitHub'a otomatik yükle
clapp publish ./my-app --push
```

## ✅ En İyi Uygulamalar

### 1. İsimlendirme
- Uygulama adları küçük harf ve tire kullanın: `my-app`
- Açıklayıcı isimler seçin
- Benzersiz isimler kullanın

### 2. Sürüm Yönetimi
- Semantic versioning kullanın: `1.0.0`
- Her değişiklikte sürüm artırın
- CHANGELOG.md dosyası ekleyin

### 3. Dokümantasyon
- README.md dosyası ekleyin
- Kullanım örnekleri verin
- API dokümantasyonu ekleyin

### 4. Hata Yönetimi
- Uygun hata mesajları verin
- Graceful degradation sağlayın
- Log dosyaları kullanın

### 5. Güvenlik
- Hassas bilgileri kodlamayın
- Input validation yapın
- Güvenli dosya işlemleri kullanın

### 6. Performans
- Gereksiz bağımlılıklardan kaçının
- Hızlı başlangıç sağlayın
- Bellek kullanımını optimize edin

## 🆘 Yardım

### Hata Ayıklama

```bash
# Sistem durumunu kontrol et
clapp doctor

# Ortam kontrolü
clapp check-env

# Uygulama konumunu bul
clapp where my-app
```

### Destek

- GitHub Issues: [clapp repository](https://github.com/mburakmmm/clapp)
- Dokümantasyon: Bu rehber
- Örnekler: `templates/` klasörü

## 📝 Örnekler

Daha fazla örnek için `templates/` klasörünü inceleyin:

- `templates/python/` - Python örnekleri
- `templates/lua/` - Lua örnekleri
- `templates/dart/` - Dart örnekleri
- `templates/go/` - Go örnekleri
- `templates/rust/` - Rust örnekleri

Her örnek tam çalışan bir uygulama içerir ve kopyalanıp değiştirilebilir. 