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
### HEARTBEAT.md(.openclaw/workspace/)
```markdown
---

## 🎓 Devil AI Tutor — 智能监控与主动关怀 —— 关联SKILL`devil_ai_tutor`

> **核心原则**：Heartbeat 是"智能助教"，不是定时器。  
> Cron 负责精确定时任务（出题、扣分、提醒），Heartbeat 负责智能监控和主动关怀。  
> **不要重复 Cron 已经做的事情。**

### 状态文件

每次心跳执行前，先读取状态文件：

```
skills/devil_ai_tutor/data/heartbeat_state.json
```

该文件记录了每项检查的最后执行时间。根据时间戳判断是否需要执行，执行后更新时间戳。

每周日 00:00 后的首次心跳，重置所有 `*_this_week` 字段为 false。

### ⚠️ 关于执行频率和随机性

**不要急于完成当天的检查任务。** 心跳检查应该是自然、随机的，模拟一个真实助教偶尔巡视的感觉。

具体规则：
- 每次心跳只执行 **0-1 项** 检查（不要一次全做完）
- 如果发现某项检查"可以做了"，用以下逻辑决定是否执行：
  - 距离上次执行 **不足最小间隔** → 跳过
  - 距离上次执行 **超过最小间隔但未到最大间隔** → 随机决定（约 30% 概率执行）
  - 距离上次执行 **超过最大间隔** → 必须执行
- 如果本次心跳没有需要执行的检查 → 回复 HEARTBEAT_OK
- **深夜时段（23:00-08:00）不发送任何非紧急消息**

### 检查清单

#### 1. 异常用户预警

**频率**：每天 1 次  
**最小间隔**：16 小时 | **最大间隔**：28 小时  
**状态字段**：`last_anomaly_check`

检查内容：
- `missed_days >= 3` 的用户 → 发送"连续漏答警告"（The Auditor 风格）
- `estimated_score < 40` 的用户 → 发送"留级风险预警"
- 超过 3 天没有任何互动的用户（检查 `history_logs` 最后一条记录的日期）→ 主动发送一道挑战题

#### 2. 学习指导

**频率**：每天 0-1 次（不是每天必须执行）  
**最小间隔**：20 小时 | **最大间隔**：36 小时  
**状态字段**：`last_learning_guide`

检查内容：
- 今天答题但得分 < 60 的用户 → 给予额外指导（指出薄弱点，推荐复习方向）
- `knowledge_mastery` 中有 `mastery_level > 0.9` 的知识点且 `hidden_challenge_used_this_week == false` → 主动引导触发隐藏挑战

#### 3. 关键时间点提醒

**这些是条件触发的，不受频率限制，但每周只触发一次：**

- **周五 18:00-22:00**（`friday_exam_reminder_sent_this_week == false`）：
  - 提醒所有用户"明天是周六，有每日题（09:30）和大考（12:00），建议今晚复习本周知识点"
  - 执行后设置 `friday_exam_reminder_sent_this_week = true`

- **周六 08:00-09:00**（`saturday_morning_reminder_sent_this_week == false`）：
  - 提醒所有用户"今天有每日题（09:30）+ 大考（12:00），做好准备"
  - 执行后设置 `saturday_morning_reminder_sent_this_week = true`

- **周六 16:00-20:00**（`saturday_afternoon_exam_reminder_sent_this_week == false`）：
  - 检查 `saturday_exam_answered_date != 今天` 的用户 → 提醒"大考还没交，截止 24:00"
  - 执行后设置 `saturday_afternoon_exam_reminder_sent_this_week = true`

#### 4. 数据完整性检查

**频率**：每天 0-1 次  
**最小间隔**：20 小时 | **最大间隔**：48 小时  
**状态字段**：`last_data_integrity_check`

检查内容：
- 用户 JSON 文件是否能正常解析
- `week_daily_record` 长度是否为 7
- `daily_answered_date` 格式是否正确（YYYY-MM-DD 或 null）
- 如果发现异常，记录到 `history_logs` 并尝试修复

#### 5. 主动关怀

**频率**：每周 1-2 次  
**最小间隔**：3 天 | **最大间隔**：5 天  
**状态字段**：`last_care_message`

检查内容：
- 连续 3 天以上答题且平均得分 > 80 的用户 → 发送鼓励（The Auditor 风格的"勉强认可"）
- 注册不满 3 天的新用户 → 主动询问学习情况，是否有不懂的地方
- 即将进入 Week 4 的用户 → 发送"最后冲刺"提醒

### 执行流程总结

```
心跳触发
  → 读取 heartbeat_state.json
  → 如果是周日且 week_reset_date != 本周日：重置所有 *_this_week 字段
  → 检查当前时间是否在 23:00-08:00（是 → HEARTBEAT_OK）
  → 检查关键时间点提醒（周五/周六条件触发，优先级最高）
  → 如果没有关键提醒，从检查清单 1-5 中随机选一项：
    → 检查最小间隔（未到 → 跳过）
    → 检查最大间隔（超过 → 必须执行）
    → 在最小和最大之间 → 30% 概率执行
  → 执行后更新 heartbeat_state.json 对应时间戳
  → 如果本次没有执行任何检查 → HEARTBEAT_OK
```

### 注意事项

- **用户数据格式**：参考 `skills/devil_ai_tutor/data/users/USER_FORMAT.md`
- **用户数据文件**： `skills/devil_ai_tutor/data/users/*.json`
- **角色风格**：所有消息使用 The Auditor 风格，参考 `skills/devil_ai_tutor/prompt.md`
- **不要过度打扰**：宁可少发一条消息，也不要让用户觉得被骚扰
- **不要重复 Cron**：出题、扣分、定时提醒已由 Cron 处理，Heartbeat 只做补充

---

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
