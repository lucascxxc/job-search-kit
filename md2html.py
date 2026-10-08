# -*- coding: utf-8 -*-
"""
把 job-search 目录下的所有 .md 转成带样式的单文件 HTML
- 双主题自动切换（跟随系统亮/暗）
- 表格美化（斑马纹 + 表头固定色 + 横向滚动）
- 顶部导航条 + 返回索引
- 响应式，手机可读
- 打印优化
"""
import os
import re
import glob
import html as html_mod
import markdown

SRC_DIR = r'C:/Users/EngineeringCenter/WorkBuddy/2026-09-09-10-13-17/job-search'
OUT_DIR = os.path.join(SRC_DIR, 'html')
os.makedirs(OUT_DIR, exist_ok=True)

CSS = """
:root{
  --bg:#ffffff; --fg:#1a1a1a; --muted:#5a6472; --line:#e3e6ea;
  --card:#f7f9fb; --accent:#1f6feb; --accent-soft:#e8f1ff;
  --th:#eef2f7; --td-odd:#ffffff; --td-even:#fafbfc;
  --warn-bg:#fff8e1; --warn-border:#f0c36d;
  --ok:#1a7f37; --bad:#c1121f;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#16181d; --fg:#e6e8eb; --muted:#98a1ae; --line:#2c313a;
    --card:#1c2026; --accent:#58a6ff; --accent-soft:#13233b;
    --th:#22272e; --td-odd:#1a1e24; --td-even:#1f242b;
    --warn-bg:#332b12; --warn-border:#8a6d2f;
    --ok:#3fb950; --bad:#f85149;
  }
}
*{box-sizing:border-box}
body{
  margin:0; padding:0;
  font-family:"Microsoft YaHei","PingFang SC","Hiragino Sans GB","Segoe UI",sans-serif;
  background:var(--bg); color:var(--fg);
  font-size:15px; line-height:1.85;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:960px; margin:0 auto; padding:0 24px 80px}
.nav{
  position:sticky; top:0; z-index:10;
  background:var(--bg); border-bottom:1px solid var(--line);
  padding:10px 24px; margin-bottom:28px;
  display:flex; align-items:center; gap:14px; flex-wrap:wrap;
}
.nav a{
  color:var(--accent); text-decoration:none; font-size:13.5px;
  padding:4px 10px; border-radius:6px; background:var(--accent-soft);
}
.nav a:hover{text-decoration:underline}
.nav .title{font-weight:700; font-size:14px; color:var(--fg); background:none; padding:0}

h1{
  font-size:26px; font-weight:700; margin:34px 0 18px;
  padding-bottom:12px; border-bottom:2px solid var(--accent);
  line-height:1.4;
}
h2{
  font-size:20px; font-weight:700; margin:30px 0 14px;
  padding-left:11px; border-left:4px solid var(--accent); line-height:1.5;
}
h3{font-size:16.5px; font-weight:700; margin:24px 0 12px; color:var(--fg)}
h4{font-size:15px; font-weight:700; margin:18px 0 10px; color:var(--muted)}
p{margin:12px 0}
hr{border:none; border-top:1px solid var(--line); margin:30px 0}

ul,ol{padding-left:26px; margin:12px 0}
li{margin:6px 0}
li>ul,li>ol{margin:4px 0}

table{
  border-collapse:collapse; width:100%; margin:18px 0;
  font-size:13.5px; display:block; overflow-x:auto; white-space:nowrap;
}
thead{display:table-header-group}
th{
  background:var(--th); font-weight:700; text-align:left;
  padding:9px 12px; border:1px solid var(--line);
  position:sticky; top:0;
}
td{padding:9px 12px; border:1px solid var(--line); white-space:normal; min-width:80px}
tbody tr:nth-child(odd){background:var(--td-odd)}
tbody tr:nth-child(even){background:var(--td-even)}
tbody tr:hover{background:var(--accent-soft)}

blockquote{
  margin:16px 0; padding:12px 16px;
  background:var(--warn-bg); border-left:4px solid var(--warn-border);
  border-radius:0 6px 6px 0; color:var(--fg);
}
blockquote p{margin:6px 0}

code{
  background:var(--card); padding:2px 6px; border-radius:4px;
  font-family:"Cascadia Mono","Consolas",monospace; font-size:13px;
  border:1px solid var(--line);
}
pre{
  background:var(--card); padding:14px 16px; border-radius:8px;
  overflow-x:auto; border:1px solid var(--line);
}
pre code{background:none; border:none; padding:0}

strong{font-weight:700; color:var(--fg)}
a{color:var(--accent)}

/* 打印 / 导出 PDF：强制亮色，避免暗底 */
@media print{
  :root{
    --bg:#ffffff !important; --fg:#1a1a1a !important; --muted:#5a6472 !important;
    --line:#cccccc !important; --card:#f5f5f5 !important;
    --accent:#1f6feb !important; --accent-soft:#eef4ff !important;
    --th:#eaeaea !important; --td-odd:#ffffff !important; --td-even:#f7f7f7 !important;
    --warn-bg:#fff8e1 !important; --warn-border:#d0a020 !important;
    --ok:#1a7f37 !important; --bad:#c1121f !important;
  }
  .nav{display:none}
  body{font-size:10.5pt; line-height:1.6}
  .wrap{max-width:100%; padding:0}
  table{display:table; width:100%; font-size:8.5pt; white-space:normal}
  td{white-space:normal}
  th{position:static; background:#eaeaea !important}
  tbody tr:hover{background:transparent}
  h1{page-break-after:avoid; font-size:17pt}
  h2{page-break-after:avoid; font-size:13.5pt}
  h3{page-break-after:avoid}
  table,blockquote,pre{page-break-inside:avoid}
  a{color:#1a1a1a !important; text-decoration:none}
}
"""

TPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<div class="nav">
  <span class="title">{title}</span>
  <a href="index.html">&#8592; 返回目录</a>
  <a href="javascript:window.print()">&#128424; 打印 / 存 PDF</a>
</div>
<div class="wrap">
{body}
</div>
</body>
</html>
"""


def md_to_html(md_text):
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc', 'attr_list', 'sane_lists'])
    return md.convert(md_text), md.toc


def derive_title(md_text, filename):
    m = re.search(r'^#\s+(.+)$', md_text, re.M)
    if m:
        return m.group(1).strip()
    return os.path.splitext(filename)[0]


def convert(path):
    with open(path, encoding='utf-8') as f:
        md_text = f.read()
    title = derive_title(md_text, os.path.basename(path))
    body, toc = md_to_html(md_text)
    out_html = TPL.format(title=html_mod.escape(title), css=CSS, body=body)
    out_name = os.path.splitext(os.path.basename(path))[0] + '.html'
    out_path = os.path.join(OUT_DIR, out_name)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(out_html)
    return title, out_name, len(md_text)


def build_index(items):
    # 分组
    groups = {
        '总览 / 对比': [],
        '岗位档案': [],
        '简历 / 模板': [],
        '其他': [],
    }
    for title, name, size in items:
        if '横向对比' in title or '总览' in title:
            groups['总览 / 对比'].append((title, name, size))
        elif re.match(r'^J\d+', name) or 'J0' in name[:2]:
            groups['岗位档案'].append((title, name, size))
        elif any(k in title for k in ['简历', '模板', '特点', 'AI应用']):
            groups['简历 / 模板'].append((title, name, size))
        else:
            groups['其他'].append((title, name, size))

    parts = []
    for gname in ['总览 / 对比', '岗位档案', '简历 / 模板', '其他']:
        lst = groups[gname]
        if not lst:
            continue
        parts.append(f'<h2>{gname}</h2>')
        parts.append('<table><thead><tr><th style="min-width:320px">文档</th><th>字数</th><th>打开</th></tr></thead><tbody>')
        for title, name, size in sorted(lst):
            parts.append(
                f'<tr><td>{html_mod.escape(title)}</td>'
                f'<td>{size:,}</td>'
                f'<td><a href="{name}">打开 &#8594;</a></td></tr>'
            )
        parts.append('</tbody></table>')

    body = f"""
<h1>秋招岗位分析 · 文档目录</h1>
<p>共 <strong>{len(items)}</strong> 份文档。点标题直接打开；每页右上角可「打印 / 存 PDF」。</p>
<blockquote>
<p><strong>阅读建议</strong>：先看《横向对比总览》确定投递优先级，再打开具体岗位档案看招呼语和投递前动作。</p>
</blockquote>
{''.join(parts)}
"""
    out_html = TPL.format(title='秋招岗位分析 · 文档目录', css=CSS, body=body)
    with open(os.path.join(OUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(out_html)


def main():
    md_files = sorted(glob.glob(os.path.join(SRC_DIR, '*.md')))
    items = []
    for p in md_files:
        try:
            items.append(convert(p))
        except Exception as e:
            print('FAIL', os.path.basename(p), e)
    build_index(items)
    print(f'转换完成：{len(items)} 份 md -> html，输出目录：{OUT_DIR}')
    for t, n, s in items:
        print(f'  {n:<56} {s:>6,} 字')
    print('  索引：index.html')


if __name__ == '__main__':
    main()
