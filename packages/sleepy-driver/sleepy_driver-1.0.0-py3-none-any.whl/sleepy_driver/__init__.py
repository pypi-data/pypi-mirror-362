"""
SleepyDriver - 졸음 감지 라이브러리

사용 예시:
    # 간단한 사용법
    from sleepy_driver import DrowsinessDetector
    
    detector = DrowsinessDetector.create_with_model("opencv")
    result = detector.detect(frame)
    
    if result.is_drowsy:
        print(f"졸음 감지! {result.duration_ms}ms")

    # 고급 사용법
    from sleepy_driver import EyeStateDetector, TimeBased
    
    class MyCustomModel(EyeStateDetector):
        def detect_eye_state(self, eye_image):
            # 사용자 구현
            return is_closed, confidence
    
    detector = DrowsinessDetector.create_with_custom_components(
        eye_detector=MyCustomModel(),
        drowsiness_analyzer=TimeBased(threshold_ms=2000)
    )
"""

from .core.detector import Detector, DetectionResult
from .core.results import EyeDetectionResult, DrowsinessResult
from .drowsiness.detector import DrowsinessDetector
from .drowsiness.analyzer import TimeBased, MLBased
from .models.base import EyeStateDetector
from .eye.targeting import EyeTargeting
from .models.registry import ModelRegistry

__version__ = "1.0.0"
__author__ = "SleepyDriver Team"

# 사용자가 주로 사용할 클래스들을 노출
__all__ = [
    # 메인 API
    "DrowsinessDetector",
    
    # 결과 클래스들
    "DetectionResult",
    "EyeDetectionResult", 
    "DrowsinessResult",
    
    # 컴포넌트 인터페이스
    "EyeStateDetector",
    "EyeTargeting",
    
    # 졸음 분석기들
    "TimeBased",
    "MLBased",
    
    # 모델 관리
    "ModelRegistry",
    
    # 기본 클래스
    "Detector"
]

# 편의 함수들
def list_available_models():
    """사용 가능한 모든 모델 목록 반환"""
    return ModelRegistry.list_models()

def quick_detector(model_name="opencv", threshold_ms=1000):
    """빠른 설정을 위한 편의 함수"""
    return DrowsinessDetector.create_with_model(model_name, threshold_ms) 