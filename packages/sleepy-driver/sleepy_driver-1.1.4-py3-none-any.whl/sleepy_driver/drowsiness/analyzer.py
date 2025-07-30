"""
졸음 분석 알고리즘들

시간 기반, ML 기반 등 다양한 졸음 분석 방법을 제공합니다.
"""

import time
from abc import ABC, abstractmethod
from ..core.results import EyeDetectionResult, DrowsinessResult

class DrowsinessAnalyzer(ABC):
    """졸음 분석기 기본 인터페이스"""
    
    @abstractmethod
    def analyze(self, eye_result: EyeDetectionResult) -> DrowsinessResult:
        """눈 감지 결과를 바탕으로 졸음 상태 분석"""
        pass
    
    @abstractmethod
    def reset(self):
        """분석 상태 초기화"""
        pass

class TimeBased(DrowsinessAnalyzer):
    """
    시간 기반 졸음 분석기
    
    눈이 일정 시간 이상 감겨 있으면 졸음으로 판단합니다.
    """
    
    def __init__(self, threshold_ms: float = 1000.0):
        self.threshold_ms = threshold_ms
        self.closed_start_time = None
        self.total_closed_time = 0.0
    
    def analyze(self, eye_result: EyeDetectionResult) -> DrowsinessResult:
        """
        시간 기반 졸음 분석
        
        Args:
            eye_result: 눈 감지 결과
            
        Returns:
            DrowsinessResult: 졸음 분석 결과
        """
        current_time = time.time()
        
        # 양쪽 눈이 모두 감겨있는 경우만 카운트
        if eye_result.both_eyes_closed:
            if self.closed_start_time is None:
                self.closed_start_time = current_time
            
            self.total_closed_time = (current_time - self.closed_start_time) * 1000
        else:
            # 눈이 뜨여있으면 초기화
            self.reset()
        
        # 졸음 판단
        is_drowsy = self.total_closed_time >= self.threshold_ms
        
        return DrowsinessResult(
            success=True,
            message="시간 기반 분석 완료",
            is_drowsy=is_drowsy,
            closed_duration_ms=self.total_closed_time,
            threshold_ms=self.threshold_ms,
            confidence=min(1.0, self.total_closed_time / self.threshold_ms),
            timestamp=current_time,
            # 눈 상태 정보 전달
            left_eye_closed=eye_result.left_eye_closed,
            right_eye_closed=eye_result.right_eye_closed,
            both_eyes_closed=eye_result.both_eyes_closed
        )
    
    def reset(self):
        """상태 초기화"""
        self.closed_start_time = None
        self.total_closed_time = 0.0

class MLBased(DrowsinessAnalyzer):
    """
    ML 기반 졸음 분석기 (미래 확장용)
    """
    
    def __init__(self):
        pass
    
    def analyze(self, eye_result: EyeDetectionResult) -> DrowsinessResult:
        """ML 기반 분석 (미구현)"""
        return DrowsinessResult(
            success=False,
            message="ML 기반 분석은 아직 구현되지 않았습니다",
            is_drowsy=False
        )
    
    def reset(self):
        pass 