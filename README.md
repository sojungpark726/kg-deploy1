# App Design 팀 · 신속한 실행 정확한 디자인

[![App Design 팀 링크 미리보기](assets/web/og-image.png)](https://kg-deploy1-iota.vercel.app/)

키글 앱디자인팀의 미션과 주요 업무, 팀원을 한 페이지에 소개하는 사내 협업 안내 페이지입니다.

**사이트:** https://kg-deploy1-iota.vercel.app/

## 구성

| 파일 | 내용 |
| --- | --- |
| `artifact.html` | 페이지 원본 (Claude 아티팩트로도 게시) |
| `index.html` | 배포용 페이지 (`artifact.html`과 같은 내용에 문서 머리말을 붙인 것) |
| `team-landing-guide.md` | 페이지 구성·연출·수치를 정리한 가이드 |
| `assets/` / `assets/web/` | 이미지 원본 / 웹용 사본 (OG 이미지 `assets/web/og-image.png` 포함) |
| `fonts/` | Pretendard 가변 폰트 |
| `gen_assets.py`, `gen_og.py` | 이미지 생성·OG 이미지 편집 스크립트 (OpenAI 이미지 API, 키는 저장소에 없는 `.env`에서 읽음) |
| `vercel.json` | Vercel 배포 설정 (빌드 없이 `index.html`, `fonts/`, `assets/web/`만 배포) |

## 배포

- **Vercel:** `main` 브랜치에 push하면 자동으로 배포합니다. https://kg-deploy1-iota.vercel.app/
- **Cloudflare Workers:** `npx wrangler deploy`로 직접 배포합니다(`wrangler.jsonc`, `scripts/build-site.mjs`). https://kg-app-design.landing-test.workers.dev
