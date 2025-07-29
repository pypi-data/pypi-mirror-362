# clapp Uygulama Dosya Yapısı ve Manifest Rehberi

Bu doküman, clapp paket yöneticisi ile Python ve Lua uygulamalarının nasıl paketlenip çalıştırılabileceğini anlatır.

---

## 1. Genel Klasör Yapısı

Her uygulama, `apps/` klasörü altında kendi adında bir klasöre sahip olmalıdır:

```
apps/
  └── uygulama-adı/
        ├── manifest.json
        ├── main.py         # (Python için)
        └── main.lua        # (Lua için)
```

- **manifest.json**: Uygulamanın tanımını ve çalıştırma bilgisini içerir.
- **main.py** veya **main.lua**: Uygulamanın giriş noktası (entry file).

---

## 2. manifest.json Dosyası

Bu dosya zorunludur ve şu alanları içermelidir:

| Alan         | Tip     | Açıklama                                 | Zorunlu |
|--------------|---------|------------------------------------------|---------|
| name         | string  | Uygulamanın adı                          | Evet    |
| version      | string  | Sürüm                                    | Evet    |
| language     | string  | "python" veya "lua"                      | Evet    |
| entry        | string  | Giriş dosyasının adı (örn: "main.py")    | Evet    |
| description  | string  | Açıklama                                 | Hayır   |
| dependencies | list    | Bağımlı olduğu diğer clapp uygulamaları  | Hayır   |

---

### Python Uygulaması Örneği

**Klasör yapısı:**
```
apps/hello-python/
    ├── manifest.json
    └── main.py
```

**manifest.json:**
```json
{
  "name": "hello-python",
  "version": "1.0.0",
  "language": "python",
  "entry": "main.py",
  "description": "Basit bir Python merhaba dünya uygulaması"
}
```

**main.py:**
```python
print("Merhaba, clapp ile Python dünyası!")
```

---

### Lua Uygulaması Örneği

**Klasör yapısı:**
```
apps/hello-lua/
    ├── manifest.json
    └── main.lua
```

**manifest.json:**
```json
{
  "name": "hello-lua",
  "version": "1.0.0",
  "language": "lua",
  "entry": "main.lua",
  "description": "Basit bir Lua merhaba dünya uygulaması"
}
```

**main.lua:**
```lua
print("Merhaba, clapp ile Lua dünyası!")
```

---

## 3. Dikkat Edilmesi Gerekenler

- **entry** alanı, çalıştırılacak dosyanın adını tam olarak belirtmelidir.
- **language** alanı sadece `"python"` veya `"lua"` olmalıdır (küçük harf).
- Bağımlılıklar (dependencies) başka clapp uygulamalarının adlarını içeren bir liste olabilir.
- Her uygulamanın kendi klasöründe bir adet manifest.json dosyası olmalıdır.
- Ek dosyalar (resim, veri, modül vs.) gerekiyorsa aynı klasöre eklenebilir, ama manifestte sadece ana giriş dosyası belirtilir.

---

## 4. Çalıştırma

Kurulumdan sonra:
```sh
clapp run hello-python
clapp run hello-lua
```
komutlarıyla uygulamalar otomatik olarak ilgili dilde çalıştırılır.

---

Soruların olursa veya örnek bir uygulama oluşturmak istersen, bana ulaşabilirsin! 