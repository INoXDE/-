import os
import re

# 작업할 폴더 경로 (현재 폴더)
folder_path = r"F:\simya"

# 코드 패턴: "RJ", "rj", "꺼" 또는 "거" 뒤에 여섯 자리 숫자 및 선택적으로 두 자리 숫자
pattern = re.compile(r"((?:RJ|꺼|거)\d{6}(?:\d{2})?)", re.IGNORECASE)

for file_name in os.listdir(folder_path):
    full_path = os.path.join(folder_path, file_name)
    if os.path.isfile(full_path):
        match = pattern.search(file_name)
        if match:
            original_code = match.group(0)
            # 접두어가 "RJ" 또는 "rj"인 경우: 앞 2글자 제거, 그 외("꺼", "거"): 앞 1글자 제거
            if original_code[:2].lower() == "rj":
                digits = original_code[2:]
            else:
                digits = original_code[1:]
            # 항상 결과는 대문자 "RJ"와 숫자 배열로 만듦
            rj_code = "RJ" + digits

            # 파일명에서 해당 코드를 제거한 나머지 문자열 (공백 제거)
            remaining = pattern.sub("", file_name).strip()
            # 새 파일명 구성: RJ코드 + 공백 + 남은 문자열
            new_file_name = f"{rj_code} {remaining}"
            new_full_path = os.path.join(folder_path, new_file_name)
            
            print(f"Renaming: '{file_name}' -> '{new_file_name}'")
            os.rename(full_path, new_full_path)
