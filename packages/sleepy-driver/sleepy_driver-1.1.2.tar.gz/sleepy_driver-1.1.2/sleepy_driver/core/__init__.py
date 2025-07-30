"""
Core 모듈 - 기본 인터페이스와 결과 클래스들

이 모듈은 라이브러리의 핵심 추상 클래스들과 데이터 구조를 제공합니다.
"""

from .detector import Detector
from .results import DetectionResult, EyeDetectionResult, DrowsinessResult

__all__ = [
    "Detector",
    "DetectionResult", 
    "EyeDetectionResult",
    "DrowsinessResult"
] 