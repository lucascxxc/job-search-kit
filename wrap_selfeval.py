# -*- coding: utf-8 -*-
"""把三版自我评价的纯文本按版心宽度自动断行。
版心：正文左边 x=38，原 PDF 正文行最宽到 x=562 → 可用宽度 524px。
贪心分行：逐字累加宽度，超过 SAFE=519（留 5px 余量）即在当前字前断行。
"""
import pymupdf

MSYH = r'C:/Windows/Fonts/msyh.ttc'
f = pymupdf.Font(fontname='msyh', fontfile=MSYH)
SIZE = 9.9
SAFE = 519.0

VERSIONS = {
    'V1 业财融合版': (
        '具备甲方业财融合与乙方审计合规双重实习背景：在商业航天企业负责50+个在研项目的预算执行跟踪与支出核对，'
        '主动将财务数据与业务进度交叉比对，纠正多笔支出与预算科目归属偏差，支撑更准确的成本归集与业财口径一致；'
        '在事务所年审中独立完成20+家企业函证、底稿撰写与附注编制，熟悉合规交付口径。'
        '同时自建AI Agent台账工作流提效60%，将周报制作固化为8步流程Skill，一次配置、长期复用。'
        '责任心强，适应高强度多任务环境，善于跨部门沟通与协同推进。'
    ),
    'V2 AI 数智化版': (
        '具备甲方业财融合与乙方审计合规双重实习背景，习惯把学到的新东西在两周内做成能跑起来的工具：'
        '在商业航天企业自建AI Agent台账工作流，将每周台账整理从5小时压缩到2小时、提效60%，'
        '并把周报制作固化为8步流程Skill；自研财务分析报告生成器，上传三表自动输出10+核心指标与风险清单，有可体验链接。'
        '在事务所年审中独立完成20+家企业函证、底稿撰写与附注编制，实地+电话核实100余项资产、取证准确率100%，'
        '熟悉从业务端到财务端再到审计端的运作闭环。责任心强，适应高强度多任务环境，善于跨部门沟通与协同推进。'
    ),
    'V3 审计合规版': (
        '具备乙方审计合规与甲方业财融合双重实习背景：两段事务所实习累计承接60余家企业的年报审计、底稿撰写与加工账整理，'
        '独立完成20余家单位的银行及往来款函证全流程制作与年审附注填写，另独立完成40+份函证填制与跟进、回函率95%；'
        '项目出差期间实地+电话核实100余项资产存放状态，取证准确率100%。'
        '在商业航天企业参与50+个在研项目的预算执行跟踪，理解业务数据如何流向财务核算。'
        '熟练使用鼎信诺、新纪元等审计软件与久其、金蝶等财务系统，另自建AI Agent台账工作流提效60%。'
        '责任心强，适应高强度多任务环境，善于跨部门沟通与协同推进。'
    ),
}

def wrap(text, safe=SAFE):
    """贪心断行。返回 (lines, widths)"""
    lines, cur, cur_w = [], '', 0.0
    # 断行禁则：行首不能出现这些标点
    NO_START = '，。；、）」』！？：'
    for ch in text:
        w = f.text_length(ch, fontsize=SIZE)
        if cur_w + w > safe:
            # 若下一字是禁则标点，把它留在本行（允许微超）
            lines.append(cur)
            cur, cur_w = ch, w
        else:
            cur += ch
            cur_w += w
    if cur:
        lines.append(cur)
    return lines, [f.text_length(l, fontsize=SIZE) for l in lines]

over = 0
for name, text in VERSIONS.items():
    lines, widths = wrap(text)
    print(f'\n{"="*66}\n{name}   （共 {len(lines)} 行）\n{"="*66}')
    for i, (l, w) in enumerate(zip(lines, widths), 1):
        flag = 'OK ' if w <= 524 else 'OVER'
        if w > 524:
            over += 1
        print(f'L{i} [{w:5.1f}px] {flag}')
        print(f'    {l}')
print(f'\n超限行数：{over}')
