"""링크 공유용 OG 이미지 편집 스크립트 (OpenAI 이미지 편집 API).

사용법:  python gen_og.py <캡처 PNG>
실제 사이트 히어로를 1200×630으로 캡처한 이미지를 입력으로 넣으면, 이미지 모델이 OG 카드로 다듬어
assets/og-image-raw.png (1536×1024)로 저장합니다. 최종 1200×630 자르기는 브라우저 캡처로 따로 합니다.
.env 의 OPENAI_API_KEY 를 사용합니다.
"""
import base64
import json
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path

from gen_assets import MODEL, ROOT, load_key

PROMPT = (
    "Polish this website hero screenshot into a clean social link-preview (Open Graph) image for the "
    "'App Design' team at Kigle. Keep the exact same design: the colorful 'kigle' logo, the large bold "
    "black headline 'App Design' whose i-dot is a small red diamond, and the Korean slogan "
    "'신속한 실행 정확한 디자인' directly under it. Reproduce every letter exactly, same font weight, "
    "same spelling, centered, no added or removed words. Keep the abstract corner shapes (coral red #FF3B40 "
    "rounded diamonds and big circle, light gray circles and pill) and the faint dot pattern, but make the "
    "composition balanced and calm so the text is clearly readable at small sizes; no shape may touch the text. "
    "The output canvas is 3:2: keep the logo, headline and slogan inside the central horizontal band "
    "(middle half of the height) and extend the background and corner shapes naturally above and below. "
    "Flat vector style, solid fills, white background, no extra text, no watermark."
)


def edit(src: Path, key: str) -> bytes:
    boundary = uuid.uuid4().hex
    parts = []

    def field(name, value):
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())

    for k, v in {"model": MODEL, "prompt": PROMPT, "size": "1536x1024", "quality": "high",
                 "output_format": "png", "n": "1"}.items():
        field(k, v)
    parts.append(
        f'--{boundary}\r\nContent-Disposition: form-data; name="image[]"; filename="{src.name}"\r\n'
        "Content-Type: image/png\r\n\r\n".encode() + src.read_bytes() + b"\r\n"
    )
    parts.append(f"--{boundary}--\r\n".encode())
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/edits",
        data=b"".join(parts),
        headers={"Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as res:
            data = json.load(res)
    except urllib.error.HTTPError as e:
        sys.exit(f"실패 HTTP {e.code} {e.read().decode(errors='replace')[:400]}")
    return base64.b64decode(data["data"][0]["b64_json"])


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    out = ROOT / "assets" / "og-image-raw.png"
    out.write_bytes(edit(Path(sys.argv[1]), load_key()))
    print(f"저장 {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
