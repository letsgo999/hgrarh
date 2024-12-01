import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import platform

# 시각화 스타일 설정
plt.style.use('seaborn')
st.set_option('deprecation.showPyplotGlobalUse', False)

# 폰트 설정
if platform.system() == 'Linux':
    plt.rc('font', family='DejaVu Sans')
else:
    plt.rc('font', family='Malgun Gothic')
    
plt.rc('axes', unicode_minus=False)

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
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if chart_type == "선 그래프":
                sns.lineplot(data=df, x=x_col, y=y_col, marker='o')
            elif chart_type == "막대 그래프":
                sns.barplot(data=df, x=x_col, y=y_col)
            else:  # 산점도
                sns.scatterplot(data=df, x=x_col, y=y_col)
            
            plt.title(f"{x_col} vs {y_col}", pad=20)
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            st.pyplot(fig)
            plt.close()
            
            # 기본 통계 정보 표시
            st.subheader("📊 기본 통계 정보")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**{y_col} 통계:**")
                st.write(df[y_col].describe())
            
            with col2:
                st.write(f"**상관관계:**")
                if df[x_col].dtype.kind in 'biufc' and df[y_col].dtype.kind in 'biufc':
                    corr = df[x_col].corr(df[y_col])
                    st.write(f"{x_col}와 {y_col}의 상관계수: {corr:.3f}")
                else:
                    st.write("숫자형 데이터에 대해서만 상관관계를 계산할 수 있습니다.")
            
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
        st.write("CSV 파일의 형식을 확인해주세요.")
