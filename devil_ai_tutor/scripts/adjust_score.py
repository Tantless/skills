#!/usr/bin/env python3
"""
adjust_score.py — 调整用户分数字段

直接修改 data/users/{username}.json 中的分数字段，无需人工确认。
供 devil_ai_tutor SKILL 在管理员模式下调用。

用法:
    python adjust_score.py <username> <score_type> <new_score>

参数:
    username    用户名，对应 data/users/{username}.json
    score_type  平时分 | 实际段位分
    new_score   新分数值（整数或小数）

退出码:
    0  成功
    1  参数错误 / 文件不存在 / 字段映射缺失
"""

import argparse
import json
import sys
from pathlib import Path

SCORE_FIELD_MAP = {
    "平时分": ("current_week_state", "estimated_score"),
    "实际段位分": ("actual_score",),
}

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "users"


def parse_args():
    parser = argparse.ArgumentParser(
        description="调整 devil_ai_tutor 用户的分数字段"
    )
    parser.add_argument("username", help="目标用户名")
    parser.add_argument(
        "score_type",
        choices=list(SCORE_FIELD_MAP.keys()),
        help="分数类型：平时分 | 实际段位分",
    )
    parser.add_argument("new_score", type=float, help="新分数值")
    return parser.parse_args()


def main():
    args = parse_args()

    user_file = DATA_DIR / f"{args.username}.json"
    if not user_file.exists():
        print(f"错误: 用户文件不存在: {user_file}", file=sys.stderr)
        sys.exit(1)

    with user_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    keys = SCORE_FIELD_MAP[args.score_type]
    try:
        if len(keys) == 1:
            old_value = data[keys[0]]
            data[keys[0]] = args.new_score
        else:
            old_value = data[keys[0]][keys[1]]
            data[keys[0]][keys[1]] = args.new_score
    except KeyError as e:
        print(f"错误: 用户数据中缺少字段 {e}", file=sys.stderr)
        sys.exit(1)

    with user_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"成功: {args.username} 的 {args.score_type} 已从 {old_value} 更新为 {args.new_score}")


if __name__ == "__main__":
    main()
