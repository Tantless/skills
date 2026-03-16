# 魔鬼 AI 导师 (Devil AI Tutor)

一个严格监督学习的 AI 导师 Skill，通过 30 天魔鬼训练营将你从 AI 门外汉培养成 AI 应用工程师。

## 特性

- 🔥 **严厉导师人设**：毒舌但专业的 The Auditor，拒绝浅表学习
- 📊 **三轨制计分**：平时分 + 实际段位分 + 总分，全方位评估学习进度
- 📚 **30 天课程**：LLM 基础 → RAG → Agent → 工程化，循序渐进
- ⏰ **自动化监督**：每日 20:00 出题，周六大考，自动结算晋级
- 🎯 **费曼学习法**：强制复述 + 隐藏挑战，深度理解核心概念

## 快速启动

1. 将此 Skill 放入 OpenClaw 的 skill 目录
2. 确保 OpenClaw 能正常加载该 Skill
3. 向 OpenClaw 说：`我想注册 tutor 计划`
4. 配置定时任务（见下方），可以写入openclaw的 `HEARTBEAT.md`

## 定时任务配置
### HEARTBEAT.md
```yaml
⏰ 魔鬼 AI 导师定时任务
- 每日 20:00: 下发今日考题
- 每日 24:00: 检查未答题用户，执行扣分
- 每周六 20:00: 发布周六大考
- 每周六 24:00: 结算成绩，判断晋级/留级
- 关联 SKILL: devil_ai_tutor
```

### corn (.openclaw/corn/jobs.json)
```json
{
  "version": 1,
  "jobs": [
    {
      "id": "7cb1086d-711d-44c4-b70c-d957f7d45da6",
      "name": "魔鬼AI导师-每日9点半出题",
      "enabled": true,
      "createdAtMs": 1773137487308,
      "updatedAtMs": 1773624807324,
      "schedule": {
        "kind": "cron",
        "expr": "30 9 * * *"
      },
      "sessionTarget": "main",
      "wakeMode": "now",
      "payload": {
        "kind": "systemEvent",
        "text": "现在是每日 09:30，请检查 syllabus.json 并下发今日例题。读取 skills/devil_ai_tutor/data/users/ 目录下的所有用户，通过 Telegram 或其他平台 @ 他们发送今日考题。提醒用户截止时间为 24:00。"
      },
      "state": {
        "nextRunAtMs": 1773711000000,
        "lastRunAtMs": 1773624600006,
        "lastRunStatus": "ok",
        "lastStatus": "ok",
        "lastDurationMs": 207318,
        "lastDeliveryStatus": "not-requested",
        "consecutiveErrors": 0
      }
    },
    {
      "id": "31016751-7941-44c7-9139-6af698f189ea",
      "name": "魔鬼AI导师-每日00点超时扣分",
      "enabled": true,
      "createdAtMs": 1773137498179,
      "updatedAtMs": 1773590489255,
      "schedule": {
        "kind": "cron",
        "expr": "0 0 * * *",
        "tz": "Asia/Shanghai"
      },
      "sessionTarget": "main",
      "wakeMode": "now",
      "payload": {
        "kind": "systemEvent",
        "text": "现在是每日 00:00 超时扣分时间。请先读取 skills/devil_ai_tutor/data/users/USER_FORMAT.md 了解字段含义，然后检查 skills/devil_ai_tutor/data/users/ 目录下的所有用户 JSON 文件。判断标准：如果用户的 daily_answered_date 不等于昨天的日期（YYYY-MM-DD），则视为昨天未答题。对未答题用户执行 -10 分扣分，更新 missed_days += 1，通过 Telegram 通知扣分结果。然后重置所有用户的每日状态：daily_answered = false, feynman_used_today = false（但不修改 daily_answered_date 和 feynman_used_date，保留历史记录）。"
      },
      "state": {
        "nextRunAtMs": 1773676800000,
        "lastRunAtMs": 1773590400019,
        "lastRunStatus": "ok",
        "lastStatus": "ok",
        "lastDurationMs": 89236,
        "lastDeliveryStatus": "not-requested",
        "consecutiveErrors": 0
      }
    },
    {
      "id": "124ac4de-e199-408b-b6ce-ebf8c2fd76b0",
      "name": "魔鬼AI导师-周六12点大考",
      "enabled": true,
      "createdAtMs": 1773137519896,
      "updatedAtMs": 1773460803156,
      "schedule": {
        "kind": "cron",
        "expr": "0 12 * * 6"
      },
      "sessionTarget": "main",
      "wakeMode": "now",
      "payload": {
        "kind": "systemEvent",
        "text": "现在是周六 12:00，请根据本周学习内容生成一道综合实战设计题。读取 skills/devil_ai_tutor/data/users/ 目录下的所有用户，通过 Telegram 或其他平台 @ 他们发送周六大考题目。提醒截止时间为当日 24:00。"
      },
      "state": {
        "nextRunAtMs": 1774065600000,
        "lastRunAtMs": 1773460800015,
        "lastRunStatus": "ok",
        "lastStatus": "ok",
        "lastDurationMs": 3141,
        "lastDeliveryStatus": "not-requested",
        "consecutiveErrors": 0
      }
    },
    {
      "id": "2ca358d1-4e65-4c77-8b34-3adefd28196a",
      "name": "魔鬼AI导师-每日20点提醒",
      "enabled": true,
      "createdAtMs": 1773294753652,
      "updatedAtMs": 1773576059681,
      "schedule": {
        "kind": "cron",
        "expr": "0 20 * * *",
        "tz": "Asia/Shanghai"
      },
      "sessionTarget": "main",
      "wakeMode": "now",
      "payload": {
        "kind": "systemEvent",
        "text": "现在是每日 20:00 提醒时间。请先读取 skills/devil_ai_tutor/data/users/USER_FORMAT.md 了解字段含义，然后检查 skills/devil_ai_tutor/data/users/ 目录下的所有用户 JSON 文件。判断标准：如果用户的 daily_answered_date 不等于今天的日期（YYYY-MM-DD），则视为今天未答题。对未答题用户通过 Telegram 发送提醒消息，提醒截止时间为 24:00，超时将扣 10 分。注意：此时仅提醒，不扣分，不修改任何字段。"
      },
      "state": {
        "nextRunAtMs": 1773662400000,
        "lastRunAtMs": 1773576000015,
        "lastRunStatus": "ok",
        "lastStatus": "ok",
        "lastDurationMs": 59666,
        "lastDeliveryStatus": "not-requested",
        "consecutiveErrors": 0
      }
    }
  ]
}
```
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
