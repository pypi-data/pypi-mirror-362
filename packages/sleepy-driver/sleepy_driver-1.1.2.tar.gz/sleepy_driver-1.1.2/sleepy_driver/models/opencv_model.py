"""
OpenCV 기반 눈 상태 감지 모델

순수 OpenCV 기술만을 사용하여 눈의 개폐 상태를 판단합니다.
입력: 90x90 크기의 눈 이미지
출력: (is_closed: bool, confidence: float)
"""

import cv2
import numpy as np
from typing import Tuple
from .base import EyeStateDetector

class OpenCVEyeModel(EyeStateDetector):
    """
    OpenCV 기반 눈 감지 모델
    
    에지 밀도와 밝기 분산을 이용해 눈 감김 상태를 판단합니다.
    """
    
    def __init__(self):
        super().__init__()
        # 눈을 떴는지, 감았는지 임계값
        self.EDGE_DENSITY_MIN = 5.0 
        self.EDGE_DENSITY_MAX = 30.0
        
        # 밝기 분산 임계값
        self.VARIANCE_MIN = 300.0
        self.VARIANCE_MAX = 1500.0
    
    def initialize(self) -> bool:
        """OpenCV 모델은 별도 초기화가 필요하지 않음"""
        self.is_initialized = True
        return True
    
    def detect_eye_state(self, eye_image: np.ndarray) -> Tuple[bool, float]:
        """
        OpenCV 기반 눈 상태 감지 (기존 로직과 동일)
        
        Args:
            eye_image: 90x90 크기의 눈 이미지
            
        Returns:
            Tuple[bool, float]: (is_closed, confidence)
        """
        try:
            # 기존 predict 메서드 로직을 그대로 적용
            result = self._predict_legacy(eye_image)
            
            # 기존 방식: 0 또는 1만 반환
            is_closed = bool(result)
            confidence = 0.8 if result == 1 else 0.2  # 기본 신뢰도
            
            return is_closed, confidence
            
        except Exception as e:
            # 에러 발생 시 안전하게 처리
            return False, 0.0
    
    def _predict_legacy(self, eye_img):
        """기존 predict 메서드 로직을 그대로 구현"""
        # 1. 이미지 흑백으로 통일
        gray_eye = eye_img
        if len(eye_img.shape) == 3:
            gray_eye = cv2.cvtColor(eye_img, cv2.COLOR_BGR2GRAY)

        # 2-1) 명암 대비 향상 및 노이즈 제거
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        preprocessed_img = clahe.apply(gray_eye)
        preprocessed_img = cv2.GaussianBlur(preprocessed_img, (7, 7), 0)

        # 2-2) 동공 검출 (가장 중요한 신호)
        circles = cv2.HoughCircles(
            preprocessed_img, cv2.HOUGH_GRADIENT, dp=2, minDist=30,
            param1=50, param2=30, minRadius=5, maxRadius=20
        )
        if circles is not None:
            return 0  # 동공이 감지되면 무조건 뜸

        # 4. 가로 에지(눈 감김 실선) 분석
        sobel_y = cv2.Sobel(preprocessed_img, cv2.CV_64F, 0, 1, ksize=5)
        edge_density = np.mean(np.absolute(sobel_y))
        edge_score = (edge_density - self.EDGE_DENSITY_MIN) / (self.EDGE_DENSITY_MAX - self.EDGE_DENSITY_MIN)
        edge_score = np.clip(edge_score, 0.0, 1.0)

        # 5. 밝기 분산 분석
        variance = np.var(gray_eye)
        variance_score = (variance - self.VARIANCE_MIN) / (self.VARIANCE_MAX - self.VARIANCE_MIN)
        variance_score = 1.0 - np.clip(variance_score, 0.0, 1.0)

        # 6. 최종 점수 융합
        final_score = 0.7 * edge_score + 0.3 * variance_score
        result = np.clip(final_score, 0.0, 1.0)
        
        # 기존 로직: 0.95 이하면 0, 아니면 1
        if result <= 0.95:
            return 0
        return 1
    
    def _calculate_closed_probability(self, edge_density: float, variance: float) -> float:
        """
        에지 밀도와 밝기 분산을 기반으로 눈 감김 확률 계산
        
        감은 눈의 특징:
        - 낮은 에지 밀도 (눈꺼풀이 매끄러움)
        - 낮은 밝기 분산 (상대적으로 균일한 밝기)
        """
        # 에지 밀도 점수 (낮을수록 감은 눈)
        if edge_density <= self.EDGE_DENSITY_MIN:
            edge_score = 1.0
        elif edge_density >= self.EDGE_DENSITY_MAX:
            edge_score = 0.0
        else:
            edge_score = 1.0 - (edge_density - self.EDGE_DENSITY_MIN) / (self.EDGE_DENSITY_MAX - self.EDGE_DENSITY_MIN)
        
        # 분산 점수 (낮을수록 감은 눈)
        if variance <= self.VARIANCE_MIN:
            variance_score = 1.0
        elif variance >= self.VARIANCE_MAX:
            variance_score = 0.0
        else:
            variance_score = 1.0 - (variance - self.VARIANCE_MIN) / (self.VARIANCE_MAX - self.VARIANCE_MIN)
        
        # 가중 평균 (에지가 더 중요)
        closed_probability = (edge_score * 0.7) + (variance_score * 0.3)
        
        return np.clip(closed_probability, 0.0, 1.0) 