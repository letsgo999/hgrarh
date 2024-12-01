import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import platform
import matplotlib.font_manager as fm
import os

# 한글 폰트 설정 함수
def set_korean_font():
    # 나눔고딕 폰트 다운로드 및 설치
    import requests
    import zipfile
    from io import BytesIO
    
    # 폰트 파일 다운로드 (나눔고딕)
    font_url = "https://raw.githubusercontent.com/googlefonts/nanum-gothic/main/fonts/NanumGothic-Regular.ttf"
    response = requests.get(font_url)
    
    # fonts 디렉토리 생성
    os.makedirs('fonts', exist_ok=True)
    
    # 폰트 파일 저장
    font_path = 'fonts/NanumGothic-Regular.ttf'
    with open(font_path, 'wb') as f:
        f.write(response.content)
    
    # 폰트 등록
    font_path = fm.fontManager.addfont(font_path)
    
    # matplotlib 폰트 설정
    plt.rc('font', family='NanumGothic')
    mpl.rcParams['axes.unicode_minus'] = False

# 한글 폰트 설정 적용
set_korean_font()

# 메인 앱 타이틀
st.title("한글 깨짐 방지 차트 생성기")

# CSV 파일 업로드
st.subheader("데이터 업로드 및 시각화")
data_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if data_file:
    try:
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
            plt.title(f"{y_col} 분석 차트", pad=20)
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.grid(True)
            plt.tight_layout()  # 레이아웃 자동 조정
            st.pyplot(fig)
            plt.close()  # 메모리 관리를 위해 figure 닫기
            
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
