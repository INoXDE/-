import os
import re
import shutil

base_dir = "."
all_files = os.listdir(base_dir)

# 통합 정규식: RJ 뒤에 연속된 숫자와 (선택적) 추가 문자열, 확장자는 7z 또는 zip
pattern = re.compile(r'^RJ(\d+)(.*)\.(7z|zip)$', re.IGNORECASE)

for fname in all_files:
    if fname.lower().endswith((".7z", ".zip")) and fname.startswith("RJ"):
        m = pattern.match(fname)
        if m:
            num = m.group(1)
            extra = m.group(2).strip()  # 추가 문자열가 있다면 예: "-2D", "ver.25.03.10" 등
            # 폴더명은 추가 문자열이 있을 경우 단일 공백을 두고 결합
            if extra:
                folder_name = f"RJ{num} {extra}"
            else:
                folder_name = f"RJ{num}"
                
            folder_path = os.path.join(base_dir, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"폴더 생성: {folder_name}")
            else:
                print(f"이미 존재하는 폴더: {folder_name}")
                
            source = os.path.join(base_dir, fname)
            destination = os.path.join(folder_path, fname)
            try:
                shutil.move(source, destination)
                print(f"'{fname}' 파일을 '{folder_name}' 폴더로 이동했습니다.")
            except Exception as e:
                print(f"'{fname}' 파일 이동 중 오류 발생: {e}")
        else:
            print(f"파일 '{fname}'는 예상 형식에 맞지 않습니다.")
