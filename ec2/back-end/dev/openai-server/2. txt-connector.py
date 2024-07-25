import os
import sys
from pymongo import MongoClient
import openai
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.memory import ConversationBufferMemory

# .env 파일에서 환경 변수 로드
load_dotenv()

# MongoDB Atlas 클러스터 URI 및 데이터베이스/컬렉션 설정
mongo_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongo_uri)
db = client.mydatabase
faq_collection = db.faq
chat_collection = db.chat_history

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# MongoDB 데이터 로드 및 Document 형식으로 변환
def load_data_from_mongodb():
    documents = []
    for doc in faq_collection.find():
        documents.append(Document(page_content=doc['answer'], metadata={'source': doc['question']}))
    return documents

# 데이터 로드
documents = load_data_from_mongodb()

# 벡터 스토어 인덱스 생성
index = VectorstoreIndexCreator().from_documents(documents)

# 대화 기록을 저장할 메모리 객체 생성
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ChatOpenAI 모델을 사용하여 LLM을 생성하고 생성된 인덱스로 ConversationalRetrievalChain 생성
chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7),
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 3}),
    memory=memory,
    get_chat_history=lambda h: h,
    verbose=True
)

def get_response(query):
    result = chain({"question": query})
    return result['answer']

if __name__ == "__main__":
    print("챗봇을 시작합니다. 종료하려면 'quit', 'q', 또는 'exit'를 입력하세요.")
    while True:
        user_input = input("\n사용자: ")
        if user_input.lower() in ['quit', 'q', 'exit']:
            print("챗봇을 종료합니다.")
            break

        # 사용자 입력을 MongoDB에 저장
        chat_collection.insert_one({"role": "user", "content": user_input})
        
        # 챗봇 응답 생성
        response = get_response(user_input)
        
        # 챗봇 응답을 MongoDB에 저장
        chat_collection.insert_one({"role": "assistant", "content": response})
        
        print(f"챗봇: {response}")
