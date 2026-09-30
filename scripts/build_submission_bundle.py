"""Build a submission snapshot without replacing historical GitHub Release assets."""
from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

from build_package import collect_submission_files, ROOT

OUTPUT = ROOT / 'submission'


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    source_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    status = subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=all'], cwd=ROOT, text=True)
    if any(line[3:].replace('\\', '/').split('/')[0] != 'submission' for line in status.splitlines()):
        raise RuntimeError('Commit source changes before building the submission snapshot.')
    OUTPUT.mkdir(exist_ok=True)
    archive = OUTPUT / 'phan-loai-van-ban-naive-bayes-nop-bai.zip'
    files = collect_submission_files()
    if not any(p.relative_to(ROOT).as_posix() == '.github/workflows/ci.yml' for p in files):
        raise RuntimeError('CI workflow is missing from the submission.')
    entries = []
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as package:
        for path in files:
            name = path.relative_to(ROOT).as_posix()
            data = path.read_bytes()
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            package.writestr(info, data)
            entries.append({'path': name, 'size_bytes': len(data), 'sha256': digest(data)})
        metadata = {'source_commit': source_commit, 'course': 'Trí tuệ nhân tạo', 'instructor': 'To be completed by the group', 'main_presentation': 'presentation/phan-loai-van-ban-naive-bayes-v3.pptx', 'report_pdf': 'docs/bao-cao-do-an.pdf'}
        data = json.dumps(metadata, indent=2, ensure_ascii=False).encode('utf-8')
        info = zipfile.ZipInfo('SUBMISSION_INFO.json', date_time=(2026, 10, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        package.writestr(info, data)
        entries.append({'path': 'SUBMISSION_INFO.json', 'size_bytes': len(data), 'sha256': digest(data)})
    with zipfile.ZipFile(archive) as package:
        if package.testzip() is not None:
            raise RuntimeError('ZIP integrity check failed.')
        for entry in entries:
            if digest(package.read(entry['path'])) != entry['sha256']:
                raise RuntimeError(f"Hash mismatch: {entry['path']}")
    archive_hash = digest(archive.read_bytes())
    manifest = {'source_commit': source_commit, 'archive_name': archive.name, 'archive_sha256': archive_hash, 'archive_size_bytes': archive.stat().st_size, 'total_files': len(entries), 'files': entries}
    (OUTPUT / 'MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUTPUT / 'CHECKSUMS.sha256').write_text(f'{archive_hash}  {archive.name}\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in manifest.items() if k != 'files'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
