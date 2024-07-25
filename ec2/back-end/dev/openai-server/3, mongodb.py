from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import platform
from langchain.schema import Document
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# 플랫폼에 따라 MongoDB 접속 비밀번호 파일 경로 설정
current_os = platform.system()
if current_os == 'Windows':
    PASSWORD_FILE = "C:/Users/admin/project/portfolio-project/back-end/main/database/password-mongo-token.txt"
else:
    PASSWORD_FILE = "/app/mongo-token.txt"

# 비밀번호 파일에서 MongoDB 접속 비밀번호 읽기
with open(PASSWORD_FILE, "r") as f:
    PASSWORD = f.read().strip()

# MongoDB Atlas 연결
client = MongoClient(f"mongodb+srv://jsilvercastle:{PASSWORD}@portfolio.tja9u0o.mongodb.net/?retryWrites=true&w=majority&appName=portfolio")

# MongoDB 연결 테스트
try:
    client.admin.command('ismaster')
except ConnectionFailure:
    print('MongoDB server not available')

# 데이터베이스 및 컬렉션 선택
portfolio_db = client['portfolio']
database = portfolio_db['database']

# 데이터 로드 함수 정의
def load_data_from_mongodb():
    documents = []

    # 데이터베이스에서 문서들을 가져와 Document 객체로 변환하여 리스트에 추가
    for doc in database.find():
        # 문서의 모든 값들을 하나의 문자열로 합쳐서 page_content로 사용
        page_content = ", ".join(str(value) for value in doc.values())
        documents.append(Document(page_content=page_content, metadata={'source': doc.get('name', 'unknown')}))

    return documents

# 데이터 로드
documents = load_data_from_mongodb()

# OpenAIEmbeddings을 사용하여 벡터 스토어 인덱스 생성
embedding = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embedding)
index = VectorstoreIndexCreator(vectorstore=vectorstore).from_documents(documents)

print(index)
