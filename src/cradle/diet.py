import os
import traceback
import json
import re
from typing import List, Dict, Any, Optional

def get_diet_traceback(exc: Exception, max_stack_depth: int = 10) -> str:
    """
    트레이스백에서 불필요한 경로(site-packages, python internal)를 제거하고
    최근 N개의 핵심 로직만 남긴 JSON 문자열을 반환합니다.
    """
    tb = traceback.extract_tb(exc.__traceback__)
    root_dir = os.getcwd()

    clean_frames = []
    
    # 필터링할 패턴들 (가상환경, 라이브러리, 내부 시스템 경로)
    exclude_patterns = [
        re.compile(r"site-packages"),
        re.compile(r"lib[\\/]python"),
        re.compile(r"importlib"),
        re.compile(r"\.venv"),
        re.compile(r"anaconda"),
        re.compile(r"miniconda"),
    ]

    # 뒤에서부터 (최신순) 검토하며 max_stack_depth만큼만 유지
    # 하지만 트레이스백은 보통 실행 순서대로 (부모 -> 자식) 보여주는 것이 좋으므로
    # 필터링 후 마지막 N개를 선택함.
    
    for frame in tb:
        filename = frame.filename
        
        # 1. 절대 경로를 상대 경로로 변환하여 토큰 절약
        # 프로젝트 루트 외부는 is_internal로 간주
        if filename.startswith(root_dir):
            rel_path = os.path.relpath(filename, root_dir)
            is_internal = False
        else:
            rel_path = filename
            is_internal = True

        # 2. 내부 경로나 라이브러리 경로는 건너뜀 (단, 프로젝트 루트 내부는 무조건 포함)
        if is_internal and any(p.search(filename) for p in exclude_patterns):
            continue

        clean_frames.append({
            "f": rel_path,  # file -> f (토큰 다이어트)
            "l": frame.lineno,  # line -> l
            "fn": frame.name,  # function -> fn
            "c": frame.line   # code -> c
        })

    # 최신 N개 프레임만 유지
    if len(clean_frames) > max_stack_depth:
        clean_frames = clean_frames[-max_stack_depth:]

    diet_info = {
        "type": type(exc).__name__, # error_type -> type
        "msg": str(exc), # message -> msg
        "stack": clean_frames
    }

    # 토큰 절약을 위해 separators=(',', ':') 사용 가능하나, 로그 가독성을 위해 현재는 유지
    return json.dumps(diet_info, indent=2, ensure_ascii=False)

def get_diet_data(data: Any, max_str_len: int = 100) -> Any:
    """
    일반 데이터 구조에서 민감한 정보를 마스킹하고 긴 문자열을 축소합니다.
    """
    mask_keys = {"password", "secret", "token", "key", "auth", "pwd", "ssn"}
    
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            if k.lower() in mask_keys or any(mk in k.lower() for mk in mask_keys):
                new_dict[k] = "********"
            else:
                new_dict[k] = get_diet_data(v, max_str_len)
        return new_dict
    elif isinstance(data, list):
        return [get_diet_data(item, max_str_len) for item in data]
    elif isinstance(data, str):
        if len(data) > max_str_len:
            return data[:max_str_len // 2] + "..." + data[-max_str_len // 2:]
        return data
    return data
