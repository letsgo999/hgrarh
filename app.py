import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import numpy as np
from matplotlib import font_manager
import os
import subprocess
import sys

# 한글 폰트 설정을 위한 함수
def setup_korean_font():
    # 우분투 환경에서 한글 폰트 설치
    try:
        os.system('apt-get update -y')
        os.system('apt-get install -y fonts-nanum')
        os.system('fc-cache -fv')
        
        # 나눔고딕 폰트 경로
        font_dirs = ['/usr/share/fonts/truetype/nanum']
        font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
        
        for font_file in font_files:
            font_manager.fontManager.addfont(font_file)
            
        # 기본 폰트를 나눔고딕으로 설정
        plt.rcParams['font.family'] = 'NanumGothic'
    except:
        # 폰트 설치 실패시 대체 방안
        plt.rcParams['font.family'] = 'Arial Unicode MS'
    finally:
        plt.rcParams['axes.unicode_minus'] = False

# 메인 앱 시작
st.set_page_config(page_title="데이터 시각화 도구", layout="wide")

# 한글 폰트 설정 적용
setup_korean_font()

# 메인 앱 타이틀
st.title("📊 데이터 시각화 도구")

# CSV 파일 업로드
st.subheader("📁 데이터 업로드")
data_file = st.file_uploader("CSV 파일을 업로드해주세요", type=["csv"])

if data_file:
    try:
        # UTF-8로 데이터 읽기 시도
        try:
            df = pd.read_csv(data_file, encoding='utf-8')
        except UnicodeDecodeError:
            # UTF-8 실패시 CP949로 시도
            df = pd.read_csv(data_file, encoding='cp949')
        
        # 데이터프레임 미리보기
        st.subheader("📋 데이터 미리보기")
        st.dataframe(df.head())
        
        # 컬럼 선택
        st.subheader("📈 차트 설정")
        columns = df.columns.tolist()
        
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("X축 선택", columns)
        with col2:
            y_col = st.selectbox("Y축 선택", columns)
        
        # 차트 종류 선택
        chart_type = st.selectbox(
            "차트 종류 선택",
            ["막대 그래프", "선 그래프", "산점도"]
        )
        
        # 차트 생성
        if st.button("차트 생성"):
            # 새로운 figure 생성
            fig = plt.figure(figsize=(12, 6))
            
            # 차트 그리기
            if chart_type == "막대 그래프":
                plt.bar(range(len(df[x_col])), df[y_col])
                plt.xticks(range(len(df[x_col])), df[x_col], rotation=45)
            elif chart_type == "선 그래프":
                plt.plot(df[x_col], df[y_col], marker='o')
                plt.xticks(rotation=45)
            else:  # 산점도
                plt.scatter(df[x_col], df[y_col])
            
            # 차트 스타일링
            plt.title(f"{x_col} vs {y_col}", pad=20, fontsize=16)
            plt.xlabel(x_col, fontsize=12)
            plt.ylabel(y_col, fontsize=12)
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # 레이아웃 조정
            plt.tight_layout()
            
            # 차트 표시
            st.pyplot(fig)
            
            # 기본 통계 정보
            if np.issubdtype(df[y_col].dtype, np.number):
                st.subheader("📊 기본 통계 정보")
                stats = df[y_col].describe()
                st.write(f"**{y_col} 통계:**")
                st.write(stats)
            
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
        st.write("CSV 파일의 형식을 확인해주세요.")
