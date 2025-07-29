import os
from typing import Optional

from qore_client.config import __api_endpoint__, __build_date__, __env__

# 빌드 환경 설정
BUILD_ENV = __env__
BUILD_DATE = __build_date__
API_ENDPOINT = __api_endpoint__

# 인증 정보
ACCESS_KEY: Optional[str] = os.getenv("QORE_ACCESS_KEY")
SECRET_KEY: Optional[str] = os.getenv("QORE_SECRET_KEY")
