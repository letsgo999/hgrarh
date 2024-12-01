import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl

# 시스템 폰트 사용 설정
mpl.rcParams['font.family'] = 'DejaVu Sans'
mpl.rcParams['axes.unicode_minus'] = False

# 메인 앱 타이틀
st.title("한글 깨짐 방지 차트 생성기")

# CSV 파일 업로드
st.subheader("데이터 업로드 및 시각화")
data_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if data_file:
    df = pd.read_csv(data_file)
    st.dataframe(df)

    # X축과 Y축 선택
    columns = df.columns.tolist()
    x_col = st.selectbox("X축 선택", columns)
    y_col = st.selectbox("Y축 선택", columns)

    # 차트 생성 및 표시
    if st.button("차트 생성"):
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.plot(df[x_col], df[y_col], marker='o')
        plt.title("한글 차트")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.grid(True)
        st.pyplot(fig)
