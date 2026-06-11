import json
import shutil
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEDULE_PATH = ROOT / 'data' / 'schedule.json'
BACKUP_PATH = ROOT / 'data' / 'schedule.json.bak'

PROVIDED = [
    {"date":"2026-04-02","title":"入学式","category":"event","semester":"前期"},
    {"start_date":"2026-04-03","end_date":"2026-04-09","title":"オリエンテーション","category":"orientation","semester":"前期"},
    {"date":"2026-04-10","title":"授業開始日","category":"class_start","semester":"前期"},
    {"date":"2026-04-29","title":"昭和の日授業実施日","category":"class_on_holiday","semester":"前期","makeup_holiday":"2026-05-01"},
    {"date":"2026-05-01","title":"休日振替日（昭和の日）","category":"substitute_holiday","semester":"前期"},
    {"date":"2026-05-03","title":"憲法記念日","category":"holiday","semester":"前期"},
    {"date":"2026-05-04","title":"みどりの日","category":"holiday","semester":"前期"},
    {"date":"2026-05-05","title":"こどもの日","category":"holiday","semester":"前期"},
    {"date":"2026-05-06","title":"振替休日（憲法記念日）","category":"holiday","semester":"前期"},
    {"date":"2026-05-24","title":"合同体育祭","category":"event","semester":"前期","note":"太線上：前前期、太線下：前後期"},
    {"date":"2026-06-14","title":"オープンキャンパス（鳩山）","category":"open_campus","semester":"前期"},
    {"date":"2026-07-12","title":"オープンキャンパス（鳩山）","category":"open_campus","semester":"前期"},
    {"date":"2026-07-20","title":"海の日授業実施日","category":"class_on_holiday","semester":"前期","makeup_holiday":"2026-08-07"},
    {"start_date":"2026-07-23","end_date":"2026-07-24","title":"特定科目試験日","category":"exam","semester":"前期","note":"授業・補講は行いません"},
    {"start_date":"2026-07-25","end_date":"2026-07-28","title":"一斉休講の振替授業日","category":"makeup_class_day","semester":"前期"},
    {"date":"2026-08-01","title":"オープンキャンパス（鳩山）","category":"open_campus","semester":"前期"},
    {"date":"2026-08-02","title":"オープンキャンパス（鳩山）","category":"open_campus","semester":"前期"},
    {"date":"2026-08-07","title":"休日振替日（海の日）","category":"substitute_holiday","semester":"前期"},
    {"start_date":"2026-08-08","end_date":"2026-08-17","title":"一斉休業期間","category":"closure","semester":"前期"},
    {"date":"2026-08-11","title":"山の日","category":"holiday","semester":"前期"},
    {"date":"2026-09-01","title":"前期成績発表","category":"grades","semester":"後期"},
    {"date":"2026-09-11","title":"創立記念日（休日）","category":"holiday","semester":"後期"},
    {"date":"2026-09-12","title":"授業開始日（後期）","category":"class_start","semester":"後期"},
    {"date":"2026-09-19","title":"前期末卒業式（予定）","category":"ceremony","semester":"後期"},
    {"date":"2026-09-21","title":"敬老の日授業実施日","category":"class_on_holiday","semester":"後期","makeup_holiday":"2026-10-02"},
    {"date":"2026-09-22","title":"国民の休日授業実施日","category":"class_on_holiday","semester":"後期","makeup_holiday":"2026-12-26"},
    {"date":"2026-09-23","title":"秋分の日","category":"holiday","semester":"後期"},
    {"date":"2026-10-02","title":"休日振替日（敬老の日）","category":"substitute_holiday","semester":"後期"},
    {"date":"2026-10-12","title":"スポーツの日授業実施日","category":"class_on_holiday","semester":"後期","makeup_holiday":"2027-01-05"},
    {"start_date":"2026-10-29","end_date":"2026-10-30","title":"鳩山祭準備日（休講）","category":"festival_preparation","semester":"後期"},
    {"start_date":"2026-10-31","end_date":"2026-11-01","title":"鳩山祭（休講）","category":"festival","semester":"後期"},
    {"start_date":"2026-11-02","end_date":"2026-11-03","title":"鳩山祭片付日（休講）","category":"festival_cleanup","semester":"後期"},
    {"date":"2026-11-03","title":"文化の日","category":"holiday","semester":"後期"},
    {"date":"2026-11-23","title":"勤労感謝の日授業実施日","category":"class_on_holiday","semester":"後期","makeup_holiday":"2027-01-06"},
    {"date":"2026-12-15","title":"キャリアイベント【卒業生による仕事研究セミナー】（休講）","category":"career_event","semester":"後期"},
    {"date":"2026-12-26","title":"休日振替日（国民の休日）","category":"substitute_holiday","semester":"後期"},
    {"date":"2027-01-01","title":"元旦","category":"holiday","semester":"後期"},
    {"date":"2027-01-05","title":"休日振替日（スポーツの日）","category":"substitute_holiday","semester":"後期"},
    {"date":"2027-01-06","title":"休日振替日（勤労感謝の日）","category":"substitute_holiday","semester":"後期"},
    {"date":"2027-01-11","title":"成人の日","category":"holiday","semester":"後期"},
    {"start_date":"2027-01-13","end_date":"2027-01-14","title":"特定科目試験日","category":"exam","semester":"後期","note":"授業・補講は行いません"},
    {"start_date":"2027-01-15","end_date":"2027-01-16","title":"大学入学共通テストに伴う休講","category":"no_classes","semester":"後期"},
    {"start_date":"2027-01-18","end_date":"2027-01-20","title":"一斉休講の振替授業日","category":"makeup_class_day","semester":"後期"},
    {"date":"2027-02-11","title":"建国記念の日","category":"holiday","semester":"後期"},
    {"date":"2027-02-23","title":"天皇誕生日","category":"holiday","semester":"後期"},
    {"date":"2027-03-02","title":"進級発表・卒業発表・後期成績発表","category":"grades","semester":"後期"},
    {"date":"2027-03-19","title":"卒業式","category":"ceremony","semester":"後期"},
    {"date":"2027-03-21","title":"春分の日","category":"holiday","semester":"後期"},
    {"date":"2027-03-22","title":"振替休日（春分の日）","category":"holiday","semester":"後期"}
]

CATEGORY_EQUIVALENCE = {
    'holiday_class': 'class_on_holiday',
    'substitute_day': 'substitute_holiday',
    'grade': 'grades',
    'makeup_class': 'makeup_class_day',
    'vacation': 'closure',
    'festival_prepare': 'festival_preparation',
    'career': 'career_event',
    'holiday_day': 'holiday',
}

PARENS_REMOVAL = re.compile(r'[（\(].*?[）\)]')
FULLWIDTH_BRACKETS = re.compile(r'【.*?】')


def normalize_title(title: str) -> str:
    s = title or ''
    s = PARENS_REMOVAL.sub('', s)
    s = FULLWIDTH_BRACKETS.sub('', s)
    s = s.replace('前期', '').replace('後期', '')
    s = s.replace('休講', '').replace('予定', '')
    s = s.replace('（', '').replace('）', '')
    s = s.replace(' ', '').replace('\u3000', '')
    return s.strip()


def normalize_category(category: str) -> str:
    if category is None:
        return ''
    return CATEGORY_EQUIVALENCE.get(category, category)


def same_title(a: str, b: str) -> bool:
    if not a or not b:
        return False
    na = normalize_title(a)
    nb = normalize_title(b)
    return na == nb or na in nb or nb in na


def same_category(a: str, b: str) -> bool:
    return normalize_category(a) == normalize_category(b)


def make_key(entry):
    if 'date' in entry:
        return ('date', entry['date'])
    if 'start_date' in entry and 'end_date' in entry:
        return ('range', entry['start_date'], entry['end_date'])
    return None


def entry_title(entry):
    return entry.get('name') or entry.get('title') or ''


def entry_category(entry):
    return normalize_category(entry.get('type') or entry.get('category') or '')


def date_in_range(date_str, start_str, end_str):
    return start_str <= date_str <= end_str


def find_existing_matches(provided, existing_entries):
    matches = []
    for existing in existing_entries:
        if 'date' in provided and 'date' in existing:
            if provided['date'] == existing['date']:
                if same_title(provided['title'], entry_title(existing)) or same_category(provided['category'], entry_category(existing)):
                    matches.append(existing)
        elif 'date' in provided and 'start_date' in existing and 'end_date' in existing:
            if date_in_range(provided['date'], existing['start_date'], existing['end_date']):
                if same_title(provided['title'], entry_title(existing)) or same_category(provided['category'], entry_category(existing)):
                    matches.append(existing)
        elif 'start_date' in provided and 'end_date' in provided and 'start_date' in existing and 'end_date' in existing:
            if provided['start_date'] == existing['start_date'] and provided['end_date'] == existing['end_date']:
                if same_title(provided['title'], entry_title(existing)) or same_category(provided['category'], entry_category(existing)):
                    matches.append(existing)
    return matches


def convert_provided_to_entry(item):
    entry = {}
    if 'date' in item:
        entry['date'] = item['date']
    if 'start_date' in item:
        entry['start_date'] = item['start_date']
        entry['end_date'] = item['end_date']
    entry['name'] = item['title']
    entry['type'] = item['category']
    if 'note' in item:
        entry['note'] = item['note']
    else:
        entry['note'] = ''
    return entry


def main():
    if not SCHEDULE_PATH.exists():
        raise FileNotFoundError(f'Missing schedule file: {SCHEDULE_PATH}')
    shutil.copy2(SCHEDULE_PATH, BACKUP_PATH)
    with SCHEDULE_PATH.open('r', encoding='utf-8') as f:
        existing = json.load(f)

    added = []
    skipped = []
    for item in PROVIDED:
        if find_existing_matches(item, existing):
            skipped.append(item)
            continue
        added.append(convert_provided_to_entry(item))

    existing.extend(added)
    existing.sort(key=lambda e: e.get('start_date', e.get('date', '9999-12-31')))
    with SCHEDULE_PATH.open('w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=4)

    print(f'Backup saved to: {BACKUP_PATH}')
    print(f'Existing count before add: {len(existing) - len(added)}')
    print(f'Added entries: {len(added)}')
    print(f'Skipped duplicates: {len(skipped)}')
    if added:
        print('\nAdded:')
        for item in added:
            print(' -', item['name'], item.get('date', f"{item.get('start_date')} to {item.get('end_date')}") )
    if skipped:
        print('\nSkipped:')
        for item in skipped:
            print(' -', item['title'], item.get('date', f"{item.get('start_date')} to {item.get('end_date')}") )

if __name__ == '__main__':
    main()
