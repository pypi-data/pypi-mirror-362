"""
기본 감지기 인터페이스

모든 감지기는 Detector 추상 클래스를 상속받아 일관된 인터페이스를 제공합니다.
"""

from abc import ABC, abstractmethod
from typing import Any
from .results import DetectionResult

class Detector(ABC):
    """
    최상위 감지기 추상 클래스
    
    모든 감지기(눈 감지, 고개 움직임 감지, 표정 감지 등)의 공통 인터페이스를 정의합니다.
    """
    
    def __init__(self, name: str = "Detector"):
        self.name = name
        self.is_initialized = False
        self._config = {}
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        감지기 초기화
        
        Returns:
            bool: 초기화 성공 여부
        """
        pass
    
    @abstractmethod 
    def detect(self, frame: Any) -> DetectionResult:
        """
        감지 실행
        
        Args:
            frame: 입력 이미지 프레임 (numpy array)
            
        Returns:
            DetectionResult: 감지 결과
        """
        pass
    
    def configure(self, **kwargs):
        """감지기 설정 업데이트"""
        self._config.update(kwargs)
    
    def get_config(self):
        """현재 설정 반환"""
        return self._config.copy()
    
    def cleanup(self):
        """리소스 정리"""
        self.is_initialized = False
    
    def __enter__(self):
        """컨텍스트 매니저 지원"""
        if not self.is_initialized:
            self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 지원"""
        self.cleanup() 