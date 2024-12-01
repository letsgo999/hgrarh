import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl

# 기본 설정
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
st.set_option('deprecation.showPyplotGlobalUse', False)

# 메인 앱 타이틀
st.title("📊 데이터 시각화 도구")

# CSV 파일 업로드
st.subheader("📁 데이터 업로드")
data_file = st.file_uploader("CSV 파일을 업로드해주세요", type=["csv"])

if data_file:
    try:
        # 데이터 읽기
        df = pd.read_csv(data_file)
        
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
            ["선 그래프", "막대 그래프", "산점도"]
        )
        
        # 차트 생성
        if st.button("차트 생성"):
            st.subheader("🎨 시각화 결과")
            
            # 새로운 figure 생성
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if chart_type == "선 그래프":
                plt.plot(df[x_col], df[y_col], marker='o')
            elif chart_type == "막대 그래프":
                plt.bar(df[x_col], df[y_col])
            else:  # 산점도
                plt.scatter(df[x_col], df[y_col])
            
            # 차트 꾸미기
            plt.title(f"{x_col} vs {y_col}")
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            
            # x축 레이블 회전
            if len(str(df[x_col].iloc[0])) > 10:
                plt.xticks(rotation=45, ha='right')
            
            # 그리드 추가
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # 레이아웃 조정
            plt.tight_layout()
            
            # 차트 표시
            st.pyplot(fig)
            plt.close()
            
            # 기본 통계 정보 표시
            st.subheader("📊 기본 통계 정보")
            
            # 수치형 데이터인 경우에만 통계 정보 표시
            if df[y_col].dtype.kind in 'biufc':
                stats = df[y_col].describe()
                st.write(f"**{y_col} 통계:**")
                st.write(stats)
            else:
                st.write(f"{y_col}은(는) 수치형 데이터가 아니어서 통계를 계산할 수 없습니다.")
            
    except Exception as e:
        st.error("오류가 발생했습니다. CSV 파일의 형식을 확인해주세요.")
        st.write(f"상세 오류: {str(e)}")
