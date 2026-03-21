"""
K-HOPE 플랫폼 타당성 분석 대시보드
화순전남대학교병원 - 한국인 암 환자 맞춤형 디지털 스마트 바이오 임상시험 체계
Developed by TeamNubiz
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from data.virtual_data import (
    PROJECT, TOTAL_SCORE, TOTAL_GRADE, TOTAL_MAX, ONE_LINE,
    DOMAIN_SCORES, BUDGET, BUDGET_COMPOSITION, KPI_TARGETS,
    KPI_YEARLY, KPI_YEARS, SUB_PROJECTS, PARTNERS,
    SWOT, MARKET_DCT, MARKET_AI_CLINICAL, MARKET_OOC, MARKET_CRO_KR,
    BENCHMARK_TABLE, KR_CLINICAL_RANK, KR_CLINICAL_APPROVAL,
    RISKS, REVENUE_MODEL, ROADMAP, RECOMMENDATIONS,
)

# ─── 색상 팔레트 ───
MINT = "#00c2a8"
PURPLE = "#8b5cf6"
AMBER = "#e8b84b"
RED = "#ef4444"
BLUE = "#3b82f6"
PINK = "#ec4899"
GRAY = "#9ca3af"
TEXT = "#e8eaf2"
BG_CARD = "linear-gradient(135deg, #101828, #1a2540)"
BORDER = "#1e293b"

# ─── Plotly 공통 레이아웃 ───
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Noto Sans KR, sans-serif", color=TEXT, size=13),
    margin=dict(l=40, r=40, t=50, b=40),
)


# ═══════════════════════════════════════════════════
# Page Config
# ═══════════════════════════════════════════════════
st.set_page_config(
    page_title="K-HOPE 타당성 분석 | TeamNubiz",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800;900&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0&display=swap');
html, body, [class*="st-"], h1, h2, h3, h4, h5, h6, p, span, div, li, a, button, label {
    font-family: 'Noto Sans KR', sans-serif !important;
}
[data-testid="stIconMaterial"], [data-testid="stIconMaterial"] * {
    font-family: 'Material Symbols Rounded' !important;
}
h1 { font-weight: 900 !important; }
h2 { font-weight: 700 !important; }
h3 { font-weight: 600 !important; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] { background: transparent !important; }
.stDeployButton {display: none;}

/* Sidebar */
section[data-testid="stSidebar"] { background: #060b16; border-right: 1px solid #1e293b; }
.nav-link {
    display: block; padding: 5px 12px; margin: 2px 0;
    color: #9ca3af; text-decoration: none !important;
    border-radius: 6px; font-size: 0.82rem; transition: all 0.2s ease;
}
.nav-link:hover { color: #00c2a8 !important; background: rgba(0,194,168,0.08); padding-left: 16px; }
.nav-active { color: #00c2a8 !important; background: rgba(0,194,168,0.10); font-weight: 600; }

/* Metric Cards */
.mc {
    background: linear-gradient(135deg, #101828, #1a2540);
    border: 1px solid #1e293b; border-radius: 16px; padding: 24px; text-align: center;
}
.mc-v { font-size: 2rem; font-weight: 900; margin: 8px 0 4px; }
.mc-l { font-size: 0.82rem; color: #9ca3af; }

/* Hero Score Card */
.hero-score {
    background: linear-gradient(135deg, #0f172a 0%, #1a1040 50%, #0f172a 100%);
    border: 1px solid #2d1b69; border-radius: 24px; padding: 40px 32px;
    text-align: center; position: relative; overflow: hidden;
}
.hero-score::before {
    content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(ellipse at center, rgba(139,92,246,0.08) 0%, transparent 60%);
}
.hero-score .score-num {
    font-size: 5rem; font-weight: 900; line-height: 1;
    background: linear-gradient(135deg, #00c2a8, #8b5cf6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-score .score-max { font-size: 1.5rem; color: #6b7280; font-weight: 400; }
.hero-score .score-grade {
    display: inline-block; margin-top: 8px; padding: 4px 20px;
    background: rgba(0,194,168,0.15); color: #00c2a8; border-radius: 20px;
    font-weight: 700; font-size: 1.1rem; letter-spacing: 2px;
}

/* SWOT */
.swot-card {
    border-radius: 16px; padding: 20px; min-height: 200px;
    border: 1px solid #1e293b;
}
.swot-s { background: linear-gradient(135deg, rgba(0,194,168,0.12), rgba(0,194,168,0.04)); border-color: rgba(0,194,168,0.3); }
.swot-w { background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(239,68,68,0.04)); border-color: rgba(239,68,68,0.3); }
.swot-o { background: linear-gradient(135deg, rgba(59,130,246,0.12), rgba(59,130,246,0.04)); border-color: rgba(59,130,246,0.3); }
.swot-t { background: linear-gradient(135deg, rgba(232,184,75,0.12), rgba(232,184,75,0.04)); border-color: rgba(232,184,75,0.3); }
.swot-title { font-weight: 800; font-size: 1.1rem; margin-bottom: 12px; }
.swot-item { font-size: 0.85rem; color: #d1d5db; padding: 4px 0; line-height: 1.5; }
.swot-item b { color: #e8eaf2; }

/* Risk badge */
.risk-critical { background: rgba(239,68,68,0.2); color: #ef4444; padding: 2px 10px; border-radius: 10px; font-size: 0.78rem; font-weight: 600; }
.risk-high { background: rgba(232,184,75,0.2); color: #e8b84b; padding: 2px 10px; border-radius: 10px; font-size: 0.78rem; font-weight: 600; }
.risk-medium { background: rgba(59,130,246,0.2); color: #3b82f6; padding: 2px 10px; border-radius: 10px; font-size: 0.78rem; font-weight: 600; }

/* Timeline */
.tl-card {
    background: linear-gradient(135deg, #101828, #1a2540);
    border: 1px solid #1e293b; border-radius: 16px; padding: 24px;
    border-left: 4px solid #00c2a8; margin-bottom: 16px;
}
.tl-card h4 { margin: 0 0 4px; color: #00c2a8; font-weight: 700; }
.tl-phase { display: inline-block; background: rgba(139,92,246,0.2); color: #8b5cf6; padding: 2px 12px; border-radius: 12px; font-size: 0.78rem; font-weight: 600; margin-bottom: 8px; }
.tl-budget { color: #e8b84b; font-weight: 600; font-size: 0.9rem; }
.tl-item { font-size: 0.84rem; color: #d1d5db; padding: 3px 0; line-height: 1.5; }
.tl-milestone { font-size: 0.82rem; color: #9ca3af; margin-top: 8px; padding: 8px 12px; background: rgba(0,194,168,0.06); border-radius: 8px; }

/* Recommendation card */
.rec-card {
    background: linear-gradient(135deg, #101828, #1a2540);
    border: 1px solid #1e293b; border-radius: 16px; padding: 20px;
    border-top: 3px solid #8b5cf6;
}
.rec-num { font-size: 1.8rem; font-weight: 900; color: #8b5cf6; opacity: 0.6; }
.rec-title { font-weight: 700; color: #e8eaf2; font-size: 1rem; margin: 4px 0 8px; }
.rec-detail { font-size: 0.84rem; color: #9ca3af; line-height: 1.6; }

/* Section divider */
.section-divider {
    margin: 2.5rem 0 1.5rem;
    border: 0; height: 1px;
    background: linear-gradient(90deg, transparent, #1e293b 20%, #1e293b 80%, transparent);
}

/* Sub project card */
.sp-card {
    background: linear-gradient(135deg, #101828, #1a2540);
    border: 1px solid #1e293b; border-radius: 16px; padding: 20px;
    height: 100%;
}
.sp-id { font-weight: 800; font-size: 1rem; color: #00c2a8; }
.sp-name { font-weight: 600; font-size: 0.9rem; color: #e8eaf2; margin: 4px 0 8px; }
.sp-goal { font-size: 0.82rem; color: #9ca3af; line-height: 1.5; }
.sp-tag { display: inline-block; background: rgba(139,92,246,0.15); color: #a78bfa; padding: 2px 8px; border-radius: 8px; font-size: 0.72rem; margin: 2px 2px 0 0; }

/* Table custom */
.custom-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.custom-table th { background: #101828; color: #9ca3af; padding: 10px 12px; text-align: left; border-bottom: 1px solid #1e293b; font-weight: 600; }
.custom-table td { padding: 10px 12px; border-bottom: 1px solid #1e293b; color: #d1d5db; }
.custom-table tr:hover td { background: rgba(0,194,168,0.04); }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# Sidebar
# ═══════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1.2rem 0 0.5rem;">
        <div style="font-size:1.5rem; font-weight:900; background:linear-gradient(135deg,#00c2a8,#8b5cf6);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent; letter-spacing:2px;">NUBIZ</div>
        <div style="font-size:0.72rem; color:#9ca3af; margin-top:4px;">K-HOPE 타당성 분석 대시보드</div>
    </div>
    <hr style="border-color:#1e293b;">
    """, unsafe_allow_html=True)

    page = st.radio(
        "메뉴",
        ["종합 대시보드", "SWOT 분석", "시장 분석", "리스크 분석", "전략 제언"],
        label_visibility="collapsed",
    )

    st.markdown('<hr style="border-color:#1e293b;">', unsafe_allow_html=True)
    st.markdown("""
    <a class="nav-link" href="https://www.teamnubiz.com" target="_blank">🏠 홈</a>
    <a class="nav-link" href="https://www.teamnubiz.com/projects" target="_blank">📂 프로젝트</a>
    <hr style="border-color:#1e293b;">
    <div style="text-align:center; padding:6px 0;">
        <a href="https://teamnubiz.com" target="_blank" style="color:#00c2a8; text-decoration:none; font-size:0.8rem;">teamnubiz.com</a><br>
        <span style="color:#4b5563; font-size:0.7rem;">contact@teamnubiz.com</span>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════
def metric_card(label, value, color=MINT):
    """메트릭 카드 HTML 반환"""
    return f'<div class="mc"><div class="mc-l">{label}</div><div class="mc-v" style="color:{color};">{value}</div></div>'


def make_radar_chart():
    """영역별 레이더 차트 생성"""
    categories = list(DOMAIN_SCORES.keys())
    values = [DOMAIN_SCORES[c]["pct"] for c in categories]
    # 레이더 차트는 닫혀야 하므로 첫 값을 마지막에 추가
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill="toself",
        fillcolor="rgba(0,194,168,0.15)",
        line=dict(color=MINT, width=2),
        marker=dict(size=8, color=MINT),
        name="K-HOPE 점수",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 100],
                gridcolor="rgba(255,255,255,0.08)",
                tickfont=dict(size=10, color=GRAY),
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.08)",
                tickfont=dict(size=12, color=TEXT),
            ),
        ),
        showlegend=False,
        height=400,
        margin=dict(l=80, r=80, t=40, b=40),
    )
    return fig


def make_gauge_chart():
    """종합 점수 게이지 차트"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=TOTAL_SCORE,
        number=dict(
            font=dict(size=60, color=TEXT, family="Noto Sans KR"),
            suffix="<span style='font-size:24px;color:#6b7280;'> / 100</span>",
        ),
        gauge=dict(
            axis=dict(range=[0, 100], tickwidth=1, tickcolor=GRAY, dtick=20,
                      tickfont=dict(size=11, color=GRAY)),
            bar=dict(color="rgba(0,0,0,0)"),
            bgcolor="rgba(255,255,255,0.03)",
            borderwidth=0,
            steps=[
                dict(range=[0, 40], color="rgba(239,68,68,0.15)"),
                dict(range=[40, 60], color="rgba(232,184,75,0.15)"),
                dict(range=[60, 80], color="rgba(59,130,246,0.15)"),
                dict(range=[80, 100], color="rgba(0,194,168,0.15)"),
            ],
            threshold=dict(
                line=dict(color=MINT, width=4),
                thickness=0.85,
                value=TOTAL_SCORE,
            ),
        ),
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=280,
        margin=dict(l=30, r=30, t=30, b=10),
    )
    return fig


def make_budget_pie():
    """사업비 구성 파이 차트"""
    labels = list(BUDGET_COMPOSITION.keys())
    values = list(BUDGET_COMPOSITION.values())
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=[MINT, PURPLE]),
        textinfo="label+percent",
        textfont=dict(size=13, color=TEXT),
        hovertemplate="%{label}<br>%{value}억원<br>%{percent}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=300,
        showlegend=False,
        annotations=[dict(
            text=f"<b>{BUDGET['total']}</b><br>억원",
            x=0.5, y=0.5, font=dict(size=18, color=TEXT), showarrow=False,
        )],
    )
    return fig


def make_kpi_trend_chart(selected_kpis=None):
    """KPI 연차별 추이 차트"""
    colors = [MINT, PURPLE, AMBER, BLUE, PINK, RED, "#10b981"]
    if selected_kpis is None:
        selected_kpis = list(KPI_YEARLY.keys())

    fig = go.Figure()
    for i, kpi in enumerate(selected_kpis):
        if kpi in KPI_YEARLY:
            fig.add_trace(go.Bar(
                name=kpi,
                x=KPI_YEARS,
                y=KPI_YEARLY[kpi],
                marker_color=colors[i % len(colors)],
                text=KPI_YEARLY[kpi],
                textposition="outside",
                textfont=dict(size=11),
            ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        barmode="group",
        height=400,
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="건/명"),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
            font=dict(size=11),
        ),
    )
    return fig


def make_market_chart():
    """시장 규모 차트 (다중 시장)"""
    fig = go.Figure()

    markets = [
        (MARKET_DCT, MINT, "DCT"),
        (MARKET_AI_CLINICAL, PURPLE, "AI 임상시험"),
    ]
    for market, color, name in markets:
        years = [d["year"] for d in market["data"]]
        values = [d["value"] for d in market["data"]]
        fig.add_trace(go.Scatter(
            x=years, y=values, name=f"{name} (CAGR {market['cagr']})",
            mode="lines+markers",
            line=dict(color=color, width=3),
            marker=dict(size=8),
            hovertemplate=f"{name}<br>%{{x}}년: $%{{y}}억<extra></extra>",
        ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=400,
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="연도"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="시장 규모 (억 달러)"),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
            font=dict(size=11),
        ),
    )
    return fig


def make_ooc_market_chart():
    """OoC 시장 규모 차트"""
    years = [d["year"] for d in MARKET_OOC["data"]]
    values = [d["value"] for d in MARKET_OOC["data"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[str(y) for y in years], y=values,
        marker=dict(
            color=values,
            colorscale=[[0, PURPLE], [1, MINT]],
        ),
        text=[f"${v}억" for v in values],
        textposition="outside",
        textfont=dict(size=12, color=TEXT),
        hovertemplate="OoC 시장<br>%{x}년: $%{y}억<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=350,
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="시장 규모 (억 달러)"),
        showlegend=False,
    )
    return fig


def make_risk_heatmap():
    """리스크 히트맵 (산점도)"""
    fig = go.Figure()

    grade_colors = {"심각": RED, "높음": AMBER, "중간": BLUE}
    for risk in RISKS:
        fig.add_trace(go.Scatter(
            x=[risk["prob"] * 100],
            y=[risk["impact"] * 100],
            mode="markers+text",
            marker=dict(
                size=30 + risk["prob"] * risk["impact"] * 40,
                color=grade_colors.get(risk["grade"], GRAY),
                opacity=0.7,
                line=dict(width=2, color="rgba(255,255,255,0.2)"),
            ),
            text=[f"R{risk['id']}"],
            textposition="middle center",
            textfont=dict(size=11, color="white", family="Noto Sans KR"),
            name=f"R{risk['id']}: {risk['name']}",
            hovertemplate=(
                f"<b>{risk['name']}</b><br>"
                f"발생가능성: {risk['prob']*100:.0f}%<br>"
                f"영향도: {risk['impact']*100:.0f}%<br>"
                f"등급: {risk['grade']}<extra></extra>"
            ),
        ))

    # 배경 영역
    fig.add_shape(type="rect", x0=60, y0=60, x1=100, y1=100,
                  fillcolor="rgba(239,68,68,0.06)", line=dict(width=0))
    fig.add_shape(type="rect", x0=30, y0=60, x1=60, y1=100,
                  fillcolor="rgba(232,184,75,0.06)", line=dict(width=0))
    fig.add_shape(type="rect", x0=60, y0=30, x1=100, y1=60,
                  fillcolor="rgba(232,184,75,0.06)", line=dict(width=0))
    fig.add_shape(type="rect", x0=0, y0=0, x1=30, y1=30,
                  fillcolor="rgba(59,130,246,0.06)", line=dict(width=0))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=450,
        xaxis=dict(
            title="발생 가능성 (%)", range=[25, 80],
            gridcolor="rgba(255,255,255,0.05)",
            zeroline=False,
        ),
        yaxis=dict(
            title="영향도 (%)", range=[45, 100],
            gridcolor="rgba(255,255,255,0.05)",
            zeroline=False,
        ),
        showlegend=True,
        legend=dict(
            font=dict(size=10), bgcolor="rgba(0,0,0,0)",
            yanchor="top", y=0.99, xanchor="left", x=0.01,
        ),
    )
    return fig


def make_revenue_model_chart():
    """수익 모델 차트 (수평 막대)"""
    models = [r["model"] for r in REVENUE_MODEL]
    mins = [r["min"] for r in REVENUE_MODEL]
    maxs = [r["max"] for r in REVENUE_MODEL]
    ranges = [r["max"] - r["min"] for r in REVENUE_MODEL]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=models, x=mins, orientation="h",
        marker=dict(color="rgba(0,0,0,0)"),
        showlegend=False,
        hoverinfo="skip",
    ))
    fig.add_trace(go.Bar(
        y=models, x=ranges, orientation="h",
        marker=dict(
            color=[MINT, PURPLE, AMBER, BLUE, PINK],
            opacity=0.8,
        ),
        text=[f"{mi}~{ma}억원" for mi, ma in zip(mins, maxs)],
        textposition="outside",
        textfont=dict(size=12, color=TEXT),
        name="예상 연간 규모",
        hovertemplate="%{y}<br>예상: %{text}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        barmode="stack",
        height=350,
        xaxis=dict(
            title="예상 연간 규모 (억원)",
            gridcolor="rgba(255,255,255,0.05)",
        ),
        yaxis=dict(autorange="reversed"),
        showlegend=False,
    )
    return fig


def make_cro_market_chart():
    """국내 CRO 시장 추이"""
    years = [d["year"] for d in MARKET_CRO_KR["data"]]
    values = [d["value"] for d in MARKET_CRO_KR["data"]]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=values,
        mode="lines+markers+text",
        line=dict(color=AMBER, width=3),
        marker=dict(size=10, color=AMBER),
        text=[f"${v}억" for v in values],
        textposition="top center",
        textfont=dict(size=11),
        hovertemplate="국내 CRO 시장<br>%{x}년: $%{y}억<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=350,
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="시장 규모 (억 달러)"),
        showlegend=False,
    )
    return fig


# ═══════════════════════════════════════════════════
# Pages
# ═══════════════════════════════════════════════════

def page_dashboard():
    """종합 대시보드 페이지"""
    # ─── 헤더 ───
    st.markdown(f"""
    <div style="margin-bottom: 8px;">
        <span style="font-size:0.85rem; color:{GRAY};">화순전남대학교병원</span>
    </div>
    <h1 style="margin-top:0; margin-bottom:4px; font-size:2.2rem;">
        <span style="background:linear-gradient(135deg,{MINT},{PURPLE});
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;">K-HOPE</span>
        플랫폼 타당성 분석
    </h1>
    <p style="color:{GRAY}; font-size:0.9rem; margin-bottom:1.5rem;">
        {PROJECT['full_name']}<br>
        사업 기간: {PROJECT['period']} | 총 사업비: {BUDGET['total']}억원
    </p>
    """, unsafe_allow_html=True)

    # ─── 종합 점수 + 레이더 ───
    col_gauge, col_radar = st.columns([1, 1])
    with col_gauge:
        st.markdown("#### 종합 타당성 점수")
        st.plotly_chart(make_gauge_chart(), use_container_width=True)
        st.markdown(f"""
        <div style="text-align:center;">
            <span class="hero-score score-grade" style="display:inline-block; padding:4px 20px;
            background:rgba(0,194,168,0.15); color:#00c2a8; border-radius:20px;
            font-weight:700; font-size:1.1rem; letter-spacing:2px;">
                {TOTAL_GRADE} 등급
            </span>
        </div>
        <p style="color:{GRAY}; font-size:0.82rem; text-align:center; margin-top:12px; padding: 0 12px;">
            {ONE_LINE}
        </p>
        """, unsafe_allow_html=True)

    with col_radar:
        st.markdown("#### 영역별 점수 (20점 만점)")
        st.plotly_chart(make_radar_chart(), use_container_width=True)

    # ─── 영역별 점수 카드 ───
    cols = st.columns(5)
    domain_colors = [MINT, PURPLE, AMBER, BLUE, PINK]
    for i, (domain, info) in enumerate(DOMAIN_SCORES.items()):
        with cols[i]:
            st.markdown(metric_card(
                domain.replace("타당성", ""),
                f"{info['score']}<span style='font-size:0.9rem;color:{GRAY};'>/20</span>",
                domain_colors[i],
            ), unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ─── 핵심 KPI ───
    st.markdown("#### 핵심 성과 목표 (3년 누적)")
    kpi_items = list(KPI_TARGETS.items())
    row1 = kpi_items[:5]
    row2 = kpi_items[5:]

    cols1 = st.columns(len(row1))
    for i, (k, v) in enumerate(row1):
        with cols1[i]:
            unit = "건" if "논문" in k or "특허" in k or "시험" in k or "IND" in k or "IRB" in k or "기술" in k else "명+"
            st.markdown(metric_card(k, f"{v}{unit}", domain_colors[i % len(domain_colors)]), unsafe_allow_html=True)

    cols2 = st.columns(len(row2))
    for i, (k, v) in enumerate(row2):
        with cols2[i]:
            unit = "건" if "논문" in k or "특허" in k or "시험" in k or "IND" in k or "IRB" in k or "기술" in k else "명+"
            st.markdown(metric_card(k, f"{v}{unit}", domain_colors[(i + len(row1)) % len(domain_colors)]), unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ─── 예산 & KPI 추이 ───
    col_budget, col_kpi = st.columns([1, 2])
    with col_budget:
        st.markdown("#### 사업비 구성")
        st.plotly_chart(make_budget_pie(), use_container_width=True)
        for item in BUDGET["yearly"]:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:6px 12px; margin:2px 0;
                        background:rgba(255,255,255,0.02); border-radius:8px;">
                <span style="color:{GRAY}; font-size:0.85rem;">{item['year']}</span>
                <span style="color:{TEXT}; font-weight:600; font-size:0.85rem;">{item['amount']}억원</span>
            </div>
            """, unsafe_allow_html=True)

    with col_kpi:
        st.markdown("#### KPI 연차별 추이")
        kpi_options = list(KPI_YEARLY.keys())
        default_kpis = ["SCI 논문", "임상시험 수행", "비임상시험 수행", "인력양성"]
        selected = st.multiselect("표시할 KPI 선택", kpi_options, default=default_kpis, label_visibility="collapsed")
        if selected:
            st.plotly_chart(make_kpi_trend_chart(selected), use_container_width=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ─── 3대 세부과제 ───
    st.markdown("#### 3대 세부과제")
    sp_cols = st.columns(3)
    sp_colors = [MINT, PURPLE, AMBER]
    for i, sp in enumerate(SUB_PROJECTS):
        with sp_cols[i]:
            tags_html = "".join([f'<span class="sp-tag">{kw}</span>' for kw in sp["keywords"]])
            st.markdown(f"""
            <div class="sp-card" style="border-top: 3px solid {sp_colors[i]};">
                <div class="sp-id">{sp['id']}</div>
                <div class="sp-name">{sp['name']}</div>
                <div class="sp-goal">{sp['goal']}</div>
                <div style="margin-top:10px;">{tags_html}</div>
            </div>
            """, unsafe_allow_html=True)


def page_swot():
    """SWOT 분석 페이지"""
    st.markdown(f"""
    <h1 style="font-size:2rem;">
        <span style="background:linear-gradient(135deg,{MINT},{PURPLE});
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;">SWOT</span> 분석
    </h1>
    <p style="color:{GRAY}; font-size:0.88rem; margin-bottom:1.5rem;">K-HOPE 플랫폼의 내부 역량과 외부 환경 분석</p>
    """, unsafe_allow_html=True)

    def swot_section(items, css_class, title, color):
        items_html = ""
        for item in items:
            items_html += f'<div class="swot-item"><b>{item["title"]}</b></div>'
        return f"""
        <div class="swot-card {css_class}">
            <div class="swot-title" style="color:{color};">{title}</div>
            {items_html}
        </div>
        """

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(swot_section(SWOT["strengths"], "swot-s", "S - 강점 (Strengths)", MINT), unsafe_allow_html=True)
    with col2:
        st.markdown(swot_section(SWOT["weaknesses"], "swot-w", "W - 약점 (Weaknesses)", RED), unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown(swot_section(SWOT["opportunities"], "swot-o", "O - 기회 (Opportunities)", BLUE), unsafe_allow_html=True)
    with col4:
        st.markdown(swot_section(SWOT["threats"], "swot-t", "T - 위협 (Threats)", AMBER), unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ─── 상세 확장 패널 ───
    st.markdown("#### 항목별 상세 분석")

    sections = [
        ("strengths", "강점 (Strengths)", MINT),
        ("weaknesses", "약점 (Weaknesses)", RED),
        ("opportunities", "기회 (Opportunities)", BLUE),
        ("threats", "위협 (Threats)", AMBER),
    ]
    for key, label, color in sections:
        st.markdown(f'<p style="color:{color}; font-weight:700; margin-top:16px; margin-bottom:4px;">{label}</p>', unsafe_allow_html=True)
        for item in SWOT[key]:
            with st.expander(item["title"]):
                st.markdown(f'<p style="font-size:0.88rem; color:#d1d5db; line-height:1.7;">{item["detail"]}</p>', unsafe_allow_html=True)


def page_market():
    """시장 분석 페이지"""
    st.markdown(f"""
    <h1 style="font-size:2rem;">
        <span style="background:linear-gradient(135deg,{MINT},{PURPLE});
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;">시장</span> 분석
    </h1>
    <p style="color:{GRAY}; font-size:0.88rem; margin-bottom:1.5rem;">K-HOPE 핵심 기술 분야의 글로벌 시장 동향</p>
    """, unsafe_allow_html=True)

    # ─── 핵심 시장 지표 카드 ───
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.markdown(metric_card("DCT 시장 (2030)", "$186.2억", MINT), unsafe_allow_html=True)
    with mc2:
        st.markdown(metric_card("AI 임상시험 (2030)", "$54억+", PURPLE), unsafe_allow_html=True)
    with mc3:
        st.markdown(metric_card("OoC 시장 (2030)", "$9.5억", AMBER), unsafe_allow_html=True)
    with mc4:
        st.markdown(metric_card("국내 CRO (2025)", "$27.7억", BLUE), unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ─── DCT & AI 임상시험 시장 ───
    col_main, col_ooc = st.columns([1, 1])
    with col_main:
        st.markdown("#### DCT & AI 임상시험 시장 전망")
        st.plotly_chart(make_market_chart(), use_container_width=True)

    with col_ooc:
        st.markdown(f"#### Organ-on-Chip 시장 (CAGR {MARKET_OOC['cagr']})")
        st.plotly_chart(make_ooc_market_chart(), use_container_width=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ─── 국내 CRO 시장 ───
    col_cro, col_rank = st.columns([1, 1])
    with col_cro:
        st.markdown(f"#### 국내 CRO 시장 추이 (CAGR {MARKET_CRO_KR['cagr']})")
        st.plotly_chart(make_cro_market_chart(), use_container_width=True)

    with col_rank:
        st.markdown("#### 한국 임상시험 글로벌 순위 변화")
        rank_fig = go.Figure()
        years_r = [str(r["year"]) for r in KR_CLINICAL_RANK]
        ranks = [r["rank"] for r in KR_CLINICAL_RANK]
        shares = [r["share"] for r in KR_CLINICAL_RANK]

        rank_fig.add_trace(go.Bar(
            x=years_r, y=ranks,
            marker=dict(color=[MINT, RED]),
            text=[f"{r}위 ({s}%)" for r, s in zip(ranks, shares)],
            textposition="outside",
            textfont=dict(size=14, color=TEXT),
        ))
        rank_fig.update_layout(
            **PLOTLY_LAYOUT,
            height=350,
            yaxis=dict(
                autorange="reversed", title="글로벌 순위",
                gridcolor="rgba(255,255,255,0.05)", range=[0, 8],
            ),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            showlegend=False,
        )
        st.plotly_chart(rank_fig, use_container_width=True)
        st.markdown(f'<p style="color:{RED}; font-size:0.82rem; text-align:center;">2023년 4위 -> 2024년 6위로 하락 (호주/스페인/독일에 추월)</p>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ─── 국내 경쟁 현황 비교표 ───
    st.markdown("#### 국내 경쟁 사업 비교")
    table_rows = ""
    for b in BENCHMARK_TABLE:
        highlight = 'style="color:#00c2a8; font-weight:600;"' if "K-HOPE" in b["name"] else ""
        table_rows += f"""
        <tr>
            <td {highlight}>{b['name']}</td>
            <td>{b['area']}</td>
            <td>{b['diff']}</td>
        </tr>
        """
    st.markdown(f"""
    <table class="custom-table">
        <thead>
            <tr><th>기관/사업</th><th>핵심 영역</th><th>K-HOPE 대비 차별점</th></tr>
        </thead>
        <tbody>{table_rows}</tbody>
    </table>
    """, unsafe_allow_html=True)


def page_risk():
    """리스크 분석 페이지"""
    st.markdown(f"""
    <h1 style="font-size:2rem;">
        <span style="background:linear-gradient(135deg,{MINT},{PURPLE});
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;">리스크</span> 분석
    </h1>
    <p style="color:{GRAY}; font-size:0.88rem; margin-bottom:1.5rem;">핵심 리스크 5건의 발생가능성 x 영향도 분석 및 대응 전략</p>
    """, unsafe_allow_html=True)

    # ─── 리스크 히트맵 ───
    st.markdown("#### 리스크 히트맵")
    st.plotly_chart(make_risk_heatmap(), use_container_width=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ─── 대응 전략 표 ───
    st.markdown("#### 리스크 대응 전략")
    for risk in RISKS:
        grade_class = {"심각": "risk-critical", "높음": "risk-high", "중간": "risk-medium"}.get(risk["grade"], "risk-medium")
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#101828,#1a2540); border:1px solid #1e293b;
                    border-radius:12px; padding:16px 20px; margin-bottom:10px;">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
                <span style="font-weight:800; color:{TEXT}; font-size:1rem;">R{risk['id']}</span>
                <span style="font-weight:600; color:{TEXT}; font-size:0.92rem;">{risk['name']}</span>
                <span class="{grade_class}">{risk['grade']}</span>
                <span style="color:{GRAY}; font-size:0.8rem; margin-left:auto;">
                    발생가능성 {risk['prob']*100:.0f}% | 영향도 {risk['impact']*100:.0f}%
                </span>
            </div>
            <div style="font-size:0.84rem; color:#9ca3af; line-height:1.6; padding-left:4px;">
                {risk['response']}
            </div>
        </div>
        """, unsafe_allow_html=True)


def page_strategy():
    """전략 제언 페이지"""
    st.markdown(f"""
    <h1 style="font-size:2rem;">
        <span style="background:linear-gradient(135deg,{MINT},{PURPLE});
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;">전략</span> 제언
    </h1>
    <p style="color:{GRAY}; font-size:0.88rem; margin-bottom:1.5rem;">K-HOPE 사업의 성공적 추진을 위한 핵심 권고사항 및 로드맵</p>
    """, unsafe_allow_html=True)

    # ─── 핵심 권고사항 ───
    st.markdown("#### 핵심 권고사항 5가지")
    for i, rec in enumerate(RECOMMENDATIONS):
        col_num, col_content = st.columns([1, 11])
        with col_num:
            st.markdown(f'<div class="rec-num">0{i+1}</div>', unsafe_allow_html=True)
        with col_content:
            st.markdown(f"""
            <div class="rec-card">
                <div class="rec-title">{rec['title']}</div>
                <div class="rec-detail">{rec['detail']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("", unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ─── 수익 모델 ───
    st.markdown("#### 사업 종료 후 자립 운영 수익 모델 (2028년~)")
    col_rev_chart, col_rev_detail = st.columns([3, 2])
    with col_rev_chart:
        st.plotly_chart(make_revenue_model_chart(), use_container_width=True)

    with col_rev_detail:
        total_min = sum(r["min"] for r in REVENUE_MODEL)
        total_max = sum(r["max"] for r in REVENUE_MODEL)
        st.markdown(f"""
        <div class="mc" style="margin-bottom:12px;">
            <div class="mc-l">예상 연간 총 수익</div>
            <div class="mc-v" style="color:{MINT};">{total_min}~{total_max}억원</div>
        </div>
        """, unsafe_allow_html=True)
        for r in REVENUE_MODEL:
            st.markdown(f"""
            <div style="padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.05);">
                <div style="font-size:0.88rem; color:{TEXT}; font-weight:600;">{r['model']}</div>
                <div style="font-size:0.78rem; color:{GRAY};">{r['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ─── 로드맵 타임라인 ───
    st.markdown("#### 연차별 로드맵")
    tl_colors = [MINT, PURPLE, AMBER]
    for i, phase in enumerate(ROADMAP):
        items_html = "".join([f'<div class="tl-item">- {item}</div>' for item in phase["items"]])
        st.markdown(f"""
        <div class="tl-card" style="border-left-color:{tl_colors[i]};">
            <h4 style="color:{tl_colors[i]};">{phase['year']}</h4>
            <span class="tl-phase">{phase['phase']}</span>
            <span class="tl-budget" style="margin-left:12px;">{phase['budget']}</span>
            {items_html}
            <div class="tl-milestone">마일스톤: {phase['milestones']}</div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# Page Router
# ═══════════════════════════════════════════════════
PAGE_MAP = {
    "종합 대시보드": page_dashboard,
    "SWOT 분석": page_swot,
    "시장 분석": page_market,
    "리스크 분석": page_risk,
    "전략 제언": page_strategy,
}

PAGE_MAP[page]()
