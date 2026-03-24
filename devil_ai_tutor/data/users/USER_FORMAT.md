# 用户数据格式说明 (User Data Format)

> **重要**：本文件定义 `data/users/{username}.json` 的数据结构和字段含义。  
> 所有读写用户数据的操作必须遵循此格式。

---

## 文件命名规则

- 文件名：`{username}.json`（用户的 Telegram username 或唯一标识符，两者均可）
- 位置：`./data/users/`
- 格式：标准 JSON（不支持注释）

---

## 完整数据结构

```json
{
  "telegram_id": "6491617158",
  "wechat_chat_id": null,
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
| `telegram_id` | string | 用户的 Telegram ID，用于 Telegram 渠道推送；null 表示未绑定 Telegram |
| `wechat_chat_id` | string\|null | 用户的微信会话 ID，用于微信渠道推送；null 表示未绑定微信 |
| `username` | string | 用户唯一标识符（Telegram username 或自定义名称） |
| `display_name` | string | 用户的显示名称（用于 @ 提及） |
| `enrollment_date` | string | 注册日期（YYYY-MM-DD 格式） |
| `level` | string | 当前等级（L1/L2/L3/L4，对应 Week 1-4） |
| `actual_score` | number | 实际段位分（0-100，每周六 24:00 结算后更新） |
| `total_score` | number | 总分（0.00-100.00，代表成为 AI 应用工程师的整体能力） |

---

### `current_week_state` — 本周状态（周指段位周，非自然周）

| 字段 | 类型 | 说明 | 重置时机 |
|------|------|------|----------|
| `week_number` | number | 当前所在周数（1-4） | 晋级时 +1 |
| `current_topic` | string | 当前知识点 ID（如 K1_2） | 每日出题时更新 |
| `estimated_score` | number | 平时预估分（影响周六结算） | 每次互动后更新 |
| `interactive_bonus` | number | 互动加分累计 | 每周六 24:00 |
| `daily_answered` | boolean | 今天是否已答题（快速判断用） | 每日 00:00 |
| `daily_answered_date` | string/null | 最后答题日期（YYYY-MM-DD，防跨天误判） | 用户答题时更新 |
| `week_daily_record` | array[7] | 本段位周期答题记录（第一天到第七天，0=未答，1=已答） | 每周六 24:00 升段后 |
| `saturday_exam_answered` | boolean | 本段位周期大考是否已答 | 每周六 24:00 |
| `saturday_exam_answered_date` | string/null | 周六大考答题日期（YYYY-MM-DD） | 用户答大考时更新 |
| `missed_days` | number | 累计漏答天数 | 每次超时扣分时 +1 |
| `extra_practice_count` | number | 主动加练次数 | 每周六 24:00 |
| `feynman_used_today` | boolean | 今天是否已使用费曼复述加分 | 每日 00:00 |
| `feynman_used_date` | string/null | 最后使用费曼复述的日期（YYYY-MM-DD） | 使用时更新 |
| `hidden_challenge_used_this_week` | boolean | 本段位周期是否已触发隐藏挑战 | 每周六 24:00 |
| `early_exam_requested` | boolean | 是否申请了提前大考 | 提前大考结算后重置 |
| `early_exam_taken` | boolean | 是否已参加提前大考 | 提前大考结算后重置 |
| `try_it_mode` | boolean | 下次大考是否为"试一试"模式（免惩罚） | 使用后重置 |
| `try_it_accumulated_score` | number | "试一试"模式累计的平时分 | 每周六 24:00 |

---

### `week_daily_record` 数组说明

**重要**：此数组记录的是"本段位周期"的答题情况，而非"本自然周"。

- **长度**：固定 7 个元素
- **索引对应**：
  - `[0]` = 段位周第一天
  - `[1]` = 段位周第二天
  - `[2]` = 段位周第三天
  - `[3]` = 周四
  - `[4]` = 周五
  - `[5]` = 周六
  - `[6]` = 周日
- **值含义**：
  - `0` = 当天未答题
  - `1` = 当天已答题
- **更新时机**：用户答题后，根据当前星期几更新对应索引
- **重置时机**：每周六 24:00 结算升段后重置为 `[0,0,0,0,0,0,0]`

**段位周期说明**：
- 用户在某个段位（如 L1）期间，每天答一道该段位的题目（K1_1, K1_2, K1_3, K1_4）
- 当该段位的所有知识点题目都答完后，如果还未到周六大考，会触发薄弱点巩固题
- 周六大考通过后升段，此数组重置，开始记录新段位周期的答题情况

**星期几转数组索引的计算方法**：
```javascript
// JavaScript 示例
const dayOfWeek = new Date().getDay(); // 0=周日, 1=周一, ..., 6=周六
const arrayIndex = (dayOfWeek + 6) % 7; // 转换为 0=周一, 6=周日
```

---

### `weekly_scores` — 历史成绩

每个段位周期结算后，如果用户成功晋级（实际分 ≥ 60），会追加一条记录：

| 字段 | 类型 | 说明 |
|------|------|------|
| `week` | number | 周数（1-4） |
| `actual_score` | number | 本段位周期实际段位分 |
| `exam_score` | number | 大考得分 |
| `final_estimated_score` | number | 本段位周期最终平时分 |
| `date` | string | 结算日期（YYYY-MM-DD） |

**注意**：留级的段位周期不会记录到此数组。

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

### `weak_points_history` — 薄弱点历史记录

**功能说明**：记录用户在每日考试和周六大考中表现不佳的题目，用于追踪用户的薄弱知识点和理解程度。这使得 AI 导师能够更人性化地了解用户的学习困难点，并在后续教学中针对性地强化。

**触发条件**：当用户答题得分率 ≤ 80% 时，自动记录到此数组。

**记录范围**：
- ✅ 每日考试（daily_quiz）
- ✅ 周六大考（saturday_exam）
- ❌ 主动加练（extra_practice）
- ❌ 隐藏挑战（hidden_challenge）

**数据结构**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `date` | string | 答题日期（YYYY-MM-DD） |
| `topic_id` | string | 知识点 ID（如 K1_2、EXAM_W1） |
| `topic_name` | string | 知识点名称（如"提示词工程"） |
| `question_type` | string | 题目类型（`daily_quiz` / `saturday_exam`） |
| `score` | number | 用户得分 |
| `max_score` | number | 题目满分 |
| `score_percentage` | number | 得分率（0-100，保留1位小数） |
| `understanding_level` | string | 理解程度等级（见下表） |
| `weak_points` | array[string] | 具体薄弱点列表（AI 分析的不足之处） |

**理解程度等级（understanding_level）**：

| 等级 | 得分率范围 | 说明 |
|------|-----------|------|
| `critical` | 0% - 40% | 严重不理解，需要重新学习 |
| `weak` | 40% - 60% | 理解薄弱，需要强化练习 |
| `moderate` | 60% - 80% | 基本理解但有欠缺，需要查漏补缺 |

**示例**：

```json
"weak_points_history": [
  {
    "date": "2026-03-12",
    "topic_id": "K1_3",
    "topic_name": "Function Calling (工具调用)",
    "question_type": "daily_quiz",
    "score": 35,
    "max_score": 100,
    "score_percentage": 35.0,
    "understanding_level": "critical",
    "weak_points": [
      "JSON Schema 格式完全错误",
      "Function Calling 机制理解为关键词匹配（错误）",
      "多工具调用未区分 parallel/sequential"
    ]
  },
  {
    "date": "2026-03-14",
    "topic_id": "K1_4",
    "topic_name": "API 交互与多模型选型",
    "question_type": "daily_quiz",
    "score": 52,
    "max_score": 100,
    "score_percentage": 52.0,
    "understanding_level": "weak",
    "weak_points": [
      "选型思路基本正确但表述不专业",
      "SSE 只知表面不知协议细节（缺 Last-Event-ID）",
      "退避策略缺 jitter 和 max backoff",
      "成本计算数学错误"
    ]
  }
]
```

**更新规则**：

1. **触发时机**：用户提交答案并完成评分后，立即判断是否需要记录
2. **判断逻辑**：
   ```
   IF (question_type == "daily_quiz" OR question_type == "saturday_exam")
      AND (score / max_score <= 0.8) THEN
      记录到 weak_points_history
   ```
3. **理解程度计算**：
   ```
   score_percentage = (score / max_score) * 100

   IF score_percentage < 40:
       understanding_level = "critical"
   ELSE IF score_percentage < 60:
       understanding_level = "weak"
   ELSE IF score_percentage <= 80:
       understanding_level = "moderate"
   ```
4. **数据上限**：建议保留最近 50 条记录，超出后删除最早的记录（避免数据过大）

**使用场景**：

- **个性化教学**：AI 导师在后续对话中可以引用用户的薄弱点，进行针对性提问
- **复习提醒**：在周末或新周开始时，提醒用户复习薄弱知识点
- **进度追踪**：对比同一知识点在不同时间的表现，判断是否有进步
- **大考准备**：在周六大考前，重点复习 `understanding_level` 为 `critical` 或 `weak` 的知识点

---

### 提前大考相关字段说明

**`early_exam_requested`**：
- 类型：boolean
- 说明：用户是否申请了提前大考
- 触发条件：用户完成本段位所有知识点后主动申请
- 重置时机：提前大考结算后（无论通过或失败）

**`early_exam_taken`**：
- 类型：boolean
- 说明：用户是否已参加提前大考
- 用途：防止重复申请
- 重置时机：周六 24:00 结算后

**`try_it_mode`**：
- 类型：boolean
- 说明：下次大考是否为"试一试"模式（免惩罚模式）
- 触发条件：用户提前大考通过，且通过时距离下次周六 ≤ 2 天（周四、周五、周六）
- 效果：该模式下的大考失败不留级、不扣分，平时分继续累计到下次大考
- 重置时机：使用后立即重置

**`try_it_accumulated_score`**：
- 类型：number
- 说明："试一试"模式下累计的平时分
- 用途：如果"试一试"大考失败，该分数会累计到下次正常大考的平时分中
- 计算：`try_it_accumulated_score = 上次段位周期平时分 + 本次段位周期平时分`
- 重置时机：成功晋级后重置为 0

---

## 关键判断逻辑

### ⚠️ 防止跨天误判

所有答题状态判断必须基于日期字段，而非布尔值：

| 场景 | 错误判断 ❌ | 正确判断 ✅ |
|------|-----------|-----------|
| 20:00 提醒 | `daily_answered == false` | `daily_answered_date != today` |
| 00:00 扣分 | `daily_answered == false` | `daily_answered_date != yesterday` |
| 周六结算 | `saturday_exam_answered == false` | `saturday_exam_answered_date != 本段位周期的周六` |
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
6. **判断是否需要记录薄弱点**：
   - 如果题目类型为 `daily_quiz` 或 `saturday_exam`
   - 且得分率 ≤ 80%（即 `score / max_score <= 0.8`）
   - 则追加记录到 `weak_points_history`，包含：
     - 答题日期、知识点 ID 和名称
     - 得分、满分、得分率
     - 理解程度等级（critical/weak/moderate）
     - AI 分析的具体薄弱点列表

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
4. 重置所有段位周期级别字段：
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
   - `early_exam_taken = false`
   - 如果晋级：`try_it_accumulated_score = 0`
   - 如果留级：`try_it_accumulated_score = 0`

---

## 模板文件

参考 `user_template.json` 创建新用户数据。

---

**最后更新**：2026-03-24
**维护者**：The Auditor (魔鬼 AI 导师系统)
