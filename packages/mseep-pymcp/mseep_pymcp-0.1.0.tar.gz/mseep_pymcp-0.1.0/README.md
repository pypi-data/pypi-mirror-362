[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/hoonzinope-pymcp-mysql-badge.png)](https://mseep.ai/app/hoonzinope-pymcp-mysql)

# pymcp

`pymcp`는 FastMCP를 기반으로 한 Python 프로젝트로, MySQL 데이터베이스와 상호작용할 수 있는 도구를 제공합니다. 이 프로젝트는 서버와 클라이언트 간의 통신을 지원하며, 다양한 도구를 통해 데이터를 조회하고 분석할 수 있습니다.

## 프로젝트 구조

```
pymcp/
├── client.py          # 클라이언트 코드
├── main.py            # 서버 실행 코드
├── src/
│   ├── env.py         # 로컬 환경 설정
│   ├── env_dev.py     # 개발 환경 설정
│   ├── mcp_instance.py # MCP 인스턴스 초기화
│   ├── mysql_tool.py  # MySQL 관련 도구 정의
├── pyproject.toml     # 프로젝트 메타데이터 및 의존성
├── requirements.txt   # 의존성 목록
└── README.md          # 프로젝트 설명
```

## 설치 및 실행

### 1. 의존성 설치

Python 3.13 이상이 필요합니다. 의존성을 설치하려면 아래 명령어를 실행하세요:

```bash
pip install -r requirements.txt
```

### 2. 서버 실행

서버를 실행하려면 `main.py`를 실행하세요:

```bash
python main.py
```

서버는 기본적으로 `0.0.0.0:8080`에서 실행됩니다.

### 3. 클라이언트 실행

클라이언트를 실행하려면 `client.py`를 실행하세요:

```bash
python client.py
```

클라이언트는 서버와 통신하여 MySQL 쿼리를 실행하거나 도구 목록을 조회할 수 있습니다.

## 환경 설정

환경에 따라 MySQL 설정이 다르게 적용됩니다:

- **로컬 환경**: `src/env.py`
- **개발 환경**: `src/env_dev.py`

환경은 `APP_ENV` 환경 변수를 통해 설정할 수 있습니다. 기본값은 `local`입니다.

```bash
export APP_ENV=dev  # 개발 환경 설정
```

## 제공 도구

서버에서 제공하는 도구는 다음과 같습니다:

1. **`describe_tools`**  
   사용 가능한 도구 목록과 사용법을 설명합니다.

2. **`query_mysql(sql: str)`**  
   주어진 SQL 쿼리를 실행하고 결과를 반환합니다.  
   예시: `query_mysql("SELECT * FROM users LIMIT 10;")`

## 주요 파일 설명

### `main.py`

서버를 실행하는 진입점입니다. MCP 인스턴스를 초기화하고 도구를 등록한 뒤 서버를 실행합니다.

### `client.py`

서버와 상호작용하는 클라이언트 코드입니다. 서버에 연결하여 도구를 호출할 수 있습니다.

### `src/mysql_tool.py`

MySQL 관련 도구를 정의한 파일입니다. `query_mysql`와 같은 도구를 통해 SQL 쿼리를 실행할 수 있습니다.

### `src/env.py` 및 `src/env_dev.py`

MySQL 연결 설정을 포함한 환경 변수 파일입니다. 환경에 따라 적절한 설정을 로드합니다.
