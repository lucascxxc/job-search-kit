# -*- coding: utf-8 -*-
"""
用 Chrome headless 把 html/ 下的 HTML 批量导出为 PDF（白底、A4、含背景色）
"""
import os
import glob
import subprocess
import time

BASE = r'C:/Users/EngineeringCenter/WorkBuddy/2026-09-09-10-13-17/job-search'
HTML_DIR = os.path.join(BASE, 'html')
PDF_DIR = os.path.join(BASE, 'pdf')
os.makedirs(PDF_DIR, exist_ok=True)

CHROME = r'C:/Program Files/Google/Chrome/Application/chrome.exe'
if not os.path.exists(CHROME):
    CHROME = r'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'


def html_to_pdf(html_path, pdf_path):
    url = 'file:///' + html_path.replace('\\', '/')
    cmd = [
        CHROME,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        '--no-pdf-header-footer',
        '--print-to-pdf=' + pdf_path,
        url,
    ]
    r = subprocess.run(cmd, capture_output=True, timeout=90)
    return os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000


def main():
    files = sorted(glob.glob(os.path.join(HTML_DIR, '*.html')))
    ok, fail = 0, []
    for p in files:
        name = os.path.splitext(os.path.basename(p))[0]
        out = os.path.join(PDF_DIR, name + '.pdf')
        try:
            if html_to_pdf(p, out):
                ok += 1
            else:
                fail.append(name)
        except Exception as e:
            fail.append(f'{name}({e})')
    print(f'PDF 完成：{ok}/{len(files)}，输出目录：{PDF_DIR}')
    if fail:
        print('失败：', fail)


if __name__ == '__main__':
    main()
