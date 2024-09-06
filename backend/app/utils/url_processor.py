import re

import requests
from requests.exceptions import ConnectionError
from requests.exceptions import RequestException
from requests.exceptions import SSLError
from requests.exceptions import Timeout


def is_https_url(url):
    """https 프로토콜 요청이 가능한 주소인가 판단하는 함수

    Args:
        url (str): http 프로토콜을 사용하여 인터넷에서 웹 페이지를 요청하는 주소

    Returns:
        Boolean: True or False
    """
    # 정규 표현식 패턴: 'https://'로 시작하고, 정상적인 도메인 형식인지 확인
    pattern = r"^https://(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}(?:[/\?#]\S*)?$"
    return bool(re.match(pattern, url, re.IGNORECASE))


def can_parse_url(url):
    """파싱이 가능한 url인가 판단하는 함수

    Args:
        url (str): http 프로토콜을 사용하여 인터넷에서 웹 페이지를 요청하는 주소

    Returns:
        url (str) or Boolean : 파싱이 가능한 url 일 경우 url을 반환하고 아닐 경우 False를 반환
    """
    try:
        # 헤더만 확인해서 정상적인 요청인가 확인
        response = requests.head(url, timeout=5, allow_redirects=True)

        if 200 <= response.status_code < 300:
            return url

        elif 300 <= response.status_code < 400:
            if "Location" in response.headers:
                return response.headers["Location"]
            else:
                return False

        else:
            return False

    except SSLError:
        print("SSL/TLS 인증 문제 발생")
        return False

    except (Timeout, ConnectionError):
        print("네트워크 문제 또는 타임아웃 발생")
        return False

    except RequestException as e:
        print(f"요청 실패 사유: {e}")
        return False


def is_valid_url(url):
    """유효한 url인가 판단하는 함수

    Args:
        url (str): http 프로토콜을 사용하여 인터넷에서 웹 페이지를 요청하는 주소

    Returns:
        Boolean: True or False
    """

    if url.startswith("https://"):
        if is_https_url(url) and can_parse_url(url):
            return True
    else:
        # https://로 시작하도록 url 수정
        url = "https://" + url.lstrip("http://").rstrip("/")

        if is_https_url(url) and can_parse_url(url):
            return True

        else:
            return False
