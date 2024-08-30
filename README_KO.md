<div align="center">
<img width="20%" src="https://github.com/user-attachments/assets/0a36e495-4467-4fdb-ac65-36c8590d6200">

<h4>링쳇은 🤖 URL 🔗 기반 챗봇 서비스 입니다.</h4>
<p>
"링쳇"은 "Ring"과 "Chatbot의 합성어 입니다. "Ring"은 URL 링크가 담고 있는 문서, 챗봇 그리고 사용자를 연결한다는 것을 상징합니다. "Ring"과 "Link"의 첫 음절이 동일하여 자연스럽게 연상이 됩니다. 
또한, "Ring"은 반지의 이미지를 연상시키고, 링쳇에서 제공하는 답변이 신뢰성있음을 암시합니다. 

</p>

</div>

## <div align="center">링쳇의🤖 핵심 기능</div>

1️⃣ `3가지 지표와 함께 링크 추천`<br>

- 평점
- 첨부된 수 
- 총 북마크 수 

2️⃣ `맞춤화된 문서 분석` <br>


3️⃣ `답변 내용 정리` 

<details open>
<summary>
 화면
</summary> <br />

<p align="center">
    <img width="49%" src="https://github.com/user-attachments/assets/73b16abf-ba93-40f3-b5ae-0d8321704b1b" alt="login"/>
&nbsp;
    <img width="49%" src="https://github.com/user-attachments/assets/4a1cbfb3-b1a6-44e3-a1d8-685f4376d855" alt="chatroom"/>
</p>

<p align="center">
    <img width="49%" src="https://github.com/user-attachments/assets/a15d8cde-3a50-479f-bea7-32406d3cb4e1" alt="link"/>
&nbsp;
    <img width="49%" src="https://github.com/user-attachments/assets/f1d86218-aad6-4f92-9d74-7819a17867d0" alt="message"/>
</p>


</details>

## <div align="center">서비스 아키텍처</div>

<div align="center">
<img width="95%" src="https://github.com/user-attachments/assets/e6a7022b-4de4-4eee-ba6b-7a9ffa8e89f0">

<br>

이 부분에서는 프로젝트의 핵심 구성요소에 대한 `개요`를 설명합니다. <br>
각 `기술 스택`에 해당하는 `장점`, `단점` 및 이 프로젝트를 위해 `선택한 이유`를 소개합니다.  

<br>

| 기술 | 선택한 이유 | 장점 | 한계 |
|---|---|---|---|
| Docker | 개발환경의 일관성 및 빠른 배포 | 서로 다른 개발환경에서 발생하는 라이브러리 종속성 문제 해결 <br> 배포시 확장에 용이함 | 컨테이너 이미지 관리의 복잡성 <br> docker 사용에 익숙하지 않으면 개발 시간 지연 가능성 초래 |
| FastAPI | API 개발 시 자동 문서화 기능 및 비동기 처리를 지원하기 때문에 개발 생산성이 높음. <br> 본 프로젝트에 필수 사항들을 쉽게 충족시켜줌. | 비동기 처리 지원 <br> 효율적인 리소스 활용 <br> Swagger 지원 <br> Pydantic 활용으로 데이터 유효성 검사 용이 | 비동기 프로그래밍에 대한 학습이 필요. <br> flask에 비해 커뮤니티 규모가 작음. |
| Langchain | 본 프로젝트는 기존에 가지고 있던 llm의 한계를 극복하고자 하는 기능이 포함되어 있음. in-context learning 방식을 쉽게 구현할 수 있는 프레임워크 중 하나인 langchain이 가장 대중적이고 구현이 직관적임. | 다양한 도구 지원으로 여러가지 기능 확장이 용이 <br> 직관적인 API로 개발이 비교적 쉬움 | 추상화 수준이 높아 세밀한 제어는 어려울 수 있다. <br> 개발된지 오래되지 않은 프레임워크라 정보 습득의 어려움 그리고 잦은 버그 발생 가능성 |
| Next.js | frontend 기술 보유자의 기술 스택이었기 때문. <br> 비교적 빠른 개발이 가능했기 때문. | SSR, SSG 지원 <br> 검색 엔진 최적화 개선 <br> 풍부한 커뮤니티 | 데이터가 자주 변경되는 페이지에서는 SSR시 매번 서버에서 렌더링 해야 하므로 성능 저하가 발생할 수 있음. <br> React에 대한 이해가 필요하여 진입장벽이 있음. |
| Oracle 23ai | Vector 컬럼을 지원하고, DB내 유사도 검색이 가능했기 때문에. 본 프로젝트에서는 url 추천 시 유사도 검색이 빈번할 것으로 예상되었기 때문에. | AI 모델을 DB 내에서 직접 실행이 가능함. <br> 데이터 이동 없이 실시간 AI 분석이 가능. <br> AI Vector Search 기능 지원. <br> SQL Firewall 지원으로 보안 강화| 비교적 높은 라이선스 비용 <br> 다른 DB에 비해 다루기가 까다로워 진입장벽이 있음. <br> 참고 자료가 비교적 적음 |
| OpenAI | 모델 성능 대비 크레딧 비용이 저렴함. <br> 충전된 크레딧을 모두 사용하면 추가 과금이 발생하지 않음. <br> 코드 관련 답변이 Gemini에 비해 우수함 | 답변이 중간에 생략되는 문제가 덜함 <br> 비용대비 준수한 성능 <br> | 최대 토큰량이 Gemini에 비해 적음 <br> 멀티모달 처리 능력이 Gemini에 비해 부족 <br>  |
| OCI free tier | AMD cpu 1, RAM 1GB 스펙의 VM 2개를 무료로 지원하기 때문에.  | 평생 무료 <br> 과금에 대한 부담감 없음. | 서비스를 운영하기에는 턱없이 부족한 컴퓨팅 리소스이기 때문에 실제 운영 환경을 가정하려면 유료 결제가 필요함. |




</div>


## <div align="center">문서</div>

<details open>
<summary>시작 하기</summary>

1. Github의 레포지토리를 클론합니다. 
2. `.env`과 `.env.local` 파일을 추가하고 설정값을 입력합니다.  
3. 오라클 클라우드에 접속하기 위한 wallet 폴더를 추가합니다. 
4. 컨테이너를 실행합니다. 

<br>

**Github의 레포지토리 클론**
```bash
git clone https://github.com/Rimember/ringchat.git  # clone
```

<br>

**`.env`과 `.env.local` 파일 추가 및 설정값을 입력**
```bash
# create .env file
cd ringchat/backend

echo "# API 
OPENAI_API_KEY = \"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\"

# oracle
DB_USER = \"USER_NAME\"
DB_PWD = \"PASSWORD\"
DB_DSN = \"DATA_SOURCE_NAME\"
DB_CONFIG_DIR = \"WALLET_FOLDER_PATH\"
DB_WALLET_LOCATION = \"WALLET_FOLDER_PATH\"
DB_WALLET_PWD = \"WALLET_PASSWORD\"" > .env
```

```bash 
# create .env.local file
cd ringchat/frontend

echo "NEXT_PUBLIC_API_URL=http://backend:8000/api/v0" > .env.local 
```

<br>

**wallet 폴더를 추가**

```bash 
mv WALLET_FOLDER_PATH ringchat/backend 
```

<br>

**컨테이너를 실행**

```bash 
cd ringchat 

docker compose up 
```
</details>


<details open>
<summary>API 문서</summary>

</details>

<details open>
<summary>데이터 베이스 엔티티 관계 다이어그램</summary>

<img width="90%" src="https://github.com/user-attachments/assets/41f76240-a9ba-425b-997e-17b942394d3e">

</details>


## <div align="center">기여자분들 ✨</div>

아래 계신분들의 노고에 감사드립니다.  


<table>
<tr>
<td align="center">
<a href="https://github.com/esy2k">
<img src="https://avatars.githubusercontent.com/u/55533535?v=4" width="100px;" alt=""/><br />
<sub><b>강동훈</b></sub></a><br />
<a href="https://github.com/Rimember/ringchat/commits?author=esy2k" title="Code">🛠️</a> 
</td>
<td align="center">
<a href="https://github.com/rudeuns">
<img src="https://avatars.githubusercontent.com/u/151593264?v=4" width="100px;" alt=""/><br />
<sub><b>선경은</b></sub></a><br />
<a href="https://github.com/Rimember/ringchat/commits?author=rudeuns" title="Code">🛠️</a> 
</td>
<td align="center">
<a href="https://github.com/teddygood">
<img src="https://avatars.githubusercontent.com/u/39366574?v=4" width="100px;" alt=""/><br />
<sub><b>이찬호</b></sub></a><br />
<a href="https://github.com/Rimember/ringchat/commits?author=teddygood" title="Code">🛠️</a> 
</td>
<td align="center">
<a href="https://github.com/ronintlim">
<img src="https://avatars.githubusercontent.com/u/44433964?v=4" width="100px;" alt=""/><br />
<sub><b>임승원</b></sub></a><br />
<a href="https://github.com/Rimember/ringchat/commits?author=ronintlim" title="Code">🛠️</a> 
</td>
<td align="center">
<a href="https://github.com/Jungjihyuk">
<img src="https://avatars.githubusercontent.com/u/33630505?v=4" width="100px;" alt=""/><br />
<sub><b>정지혁</b></sub></a><br />
<a href="https://github.com/Rimember/ringchat/commits?author=Jungjihyuk" title="Code">🛠️</a> 
</td>
</tr>
</table>