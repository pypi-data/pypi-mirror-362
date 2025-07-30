"""
메인 졸음 감지기

모든 컴포넌트를 통합하여 완전한 졸음 감지 시스템을 제공합니다.
"""

from typing import Optional
from ..core.detector import Detector
from ..core.results import EyeDetectionResult, DrowsinessResult
from ..eye.targeting import EyeTargeting
from ..models.base import EyeStateDetector
from ..models.registry import ModelRegistry
from .analyzer import DrowsinessAnalyzer, TimeBased

class DrowsinessDetector(Detector):
    """
    메인 졸음 감지기
    
    눈 타겟팅 → 눈 상태 감지 → 졸음 분석의 전체 파이프라인을 제공합니다.
    """
    
    def __init__(self, 
                 eye_model: Optional[EyeStateDetector] = None,
                 drowsiness_analyzer: Optional[DrowsinessAnalyzer] = None,
                 name: str = "DrowsinessDetector"):
        super().__init__(name)
        
        self.eye_targeting = EyeTargeting()
        self.eye_model = eye_model
        self.drowsiness_analyzer = drowsiness_analyzer or TimeBased()
    
    def initialize(self) -> bool:
        """감지기 초기화"""
        try:
            if self.eye_model is not None and hasattr(self.eye_model, 'initialize'):
                if not self.eye_model.initialize():
                    return False
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            print(f"초기화 실패: {e}")
            return False
    
    def detect(self, frame) -> DrowsinessResult:
        """졸음 감지 실행"""
        if not self.is_initialized:
            return DrowsinessResult(
                success=False,
                message="감지기가 초기화되지 않았습니다"
            )
        
        if self.eye_model is None:
            return DrowsinessResult(
                success=False,
                message="눈 감지 모델이 설정되지 않았습니다"
            )
        
        try:
            # Point 모델의 경우 특별한 처리 (전체 프레임을 사용)
            if hasattr(self.eye_model, 'detect_both_eyes_from_frame'):
                # Point 모델: 전체 프레임에서 직접 bbox 분석
                (left_closed, left_conf), (right_closed, right_conf) = self.eye_model.detect_both_eyes_from_frame(frame)
            else:
                # 다른 모델들: 90x90 눈 이미지 추출 후 분석
                # 1. 눈 영역 추출 (순서 주의: extract_both_eyes는 (right, left) 순서로 반환)
                extracted_right, extracted_left = self.eye_targeting.extract_both_eyes(frame)
                
                if extracted_right is None or extracted_left is None:
                    return DrowsinessResult(
                        success=False,
                        message="얼굴 또는 눈을 찾을 수 없습니다"
                    )
                
                # 2. 각 눈의 상태 감지 (올바른 순서로 할당)
                left_closed, left_conf = self.eye_model.detect_eye_state(extracted_left)
                right_closed, right_conf = self.eye_model.detect_eye_state(extracted_right)
            
            # 3. 눈 감지 결과 생성
            eye_result = EyeDetectionResult(
                success=True,
                message="눈 감지 완료",
                left_eye_closed=left_closed,
                right_eye_closed=right_closed,
                left_confidence=left_conf,
                right_confidence=right_conf
            )
            
            # 4. 졸음 분석
            drowsiness_result = self.drowsiness_analyzer.analyze(eye_result)
            
            return drowsiness_result
            
        except Exception as e:
            return DrowsinessResult(
                success=False,
                message=f"감지 오류: {str(e)}"
            )
    
    @classmethod
    def create_with_model(cls, model_name: str, threshold_ms: float = 1000.0) -> 'DrowsinessDetector':
        """
        모델 이름으로 감지기 생성
        
        Args:
            model_name: 등록된 모델 이름 (opencv, ml, mlp, point)
            threshold_ms: 졸음 판단 임계값 (밀리초)
            
        Returns:
            DrowsinessDetector: 설정된 감지기
        """
        eye_model = ModelRegistry.create(model_name)
        analyzer = TimeBased(threshold_ms)
        
        detector = cls(eye_model=eye_model, drowsiness_analyzer=analyzer)
        detector.initialize()
        
        return detector
    
    @classmethod
    def create_with_custom_components(cls,
                                    eye_model: EyeStateDetector,
                                    drowsiness_analyzer: Optional[DrowsinessAnalyzer] = None,
                                    threshold_ms: float = 1000.0) -> 'DrowsinessDetector':
        """
        커스텀 컴포넌트로 감지기 생성
        
        Args:
            eye_model: 사용자 정의 눈 감지 모델
            drowsiness_analyzer: 사용자 정의 졸음 분석기 (None이면 기본값)
            threshold_ms: 졸음 판단 임계값
            
        Returns:
            DrowsinessDetector: 설정된 감지기
        """
        analyzer = drowsiness_analyzer or TimeBased(threshold_ms)
        
        detector = cls(eye_model=eye_model, drowsiness_analyzer=analyzer)
        detector.initialize()
        
        return detector
    
    def reset(self):
        """분석 상태 초기화"""
        if self.drowsiness_analyzer:
            self.drowsiness_analyzer.reset()
    
    def get_model_info(self) -> str:
        """현재 사용중인 모델 정보 반환"""
        if self.eye_model is None:
            return "모델 없음"
        return getattr(self.eye_model, 'model_name', self.eye_model.__class__.__name__) 