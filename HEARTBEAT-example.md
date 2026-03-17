# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

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
