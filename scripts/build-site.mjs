// 배포용 public/ 폴더 만들기: 페이지에 실제로 쓰는 파일만 복사 (.env·원본 이미지·가이드·스크립트 제외)
// Cloudflare(wrangler.jsonc의 build.command)에서 사용. Windows(cmd)·Linux(sh) 어디서나 동작하도록 Node로 작성
import { cpSync, mkdirSync, rmSync } from 'node:fs';

const OUT = 'public';
rmSync(OUT, { recursive: true, force: true });
mkdirSync(`${OUT}/assets`, { recursive: true });
cpSync('index.html', `${OUT}/index.html`);
cpSync('fonts', `${OUT}/fonts`, { recursive: true });
cpSync('assets/web', `${OUT}/assets/web`, { recursive: true });
console.log('public/ 준비 완료');
