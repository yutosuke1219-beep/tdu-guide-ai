from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JSON読み込み
with open("data/schedule.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)

with open("data/student_life.json", "r", encoding="utf-8") as f:
    student_life = json.load(f)


@app.get("/")
def root():
    return {"message": "TDU Guide AI"}


@app.get("/schedule")
def get_schedule():
    return schedule


@app.get("/student-life")
def get_student_life():
    return student_life


@app.get("/search")
def search_schedule(keyword: str):
    results = []

    for event in schedule:
        note = event.get("note", "")
        if keyword in event["name"] or (note and keyword in note):
            results.append(event)

    return {
        "keyword": keyword,
        "results": results
    }


@app.get("/chat")
def chat(message: str):

    # ==========================
    # 学生生活関連
    # ==========================
    for item in student_life:
        if (
            item["title"] in message
            or any(keyword in message for keyword in item["keywords"])
        ):
            return {
                "message": message,
                "answer": item["answer"]
            }

    # ==========================
    # 年間予定関連
    # ==========================
    results = []

    keyword = message
    keyword = keyword.replace("はいつ？", "")
    keyword = keyword.replace("はいつ", "")
    keyword = keyword.replace("いつ？", "")
    keyword = keyword.replace("いつ", "")
    keyword = keyword.replace("？", "")
    keyword = keyword.strip()

    for event in schedule:
        note = event.get("note", "")

        if (
            keyword in event["name"]
            or event["name"] in message
            or (note and keyword in note)
            or (note and note in message)
        ):
            results.append(event)

    if not results:
        return {
            "message": message,
            "answer": "関連する情報は見つかりませんでした。"
        }

    answers = []

    for event in results:
        if event["start_date"] == event["end_date"]:
            text = f"{event['name']}は{event['start_date']}です。"
        else:
            text = f"{event['name']}は{event['start_date']}から{event['end_date']}までです。"

        if event.get("note"):
            text += f" 備考：{event['note']}。"

        answers.append(text)

    answer = "\n".join(answers)

    return {
        "message": message,
        "references": results,
        "answer": answer
    }