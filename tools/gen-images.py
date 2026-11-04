"""Генерация иллюстраций для сайта «Мир кошек».

Источник — публичный Pollinations (модель sana), без ключа.
Лимит: 1 изображение в 45 секунд на IP, поэтому скрипт работает медленно.
Водяной знак сервиса в правом нижнем углу обрезается.

Запуск: python tools/gen-images.py [ключ ...]
"""

import io
import os
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "img")
W, H = 1024, 768
CROP = 0.07  # доля высоты, срезаемая снизу вместе с водяным знаком

ITEMS = [
    (
        "kitten",
        "photograph of a ginger tabby kitten sitting on a light wooden floor in a bright living room, "
        "big curious eyes, soft window light, shallow depth of field, 50mm lens, photorealistic, fine fur detail, no text",
        11,
    ),
    (
        "bed",
        "photograph of a grey tabby cat curled up asleep on white bed sheets, warm morning sunlight, "
        "cozy bedroom, photorealistic, shallow depth of field, no text",
        12,
    ),
    (
        "tree",
        "photograph of a cat sleeping on a wooden cat tree tower next to a window in a living room, "
        "photorealistic, natural light, shallow depth of field, no text",
        13,
    ),
    (
        "together",
        "two cats, a ginger tabby and a grey cat, sitting side by side facing the camera on a wooden floor, "
        "full bodies, studio portrait, photorealistic, no text",
        14,
    ),
    (
        "food",
        "a cat eating dry kibble from a white ceramic bowl on a wooden floor, head lowered into the bowl, "
        "side view, photorealistic, natural light, no text",
        15,
    ),
    (
        "grooming",
        "a fluffy grey cat lies on a light sofa while a human hand brushes its back with a metal grooming brush, "
        "the whole cat is in the frame, living room, photorealistic, soft daylight, no text",
        116,
    ),
    (
        "play",
        "photograph of a kitten playing with a feather wand toy, paws raised, living room, "
        "photorealistic, natural light, slight motion blur, no text",
        17,
    ),
    (
        "window",
        "photograph of a black and white cat sitting on a windowsill looking outside, seen from behind, "
        "daylight, photorealistic, no text",
        18,
    ),
    (
        "litter",
        "top-down photograph of a white plastic cat litter tray filled with grey clumping litter, a scoop lying "
        "beside it on tiled bathroom floor, product photo, photorealistic, no text",
        19,
    ),
    (
        "vet",
        "photograph of a veterinarian in a white coat listening to the chest of a cat with a stethoscope, the cat "
        "lies on an examination table, bright clinic, photorealistic, no text",
        20,
    ),
]


def build_url(prompt, seed):
    q = urllib.parse.quote(prompt)
    return (
        f"https://image.pollinations.ai/prompt/{q}"
        f"?width={W}&height={H}&nologo=true&model=sana&seed={seed}"
    )


def fetch(url):
    last = None
    for attempt in range(8):
        try:
            with urllib.request.urlopen(url, timeout=240) as r:
                data = r.read()
            if len(data) < 10_000:
                raise ValueError(f"слишком маленький ответ: {len(data)} байт")
            return data
        except urllib.error.HTTPError as e:
            body = e.read()[:400].decode("utf-8", "replace")
            last = f"HTTP {e.code}: {body}"
            # 402 — лимит по IP, ждём дольше; 503 — сервис занят
            wait = 50 if e.code == 402 else 20
        except Exception as e:  # noqa: BLE001
            last = str(e)
            wait = 20
        print(f"    повтор ({attempt + 1}/8): {last}", flush=True)
        time.sleep(wait)
    raise RuntimeError(f"не удалось получить изображение: {last}")


def process(key, prompt, seed):
    path = os.path.join(OUT, key + ".jpg")
    print(f"[{key}] генерирую…", flush=True)
    data = fetch(build_url(prompt, seed))
    img = Image.open(io.BytesIO(data)).convert("RGB")
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    img = img.crop((0, 0, W, int(H * (1 - CROP))))
    img.save(path, "JPEG", quality=86, optimize=True, progressive=True)
    print(f"[{key}] готово — {os.path.relpath(path, ROOT)}, {os.path.getsize(path) // 1024} КБ", flush=True)


def main():
    keys = set(sys.argv[1:])
    items = [i for i in ITEMS if not keys or i[0] in keys]
    os.makedirs(OUT, exist_ok=True)
    for n, (key, prompt, seed) in enumerate(items):
        process(key, prompt, seed)
        if n < len(items) - 1:
            # держим паузу между запросами, чтобы не упереться в лимит 45 с
            time.sleep(50)


if __name__ == "__main__":
    main()
