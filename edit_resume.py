# 注：本文件中的 <你的姓名> / <你的学校> / <实习公司N> 为占位符，
# 使用前请替换成你自己的信息。
# -*- coding: utf-8 -*-
"""在原简历 PDF 上做最小侵入编辑：优化 AI 表述 + 加 CPA 备考，不改变无关内容与版式。
采用 PyMuPDF：redact 擦除目标行 -> 用微软雅黑重写。
"""
import pymupdf, os

SRC = r'C:/Users/EngineeringCenter/Desktop/新建文件夹/个人简历.pdf'
OUT_DIR = r'C:/Users/EngineeringCenter/WorkBuddy/2026-09-09-10-13-17/resume-output'
OUT = os.path.join(OUT_DIR, '个人简历_AI优化版_含CPA备考_v2.pdf')
os.makedirs(OUT_DIR, exist_ok=True)

MSYH = r'C:/Windows/Fonts/msyh.ttc'
MSYHBD = r'C:/Windows/Fonts/msyhbd.ttc'

# 颜色（灰阶 int -> rgb 0-1）
def rgb(c):
    return ((c >> 16) & 255) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255

BODY = rgb(6710886)   # 正文灰 0x666666

doc = pymupdf.open(SRC)

# ============ 编辑点：统一 redact 收集 ============
# (page_index, rect, [ (text, bold, x0) ... ])  —— 每行可拆 bold/regular 两段
# 这里先收集所有 redact rect，再统一 apply，再统一 insert

redacts = []   # (page_idx, rect)

# ---- P1 自我评价 L3/L4/L5（b20,b21,b22）----
for y0, y1 in [(346, 359), (362, 375), (379, 392)]:
    redacts.append((0, (38, y0, 560, y1)))

# ---- P2 AI bullet 4 行（b2-b5）----
for y0, y1 in [(37, 50), (53, 66), (70, 83), (87, 100)]:
    redacts.append((1, (38, y0, 560, y1)))

# ---- P3 AI 3 行（b13-b15）----
for y0, y1 in [(215, 228), (232, 244), (248, 261)]:
    redacts.append((2, (38, y0, 560, y1)))

# ---- P3 b12 证书句（加 CPA）----
redacts.append((2, (38, 198, 560, 211)))

# apply all redactions
for pi, rect in redacts:
    doc[pi].add_redact_annot(pymupdf.Rect(rect))
for pi in range(len(doc)):
    doc[pi].apply_redactions()

# 注册字体（必须在 apply_redactions 之后）
for p in doc:
    p.insert_font(fontname='msyh', fontfile=MSYH)
    p.insert_font(fontname='msyhbd', fontfile=MSYHBD)

# 用 Font 对象测量 bold 标题宽度
f_bold = pymupdf.Font(fontname='msyhbd', fontfile=MSYHBD)

# ============ 重写内容 ============
# 基线 y = 原 bbox y1 - 2
def put(page, x, y, text, bold=False):
    fn = 'msyhbd' if bold else 'msyh'
    page.insert_text((x, y), text, fontname=fn, fontsize=9.9, color=BODY)

# ---- P1 自我评价 L3/L4/L5 ----
p = doc[0]
put(p, 38, 357, '撰写与附注编制，熟悉从业务端到财务端再到审计端的企业运作闭环。主动落地AI工具，自建AIAgent台账工作')
put(p, 38, 373, '流提效60%，并将周报制作固化为8步流程Skill，具备把AI嵌入财务工作流的实操能力。对AI+财务方向有持续')
put(p, 38, 390, '学习热情，责任心强，适应高强度多任务环境，善于跨部门沟通与协同推进。')

# ---- P2 AI bullet 4 行 ----
p = doc[1]
bt = '•AI 辅助效率提升：'
bw = f_bold.text_length(bt, fontsize=9.9)
put(p, 38, 48, bt, bold=True)
put(p, 38 + bw, 48, '在台账核对与系统录入中，引入DeepSeek+WorkBuddy+实在Agent组合构建AI协作工作流，')
put(p, 38, 64, '实现跨系统数据智能匹配与自动回填，将每周台账整理耗时从5小时压缩至2小时，效率提升60%；并独立编写')
put(p, 38, 81, 'skill.md，将周报制作固化为覆盖封面、计划、仪表盘、资金物资、科研、质量运维、格式校对8步流程的')
put(p, 38, 98, '可复用模板，实现“一次配置、长期复用”的AI协作模式。')

# ---- P3 AI 3 行 ----
p = doc[2]
bt = '•AI 应用与数字化：'
bw = f_bold.text_length(bt, fontsize=9.9)
put(p, 38, 226, bt, bold=True)
put(p, 38 + bw, 226, '主动跟踪AI在财务领域的前沿应用，熟练运用DeepSeek、Claude、ChatGPT等大模型及AI')
put(p, 38, 242, 'Agent/MCP工具，将AI嵌入财务工作流：①台账核对自动化（提效60%）②周报8步流程Skill③自研财务分析报告')
put(p, 38, 259, '生成器（10+指标）④求职筛选自动化工作流（抓取→评分→清单）。2个作品链接，Python支撑二次开发。')

# ---- P3 b12 证书句：插入 CPA ----
put(doc[2], 38, 209, '证书，普通话证书，注册会计师（CPA）备考中（会计/税法），日语具备日常基础交流能力。')

# 子集化字体，压缩体积
doc.subset_fonts()

doc.save(OUT)
doc.close()

# ============ 验证 ============
d = pymupdf.open(OUT)
full = ''.join(pg.get_text() for pg in d)
d.close()
checks = [
    '8步流程Skill',            # 自我评价新表述
    '格式校对8步流程',          # AI bullet 新表述
    '注册会计师（CPA）备考中',   # CPA 新增
    '提效60%',                 # AI 技能强化
    '求职筛选自动化工作流',      # 新增：求职筛选自动化工作流
    'MCP',                      # 新增：MCP 连接器
    '<你的姓名>', '<你的学校>', '<实习公司1>', '<实习公司2>', '<实习公司3>',  # 无关内容保留
    '鼎信诺', '金蝶', 'CET-6', '社科杯',  # 无关内容保留
]
print('输出:', OUT)
print('文件大小:', os.path.getsize(OUT), 'bytes')
for c in checks:
    print(('OK ' if c in full else 'MISS ') + c)
print('总字数:', len(full))
