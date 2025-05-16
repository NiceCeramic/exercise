import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Google Sheets 연동 설정
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)

# Google Sheets 열기
sheet_id = "1ylWIpCAGSr421bvc_a3PYmtgDFtyv8vZnDaZ3-45Ft0"
sheet = client.open_by_key(sheet_id).sheet1

# 참여자 고정
participants = ["김가람", "이하늘", "박하진", "최지우", "정서윤", "홍지민", "윤다온"]

# 제목
st.title("🏋️ 철봉 운동 기록 시스템 (Google Sheets 연동)")

# 기록 입력 폼
with st.form("entry_form"):
    name = st.selectbox("이름", participants)
    exercise = st.selectbox("운동 종류", ["버티기", "턱걸이"])
    if exercise == "버티기":
        value = st.number_input("버틴 시간 (초)", min_value=0)
    else:
        value = st.number_input("턱걸이 횟수", min_value=0)

    submit = st.form_submit_button("기록 저장")

# 저장
if submit:
    today = datetime.now().strftime("%Y-%m-%d")
    sheet.append_row([today, name, exercise, value])
    st.success("기록이 저장되었습니다!")

# 데이터 불러오기
data = pd.DataFrame(sheet.get_all_records())

# 전체 기록
st.subheader("📋 전체 기록")
st.dataframe(data)

# 오늘 날짜
today = datetime.now().strftime("%Y-%m-%d")
today_data = data[data["날짜"] == today]

# 랭킹
st.subheader("🏆 오늘의 랭킹")
for ex in ["버티기", "턱걸이"]:
    st.markdown(f"### {ex}")
    top = today_data[today_data["운동"] == ex].sort_values(by="기록", ascending=False)
    st.table(top[["이름", "기록"]].head(5))

# 시각화
st.subheader("📈 날짜별 변화 추이")
selected_name = st.selectbox("기록 확인할 사람", ["전체"] + participants)
filtered = data if selected_name == "전체" else data[data["이름"] == selected_name]
chart_data = filtered.pivot_table(index="날짜", columns="운동", values="기록", aggfunc="mean")
st.line_chart(chart_data)
