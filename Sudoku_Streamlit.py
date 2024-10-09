import streamlit as st
import random
import time

# 초기 설정
if 'AVal' not in st.session_state:
    st.session_state.AVal = [[str(random.randint(1, 9)) for _ in range(9)] for _ in range(9)]

def num_click(i, j):
    st.session_state.AVal[i][j] = str((int(st.session_state.AVal[i][j]) % 9) + 1)  # 예시 클릭 동작

# 각 컨테이너 만들기
c1 = st.container()
c2 = st.container()
c3 = st.container()

# 각 컨테이너에 3개의 열 만들기
with c1:
    col1, col2, col3 = st.columns(3)
    for i in range(3):
        with col1:
            for j in range(3):
                button_key = f"btn_{i}_{j}_{st.session_state.AVal[i][j]}"
                if st.button(st.session_state.AVal[i][j], on_click=lambda i=i, j=j: num_click(i, j), key=button_key):
                    st.write(f"Button {i},{j} clicked.")

with c2:
    col4, col5, col6 = st.columns(3)
    for i in range(3, 6):
        with col4:
            for j in range(3):
                button_key = f"btn_{i}_{j}_{st.session_state.AVal[i][j]}"
                if st.button(st.session_state.AVal[i][j], on_click=lambda i=i, j=j: num_click(i, j), key=button_key):
                    st.write(f"Button {i},{j} clicked.")

with c3:
    col7, col8, col9 = st.columns(3)
    for i in range(6, 9):
        with col7:
            for j in range(3):
                button_key = f"btn_{i}_{j}_{st.session_state.AVal[i][j]}"
                if st.button(st.session_state.AVal[i][j], on_click=lambda i=i, j=j: num_click(i, j), key=button_key):
                    st.write(f"Button {i},{j} clicked.")

if 'ButtonList' not in st.session_state:
    st.session_state.ButtonList = [[st.button("", key=f"btn_{i}_{j}") for j in range(9)] for i in range(9)]

if 'start_time' not in st.session_state:
    st.session_state.start_time = 0

if 'elapsed_time' not in st.session_state:
    st.session_state.elapsed_time = 0

if 'past_records' not in st.session_state:
    st.session_state.past_records = []

# 타이머 함수
def start_timer():
    st.session_state.start_time = time.time()
    st.session_state.elapsed_time = 0

# 경과 시간 업데이트 함수
def update_elapsed_time():
    st.session_state.elapsed_time = int(time.time() - st.session_state.start_time)
    st.write(f"경과 시간: {st.session_state.elapsed_time} 초")

# 버튼 클릭 처리
def num_click(i, j):
    st.session_state.XLoc, st.session_state.YLoc = i, j
    st.write(f"Button {i},{j} clicked.")

# 셔플 기능
def shuffle_click():
    random19 = list(range(1, 10))
    random.shuffle(random19)
    for i in range(9):
        for j in range(9):
            st.session_state.AVal[i][j] = str(random19[(i * 9 + j) % 9])

# 숫자 버튼 처리
def key_input(value):
    i, j = st.session_state.XLoc, st.session_state.YLoc
    st.session_state.AVal[i][j] = str(value)
    st.session_state.ButtonList[i][j] = st.button(str(value), key=f"btn_{i}_{j}")
    st.write(f"Entered {value} at {i},{j}")

# UI 구현
st.title("Sudoku Game")

# 셔플 버튼
if st.button("Shuffle"):
    shuffle_click()

# 타이머 시작 버튼
if st.button("Start Timer"):
    start_timer()

# 타이머 경과 시간 업데이트
if st.session_state.start_time:
    update_elapsed_time()

# 그리드 버튼 생성
for i in range(9):
    cols = st.columns(9)
    for j, col in enumerate(cols):
        with col:
            # 버튼을 그리드에서 출력 (고유한 키를 명확히 하기 위해 i, j를 문자열로 사용)
            button_key = f"btn_{i}_{j}_{st.session_state.AVal[i][j]}"
            if st.session_state.AVal[i][j]:
                if st.button(st.session_state.AVal[i][j], on_click=lambda i=i, j=j: num_click(i, j), key=button_key):
                    st.write(f"Button {i},{j} clicked.")

# 숫자 입력 처리
st.write("Press a number key (1-9):")
for num in range(1, 10):
    if st.button(str(num)):
        key_input(num)

# 게임 완료 체크
if st.button("Check Solution"):
    err = 0
    # 행 검사
    for i in range(9):
        if len(set(st.session_state.AVal[i])) != 9:
            st.write(f"{i + 1}번째 행 오류")
            err = 1
            break

    # 열 검사
    if not err:
        for j in range(9):
            temp = [st.session_state.AVal[i][j] for i in range(9)]
            if len(set(temp)) != 9:
                st.write(f"{j + 1}번째 열 오류")
                err = 1
                break

    # 9칸 영역 검사
    if not err:
        index = [0, 3, 6]
        for i in index:
            for j in index:
                temp = []
                for k in range(3):
                    temp.append(st.session_state.AVal[i][j + k])
                    temp.append(st.session_state.AVal[i + 1][j + k])
                    temp.append(st.session_state.AVal[i + 2][j + k])
                if len(set(temp)) != 9:
                    st.write(f"{i}, {j}의 3*3 매트릭스 오류")
                    err = 1
                    break

    if err == 0:
        nickname = st.text_input("닉네임을 입력하세요", "")
        if nickname:
            elapsed_time = st.session_state.elapsed_time
            st.session_state.past_records.append((nickname, elapsed_time))
            st.session_state.past_records.sort(key=lambda x: x[1])
            rank = st.session_state.past_records.index((nickname, elapsed_time)) + 1
            st.write(f"축하합니다, {nickname}님! {rank}등입니다. 경과 시간: {elapsed_time} 초")
        else:
            st.write("닉네임을 입력하세요.")
