import aiohttp
import json

_API_URL = "https://translate.disroot.org/translate"
_DEFAULT_PARAMS = {
    "format": "text",
    "alternatives": 3,
    "source": "auto",
    "target": "ru",
    "api_key": ""  # You can add an API key here if needed
}

async def translate(text: str, lang: str) -> str:
    """
    Асинхронно переводит текст с помощью нового API для перевода.

    :param text: текст для перевода
    :param lang: направление перевода, например "en-ru"
    :return: переведённый текст
    """
    params = _DEFAULT_PARAMS.copy()
    source_lang, target_lang = lang.split("-")  # Assumes the `lang` format is like "en-ru"
    params.update({"q": text, "source": source_lang, "target": target_lang})

    async with aiohttp.ClientSession() as session:
        async with session.post(_API_URL, json=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data["translatedText"]
            raise Exception(f"Ошибка API, статус: {resp.status}")
