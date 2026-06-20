import streamlit as st
import pandas as pd
import sqlite3
import os

HISTORY_DB = "history.db"

# 6대 품질영역 카테고리 컬러 (전 페이지 공통 팔레트)
DIM_COLORS = {
    "완전성": "#1f4e87", "일관성": "#2c7a6b", "정확성": "#c0851e",
    "유용성": "#5a6b8c", "유일성": "#7a4a78", "유효성": "#b04a3e",
}


def render_home():
    """홈 대시보드 — 전체 현황 요약 + 워크플로우 안내 (리디자인)"""

    # ── 네이비 히어로 헤더 ──
    st.markdown("""
    <div style="background:linear-gradient(120deg,#0e2340 0%,#143a6b 62%,#1c4f8f 100%);
                border-radius:8px;padding:34px 38px;margin-bottom:18px;position:relative;overflow:hidden;">
      <div style="position:absolute;top:-80px;right:-40px;width:320px;height:320px;
                  background:radial-gradient(circle,rgba(46,90,168,0.45),rgba(46,90,168,0) 70%);"></div>
      <div style="position:relative;">
        <div style="color:#7fa8e0;font-size:12px;font-weight:700;letter-spacing:0.1em;margin-bottom:9px;">
          행정안전부 · 공공데이터베이스 표준화 관리 매뉴얼 2026</div>
        <div style="color:#fff;font-size:29px;font-weight:800;letter-spacing:-0.02em;line-height:1.2;">
          공공데이터 품질진단 시스템</div>
        <div style="color:#b3c2dd;font-size:14px;margin-top:11px;max-width:640px;line-height:1.6;">
          Oracle · MySQL · PostgreSQL · 파일(CSV·Excel)을 연결해 <b style="color:#fff;">6대 품질영역</b>을
          자동 진단하고, AI 표준화 어드바이저로 컬럼 표준화까지 한 번에 처리합니다.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 현재 세션 상태 ──
    cp        = st.session_state.get("current_project")
    connected = st.session_state.get("connected", False)
    queries   = st.session_state.get("diagnosis_queries", [])
    results   = st.session_state.get("diagnosis_raw_results", [])

    total_errors = 0
    if results:
        _df = pd.DataFrame(results)
        if 'error_cnt' in _df.columns:
            total_errors = int(_df[_df['error_cnt'] >= 0]['error_cnt'].sum())

    st.markdown("## 현재 작업 현황")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("현재 프로젝트", (cp.get('project_name', '미설정')[:12] if cp else "미설정"))
    c2.metric("DB 연결",      "연결됨" if connected else "미연결")
    c3.metric("진단 항목",    f"{len(results)} 개")
    c4.metric("총 오류 건수", f"{total_errors:,} 건")

    # ── 전체 이력 요약 ──
    st.markdown("## 전체 진단 이력")
    try:
        con = sqlite3.connect(HISTORY_DB)
        rows = con.execute("""
            SELECT p.org_name, d.diagnosed_at,
                   CASE WHEN d.total_items > 0
                        THEN ROUND((1.0 - CAST(d.error_items AS FLOAT)/d.total_items)*100,1)
                        ELSE 100.0 END AS quality_score
            FROM diagnosis_history d
            JOIN projects p ON d.project_id = p.id
            ORDER BY d.diagnosed_at DESC LIMIT 50
        """).fetchall()
        con.close()
    except Exception:
        rows = []

    if rows:
        hist = pd.DataFrame(rows, columns=['기관명', '진단일시', '품질점수'])
        h1, h2, h3, h4 = st.columns(4)
        h1.metric("총 진단 횟수",   f"{len(hist)} 회")
        h2.metric("참여 기관 수",   f"{hist['기관명'].nunique()} 개")
        h3.metric("평균 품질 점수", f"{hist['품질점수'].mean():.1f} 점")
        h4.metric("최고 품질 점수", f"{hist['품질점수'].max():.1f} 점")

        recent = hist.head(10).sort_values('진단일시')
        if len(recent) > 1:
            import plotly.express as px
            # 점수 구간별 인스티튜셔널 컬러
            bar_colors = ['#1f7a52' if s >= 90 else ('#2e5aa8' if s >= 80 else '#c8821a')
                          for s in recent['품질점수']]
            fig = px.bar(recent, x='진단일시', y='품질점수', height=260,
                         text='품질점수')
            fig.update_traces(marker_color=bar_colors, width=0.55,
                              textposition='outside',
                              textfont=dict(size=11, color='#5b6678'),
                              cliponaxis=False)
            fig.update_layout(
                yaxis_range=[0, 105], margin=dict(l=0, r=0, t=14, b=0),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Pretendard, sans-serif', color='#5b6678', size=11),
                xaxis=dict(showgrid=False, title=None),
                yaxis=dict(gridcolor='#eef1f6', title=None, zeroline=False),
            )
            fig.add_hline(y=80, line_dash="dash", line_color="#e0b070",
                          annotation_text="기준선 80점",
                          annotation_font=dict(color="#c8821a", size=11))
            with st.container(border=True):
                st.markdown("**최근 10회 진단 품질 점수**")
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("아직 진단 이력이 없습니다. 보고서 출력 시 이력이 자동 저장됩니다.")

    # ── 6대 품질 영역 ──
    st.markdown("## 6대 품질 진단 영역")
    areas = [
        ("완전성", "필수값 누락·공백값을 검사해 데이터가 빠짐없이 채워졌는지 확인", "COMPLETENESS"),
        ("일관성", "앞뒤 공백 등 형식의 일관성을 점검해 표기 통일성을 확인", "CONSISTENCY"),
        ("정확성", "비정상 특수문자 혼입 여부를 검사해 값의 정확성을 확인", "ACCURACY"),
        ("유용성", "더미·미상 데이터를 검출해 실제 활용 가능한 값인지 확인", "USEFULNESS"),
        ("유일성", "단일키·복합키 중복을 검사해 데이터의 유일성을 확인", "UNIQUENESS"),
        ("유효성", "날짜 형식·숫자 혼입을 검사해 정의된 형식에 맞는지 확인", "VALIDITY"),
    ]
    cols = st.columns(3)
    for i, (name, desc, code) in enumerate(areas):
        color = DIM_COLORS[name]
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #dfe4ec;border-top:3px solid {color};
                        border-radius:5px;padding:16px 18px;margin-bottom:14px;min-height:118px;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <span style="width:10px;height:10px;border-radius:3px;background:{color};"></span>
                <span style="font-size:15px;font-weight:800;color:#16233d;">{name}</span>
                <span style="font-size:9.5px;color:#9aa3b2;margin-left:auto;font-family:monospace;">{code}</span>
              </div>
              <div style="font-size:12.5px;color:#5b6678;line-height:1.55;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


render_home()
