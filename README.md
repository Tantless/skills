# 魔鬼 AI 导师 (Devil AI Tutor)

一个严格监督学习的 AI 导师 Skill，通过 30 天魔鬼训练营将你从 AI 门外汉培养成 AI 应用工程师。

## 特性

- 🔥 **严厉导师人设**：毒舌但专业的 The Auditor，拒绝浅表学习
- 📊 **三轨制计分**：平时分 + 实际段位分 + 总分，全方位评估学习进度
- 📚 **30 天课程**：LLM 基础 → RAG → Agent → 工程化，循序渐进
- ⏰ **自动化监督**：每日 9:30 出题，周六大考，自动结算晋级
- 🎯 **费曼学习法**：强制复述 + 隐藏挑战，深度理解核心概念

## 快速启动

1. 将此 Skill 放入 OpenClaw 的 skill 目录(.openclaw\workspace\skills\devil_ai_tutor)
2. 确保 OpenClaw 能正常加载该 Skill(询问openclaw是否能看到该skill)
3. 向 OpenClaw 说：`我想注册 tutor 计划`
4. 配置定时任务（见下方）

### HEARTBEAT.md
  - 你可以手动将`Skills\HEARTBEAT-example.md`中的内容添加到你openclaw的`.openclaw\workspace\HEARTBEAT.md`之后
  - 或者你可以直接告诉openclaw，`请将HEARTBEAT-example.md的内容添加到我openclaw的HEARTBEAT.md之中`

### jobs.json
  - 同样的，你可以手动将`Skills\jobs-example.json`的内容添加到你的`.openclaw\cron`目录下作为`jobs.json`
  - 或者，你可以直接告诉openclaw,`请帮我将jobs-example.json中的时钟内容添加到openclaw的cron中`

## 计分规则
**平时预估分**（初始 60）
- 每日题答对 +5
- 主动加练 +2（首次 +4）
- 费曼复述 +3~+8
- 超时未交 -10

**实际段位分**（每周六结算）
- 公式：`大考得分 × 0.7 + 平时分 × 0.3`
- ≥60 晋级，<60 留级

**总分**（0-100）
- 每周晋级时：`总分 += 实际分 / 4`
- 代表成为 AI 应用工程师的整体能力

## 文件结构

```
devil_ai_tutor/
├── SKILL.md              # 系统规则和技术实现
├── prompt.md             # 角色人设和语言风格
├── data/
│   ├── syllabus.json     # 30 天课程大纲
│   └── users/            # 用户学习数据
│       ├── user_template.json
│       └── {username}.json
└── README.md
```

## 课程大纲

- **Week 1**：LLM 核心原理、Prompt 工程、Function Calling
- **Week 2**：RAG 全流程、向量数据库、文档切分
- **Week 3**：Agent 模式、多代理协同、持久化记忆
- **Week 4**：AI 评估、微调、部署监控、未来趋势

## 注意事项

- 导师风格严厉，不鼓励不妥协，适合自律学习者
- 每日 20:00-24:00 必须答题，超时扣 10 分
- 留级不累加总分，鼓励认真学习
- 详细规则见 `SKILL.md` 和 `prompt.md`
