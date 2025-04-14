import os
import re

# ========= 1. 기존 제공 텍스트 파일 읽기 =========
provided_file = "F:\리스트_백업.txt"

# 기존 리스트를 (숫자, 추가텍스트) 튜플 형태로 저장
provided_entries = []
provided_set = set()

# 수정된 정규식: 줄의 시작에서 연속된 숫자를 추출한 후, 그 뒤에 숫자나 공백이 아닌 문자가 있으면 무시하고
# (있다면) 공백 뒤 추가 텍스트로 추출합니다.
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
            # 만약 정규식 매칭이 안되면 숫자만 추출하는 페일세이프
            m2 = re.search(r'(\d+)', line)
            if m2:
                num = m2.group(1)
                extra = line.replace(num, "").strip()
                provided_entries.append((num, extra))
                provided_set.add(num)
            else:
                print(f"제공파일의 줄 '{line}'에서 숫자 정보를 찾을 수 없습니다.")

# ========= 2. 폴더 내 7z 및 zip 파일 읽기 =========
base_dir = "F:\simya\_미분류"
all_files = os.listdir(base_dir)

# 확장자가 .7z 또는 .zip 이면서 파일명이 "RJ"로 시작하는 파일 선택
file_list = [fname for fname in all_files if fname.lower().endswith((".7z", ".zip")) and fname.startswith("RJ")]

# 중복 파일명을 저장할 리스트와 새 항목 저장 리스트
duplicates = []
folder_entries = []

# 통합 정규식: RJ 뒤에 연속된 숫자와 이어지는 (선택적) 추가 문자열, 확장자는 7z 또는 zip
pattern_folder = re.compile(r'^RJ(\d+)(.*)\.(7z|zip)$', re.IGNORECASE)

for fname in file_list:
    m = pattern_folder.match(fname)
    if m:
        num = m.group(1)
        extra = m.group(2).strip()  # 추가 문자열 (예: "-2D", "ver.25.03.10" 등)
        
        # 텍스트 결과 파일에서는 추가 문자열이 있으면 자리수를 고려하여 고정 공백 적용
        if extra:
            if len(num) == 6:
                formatted = f"{num}{' ' * 6}{extra}"
            elif len(num) == 8:
                formatted = f"{num}{' ' * 4}{extra}"
            else:
                formatted = f"{num} {extra}"
        else:
            formatted = num

        # 이미 제공된 리스트에 있으면 중복 처리
        if num in provided_set:
            duplicates.append(f"{fname} 이 중복되었습니다")
        else:
            folder_entries.append((num, extra))
    else:
        print(f"파일 '{fname}'는 예상 형식에 맞지 않습니다.")

# ========= 3. 기존 제공 리스트와 새로 추출한 항목 합치기 및 정렬 =========
combined_entries = provided_entries.copy()
combined_entries.extend(folder_entries)

# 정렬: 각 항목의 숫자 부분을 int형으로 변환하여 오름차순 정렬
try:
    combined_entries.sort(key=lambda x: int(x[0]))
except ValueError as e:
    print("정렬 중 오류:", e)
    combined_entries = [entry for entry in combined_entries if entry[0].isdigit()]
    combined_entries.sort(key=lambda x: int(x[0]))

# ========= 4. 결과물 파일 작성 =========
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

# ========= 5. 중복 파일명 터미널에 출력 =========
if duplicates:
    print("중복된 파일명:")
    for msg in duplicates:
        print(msg)
else:
    print("중복된 파일이 없습니다.")

print(f"\n최종 결과가 '{output_file}' 파일에 저장되었습니다.")
