# 시스템 모듈
import os
import sys


# 파일 절대경로 추출
def resourcePath(relativePath):
    basePath = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))    
    return os.path.join(basePath, "../" + relativePath)

# 파일 존재 유무
def isFileFunc(filePath):
    if os.path.isfile(filePath):
        return True
    else:
        return False