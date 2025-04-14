import os

def read_file(file_path):
    """
    파일을 한 줄씩 읽어 두 개의 리스트로 분리합니다.
    - merged: 번호와 설명이 있는 항목 (숫자로 시작하는 줄)
    - fixed: 번호가 아닌 고정 블록(예: getchu 아래의 리스트) – 
      번호가 아닌 첫 줄이 나오면 그 이후는 고정 블록으로 취급합니다.
    """
    merged = []
    fixed = []
    fixed_started = False
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue  # 빈 줄은 건너뜁니다.
            # 아직 고정블록 시작 전인데, 만약 줄이 숫자로 시작하지 않으면 고정블록 시작으로 판단
            if not fixed_started:
                if not line.strip()[0].isdigit():
                    fixed_started = True
                    fixed.append(line)
                    continue
                else:
                    merged.append(line)
            else:
                fixed.append(line)
    return merged, fixed

def process_line(line):
    """
    한 줄을 읽어 숫자와 부가설명(존재하면)을 분리하는 함수.
    공백 기준으로 최대 한 번 분리합니다.
    """
    parts = line.strip().split(None, 1)
    num = parts[0]
    desc = parts[1] if len(parts) > 1 else ""
    return num, desc

def main():
    # 입력 파일들의 경로
    input_files = [
        r"D:\리스트.txt",
        r"D:새 텍스트 문서.txt"
    ]
    
    # 중복 제거를 위해 번호를 key, 설명을 value로 저장하는 딕셔너리
    all_entries = {}  
    fixed_block = None  # 고정 블록은 한 번만 취합

    # 각 파일을 읽어와서 처리
    for file in input_files:
        merged, fixed = read_file(file)
        # 한 파일에서 고정 블록이 발견되면 fixed_block에 저장 (여러 파일에 있으면 첫번째만 사용)
        if fixed and fixed_block is None:
            fixed_block = fixed
        for line in merged:
            num, desc = process_line(line)
            # 이미 동일 번호가 있으면, 부가설명이 없는 기존 항목보다 설명이 있는 항목을 우선합니다.
            if num in all_entries:
                if desc and not all_entries[num]:
                    all_entries[num] = desc
            else:
                all_entries[num] = desc

    # 정렬 기준: 번호의 자리수에 따라 정렬
    # – 6자리 번호는 카테고리 0, 8자리이면 카테고리 1, 그 외는 카테고리 2로 분류한 후 숫자 값으로 오름차순 정렬.
    def sort_key(num):
        if len(num) == 6:
            category = 0
        elif len(num) == 8:
            category = 1
        else:
            category = 2
        try:
            num_int = int(num)
        except:
            num_int = float('inf')
        return (category, num_int)

    sorted_nums = sorted(all_entries.keys(), key=sort_key)

    # 출력 형식 조정
    output_lines = []
    for num in sorted_nums:
        desc = all_entries[num]
        if desc:
            if len(num) == 6:
                sep = " " * 6
            elif len(num) == 8:
                sep = " " * 4
            else:
                sep = " "
            line = f"{num}{sep}{desc}"
        else:
            line = num
        output_lines.append(line)

    # 고정 블록(예: getchu 리스트)이 있다면 마지막에 추가 (원본 그대로)
    if fixed_block:
        output_lines.append("")  # 구분을 위한 빈 줄(옵션)
        output_lines.extend(fixed_block)

    # 최종 결과를 "F:\리스트.txt"에 저장
    output_path = r"F:\리스트.txt"
    with open(output_path, "w", encoding="utf-8") as out_f:
        for line in output_lines:
            out_f.write(line + "\n")
    
    print(f"파일 병합 및 변환이 완료되었습니다. 최종 결과는 {output_path}에 저장되었습니다.")

if __name__ == "__main__":
    main()
