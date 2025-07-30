"""
눈 상태 감지 모델의 기본 인터페이스
"""

from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np

class EyeStateDetector(ABC):
    """
    눈 상태 감지 인터페이스
    
    모든 눈 감지 모델은 이 인터페이스를 구현해야 합니다.
    입력: 90x90 크기의 눈 이미지
    출력: (is_closed: bool, confidence: float)
    """
    
    def __init__(self):
        self.model_name = self.__class__.__name__
        self.is_initialized = False
    
    @abstractmethod
    def initialize(self) -> bool:
        """모델 초기화 (모델 파일 로드 등)"""
        pass
    
    @abstractmethod
    def detect_eye_state(self, eye_image: np.ndarray) -> Tuple[bool, float]:
        """
        단일 눈 이미지에서 열림/닫힘 상태 감지
        
        Args:
            eye_image: 90x90 크기의 눈 이미지 (numpy array)
            
        Returns:
            Tuple[bool, float]: (is_closed, confidence)
                - is_closed: True if closed, False if open
                - confidence: 0.0~1.0 신뢰도
        """
        pass
    
    def detect_both_eyes(self, left_eye: np.ndarray, right_eye: np.ndarray) -> Tuple[Tuple[bool, float], Tuple[bool, float]]:
        """
        양쪽 눈 동시 감지 (기본 구현: 각각 따로 감지)
        
        Returns:
            Tuple containing ((left_closed, left_conf), (right_closed, right_conf))
        """
        left_result = self.detect_eye_state(left_eye)
        right_result = self.detect_eye_state(right_eye)
        return left_result, right_result
    
    def cleanup(self):
        """리소스 정리"""
        self.is_initialized = False
    
    def __enter__(self):
        if not self.is_initialized:
            self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup() 