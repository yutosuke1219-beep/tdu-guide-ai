from fastapi import FastAPI
import json

app = FastAPI()

with open("data/schedule.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)

@app.get("/")
def root():
    return {"message": "TDU Guide AI"}

@app.get("/schedule")
def get_schedule():
    return schedule

@app.get("/search")
def search_schedule(keyword: str):
    results = []

    for event in schedule:
        if keyword in event["name"] or keyword in event.get("note", ""):
            results.append(event)

    return {
        "keyword": keyword,
        "results": results
    }

@app.get("/chat")
def chat(message: str):
    results = []

    for event in schedule:
        if event["name"] in message or event.get("note", "") in message:
            results.append(event)

    if not results:
        return {
            "message": message,
            "answer": "関連する予定は見つかりませんでした。"
        }

    event = results[0]

    answer = f"{event['name']}は{event['date']}です。"

    if event.get("note"):
        answer += f" 備考：{event['note']}。"

    return {
        "message": message,
        "references": results,
        "answer": answer
    }
