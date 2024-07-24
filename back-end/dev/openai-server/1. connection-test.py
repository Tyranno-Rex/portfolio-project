import os
import openai
import platform
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient


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
# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_query(user_input):
    # GPT를 사용하여 사용자 입력을 분석하고 적절한 쿼리 생성
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that generates search queries based on user questions.\
                Create a concise and relevant search query.\
                document format is name, url, readme, description, complete_status, multi, category, subproject."}, 
            {"role": "user", "content": f"Generate a search query for the following question: {user_input}"}
        ],
        temperature=0.3,
    )
    return response.choices[0].message['content']

# def search_mongodb(query):
#     # MongoDB에서 질문에 가장 관련된 문서를 찾습니다
#     result = database.find_one(
#         {"$text": {"$search": query}},
#         {"score": {"$meta": "textScore"}}
#     )
#     return result

# def generate_response(user_input, context):
#     # GPT-3.5를 사용하여 자연스러운 응답 생성
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant. Use the provided context to answer the question naturally and conversationally. If Korean, provide a Korean response And if English, provide an English response."},
#             {"role": "user", "content": f"Context: {context}\n\nUser Question: {user_input}\n\nProvide a natural and conversational response:"}
#         ],
#         temperature=0.7,
#     )
#     return response.choices[0].message['content']

def chat():
    print("챗봇을 시작합니다. 종료하려면 'quit', 'q', 또는 'exit'를 입력하세요.")
    while True:
        user_input = input("\n사용자: ")
        if user_input.lower() in ['quit', 'q', 'exit']:
            print("챗봇을 종료합니다.")
            break
        # 사용자 입력을 분석하여 쿼리 생성
        generated_query = generate_query(user_input)
        print(f"생성된 쿼리: {generated_query}")  # 디버깅용
        
        # # MongoDB에서 관련 문서 검색
        # result = search_mongodb(generated_query)
        
        # if result:
        #     context = f"Question: {result['question']}\nAnswer: {result['answer']}"
        #     response = generate_response(user_input, context)
        # else:
        #     response = "죄송합니다. 관련된 정보를 찾을 수 없습니다."
        
        # print(f"챗봇: {response}")

if __name__ == "__main__":
    # MongoDB 텍스트 검색 인덱스 생성
    chat()