#!/usr/bin/env python3
"""
promote_level.py — 直接晋级用户段位

直接修改 data/users/{username}.json 中的 level 字段并重置平时分，无需人工确认。
供 devil_ai_tutor SKILL 在管理员模式下调用。

用法:
    python promote_level.py <username> <new_level>

参数:
    username    用户名，对应 data/users/{username}.json
    new_level   目标段位：L1 | L2 | L3 | L4

退出码:
    0  成功
    1  参数错误 / 文件不存在 / 字段映射缺失
"""

import argparse
import json
import sys
from pathlib import Path

LEVEL_MAP = {
    "L1": "L1_基础扫盲期",
    "L2": "L2_进阶理解期",
    "L3": "L3_深度应用期",
    "L4": "L4_专家实战期",
}

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "users"


def parse_args():
    parser = argparse.ArgumentParser(
        description="直接晋级 devil_ai_tutor 用户段位"
    )
    parser.add_argument("username", help="目标用户名")
    parser.add_argument(
        "new_level",
        choices=list(LEVEL_MAP.keys()),
        help="目标段位：L1 | L2 | L3 | L4",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    user_file = DATA_DIR / f"{args.username}.json"
    if not user_file.exists():
        print(f"错误: 用户文件不存在: {user_file}", file=sys.stderr)
        sys.exit(1)

    with user_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    try:
        old_level = data["level"]
        data["level"] = LEVEL_MAP[args.new_level]
        data["current_week_state"]["estimated_score"] = 10
    except KeyError as e:
        print(f"错误: 用户数据中缺少字段 {e}", file=sys.stderr)
        sys.exit(1)

    with user_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(
        f"成功: {args.username} 段位已从 {old_level} 更新为 {LEVEL_MAP[args.new_level]}，"
        f"平时分重置为 10"
    )


if __name__ == "__main__":
    main()
