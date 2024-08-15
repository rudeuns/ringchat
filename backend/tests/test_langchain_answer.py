import os
import sys

from dotenv import load_dotenv
from langchain_core.documents import Document
from utils.get_langchain_answer import get_langchain_answer

# .env 파일 로드
load_dotenv()

# 테스트할 문서 목록 생성
documents = [
    Document(page_content="Python은 인터프리터 방식의 고수준, 범용 프로그래밍 언어입니다. Python의 설계 철학은 코드 가독성을 강조하며, 이는 눈에 띄는 공백 사용으로 이루어집니다."),
    Document(page_content="JavaScript, 흔히 JS로 약칭되며, ECMAScript 사양을 준수하는 프로그래밍 언어입니다. JavaScript는 고수준, 종종 JIT 컴파일되며, 다중 패러다임을 지원합니다."),
    Document(page_content="LangChain은 언어 모델에 의해 구동되는 애플리케이션을 개발하기 위한 프레임워크입니다. 최신 자연어 처리 기술을 활용한 애플리케이션을 구축할 수 있도록 설계되었습니다.")
]

# 문서와 관련된 첫 번째 질문 설정
question1 = "Python의 설계 철학은 무엇인가요?"

# 세션 ID 설정
session_id = "test_session"

# 첫 번째 질문에 대한 응답
response1 = get_langchain_answer(documents, question1, session_id)
print("첫 번째 질문에 대한 응답:")
print(response1)

# 두 번째 질문 설정
question2 = "내 이름은 애플이야. 내 이름이 뭐야?"

# 두 번째 질문에 대한 응답
response2 = get_langchain_answer(documents, question2, session_id)
print("\n두 번째 질문에 대한 응답:")
print(response2)

# 세 번째 질문 설정 (이전 대화를 참조하는 질문)
question3 = "내 이름이 뭐였어?"

# 세 번째 질문에 대한 응답
response3 = get_langchain_answer(documents, question3, session_id)
print("\n세 번째 질문에 대한 응답:")
print(response3)

session_id = "test_session2"

# 네 번째 질문 설정
question4 = "내 이름이 뭐였어?"

# 네 번째 질문에 대한 응답 -> 답변을 못 할 것으로 예상
response4 = get_langchain_answer(documents, question4, session_id)
print("\n네 번째 질문에 대한 응답:")
print(response4)