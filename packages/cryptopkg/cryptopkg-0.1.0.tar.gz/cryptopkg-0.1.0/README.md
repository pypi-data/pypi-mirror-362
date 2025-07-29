# cryptopkg

Универсальный пакет для симметричного шифрования (AES-GCM) и хеширования (SHA256).

## Установка зависимостей

```
pip install pycryptodome
```

## Использование

```python
from cryptopkg import CryptoLogic

key = b'some_32_byte_key________________'  # 32 байта для AES-256
crypto = CryptoLogic(key)

# Шифрование
enc = crypto.encrypt('секретное сообщение')
print(enc)

# Дешифрование
plain = crypto.decrypt(enc)
print(plain)

# Хеширование
h = CryptoLogic.generate_hash('some data')
print(h)
```

## Важно
- Ключ должен быть 16, 24 или 32 байта (AES-128/192/256).
- Не храните ключи в коде, используйте переменные окружения.
