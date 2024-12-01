import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib as mpl
import platform

# 기본 설정
plt.style.use('default')
mpl.use('Agg')
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Malgun Gothic'

# 메인 앱 시작
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
            fig, ax = plt.subplots(figsize=(12, 6))
            
            if chart_type == "막대 그래프":
                ax.bar(df[x_col], df[y_col])
            elif chart_type == "선 그래프":
                ax.plot(df[x_col], df[y_col], marker='o')
            else:  # 산점도
                ax.scatter(df[x_col], df[y_col])
            
            # 라벨 설정
            ax.set_title(f"{x_col} vs {y_col}", fontsize=16)
            ax.set_xlabel(x_col, fontsize=12)
            ax.set_ylabel(y_col, fontsize=12)
            
            # x축 라벨 회전
            plt.xticks(rotation=45, ha='right')
            
            # 그리드 추가
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # 레이아웃 조정
            plt.tight_layout()
            
            # 차트 표시
            st.pyplot(fig)
            plt.close()
            
            # 통계 정보 표시
            if np.issubdtype(df[y_col].dtype, np.number):
                st.subheader("📊 기본 통계 정보")
                stats = df[y_col].describe()
                st.write(f"**{y_col} 통계:**")
                st.write(stats)
                
    except Exception as e:
        st.error("오류가 발생했습니다. CSV 파일의 형식을 확인해주세요.")
        st.write(f"상세 오류: {str(e)}")
