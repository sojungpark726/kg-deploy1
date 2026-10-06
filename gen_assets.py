"""App Design 팀 랜딩페이지용 에셋 생성 스크립트 (OpenAI 이미지 API).

사용법:  python gen_assets.py            # 전체 생성
        python gen_assets.py icon-ip    # 특정 에셋만 다시 생성
.env 의 OPENAI_API_KEY 를 사용합니다. 결과는 assets/ 폴더에 PNG로 저장됩니다.
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "assets"
MODEL = os.environ.get("IMAGE_MODEL", "gpt-image-2.5-sunburst")

STYLE = (
    "Flat vector illustration. Clean geometric shapes, solid fills, no outlines, "
    "no heavy gradients, no texture, no 3D. Restrained limited palette: coral red #FF3B40 as the "
    "accent, soft blush #FFD9DA, warm white #FFFFFF, light gray #E8E8ED, charcoal #1D1D1F. "
    "Minimal, modern, precise, generous negative space. "
    "Absolutely no text, no letters, no numbers, no logos, no watermark."
)

ICON = (
    "A single centered icon-style illustration on a fully transparent background, "
    "the subject fills about 75% of the square canvas, consistent with a set of five matching icons. "
)

ASSETS = {
    "hero-wide": dict(
        size="1536x1024",
        background="opaque",
        prompt=(
            "Wide hero background composition for a design team website. Very light warm-white background. "
            "Large bold abstract geometric shapes — a big coral red circle, a half circle, a rounded rectangle "
            "shaped like a phone screen, a small star and a pill shape — arranged dynamically around the edges, "
            "slightly overlapping and partially cropped by the frame, suggesting speed and precision. "
            "Keep the central horizontal band calm and mostly empty so large headline text can sit on top. "
            + STYLE
        ),
    ),
    "hero-tall": dict(
        size="1024x1536",
        background="opaque",
        prompt=(
            "Tall vertical hero background composition for a mobile design team website. Very light warm-white "
            "background. Large bold abstract geometric shapes — a big coral red circle, a half circle, a rounded "
            "rectangle shaped like a phone screen, a small star and a pill shape — clustered in the lower half and "
            "the top corners, partially cropped by the frame. Keep the middle area calm and mostly empty for "
            "large headline text. " + STYLE
        ),
    ),
    "icon-game": dict(
        size="1024x1024",
        background="transparent",
        prompt=ICON
        + "Game UI design and animation: a rounded smartphone game screen showing a cute round character "
        "jumping with curved motion arcs and small keyframe dots, plus a glossy game button. " + STYLE,
    ),
    "icon-ip": dict(
        size="1024x1024",
        background="transparent",
        prompt=ICON
        + "Original character IP design: a cute round mascot creature standing on a sketch sheet, "
        "with a pencil and a few color swatch circles beside it. " + STYLE,
    ),
    "icon-ads": dict(
        size="1024x1024",
        background="transparent",
        prompt=ICON
        + "Mobile app advertising: a smartphone with a pop-up ad card bursting out of the screen, "
        "a big call-to-action pill button and a small megaphone. " + STYLE,
    ),
    "icon-thumbnail": dict(
        size="1024x1024",
        background="transparent",
        prompt=ICON
        + "Video thumbnail design: a wide 16:9 video frame with a bold composition inside (a character "
        "silhouette and a burst shape), a generic rounded play triangle button overlapping its corner. "
        "Not any real platform's logo. " + STYLE,
    ),
    # 2. 핵심가치 아이콘 (업무 아이콘과 같은 플랫 스타일)
    "value-first": dict(
        size="1024x1024",
        background="transparent",
        prompt=ICON
        + "Moving first by understanding intent: a planning brief card with a magnifying glass over it "
        "and a small lightbulb, with a forward-pointing arrow launching from the card. " + STYLE,
    ),
    "value-precise": dict(
        size="1024x1024",
        background="transparent",
        prompt=ICON
        + "Getting it right in one go: a round target with a single arrow landing exactly in the bullseye, "
        "next to a small ruler and alignment guide lines. " + STYLE,
    ),
    "value-ai": dict(
        size="1024x1024",
        background="transparent",
        prompt=ICON
        + "Designing together with AI: a friendly rounded AI assistant chip with sparkle stars, "
        "connected to a neat grid of design component tiles. " + STYLE,
    ),
    "icon-store": dict(
        size="1024x1024",
        background="transparent",
        prompt=ICON
        + "App store listing images: three tall phone-screenshot cards fanned out side by side, "
        "with a row of five rating stars and a download arrow badge. No real store logos. " + STYLE,
    ),
}


def load_key():
    for line in (ROOT / ".env").read_text(encoding="utf-8-sig").splitlines():
        if line.strip().startswith("OPENAI_API_KEY="):
            key = line.split("=", 1)[1].strip().strip('"').strip("'")
            if key:
                return key
    sys.exit("OPENAI_API_KEY 가 .env 에 없습니다.")


def generate(name, spec, key):
    body = {
        "model": MODEL,
        "prompt": spec["prompt"],
        "size": spec["size"],
        "background": spec["background"],
        "quality": "high",
        "output_format": "png",
        "n": 1,
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=300) as res:
                data = json.load(res)
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:  # 분당 이미지 수 제한 → 잠시 후 재시도
                time.sleep(30 * (attempt + 1))
                continue
            return f"{name}: 실패 HTTP {e.code} {e.read().decode(errors='replace')[:400]}"
        except Exception as e:  # noqa: BLE001
            return f"{name}: 실패 {e}"
    path = OUT / f"{name}.png"
    path.write_bytes(base64.b64decode(data["data"][0]["b64_json"]))
    return f"{name}: 저장 {path.relative_to(ROOT)} ({path.stat().st_size // 1024} KB)"


def main():
    OUT.mkdir(exist_ok=True)
    key = load_key()
    names = sys.argv[1:] or list(ASSETS)
    with ThreadPoolExecutor(max_workers=3) as pool:
        for msg in pool.map(lambda n: generate(n, ASSETS[n], key), names):
            print(msg, flush=True)


if __name__ == "__main__":
    main()
