# 魔鬼 AI 导师

> 30 天魔鬼训练营，从 AI 门外汉到 AI 应用工程师

一个严格监督学习的 AI 导师 Skill，采用三轨制计分系统和费曼学习法，通过每日练习和周考实现快速进阶。

## ✨ 特性

- 🔥 **严厉导师人设** - 毒舌但专业的 The Auditor，拒绝浅表学习
- 📊 **三轨制计分** - 平时分 + 段位分 + 总分，全方位评估进度
- 📚 **30 天课程** - LLM 基础 → RAG → Agent → 工程化
- ⏰ **自动化监督** - 每日 9:30 出题，周六大考，自动晋级
- 🎯 **费曼学习法** - 强制复述 + 隐藏挑战，深度理解

## 🚀 快速开始

### 1. 安装

将此 Skill 放入 Claude Code 的 skills 目录：

```bash
~/.claude/skills/devil_ai_tutor/
```

### 2. 注册

在你的telegram上对它说:

```
我想注册 tutor 计划
```
- 注意到`Skills\devil_ai_tutor\data\users\`目录下有以你名字为文件名的json数据文件后，代表成功注册

### 3. 配置定时任务

**方式一：自动配置**
对你的 openclaw 说:
```
请将 HEARTBEAT-example.md 添加到 HEARTBEAT.md
请将 jobs-example.json 添加到 cron 配置
```

**方式二：手动配置**
- 复制 `HEARTBEAT-example.md` 内容到 `~/.claude/workspace/HEARTBEAT.md`
- 复制 `jobs-example.json` 到 `~/.claude/cron/jobs.json`

## 📊 计分系统

| 类型 | 说明 | 规则 |
|------|------|------|
| **平时分** | 日常练习积累 | 答题 +5，加练 +2，复述 +3~8，超时 -10 |
| **段位分** | 每周六结算 | `大考 × 0.7 + 平时 × 0.3`，≥60 晋级 |
| **总分** | 整体能力 | 晋级时 `+= 段位分 / 4`，满分 100 |

## 📚 课程大纲

| 周次 | 主题 | 内容 |
|------|------|------|
| Week 1 | LLM 基础 | 核心原理、Prompt 工程、Function Calling |
| Week 2 | RAG 系统 | 向量数据库、文档切分、检索优化 |
| Week 3 | Agent 开发 | 多代理协同、持久化记忆、工具调用 |
| Week 4 | 工程化 | 评估、微调、部署监控、未来趋势 |

## 📁 项目结构

```
devil_ai_tutor/
├── SKILL.md                    # 系统规则和技术实现
├── prompt.md                   # 角色人设和语言风格
├── data/
│   ├── syllabus.json          # 30 天课程大纲
│   └── users/                 # 用户学习数据
│       ├── user_template.json
│       └── {username}.json
├── HEARTBEAT-example.md       # 定时任务配置示例
├── jobs-example.json          # Cron 配置示例
└── README.md
```

## ⚠️ 注意事项

- 导师风格严厉，适合自律学习者
- 详细规则见 [SKILL.md](SKILL.md)

## 📄 License

MIT
