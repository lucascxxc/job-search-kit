# job-search-kit

秋招期间攒的一套脚本：从**抓岗位**到**出可读清单**，再到**改简历**。

不是框架，是一堆各干一件事的小脚本。每个都能单独拿走用。

---

## 脚本

| 脚本 | 干什么 |
|---|---|
| `md2html.py` | Markdown → 单文件 HTML（双主题、表格美化、顶部导航、响应式、打印优化） |
| `build_today_index.py` | 按文件 mtime 筛出当天新增的岗位档案，生成按契合度排序的今日索引页 |
| `html2pdf.py` | Chrome / Edge headless 批量把 HTML 导出成 PDF（白底、A4、保留背景色） |
| `edit_resume.py` | 在原简历 PDF 上做最小侵入编辑 |
| `measure_selfeval.py` | 测量每行文字宽度，确认不超出原 PDF 版心 |
| `wrap_selfeval.py` | 按版心宽度自动断行 |
| `check_selfeval.py` | 断行后复核每行宽度是否仍达标 |

---

## 值得一提的两处

### 1. 改简历：最小侵入，零行溢出

`edit_resume.py` 不在 Word 里重排，而是**直接在原 PDF 上改**：

```
PyMuPDF → redact 擦除目标行 → 用微软雅黑按原位置重写
```

原则是不改变任何无关内容与版式。

难点在**行宽**。原 PDF 正文左边界 `x=38`，最宽到 `x=562`，
可用宽度 524px，安全线取 **519**（留 5px 余量）。

改写后的文字只要超一个字，整行就会溢出、破坏排版。
所以配套了测量、断行、复核三个脚本：

```
wrap_selfeval.py  按 519px 贪心断行（逐字累加宽度，超了就在当前字前断）
measure_selfeval.py  测量实际宽度
check_selfeval.py    复核是否达标
```

字体固定用微软雅黑（`C:/Windows/Fonts/msyh.ttc`），
测量和实际渲染用同一套度量，才不会出现「测着没超、看着超了」。

### 2. 报告：一份内容，多种载体

岗位分析写成 Markdown，然后：

```
md2html.py  →  单文件 HTML（手机可读、能打印）
html2pdf.py →  PDF（发给别人、存档）
```

HTML 做了双主题和打印优化，因为**手机上看**和**打印出来**都是真实需求。

---

## 依赖

```bash
pip install pymupdf
```

`html2pdf.py` 需要本机装 Chrome 或 Edge。

---

## 关于隐私

仓库里只有脚本，**不含任何简历内容、岗位数据和个人信息**。

`edit_resume.py` 里的姓名、学校、公司名称已替换为
`<你的姓名>` / `<你的学校>` / `<实习公司N>` 占位符，使用前请替换成你自己的信息。
