"""
공공데이터 품질진단 시스템 — 메인 진입점 (리디자인)
st.navigation 기반 단일 대시보드 앱

리디자인 컨셉:
  · 공공/행정 톤 — 딥 네이비(#102a4c) + 톤다운된 인스티튜셔널 블루(#2e5aa8)
  · Pretendard 본문, 정연한 1px 보더 + 4~5px 라운드 카드
  · 레드는 위험/오류 배지에만 최소 사용

실행:  streamlit run app.py
"""
import streamlit as st

# ── 전역 페이지 설정 (앱 전체에서 단 1회) ──────────
st.set_page_config(
    page_title="공공데이터 품질진단 시스템",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 전역 디자인 시스템 (모든 페이지 공통 스킨) ──────────
st.markdown("""
<style>
/* ===== 폰트 ===== */
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.css');

html, body, [class*="css"], [data-testid="stAppViewContainer"] *,
[data-testid="stSidebar"] * {
    font-family: 'Pretendard Variable', 'Pretendard', -apple-system, system-ui, sans-serif !important;
    word-break: keep-all;
}

/* ===== 디자인 토큰 =====
   navy   #102a4c   blue  #2e5aa8   bg  #eef1f6
   border #dfe4ec   ink   #16233d   sub #5b6678
*/

/* ===== 본문 배경 ===== */
[data-testid="stAppViewContainer"] { background: #eef1f6; }
[data-testid="stHeader"] { background: rgba(255,255,255,0.0); }
.block-container { padding-top: 2.0rem; padding-bottom: 3rem; max-width: 1180px; }

/* ===== 본문 타이포 ===== */
[data-testid="stMarkdownContainer"] h1 {
    font-size: 25px; font-weight: 800; color: #16233d;
    letter-spacing: -0.02em; margin-bottom: .25rem;
}
[data-testid="stMarkdownContainer"] h2 {
    font-size: 18px; font-weight: 800; color: #16233d;
    border-left: 4px solid #102a4c; padding-left: 11px; margin-top: 1.6rem;
}
[data-testid="stMarkdownContainer"] h3 {
    font-size: 15px; font-weight: 800; color: #16233d;
}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li { color: #3a4660; font-size: 13.5px; }

/* ===== 사이드바 ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(185deg, #0e2340 0%, #0a1a30 100%);
    border-right: 1px solid #0a1730;
    width: 290px !important;
}
[data-testid="stSidebar"] * { color: #cdd6ec !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] strong { color: #ffffff !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.09); margin: .8rem 0; }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color: #6b7ca0 !important; }

/* 사이드바 네비게이션 그룹 라벨 */
[data-testid="stSidebarNav"] ul { padding-top: .3rem; }
[data-testid="stSidebarNav"] [data-testid="stSidebarNavSeparator"] { display:none; }
[data-testid="stSidebarNav"] a {
    border-radius: 7px; margin: 1px 8px; padding: 7px 10px;
    transition: all .15s; color: #9aa7c4 !important; font-weight: 600;
}
[data-testid="stSidebarNav"] a:hover { background: rgba(255,255,255,0.07); color: #dfe7f5 !important; }
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(91,145,224,0.16) !important;
    box-shadow: inset 2px 0 0 #5b91e0;
    color: #ffffff !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] span { color:#ffffff !important; }

/* ===== 상태 배지 ===== */
.status-on  { background:#e9f4ee; color:#1f7a52 !important; padding:3px 11px;
              border-radius:12px; font-size:11px; font-weight:700; border:1px solid #c9e6d6; }
.status-off { background:#fbecec; color:#b23b3b !important; padding:3px 11px;
              border-radius:12px; font-size:11px; font-weight:700; border:1px solid #f0cccc; }

/* 사이드바 내 배지는 가독성 위해 밝은 톤 유지 */
[data-testid="stSidebar"] .status-on  { background: rgba(62,192,122,0.16); color:#7ee0a8 !important; border-color: rgba(62,192,122,0.3); }
[data-testid="stSidebar"] .status-off { background: rgba(220,80,80,0.16); color:#f0a0a0 !important; border-color: rgba(220,80,80,0.3); }

/* ===== 카드 / 컨테이너 보더 ===== */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff; border: 1px solid #dfe4ec !important;
    border-radius: 5px; box-shadow: 0 1px 2px rgba(16,42,76,0.03);
}

/* ===== 메트릭 ===== */
[data-testid="stMetric"] {
    background: #ffffff; border: 1px solid #dfe4ec; border-radius: 5px;
    padding: 14px 18px;
}
[data-testid="stMetricLabel"] p { color: #6c7689 !important; font-size: 12px !important; font-weight: 600; }
[data-testid="stMetricValue"] { font-size: 26px !important; font-weight: 800; color: #16233d; }
[data-testid="stMetricDelta"] { font-size: 12px; }

/* ===== 버튼 ===== */
.stButton > button {
    border-radius: 6px; font-weight: 700; font-size: 13.5px;
    border: 1px solid #d3d9e6; color: #3a4660; background: #ffffff;
    padding: .42rem 1.1rem; transition: all .14s;
}
.stButton > button:hover { border-color: #102a4c; color: #102a4c; background:#f6f8fc; }
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
    background: #102a4c; color: #ffffff; border-color: #102a4c;
}
.stButton > button[kind="primary"]:hover { background: #16335c; color:#fff; }
.stDownloadButton > button {
    border-radius: 6px; font-weight: 700; background: #2e5aa8;
    color: #fff; border: none; padding: .42rem 1.1rem;
}
.stDownloadButton > button:hover { background: #244a8c; color:#fff; }

/* ===== 탭 ===== */
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid #e1e6ee; }
.stTabs [data-baseweb="tab"] {
    font-weight: 700; font-size: 13.5px; color: #8a93a3;
    padding: 10px 18px; background: transparent;
}
.stTabs [aria-selected="true"] { color: #102a4c !important; }
.stTabs [data-baseweb="tab-highlight"] { background: #2e5aa8; height: 2px; }

/* ===== 입력 컨트롤 ===== */
[data-baseweb="input"], [data-baseweb="select"] > div, .stTextInput input, .stNumberInput input {
    border-radius: 6px !important;
}
.stSelectbox label, .stTextInput label, .stNumberInput label,
.stMultiSelect label, .stRadio label, .stTextArea label {
    font-size: 12px !important; font-weight: 700 !important; color: #3a4660 !important;
}

/* ===== 데이터프레임 / 테이블 ===== */
[data-testid="stDataFrame"], [data-testid="stTable"] {
    border: 1px solid #dfe4ec; border-radius: 5px; overflow: hidden;
}
[data-testid="stTable"] thead tr th {
    background: #102a4c; color: #cdd6ec; font-weight: 700; font-size: 11.5px;
}

/* ===== expander ===== */
[data-testid="stExpander"] {
    border: 1px solid #dfe4ec !important; border-radius: 5px !important; background:#fff;
}
[data-testid="stExpander"] summary { font-weight: 700; color: #16233d; }

/* ===== alert (info/success/warning/error) — 톤 정돈 ===== */
[data-testid="stAlert"] { border-radius: 6px; border: 1px solid #dfe4ec; }

/* ===== 진행 막대 ===== */
[data-testid="stProgress"] > div > div > div { background: #2e5aa8; }

/* ===== 코드/모노 ===== */
code, .qd-mono { font-family: 'SFMono-Regular', ui-monospace, Menlo, Consolas, monospace !important; }
</style>
""", unsafe_allow_html=True)


# ── 세션 상태 전역 초기화 (KeyError 방지) ──────────
for _k, _v in {
    "current_project": None,
    "connected": False,
    "connector": None,
    "diagnosis_queries": [],
    "diagnosis_raw_results": [],
}.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ── 페이지 정의 (워크플로우 단계별 그룹핑) ──────────
home = st.Page("pages/0_home.py", title="홈 대시보드", icon="🏠", default=True)

p_project = st.Page("pages/1_project.py",      title="프로젝트 관리",   icon="📋")
p_connect = st.Page("pages/2_data_connect.py", title="데이터 연결",     icon="🔌")

p_set     = st.Page("pages/3_diagnosis_set.py", title="진단 항목 설정",  icon="⚙️")
p_run     = st.Page("pages/4_diagnosis_run.py", title="진단 실행",       icon="▶️")
p_result  = st.Page("pages/5_result.py",        title="결과 분석",       icon="📈")

p_report  = st.Page("pages/6_report.py",   title="보고서 출력",        icon="📄")
p_erd     = st.Page("pages/7_erd.py",      title="ERD 자동화",         icon="🗺️")
p_std     = st.Page("pages/8_standard.py", title="AI 표준화 어드바이저", icon="🤖")

nav = st.navigation({
    "  ": [home],
    "① 준비":   [p_project, p_connect],
    "② 진단":   [p_set, p_run, p_result],
    "③ 산출물": [p_report, p_erd, p_std],
})


# ── 공통 사이드바: 현재 상태 + 진행 단계 ──────────
def render_sidebar_status():
    with st.sidebar:
        st.markdown("---")

        cp        = st.session_state.get("current_project")
        connected = st.session_state.get("connected", False)
        has_q     = bool(st.session_state.get("diagnosis_queries"))
        has_r     = bool(st.session_state.get("diagnosis_raw_results"))

        # 현재 프로젝트 카드
        if cp:
            org  = cp.get("org_name", "")
            proj = cp.get("project_name", "")
        else:
            org, proj = "프로젝트 미선택", "준비 단계에서 생성하세요"
        st.markdown(
            f"""<div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
                  border-radius:8px; padding:12px 13px;">
              <div style="font-size:10px; font-weight:700; letter-spacing:.08em; color:#6b7ca0; margin-bottom:6px;">현재 프로젝트</div>
              <div style="color:#fff; font-size:13px; font-weight:700; line-height:1.35;">{org}</div>
              <div style="color:#9aa7c4; font-size:11.5px; margin-top:1px;">{proj}</div>
            </div>""",
            unsafe_allow_html=True)

        # DB 연결 상태
        st.markdown("**🔌 DB 연결**")
        if connected:
            conn = st.session_state.get("connector")
            d = ""
            try:
                if conn and conn.engine:
                    d = f" · {conn.engine.dialect.name.upper()}"
            except Exception:
                pass
            st.markdown(f"<span class='status-on'>● 연결됨{d}</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span class='status-off'>● 미연결</span>", unsafe_allow_html=True)

        # 진행 단계 (가로 게이지 바)
        st.markdown("**📊 진행 단계**")
        steps = [
            ("1 프로젝트", bool(cp)),
            ("2 DB 연결",  connected),
            ("3 항목 설정", has_q),
            ("4 진단 실행", has_r),
            ("5 결과 분석", has_r),
            ("6 보고서",    has_r),
        ]
        bars = "".join(
            f"<div style='flex:1;height:4px;border-radius:2px;background:"
            f"{'#3ec07a' if done else 'rgba(255,255,255,0.12)'}'></div>"
            for _, done in steps
        )
        st.markdown(f"<div style='display:flex;gap:4px;margin:6px 0 10px'>{bars}</div>",
                    unsafe_allow_html=True)
        prog_html = ""
        for name, done in steps:
            icon  = "✅" if done else "⬜"
            color = "#cdd6ec" if done else "#6b7ca0"
            prog_html += f"<div style='font-size:11.5px;margin:2px 0;color:{color}'>{icon} {name}</div>"
        st.markdown(prog_html, unsafe_allow_html=True)

        st.markdown("---")
        st.caption("행정안전부 표준화 관리 매뉴얼 2026")
        st.caption("© 2026 품질진단 시스템")


render_sidebar_status()

# ── 선택된 페이지 실행 ──
nav.run()
