# 用户数据格式说明 (User Data Format)

> **重要**：本文件定义 `data/users/{username}.json` 的数据结构和字段含义。  
> 所有读写用户数据的操作必须遵循此格式。

---

## 文件命名规则

- 文件名：`{username}.json`（用户的 Telegram username 或唯一标识符）
- 位置：`./data/users/`
- 格式：标准 JSON（不支持注释）

---

## 完整数据结构

```json
{
  "telegram_id": "6491617158",
  "username": "brand14757",
  "display_name": "李 虎成",
  "enrollment_date": "2026-03-10",
  "level": "L1_基础扫盲期",
  "actual_score": 0,
  "total_score": 0.00,
  "current_week_state": {
    "week_number": 1,
    "current_topic": "K1_2",
    "estimated_score": 60,
    "interactive_bonus": 0,
    "daily_answered": true,
    "daily_answered_date": "2026-03-11",
    "week_daily_record": [0, 1, 0, 0, 0, 0, 0],
    "saturday_exam_answered": false,
    "saturday_exam_answered_date": null,
    "missed_days": 1,
    "extra_practice_count": 0,
    "feynman_used_today": false,
    "feynman_used_date": null,
    "hidden_challenge_used_this_week": false
  },
  "weekly_scores": [
    {
      "week": 1,
      "actual_score": 85,
      "exam_score": 90,
      "final_estimated_score": 75,
      "date": "2026-03-15"
    }
  ],
  "knowledge_mastery": {
    "K1_1": {
      "status": "learning",
      "mastery_level": 0.6,
      "last_tested": "2026-03-11"
    }
  },
  "history_logs": [
    {
      "date": "2026-03-10",
      "event": "注册魔鬼 AI 导师训练营",
      "action": "enrollment"
    }
  ]
}
```

---

## 字段详解

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `telegram_id` | string | 用户的 Telegram ID（唯一标识符） |
| `username` | string | 用户的 Telegram username |
| `display_name` | string | 用户的显示名称（用于 @ 提及） |
| `enrollment_date` | string | 注册日期（YYYY-MM-DD 格式） |
| `level` | string | 当前等级（L1/L2/L3/L4，对应 Week 1-4） |
| `actual_score` | number | 实际段位分（0-100，每周六 24:00 结算后更新） |
| `total_score` | number | 总分（0.00-100.00，代表成为 AI 应用工程师的整体能力） |

---

### `current_week_state` — 本周状态

| 字段 | 类型 | 说明 | 重置时机 |
|------|------|------|----------|
| `week_number` | number | 当前所在周数（1-4） | 晋级时 +1 |
| `current_topic` | string | 当前知识点 ID（如 K1_2） | 每日出题时更新 |
| `estimated_score` | number | 平时预估分（影响周六结算） | 每次互动后更新 |
| `interactive_bonus` | number | 互动加分累计 | 每周六 24:00 |
| `daily_answered` | boolean | 今天是否已答题（快速判断用） | 每日 00:00 |
| `daily_answered_date` | string/null | 最后答题日期（YYYY-MM-DD，防跨天误判） | 用户答题时更新 |
| `week_daily_record` | array[7] | 本周答题记录（周一到周日，0=未答，1=已答） | 每周六 24:00 |
| `saturday_exam_answered` | boolean | 本周六大考是否已答 | 每周六 24:00 |
| `saturday_exam_answered_date` | string/null | 周六大考答题日期（YYYY-MM-DD） | 用户答大考时更新 |
| `missed_days` | number | 累计漏答天数 | 每次超时扣分时 +1 |
| `extra_practice_count` | number | 主动加练次数 | 每周六 24:00 |
| `feynman_used_today` | boolean | 今天是否已使用费曼复述加分 | 每日 00:00 |
| `feynman_used_date` | string/null | 最后使用费曼复述的日期（YYYY-MM-DD） | 使用时更新 |
| `hidden_challenge_used_this_week` | boolean | 本周是否已触发隐藏挑战 | 每周六 24:00 |

---

### `week_daily_record` 数组说明

- **长度**：固定 7 个元素
- **索引对应**：
  - `[0]` = 周一
  - `[1]` = 周二
  - `[2]` = 周三
  - `[3]` = 周四
  - `[4]` = 周五
  - `[5]` = 周六
  - `[6]` = 周日
- **值含义**：
  - `0` = 当天未答题
  - `1` = 当天已答题
- **更新时机**：用户答题后，根据当前星期几更新对应索引
- **重置时机**：每周六 24:00 结算后重置为 `[0,0,0,0,0,0,0]`

**星期几转数组索引的计算方法**：
```javascript
// JavaScript 示例
const dayOfWeek = new Date().getDay(); // 0=周日, 1=周一, ..., 6=周六
const arrayIndex = (dayOfWeek + 6) % 7; // 转换为 0=周一, 6=周日
```

---

### `weekly_scores` — 历史成绩

每周结算后，如果用户成功晋级（实际分 ≥ 60），会追加一条记录：

| 字段 | 类型 | 说明 |
|------|------|------|
| `week` | number | 周数（1-4） |
| `actual_score` | number | 本周实际段位分 |
| `exam_score` | number | 周六大考得分 |
| `final_estimated_score` | number | 本周最终平时分 |
| `date` | string | 结算日期（YYYY-MM-DD） |

**注意**：留级的周不会记录到此数组。

---

### `knowledge_mastery` — 知识点掌握度

记录每个知识点的学习状态：

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | 学习状态（`not_started` / `learning` / `mastered`） |
| `mastery_level` | number | 掌握度（0.0-1.0） |
| `last_tested` | string/null | 最后测试日期（YYYY-MM-DD） |

**知识点 ID 格式**：`K{周数}_{序号}`，例如 `K1_1`、`K2_3`

---

### `history_logs` — 历史日志

记录所有重要事件，每条日志包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| `date` | string | 事件日期（YYYY-MM-DD） |
| `event` | string | 事件描述 |
| `action` | string | 动作类型（`enrollment` / `daily_quiz_sent` / `penalty` / `score_update` 等） |
| `score_change` | number | 分数变动（可选） |
| `new_estimated_score` | number | 更新后的平时分（可选） |
| `topic` | string | 相关知识点 ID（可选） |
| `score` | number | 答题得分（可选） |
| `feedback` | string | 导师反馈（可选） |

---

## 关键判断逻辑

### ⚠️ 防止跨天误判

所有答题状态判断必须基于日期字段，而非布尔值：

| 场景 | 错误判断 ❌ | 正确判断 ✅ |
|------|-----------|-----------|
| 20:00 提醒 | `daily_answered == false` | `daily_answered_date != today` |
| 00:00 扣分 | `daily_answered == false` | `daily_answered_date != yesterday` |
| 周六结算 | `saturday_exam_answered == false` | `saturday_exam_answered_date != 本周六` |
| 费曼复述 | `feynman_used_today == true` | `feynman_used_date == today` |

**原因**：如果 cron 任务延迟或漏执行，布尔值可能不准确，但日期字段永远可靠。

---

## 数据更新规则

### 用户答题后

1. 设置 `daily_answered = true`
2. 更新 `daily_answered_date = 当前日期`
3. 更新 `week_daily_record[当前星期索引] = 1`
4. 更新 `estimated_score`（根据答题质量加分）
5. 追加 `history_logs` 记录

### 周六大考答题后

1. 设置 `saturday_exam_answered = true`
2. 更新 `saturday_exam_answered_date = 当前日期`
3. 追加 `history_logs` 记录

### 每日 00:00 重置

1. 设置 `daily_answered = false`
2. 设置 `feynman_used_today = false`
3. **不修改** `daily_answered_date` 和 `feynman_used_date`（保留历史）

### 每周六 24:00 结算

1. 计算 `actual_score`
2. 更新 `total_score`（如果晋级）
3. 追加 `weekly_scores` 记录（如果晋级）
4. 重置所有周级别字段：
   - `daily_answered = false`
   - `daily_answered_date = null`
   - `week_daily_record = [0,0,0,0,0,0,0]`
   - `saturday_exam_answered = false`
   - `saturday_exam_answered_date = null`
   - `feynman_used_today = false`
   - `feynman_used_date = null`
   - `hidden_challenge_used_this_week = false`
   - `extra_practice_count = 0`
   - `interactive_bonus = 0`

---

## 模板文件

参考 `user_template.json` 创建新用户数据。

---

**最后更新**：2026-03-12  
**维护者**：The Auditor (魔鬼 AI 导师系统)
