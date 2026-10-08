# -*- coding: utf-8 -*-
"""
生成「今日岗位分析」专属索引页 html/今日索引.html
- 只收录今天（按文件 mtime）生成/修改的 md
- 按推荐优先级排序，岗位档案在前，模板类在后
- 每行直接标契合度 / 价值档 / 年包，点开即看
"""
import os
import re
import glob
import html as html_mod
from datetime import datetime, date
import markdown
from md2html import CSS, TPL, OUT_DIR, SRC_DIR, derive_title

TODAY = date.today()


def is_today(path):
    mt = datetime.fromtimestamp(os.path.getmtime(path)).date()
    return mt == TODAY


def parse_meta(md_text):
    """从 md 里抓契合度 / 价值档 / 年包"""
    meta = {'score': '', 'tier': '', 'pkg': ''}
    m = re.search(r'契合度[评分]*[：: ]*\*{0,2}(\d{1,3})', md_text)
    if m:
        meta['score'] = m.group(1)
    m = re.search(r'综合结论[｜|]*\s*\**([A-C][+\-]?)\s*档', md_text)
    if m:
        meta['tier'] = m.group(1) + ' 档'
    m = re.search(r'年包[（(]?估[)）]?[：: ]*\*{0,2}([0-9.\-]+\s*万)', md_text)
    if not meta['pkg']:
        m2 = re.search(r'年包约\s*\**([0-9.\-]+\s*万)', md_text)
        meta['pkg'] = (m.group(1) if m else (m2.group(1) if m2 else ''))
    return meta


def main():
    md_files = sorted(glob.glob(os.path.join(SRC_DIR, '*.md')))
    today_files = [p for p in md_files if is_today(p)]

    jobs, docs = [], []
    for p in today_files:
        with open(p, encoding='utf-8') as f:
            md_text = f.read()
        title = derive_title(md_text, os.path.basename(p))
        name = os.path.splitext(os.path.basename(p))[0] + '.html'
        meta = parse_meta(md_text)
        row = (title, name, meta, len(md_text))
        if re.match(r'^J\d+', os.path.basename(p)):
            jobs.append(row)
        else:
            docs.append(row)

    # 岗位按契合度降序
    def score_key(r):
        try:
            return -int(r[2]['score'])
        except Exception:
            return 0
    jobs.sort(key=score_key)

    parts = []
    parts.append(f'<h1>今日（{TODAY.month} 月 {TODAY.day} 日）岗位分析</h1>')
    parts.append(
        f'<p>共 <strong>{len(today_files)}</strong> 份（岗位档案 {len(jobs)} 份 · 其他 {len(docs)} 份）。'
        f'按<strong>契合度从高到低</strong>排序，点「打开」看完整分析。</p>'
    )
    parts.append(
        '<blockquote><p><strong>怎么用</strong>：先看契合度列锁定前 3 名 → 打开看「投递前必做动作」→ '
        '复制招呼语去 BOSS 打招呼。每页右上角有「打印 / 存 PDF」。</p></blockquote>'
    )

    if jobs:
        parts.append('<h2>岗位档案（按契合度排序）</h2>')
        parts.append(
            '<table><thead><tr>'
            '<th style="min-width:230px">岗位</th><th>契合度</th><th>价值档</th>'
            '<th>年包</th><th>打开</th></tr></thead><tbody>'
        )
        for title, name, meta, size in jobs:
            sc = meta['score']
            if sc:
                try:
                    n = int(sc)
                    color = '#1a7f37' if n >= 90 else ('#b8860b' if n >= 80 else '#888')
                    sc_html = f'<strong style="color:{color}">{sc}</strong>'
                except Exception:
                    sc_html = sc
            else:
                sc_html = '—'
            parts.append(
                f'<tr><td>{html_mod.escape(title)}</td>'
                f'<td>{sc_html}</td>'
                f'<td>{meta["tier"] or "—"}</td>'
                f'<td>{meta["pkg"] or "—"}</td>'
                f'<td><a href="{name}">打开 &#8594;</a></td></tr>'
            )
        parts.append('</tbody></table>')

    if docs:
        parts.append('<h2>模板 / 其他</h2>')
        parts.append('<table><thead><tr><th style="min-width:320px">文档</th><th>字数</th><th>打开</th></tr></thead><tbody>')
        for title, name, meta, size in docs:
            parts.append(
                f'<tr><td>{html_mod.escape(title)}</td><td>{size:,}</td>'
                f'<td><a href="{name}">打开 &#8594;</a></td></tr>'
            )
        parts.append('</tbody></table>')

    parts.append('<hr><p><a href="index.html">&#8592; 查看全部历史文档目录</a></p>')

    body = '\n'.join(parts)
    out_html = TPL.format(title=f'今日岗位分析 · {TODAY.strftime("%m-%d")}', css=CSS, body=body)
    out_path = os.path.join(OUT_DIR, '今日索引.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(out_html)
    print(f'今日索引生成：{out_path}（岗位 {len(jobs)} + 其他 {len(docs)}）')
    for t, n, m, s in jobs:
        print(f'  {m["score"] or "-":>4}  {t}')


if __name__ == '__main__':
    main()
