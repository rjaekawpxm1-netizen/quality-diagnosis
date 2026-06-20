# 🏛️ 공공데이터 품질진단 시스템

행정안전부 공공데이터베이스 표준화 관리 매뉴얼 2026 기반  
Oracle / MySQL / PostgreSQL / 파일(CSV·Excel) 지원

---

## 📁 디렉토리 구조

```
quality_diagnosis/
├── app.py                  # Streamlit 메인 진입점
├── requirements.txt        # 의존성 목록
├── .env                    # 환경변수 (직접 생성)
├── history.db              # 진단 이력 DB (자동 생성)
│
├── core/
│   ├── connector.py        # DB 연결 (Oracle Wallet/TNS/Host, MySQL, PostgreSQL)
│   ├── query_builder.py    # 진단 쿼리 생성 엔진
│   ├── diagnosis_engine.py # 진단 실행 엔진
│   ├── report_generator.py # 엑셀·PDF 보고서 생성
│   ├── standard_loader.py  # 표준화 가이드 RAG
│   └── llm_advisor.py      # Claude API 연동
│
├── pages/
│   ├── 1_project.py        # 프로젝트 관리
│   ├── 2_data_connect.py   # DB 연결
│   ├── 3_diagnosis_set.py  # 진단 항목 설정
│   ├── 4_diagnosis_run.py  # 진단 실행
│   ├── 5_result.py         # 결과 분석
│   ├── 6_report.py         # 보고서 출력
│   ├── 7_erd.py            # ERD 자동화
│   └── 8_standard.py       # AI 표준화 어드바이저
│
├── templates/
│   ├── completeness.yaml   # 완전성 진단 규칙
│   ├── consistency.yaml    # 일관성 진단 규칙
│   ├── accuracy.yaml       # 정확성 진단 규칙
│   ├── usefulness.yaml     # 유용성 진단 규칙
│   ├── uniqueness.yaml     # 유일성 진단 규칙
│   └── validity.yaml       # 유효성 진단 규칙
│
└── standards/
    └── 공공데이터베이스.pdf  # 표준화 가이드 (직접 복사)
```

---

## ⚡ 빠른 시작

### 1. 의존성 설치

```bash
cd quality_diagnosis
pip install -r requirements.txt
```

Oracle 사용 시 추가:
```bash
pip install oracledb
```

### 2. 한글 폰트 설치 (PDF 출력용)

```bash
# Ubuntu / Debian
sudo apt-get install fonts-nanum
fc-cache -fv
```

### 3. 표준화 가이드 문서 배치

```bash
mkdir -p standards
# 공공데이터베이스 표준화 관리 매뉴얼 PDF를 standards/ 폴더에 복사
cp 공공데이터베이스.pdf standards/
```

### 4. 환경변수 설정 (선택 — AI 기능 사용 시)

```bash
cp .env.example .env
# .env 파일 열고 ANTHROPIC_API_KEY 입력
```

### 5. 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속

---

## 🔌 DB 연결 방법

### Oracle Wallet (공공기관 Cloud DB)
1. `[2] 데이터 연결` → `🔐 Oracle (Wallet)` 탭 선택
2. Wallet 폴더 파일 전체 업로드 (`cwallet.sso`, `tnsnames.ora`, `sqlnet.ora` 등)
3. Network Alias (예: `dqmdb_high`), User ID, Password 입력

### Oracle Host
1. `🔶 Oracle (host)` 탭 선택
2. Host, Port(1521), Service Name(또는 SID), User ID, Password 입력

### 파일 업로드 (CSV / Excel)
1. `📁 파일 업로드` 탭 선택
2. CSV 또는 Excel 파일 업로드 → 자동으로 SQLite에 적재

---

## 🤖 AI 기능 설정 (선택)

AI 기능(표준화 추천, ERD 관계 추론, 진단 결과 분석)은 Claude API 키가 있을 때만 동작합니다.  
**API 키 없이도** 규칙 기반 추천과 ERD 생성은 정상 동작합니다.

```bash
# .env 파일에 입력
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

---

## 📋 진단 워크플로우

```
[1] 프로젝트 생성  →  [2] DB 연결  →  [3] 진단 항목 설정
         ↓
[4] 진단 실행  →  [5] 결과 분석  →  [6] 보고서 출력 (엑셀·PDF)
         ↓
[7] ERD 자동화  →  [8] AI 표준화 추천
```

---

## 📦 주요 의존성

| 패키지 | 용도 |
|---|---|
| streamlit | 웹 UI 프레임워크 |
| sqlalchemy | DB 추상화 레이어 |
| oracledb | Oracle DB 연결 |
| pandas | 데이터 처리 |
| openpyxl | 엑셀 보고서 생성 |
| reportlab | PDF 보고서 생성 |
| plotly | 인터랙티브 차트 |
| requests | Claude API 호출 |
| pyyaml | 진단 규칙 템플릿 |

---

## ❓ 자주 묻는 문제

**Q. PDF에 한글이 깨져요**  
A. `sudo apt-get install fonts-nanum && fc-cache -fv` 실행 후 재시작

**Q. Oracle Wallet 연결이 안 돼요**  
A. Wallet 폴더에 `cwallet.sso`, `tnsnames.ora`, `sqlnet.ora` 파일이 모두 있는지 확인

**Q. AI 추천이 "API 키 없음"으로 뜨는데 규칙 기반으로 쓰고 싶어요**  
A. 정상입니다. API 키 없이도 규칙 기반 추천이 자동으로 동작합니다.

**Q. 대용량 테이블(100만 건+) 진단이 느려요**  
A. 진단 쿼리는 집계 쿼리라 빠르게 동작합니다. 드릴다운(원본 추적)은 최대 1000건으로 제한됩니다.