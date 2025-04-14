# -import os
import re

# ========= 1. 기존 제공된 텍스트 파일 읽기 =========
# 파일 이름: 보유리스트_RJ문자제거.txt
provided_file = "F:\리스트_백업.txt"

# 기존 리스트를 저장할 리스트와 중복 체크를 위한 집합을 준비합니다.
provided_entries = []  # (숫자 문자열, 추가 텍스트) 튜플로 저장. 추가 텍스트가 없으면 빈 문자열.
provided_set = set()   # 숫자 부분만 저장(정확한 중복 판별을 위해)

# 새로운 정규식을 사용합니다.
# ^(\d+)[^\d\s]*(?:\s+(.*))?$
# - 맨 앞의 연속된 숫자(\d+)를 추출하고, 그 뒤에 숫자나 공백이 아닌 문자가 있을 경우 무시한 후,
#   (있다면) 공백을 기준으로 추가 텍스트를 추출합니다.
pattern_provided = re.compile(r'^(\d+)[^\d\s]*(?:\s+(.*))?$')

with open(provided_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        m = pattern_provided.match(line)
        if m:
            num = m.group(1)
            extra = m.group(2).strip() if m.group(2) else ""
            provided_entries.append((num, extra))
            provided_set.add(num)
        else:
            # 만약 패턴에 매칭되지 않으면, 라인 내에서 숫자를 추출해보고 없으면 건너뜁니다.
            m2 = re.search(r'(\d+)', line)
            if m2:
                num = m2.group(1)
                extra = line.replace(num, "").strip()
                provided_entries.append((num, extra))
                provided_set.add(num)
            else:
                print(f"제공파일의 줄 '{line}'는 숫자 정보를 찾을 수 없습니다.")

# ========= 2. 폴더 내 7z 파일 읽기 =========
# 작업 폴더 내 파일 목록을 가져옵니다.
folder = "F:\simya\_미분류"  # 필요에 따라 경로를 변경하세요.
all_files = os.listdir(folder)

# 확장자가 .7z 이고, 파일명이 "RJ"로 시작하는 파일 선택
seven_z_files = [fname for fname in all_files if fname.lower().endswith(".7z") and fname.startswith("RJ")]

# 중복된 파일명을 저장할 리스트
duplicates = []
# 새로 추가할 항목을 저장할 리스트 (형식: (숫자문자열, 추가 텍스트))
folder_entries = []

# 개선된 정규표현식을 사용합니다.
# ^RJ(\d+)(?:\s*(.+))?\.7z$
# - 'RJ' 뒤에 오는 연속된 숫자(\d+)와,
# - (선택적으로) 공백이 있거나 바로 붙어있는 추가 문자열을 추출합니다.
pattern_folder = re.compile(r'^RJ(\d+)(?:\s*(.+))?\.7z$', re.IGNORECASE)

for fname in seven_z_files:
    m = pattern_folder.match(fname)
    if m:
        num = m.group(1)
        extra = m.group(2).strip() if m.group(2) else ""
        # 파일 이름에 따른 출력 형식 적용
        if extra:
            if len(num) == 6:
                formatted = f"{num}{' ' * 6}{extra}"
            elif len(num) == 8:
                formatted = f"{num}{' ' * 4}{extra}"
            else:
                formatted = f"{num} {extra}"
        else:
            formatted = num

        # 중복 검사: 제공 리스트에 이미 있으면 중복 처리
        if num in provided_set:
            duplicates.append(f"{fname} 이 중복되었습니다")
        else:
            folder_entries.append((num, extra))
    else:
        print(f"파일 '{fname}'는 예상 형식에 맞지 않습니다.")

# ========= 3. 제공 리스트와 폴더 항목 합치기 =========
combined_entries = provided_entries.copy()  # 기존 제공 리스트
combined_entries.extend(folder_entries)       # 새 항목 추가

# 정렬: 각 항목의 숫자 부분을 int형으로 변환하여 오름차순 정렬
try:
    combined_entries.sort(key=lambda x: int(x[0]))
except ValueError as e:
    print("정렬 중 숫자 변환 오류:", e)
    # 숫자로 변환이 불가한 항목이 있다면 건너뛰거나 에러 처리를 추가하세요.
    combined_entries = [entry for entry in combined_entries if entry[0].isdigit()]
    combined_entries.sort(key=lambda x: int(x[0]))

# ========= 4. 최종 결과물 파일 작성 =========
output_file = "F:\리스트.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for num, extra in combined_entries:
        if extra:
            if len(num) == 6:
                line = f"{num}{' ' * 6}{extra}"
            elif len(num) == 8:
                line = f"{num}{' ' * 4}{extra}"
            else:
                line = f"{num} {extra}"
        else:
            line = num
        f.write(line + "\n")

# ========= 5. 중복된 파일명 터미널 출력 =========
if duplicates:
    print("중복된 파일명:")
    for msg in duplicates:
        print(msg)
else:
    print("중복된 파일이 없습니다.")

print(f"\n최종 결과가 '{output_file}' 파일로 저장되었습니다.")
