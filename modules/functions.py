# 시스템 모듈
import os
import sys


# 파일 절대경로 추출
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))    
    return os.path.join(base_path, relative_path)

# 파일 존재 유무
def isFileFunc(file_path):
    if os.path.isfile(file_path):
        return True
    else:
        return False