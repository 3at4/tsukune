import streamlit as st
import requests
from datetime import MINYEAR, date, datetime, timedelta

# 祝日データを取得する関数（キャッシュ機能付き）
def get_holidays(year):
    url = f"https://holidays-jp.github.io/api/v1/{year}/date.json"
    response = requests.get(url)
    holidays = response.json()
    return set(datetime.strptime(date, '%Y-%m-%d').date() for date in holidays)

def calculate_business_day(start_date, delta_days, holidays):
    business_day = start_date
    while delta_days != 0:
        print(f"Calculating: business_day={business_day}, delta_days={delta_days}")  # デバッグ出力
        try:
            business_day -= timedelta(days=1)
        except OverflowError:
            raise OverflowError(f"Overflow error with date: {business_day}")
        if business_day.weekday() < 5 and business_day not in holidays:
            delta_days -= 1
    return business_day

def calculate_task_dates(tasks, end_date, holidays):
    task_dates = []
    for task in tasks:
        task_start_date = calculate_business_day(end_date, task["start_at"], holidays)
        if task["days"] > 0:
            task_end_date = calculate_business_day(task_start_date, task["days"] - 1, holidays)
        else:
            task_end_date = task_start_date
        task_dates.append((task["task"], task_start_date, task_end_date))
    return task_dates

# タスクリストの定義（AパターンとBパターン）
# Aパターンのタスクリスト
tasks_a = [
  {
    "task_id": 1,
    "task": "デザイン依頼書作成",
    "start_at": 30,
    "days": 0
  },
  {
    "task_id": 2,
    "task": "デザイン制作",
    "start_at": 25,
    "days": 4
  },
  {
    "task_id": 3,
    "task": "バナー依頼書作成",
    "start_at": 11,
    "days": 0
  },
  {
    "task_id": 4,
    "task": "素材選定",
    "start_at": 32,
    "days": 4
  },
  {
    "task_id": 5,
    "task": "素材監修依頼",
    "start_at": 28,
    "days": 0
  },
  {
    "task_id": 6,
    "task": "素材監修",
    "start_at": 28,
    "days": 4
  },
  {
    "task_id": 7,
    "task": "切り抜き発注",
    "start_at": 22,
    "days": 0
  },
  {
    "task_id": 8,
    "task": "切り抜き作業",
    "start_at": 22,
    "days": 1
  },
  {
    "task_id": 9,
    "task": "カード制作リスト作成",
    "start_at": 18,
    "days": 0
  },
  {
    "task_id": 10,
    "task": "量産発注",
    "start_at": 18,
    "days": 0
  },
  {
    "task_id": 11,
    "task": "量産",
    "start_at": 18,
    "days": 4
  },
  {
    "task_id": 12,
    "task": "量産カード画像チェック",
    "start_at": 14,
    "days": 0
  },
  {
    "task_id": 13,
    "task": "カード監修依頼",
    "start_at": 14,
    "days": 0
  },
  {
    "task_id": 14,
    "task": "カード監修",
    "start_at": 14,
    "days": 2
  },
  {
    "task_id": 15,
    "task": "バナー制作",
    "start_at": 9,
    "days": 2
  },
  {
    "task_id": 16,
    "task": "マスタ更新",
    "start_at": 2,
    "days": 0
  },
  {
    "task_id": 17,
    "task": "デバック",
    "start_at": 2,
    "days": 0
  },
  {
    "task_id": 18,
    "task": "SNS投稿依頼",
    "start_at": 1,
    "days": 0
  },
  {
    "task_id": 19,
    "task": "メンテお知らせ作成",
    "start_at": 1,
    "days": 0
  },
  {
    "task_id": 20,
    "task": "メンテナンス対応",
    "start_at": 0,
    "days": 0
  }
]
# Bパターンのタスクリスト
tasks_b = [
  {
    "task_id": 1,
    "task": "バナー依頼書作成",
    "start_at": 11,
    "days": 0
  },
  {
    "task_id": 2,
    "task": "素材選定",
    "start_at": 32,
    "days": 4
  },
  {
    "task_id": 3,
    "task": "素材監修依頼",
    "start_at": 28,
    "days": 0
  },
  {
    "task_id": 4,
    "task": "素材監修",
    "start_at": 28,
    "days": 4
  },
  {
    "task_id": 5,
    "task": "切り抜き発注",
    "start_at": 22,
    "days": 0
  },
  {
    "task_id": 6,
    "task": "切り抜き作業",
    "start_at": 22,
    "days": 1
  },
  {
    "task_id": 7,
    "task": "カード制作リスト作成",
    "start_at": 18,
    "days": 0
  },
  {
    "task_id": 8,
    "task": "量産発注",
    "start_at": 18,
    "days": 0
  },
  {
    "task_id": 9,
    "task": "量産",
    "start_at": 18,
    "days": 4
  },
  {
    "task_id": 10,
    "task": "量産カード画像チェック",
    "start_at": 14,
    "days": 0
  },
  {
    "task_id": 11,
    "task": "カード監修依頼",
    "start_at": 14,
    "days": 0
  },
  {
    "task_id": 12,
    "task": "カード監修",
    "start_at": 14,
    "days": 2
  },
  {
    "task_id": 13,
    "task": "バナー制作",
    "start_at": 9,
    "days": 2
  },
  {
    "task_id": 14,
    "task": "マスタ更新",
    "start_at": 2,
    "days": 0
  },
  {
    "task_id": 15,
    "task": "デバック",
    "start_at": 2,
    "days": 0
  },
  {
    "task_id": 16,
    "task": "SNS投稿依頼",
    "start_at": 1,
    "days": 0
  },
  {
    "task_id": 17,
    "task": "メンテお知らせ作成",
    "start_at": 1,
    "days": 0
  },
  {
    "task_id": 18,
    "task": "メンテナンス対応",
    "start_at": 0,
    "days": 0
  } 
]
# ...（タスクリスト tasks_a と tasks_b の定義）

st.title('スケジュールメイカー 決めるくん')

selected_date = st.date_input("施策の開始日を選択してください", datetime.today())
pattern = st.radio("タスクパターンを選択してください", ('Aパターン_デザインテンプレ制作あり', 'Bパターン_デザインテンプレ制作なし'))

holidays = get_holidays(selected_date.year)

# ユーザー入力日付の検査関数
def validate_input_date(input_date):
    min_valid_date = date(MINYEAR, 1, 1)
    max_valid_date = date(9999, 12, 31)  # Pythonのdateオブジェクトの最大範囲
    if not (min_valid_date <= input_date <= max_valid_date):
        raise ValueError(f"Invalid date: {input_date}. Please choose a date between {min_valid_date} and {max_valid_date}.")

# UI部分にもデバッグ出力を追加
if st.button('スケジュール生成'):
    print(f"Selected date: {selected_date}")  # 選択された日付のデバッグ出力

    # 入力された日付を検証
    validate_input_date(selected_date)
    
    # 選択したパターンに基づいてタスクリストを選択
    tasks = tasks_a if pattern == 'Aパターン' else tasks_b

    # タスクの日付を計算
    calculated_dates = calculate_task_dates(tasks, selected_date, holidays)

    # 結果の表示
    # for task_name, start, end in calculated_dates:
    #    st.write(f"{task_name}: 開始日 {start.strftime('%Y-%m-%d')}, 終了日 {end.strftime('%Y-%m-%d')}")

    # Generate and display the schedules in the desired Markdown formats

    # Format 1
    markdown_str_1 = "### タテ表示\n"
    markdown_str_1 += "|                        | 開始日     | 終了日     | \n"
    markdown_str_1 += "| ---------------------- | ---------- | ---------- | \n"
    for task_name, start, end in calculated_dates:
        markdown_str_1 += f"| {task_name} | {start.strftime('%Y-%m-%d')} | {end.strftime('%Y-%m-%d')} |\n"
    st.markdown(markdown_str_1)

    # Format 2
    markdown_str_2 = "### ヨコ表示\n"
    markdown_str_2 += "|        | " + " | ".join([task_name for task_name, _, _ in calculated_dates]) + " | \n"
    markdown_str_2 += "| ------ |" + " --- |" * len(calculated_dates) + "\n"
    markdown_str_2 += "| 開始日 | " + " | ".join([start.strftime('%Y-%m-%d') for _, start, _ in calculated_dates]) + " |\n"
    markdown_str_2 += "| 終了日 | " + " | ".join([end.strftime('%Y-%m-%d') for _, _, end in calculated_dates]) + " |\n"
    st.markdown(markdown_str_2)
