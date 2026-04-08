import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- 페이지 설정 및 한글 폰트 ---
st.set_page_config(page_title="데이터 시각화 도구", layout="wide")

# Windows: Malgun Gothic / Mac: AppleGothic
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# --- 사이드바: 파일 업로드 ---
st.sidebar.header("📂 데이터 업로드")
uploaded_file = st.sidebar.file_uploader("CSV 파일을 선택하세요", type=["csv"])

if uploaded_file is not None:
    # 데이터 불러오기
    df = pd.read_csv(uploaded_file)

    # --- 메인 화면: 데이터 미리보기 ---
    st.title("📊 데이터 분석 및 시각화")

    st.subheader("1. 데이터 미리보기")
    st.dataframe(df.head(10))  # 상위 10개 행 표시

    st.divider()  # 구분선

    # --- 사이드바: 컬럼 선택 UI ---
    st.sidebar.header("⚙️ 시각화 설정")

    # 수치형 컬럼과 범주형 컬럼 분류
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(exclude=['number']).columns.tolist()
    all_cols = df.columns.tolist()

    if len(all_cols) >= 2:
        x_axis = st.sidebar.selectbox("X축 (설명 변수)", options=all_cols, index=0)
        y_axis = st.sidebar.selectbox("Y축 (반응 변수 - 수치 권장)", options=all_cols, index=1 if len(all_cols) > 1 else 0)

        # 범주형 항목 선택 (색상 구분)
        color_axis = st.sidebar.selectbox("색상 구분 (범주형 컬럼)", options=[None] + cat_cols)

        # 추세선 옵션 (X, Y가 모두 수치형일 때 권장)
        show_reg = st.sidebar.checkbox("추세선(회귀선) 표시", value=True)

        # --- 메인 화면: 산점도 출력 ---
        st.subheader(f"2. {x_axis} vs {y_axis} 산점도")

        fig, ax = plt.subplots(figsize=(10, 5))

        if show_reg and (x_axis in num_cols and y_axis in num_cols):
            # 회귀선 그리기
            sns.regplot(data=df, x=x_axis, y=y_axis, scatter=False, color='salmon', ax=ax)
            sns.scatterplot(data=df, x=x_axis, y=y_axis, hue=color_axis, s=100, ax=ax)
        else:
            # 일반 산점도
            sns.scatterplot(data=df, x=x_axis, y=y_axis, hue=color_axis, s=100, ax=ax)
            if show_reg:
                st.warning("⚠️ 추세선은 X축과 Y축이 모두 숫자 데이터여야 표시하기 적합합니다.")

        ax.set_title(f"[{x_axis}]와 [{y_axis}]의 상관관계")
        ax.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)

    else:
        st.error("데이터에 분석 가능한 컬럼이 부족합니다.")

else:
    # 파일이 없을 때 보여주는 기본 화면
    st.title("📈 데이터 시각화 프로그램")
    st.info("왼쪽 사이드바에서 CSV 파일을 업로드해 주세요.")

    # 샘플 데이터 형식 안내
    st.write("예시 데이터 구조:")
    example_df = pd.DataFrame({
        '공부시간': [2, 4, 6],
        '점수': [60, 80, 95],
        '전공': ['공학', '인문', '자연']
    })
    st.table(example_df)