# -*- coding: utf-8 -*-
"""
簡易記帳系統 (Expense Tracker)
作者：薛淯愷
說明：使用 Python 撰寫的指令列記帳工具，支援新增收支紀錄、
      查看紀錄、依類別統計、計算結餘，並將資料存成檔案。
"""

import json
import os
from datetime import datetime

DATA_FILE = "records.json"


def load_records():
    """讀取已儲存的記帳紀錄，若檔案不存在則回傳空列表"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_records(records):
    """將記帳紀錄寫入檔案"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def add_record(records):
    """新增一筆收入或支出紀錄"""
    print("\n請選擇類型：1. 收入  2. 支出")
    type_choice = input("輸入選項 (1/2)：").strip()

    if type_choice == "1":
        record_type = "收入"
    elif type_choice == "2":
        record_type = "支出"
    else:
        print("輸入錯誤，請輸入 1 或 2。")
        return

    try:
        amount = float(input("請輸入金額：").strip())
    except ValueError:
        print("金額格式錯誤，請輸入數字。")
        return

    category = input("請輸入類別（例如：餐飲、交通、薪水、娛樂）：").strip()
    if category == "":
        category = "未分類"

    note = input("備註（可留空）：").strip()

    record = {
        "type": record_type,
        "amount": amount,
        "category": category,
        "note": note,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    records.append(record)
    save_records(records)
    print(f"已新增一筆「{record_type}」紀錄：{amount} 元（{category}）")


def show_records(records):
    """顯示所有記帳紀錄"""
    if not records:
        print("\n目前沒有任何紀錄。")
        return

    print("\n==================== 所有紀錄 ====================")
    print(f"{'日期':<18}{'類型':<6}{'金額':<10}{'類別':<10}備註")
    print("-" * 60)
    for r in records:
        print(f"{r['date']:<18}{r['type']:<6}{r['amount']:<10.0f}{r['category']:<10}{r['note']}")
    print("=" * 60)


def show_summary(records):
    """計算並顯示總收入、總支出、結餘，以及各類別統計"""
    if not records:
        print("\n目前沒有任何紀錄可統計。")
        return

    total_income = sum(r["amount"] for r in records if r["type"] == "收入")
    total_expense = sum(r["amount"] for r in records if r["type"] == "支出")
    balance = total_income - total_expense

    print("\n==================== 收支總覽 ====================")
    print(f"總收入：{total_income:.0f} 元")
    print(f"總支出：{total_expense:.0f} 元")
    print(f"結餘：{balance:.0f} 元")

    # 依類別統計支出
    category_totals = {}
    for r in records:
        if r["type"] == "支出":
            category_totals[r["category"]] = category_totals.get(r["category"], 0) + r["amount"]

    if category_totals:
        print("\n--- 支出類別統計 ---")
        # 依金額排序，從高到低
        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        for category, amount in sorted_categories:
            percentage = (amount / total_expense * 100) if total_expense > 0 else 0
            print(f"{category:<10}{amount:>8.0f} 元  ({percentage:.1f}%)")
    print("=" * 54)


def delete_record(records):
    """刪除指定編號的紀錄"""
    if not records:
        print("\n目前沒有任何紀錄可刪除。")
        return

    show_records(records)
    try:
        index = int(input("\n請輸入要刪除的紀錄編號（從上方列表數，第1筆為1）：").strip())
        if 1 <= index <= len(records):
            removed = records.pop(index - 1)
            save_records(records)
            print(f"已刪除：{removed['date']} {removed['type']} {removed['amount']} 元")
        else:
            print("編號超出範圍。")
    except ValueError:
        print("請輸入數字編號。")


def main():
    records = load_records()

    while True:
        print("\n========== 簡易記帳系統 ==========")
        print("1. 新增紀錄")
        print("2. 查看所有紀錄")
        print("3. 收支總覽與類別統計")
        print("4. 刪除紀錄")
        print("5. 離開")
        choice = input("請選擇功能 (1-5)：").strip()

        if choice == "1":
            add_record(records)
        elif choice == "2":
            show_records(records)
        elif choice == "3":
            show_summary(records)
        elif choice == "4":
            delete_record(records)
        elif choice == "5":
            print("感謝使用，再見！")
            break
        else:
            print("輸入錯誤，請輸入 1 到 5 之間的數字。")


if __name__ == "__main__":
    main()
