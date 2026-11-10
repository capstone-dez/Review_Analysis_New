
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io

# ==================================
# 1. 페이지 설정
# ==================================

st.set_page_config(
    page_title="고객 리뷰 분석 시스템",
    page_icon="📊",
    layout="wide"
)

# ==================================
# 2. 제목
# ==================================

st.title("📊 고객 리뷰 데이터 분석 시스템")

st.write(
    "앱 리뷰 데이터를 활용하여 고객 만족도와 "
    "리뷰 현황을 분석합니다."
)

st.divider()

# ==================================
# 3. CSV 파일 업로드
# ==================================

st.subheader("01. 리뷰 데이터 업로드")

uploaded_file = st.file_uploader(
    "CSV 파일을 선택해 주세요.",
    type=["csv"]
)

if uploaded_file is not None:

    df = None

    # CSV 인코딩 확인
    for encoding in ["utf-8-sig", "cp949", "euc-kr", "utf-8"]:

        try:
            df = pd.read_csv(
                io.BytesIO(uploaded_file.getvalue()),
                encoding=encoding
            )
            break

        except UnicodeDecodeError:
            continue

    if df is None:
        st.error("CSV 파일을 읽을 수 없습니다.")

    elif df.empty:
        st.warning("데이터가 없습니다.")

    else:

        st.success("CSV 파일이 정상적으로 업로드되었습니다!")

        # ==================================
        # 4. 데이터 전처리
        # ==================================

        df.columns = df.columns.astype(str).str.strip()

        if "별점" not in df.columns:

            st.error("'별점' 컬럼을 찾을 수 없습니다.")

        else:

            df["별점"] = pd.to_numeric(
                df["별점"],
                errors="coerce"
            )

            rating_data = df["별점"].dropna()

            # ==================================
            # 5. 기본 데이터 정보
            # ==================================

            st.subheader("02. 데이터 기본 정보")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "전체 리뷰 수",
                    f"{len(df):,}건"
                )

            with col2:
                if len(rating_data) > 0:
                    st.metric(
                        "평균 별점",
                        f"{rating_data.mean():.2f}점"
                    )
                else:
                    st.metric("평균 별점", "분석 불가")

            with col3:
                if len(rating_data) > 0:
                    positive = (rating_data >= 4).sum()

                    st.metric(
                        "긍정 리뷰 수",
                        f"{positive:,}건"
                    )
                else:
                    st.metric("긍정 리뷰 수", "분석 불가")

            # ==================================
            # 6. 별점별 리뷰 분석
            # ==================================

            st.subheader("03. 별점별 리뷰 현황")

            if len(rating_data) > 0:

                # 1점부터 5점까지 집계
                rating_counts = (
                    rating_data[
                        rating_data.between(1, 5)
                    ]
                    .value_counts()
                    .reindex([1, 2, 3, 4, 5], fill_value=0)
                )

                x_labels = [
                    "1점", "2점", "3점", "4점", "5점"
                ]

                y_values = rating_counts.tolist()

                fig = go.Figure()

                fig.add_trace(
                    go.Bar(
                        x=x_labels,
                        y=y_values,
                        text=[f"{v:,}" for v in y_values],
                        textposition="outside",
                        textfont=dict(
                            size=14,
                            color="#000000"
                        ),
                        marker_color="#36845D",
                        hovertemplate=(
                            "%{x}: %{y:,}건"
                            "<extra></extra>"
                        )
                    )
                )

                fig.update_layout(
    title=dict(
        text="별점별 리뷰 분포",
        font=dict(
            size=22,
            color="#174D38"
        )
    ),

    xaxis=dict(
        title=dict(
            text="별점",
            font=dict(size=16, color="#000000")
        ),
        tickfont=dict(
            size=14,
            color="#000000"
        ),
        showgrid=False
    ),

    yaxis=dict(
        title=dict(
            text="리뷰 수",
            font=dict(size=16, color="#000000")
        ),
        tickfont=dict(
            size=13,
            color="#000000"
        ),
        rangemode="tozero",
        gridcolor="#DCE5DE"
    ),

    font=dict(
        family="Malgun Gothic",
        size=14,
        color="#000000"
    ),

    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",

    height=430,
    showlegend=False,

    margin=dict(
        t=70,
        b=60,
        l=50,
        r=30
    )
)


                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.caption(
                    "※ 막대 위 숫자는 해당 별점의 리뷰 개수입니다."
                )

            else:
                st.warning("유효한 별점 데이터가 없습니다.")

            # ==================================
            # 7. 리뷰 데이터 확인
            # ==================================

            st.subheader("04. 리뷰 데이터 확인")

            st.write(
                f"총 {len(df):,}건의 데이터가 있습니다."
            )

            st.dataframe(
                df,
                use_container_width=True,
                height=350
            )

else:

    st.info("먼저 CSV 파일을 업로드해 주세요.")
