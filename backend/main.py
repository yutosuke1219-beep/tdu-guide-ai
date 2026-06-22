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

with open("data/academic/human.json", "r", encoding="utf-8") as f:
    human = json.load(f)

with open("data/academic/english.json", "r", encoding="utf-8") as f:
    english = json.load(f)

with open("data/academic/common.json", "r", encoding="utf-8") as f:
    common = json.load(f)

with open("data/academic/expert_ex.json", "r", encoding="utf-8") as f:
    expert_ex = json.load(f)

with open("data/academic/expert.json", "r", encoding="utf-8") as f:
    expert = json.load(f)

with open("data/academic/rd.json", "r", encoding="utf-8") as f:
    rd = json.load(f)

with open("data/academic/rd_cond.json", "r", encoding="utf-8") as f:
    rd_cond = json.load(f)

with open("data/academic/rd_ex.json", "r", encoding="utf-8") as f:
    rd_ex = json.load(f)

with open("data/academic/rd_ex2.json", "r", encoding="utf-8") as f:
    rd_ex2 = json.load(f)



@app.get("/")
def root():
    return {"message": "TDU Guide AI"}


@app.get("/schedule")
def get_schedule():
    return schedule


@app.get("/student-life")
def get_student_life():
    return student_life

@app.get("/human")
def get_human():
    return human

@app.get("/english")
def get_english():
    return english

@app.get("/common")
def get_common():
    return common

@app.get("/expert-ex")
def get_expert_ex():
    return expert_ex

@app.get("/expert")
def get_expert():
    return expert

@app.get("/rd")
def get_rd():
    return rd

@app.get("/rd-cond")
def get_rd_cond():
    return rd_cond

@app.get("/rd-ex")
def get_rd_ex():
    return rd_ex

@app.get("/rd-ex2")
def get_rd_ex2():
    return rd_ex2

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
        
    # 人間形成科目関連
    for subject in human:
        if (
            subject["name"] in message
            or subject.get("field", "") in message
            or subject.get("subject_group", "") in message
        ):
            return {
                "message": message,
                "answer": f"{subject['name']}は{subject['year']}年次配当の{subject['required_type']}科目で、{subject['credits']}単位です。授業形態は{subject['class_type']}です。"
            }
        
    # ==========================
    # 英語科目関連
    # ==========================
    for subject in english:
        if subject["name"] in message:
            return {
                "message": message,
                "answer": f"{subject['name']}は{subject['year']}年次配当の{subject['required_type']}科目で、{subject['credits']}単位です。授業形態は{subject['class_type']}です。"
            }

        # ==========================
    # 共通教育説明関連
    # ==========================
    for item in common:
        if (
            item["title"] in message
            or any(keyword in message for keyword in item["keywords"])
        ):
            return {
                "message": message,
                "answer": item["answer"]
            }

    # ==========================
    # 専門基礎説明関連
    # ==========================
    for item in expert_ex:
        if (
            item["title"] in message
            or any(keyword in message for keyword in item["keywords"])
        ):
            return {
                "message": message,
                "answer": item["answer"]
            }

    # ==========================
    # 専門基礎科目関連
    # ==========================
    for subject in expert:
        if subject["name"] in message:
            return {
                "message": message,
                "answer": f"{subject['name']}は{subject['year']}年次配当の{subject['required_type']}科目で、{subject['credits']}単位です。授業形態は{subject['class_type']}です。"
            }
        
    # ==========================
    # RD学系説明
    # ==========================
    for item in rd_ex:
        if (
            item["title"] in message
            or any(keyword in message for keyword in item["keywords"])
        ):
            return {
                "message": message,
                "answer": item["answer"]
            }
    # ==========================
    # RD履修モデル説明
    # ==========================
    for item in rd_ex2:
        if (
            item["title"] in message
            or any(keyword in message for keyword in item["keywords"])
        ):
            return {
                "message": message,
                "answer": item["answer"]
            }
        
        # ==========================
    # RD科目検索
    # ==========================
    for subject in rd:
        if (
            subject["name"] in message
            or subject.get("field", "") in message
        ):
            return {
                "message": message,
                "answer": f"{subject['name']}は{subject['year']}年次配当の{subject['required_type']}科目で、{subject['credits']}単位です。授業形態は{subject['class_type']}です。"
            }
        
        # ==========================
    # RD進級条件
    # ==========================
    for item in rd_cond:
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