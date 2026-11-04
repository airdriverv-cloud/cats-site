"""Проверка целостности сайта: картинки на месте, ссылки на источники отвечают.

Запуск: python tools/check-site.py [--no-links]
"""

import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def main():
    src = open(os.path.join(ROOT, "data.js"), encoding="utf-8").read()

    photos = dict(re.findall(r"^(\w+):\['([^']+)'", src, re.M))
    used = re.findall(r"photo:'(\w+)'", src)
    slugs = re.findall(r"slug:'([^']+)'", src)

    errors = []
    print(f"Статей: {len(slugs)}, иллюстраций в PHOTOS: {len(photos)}")

    for key, path in photos.items():
        full = os.path.join(ROOT, path)
        if not os.path.exists(full):
            errors.append(f"нет файла {path} (ключ {key})")
        elif os.path.getsize(full) < 5_000:
            errors.append(f"подозрительно маленький {path}")

    for key in used:
        if key not in photos:
            errors.append(f"статья ссылается на неизвестный ключ фото: {key}")
    unused = [k for k in photos if k not in used]
    if unused:
        print("Не используются на сайте:", ", ".join(unused))

    srcs = set(re.findall(r"'(https://[^']+)'", src))
    srcs |= {"https://www.cats.org.uk/help-and-advice/" + p
             for p in re.findall(r"CP\+'([^']+)'", src)}
    srcs = sorted(srcs)
    print(f"Источников: {len(srcs)}")
    if "--no-links" not in sys.argv:
        for url in srcs:
            try:
                req = urllib.request.Request(url, headers=UA)
                code = urllib.request.urlopen(req, timeout=45).status
                if code != 200:
                    errors.append(f"{code} {url}")
            except Exception as e:  # noqa: BLE001
                errors.append(f"{getattr(e, 'code', e)} {url}")

    if errors:
        print("\nОШИБКИ:")
        for e in errors:
            print(" -", e)
        return 1
    print("\nВсё в порядке.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
