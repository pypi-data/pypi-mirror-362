"""
감지 결과를 나타내는 데이터 클래스들

모든 감지 결과는 DetectionResult를 상속받아 일관된 인터페이스를 제공합니다.
"""

import time
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class DetectionResult:
    """기본 감지 결과 클래스"""
    success: bool = False
    message: str = ""
    confidence: float = 0.0
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass 
class EyeDetectionResult(DetectionResult):
    """눈 감지 결과"""
    left_eye_closed: bool = False
    right_eye_closed: bool = False
    both_eyes_closed: bool = False
    left_confidence: float = 0.0
    right_confidence: float = 0.0
    
    def __post_init__(self):
        """양쪽 눈이 모두 감겼는지 자동 계산"""
        self.both_eyes_closed = self.left_eye_closed and self.right_eye_closed

@dataclass
class DrowsinessResult(DetectionResult):
    """졸음 감지 결과"""
    is_drowsy: bool = False
    closed_duration_ms: float = 0.0
    threshold_ms: float = 1000.0
    drowsiness_level: str = "normal"  # "normal", "mild", "moderate", "severe"
    
    # 눈 상태 정보 추가 (기존 호환성)
    left_eye_closed: bool = False
    right_eye_closed: bool = False
    both_eyes_closed: bool = False
    
    def __post_init__(self):
        """졸음 수준 자동 계산"""
        if self.closed_duration_ms >= self.threshold_ms * 2:
            self.drowsiness_level = "severe"
        elif self.closed_duration_ms >= self.threshold_ms * 1.5:
            self.drowsiness_level = "moderate"
        elif self.closed_duration_ms >= self.threshold_ms:
            self.drowsiness_level = "mild"
        else:
            self.drowsiness_level = "normal" 