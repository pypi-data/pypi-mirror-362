# yatranslator

Асинхронная и простая обёртка для внутреннего API Яндекс Переводчика.

Позволяет быстро переводить текст с помощью асинхронной функции `translate`.

> ⚠️ Используется неофициальный, внутренний API. Работоспособность зависит от Яндекса и не гарантирована.

---

## Установка

pip install yatranslator

---

## Быстрый старт

import asyncio
from yatranslator import translate

async def main():
    text = "Привет, мир!"
    translated = await translate(text, "ru-en")
    print("Перевод:", translated)

asyncio.run(main())

---

## Синтаксис

translated_text = await translate(text: str, lang: str)

* `text`: строка с текстом для перевода
* `lang`: направление перевода (например, `"en-ru"`, `"ru-en"`, `"fr-ru"` и т.д.)
