import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import subprocess
import sys

# Install koreanize-matplotlib (Assume the .whl file is provided and uploaded to the app)
@st.cache_resource
def install_koreanize_matplotlib(whl_path):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", whl_path])
        st.success("koreanize-matplotlib 설치 완료!")
        import koreanize_matplotlib
        st.success("koreanize-matplotlib 임포트 성공!")
    except Exception as e:
        st.error(f"설치 중 오류 발생: {e}")
        raise e

# Upload the .whl file and install koreanize-matplotlib
st.title("한글 깨짐 방지 차트 생성기")
uploaded_file = st.file_uploader("koreanize-matplotlib .whl 파일 업로드", type="whl")

if uploaded_file:
    with open("koreanize_matplotlib_installer.whl", "wb") as f:
        f.write(uploaded_file.read())
    install_koreanize_matplotlib("koreanize_matplotlib_installer.whl")

# Upload CSV file for chart
st.subheader("데이터 업로드 및 시각화")
data_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if data_file:
    df = pd.read_csv(data_file)
    st.dataframe(df)

    # Choose columns for x and y
    columns = df.columns.tolist()
    x_col = st.selectbox("X축 선택", columns)
    y_col = st.selectbox("Y축 선택", columns)

    # Generate and display the chart
    if st.button("차트 생성"):
        plt.figure(figsize=(10, 6))
        plt.plot(df[x_col], df[y_col], marker='o')
        plt.title("한글 깨짐 방지 차트")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.grid(True)
        st.pyplot(plt)
