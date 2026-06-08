from fastapi import FastAPI
import json

app = FastAPI()

with open("data/schedule.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)

with open("data/graduation.json", "r", encoding="utf-8") as f:
    graduation = json.load(f)

with open("data/courses.json", "r", encoding="utf-8") as f:
    courses = json.load(f)

with open("data/certificate.json", "r", encoding="utf-8") as f:
    certificates = json.load(f)

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

    # 卒業関連
    if "卒業" in message:
        item = graduation[0]

        return {
            "message": message,
            "answer": f"卒業に必要な単位数は{item['value']}単位です。"
        }

    # 証明書関連
    if "証明書" in message:
        for item in certificates:
            if item["name"] in message:
                return {
                    "message": message,
                    "answer": f"{item['name']}は{item['place']}で発行できます。"
                }

        return {
            "message": message,
            "answer": "証明書に関する情報はありますが、該当する証明書名が見つかりませんでした。"
        }

    # 科目関連
    for course in courses:
        if course["name"] in message:
            return {
                "message": message,
                "answer": f"{course['name']}は{course['category']}科目です。"
            }
        
        
    # 年間予定関連
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

@app.get("/graduation")
def get_graduation():
    return graduation

@app.get("/courses")
def get_courses():
    return courses

@app.get("/certificates")
def get_certificates():
    return certificates
