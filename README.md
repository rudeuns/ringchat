<div align="center">
<img width="20%" src="https://github.com/user-attachments/assets/0a36e495-4467-4fdb-ac65-36c8590d6200">

<h4>Ringchat 🤖 is a URL-powered 🔗 chatbot service.</h4>
<p>
"RingChat" is a portmanteau of "Ring" and "Chatbot". The "Ring" symbolizes the connection between the document contained within the URL link, the chatbot, and the user. In Korean, the first syllables of "Ring" and "link" are the same, allowing for a natural association. Additionally, "Ring" evokes the image of a ring, implying reliability in the answers provided by RingChat.
</p>

</div>

## <div align="center">RingChat🤖 Key Features</div>

1️⃣ `Recommend Links along with 3 metrics` <br>

- Score
- Times attached 
- Total number of bookmark

2️⃣ `Customized document analysis` <br>


3️⃣ `Organize scattered answers` 

<details open>
<summary>
 Features
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

## <div align="center">Service architecture</div>

<div align="center">
<img width="95%" src="https://github.com/user-attachments/assets/e6a7022b-4de4-4eee-ba6b-7a9ffa8e89f0">

<br>

This section provides an `overview` of the project's core components.
Each `tech stack` is accompanied by a discussion of its `benefits`, `drawbacks`, and the specific `reasons` for its inclusion in this project.

<br>

| Technology | Why We Chose It | Benefits | Drawbacks/Limitations |
|---|---|---|---|
| Docker | Consistency in the development environment and rapid deployment | Resolving library dependency issues that arise in different development environments. <br> Easy scalability during deployment. | Complexity of container image management. <br> If not familiar with Docker, it can lead to potential delays in development time |
| FastAPI | High development productivity because it supports automatic documentation and asynchronous processing when developing API. <br> Easily fulfills the essential requirements for this project | Asynchronous processing support <br> Efficient use of resources <br> Swagger support <br> Easy data validation using Pydantic | Requires learning about asynchronous programming. <br> Community size is small compared to flask |
| Langchain | This project aims to overcome the limitations of existing LLMs. Langchain, one of the most popular and intuitive frameworks that facilitates in-context learning, is a natural choice for achieving this goal. | It's easy to extend various functions with support for a wide range of tools. <br> Development is relatively easy with an intuitive API. | The high level of abstraction can make fine-grained control difficult. <br> Since it's a relatively new framework, there might be challenges in acquiring information and a higher likelihood of encountering bugs |
| Next.js | The only person on the team who handles frontend development is proficient in Next.js. | SSR, SSG support <br> Improved search engine optimization <br> Active community | For pages where data changes frequently, SSR can cause performance degradation as the server needs to render the page every time it's requested. <br> Understanding React is necessary, which can create a barrier to entry. |
| Oracle 23ai | It supports Vector columns, enabling similarity search within the database. Similarity search was expected to be frequently used for URL recommendations in this project. | Direct AI model execution within the DB. <br> AI Vector Search support. <br> Enhanced security with SQL Firewall| Relatively high licensing fees <br> There is a barrier to entry as it is more difficult to handle than other DBs. <br> Relatively little reference material |
| OpenAI | The gpt-4o-mini model offers good performance at a relatively low credit cost. <br> Once the charged credits are exhausted, no additional charges will occur. <br> Code-related answers are superior compared to Gemini | Answers are less likely to be truncated in the middle <br> Decent performance for the cost | The maximum token limit is lower compared to Gemini <br> Multimodal processing capabilities are less developed compared to Gemini |
| OCI free tier | Because it provides two free VMs, each with an AMD CPU and 1GB of RAM.  | Two VM instance free forever <br> No worries about additional charges | The resources provided are inadequate for running actual services, therefore requiring an additional charge. |


</div>


## <div align="center">Documentation</div>

<details open>
<summary>Get Started</summary>

1. `Clone` repo
2. Set `.env` & `.env.local` files 
3. Place the wallet folder 
4. Run the containers

<br>

**Clone repo**
```bash
git clone https://github.com/Rimember/ringchat.git  # clone
```

<br>

**Set .env & .env.local**
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

**Place the wallet folder**

```bash 
mv WALLET_FOLDER_PATH ringchat/backend 
```

<br>

**Run the containers**

```bash 
cd ringchat 

docker compose up 
```
</details>


<details open>
<summary>API Document</summary>

</details>

<details open>
<summary>Database ERD</summary>

<img width="90%" src="https://github.com/user-attachments/assets/41f76240-a9ba-425b-997e-17b942394d3e">

</details>


## <div align="center">Contributors ✨</div>

Thanks goes to these wonderful people


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
<a href="https://github.com/NBHDQXT">
<img src="https://avatars.githubusercontent.com/u/179193723?v=4" width="100px;" alt=""/><br />
<sub><b>임승원</b></sub></a><br />
<a href="https://github.com/Rimember/ringchat/commits?author=NBHDQXT" title="Code">🛠️</a> 
</td>
<td align="center">
<a href="https://github.com/Jungjihyuk">
<img src="https://avatars.githubusercontent.com/u/33630505?v=4" width="100px;" alt=""/><br />
<sub><b>정지혁</b></sub></a><br />
<a href="https://github.com/Rimember/ringchat/commits?author=Jungjihyuk" title="Code">🛠️</a> 
</td>
</tr>
</table>