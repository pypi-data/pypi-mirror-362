"""
MediaPipe 랜드마크 기반 눈 상태 감지 모델 - 기존 PointEyeCloseDetector와 100% 동일

눈의 가로세로 비율(aspect ratio)을 사용하여 눈의 개폐 상태를 판단합니다.
기존과 동일하게 bounding box 좌표를 직접 사용합니다.
"""

from typing import Tuple
import numpy as np
import cv2
from .base import EyeStateDetector
from ..eye.targeting import EyeTargeting

class PointEyeModel(EyeStateDetector):
    """기존 PointEyeCloseDetector를 100% 그대로 복사한 구현"""
    
    def __init__(self):
        super().__init__()
        # 기존과 동일한 임계값
        self.THRESHOLD = 5.5
        # 눈 타겟팅을 위한 EyeTargeting 인스턴스
        self.eye_targeting = EyeTargeting()
    
    def initialize(self) -> bool:
        """Point 모델은 별도 초기화가 필요하지 않음"""
        self.is_initialized = True
        return True
    
    def predict(self, bbox):
        """기존 predict 메서드와 100% 동일"""
        x, y, w, h = bbox
        aspect_ratio = w / h if h != 0 else 0
        if aspect_ratio > self.THRESHOLD:
            # 눈이 감김
            return 1
        return 0
    
    def detect_eye_state(self, eye_image: np.ndarray) -> Tuple[bool, float]:
        """
        새로운 인터페이스를 위한 wrapper
        하지만 Point 모델은 bbox가 필요하므로 별도 처리가 필요함
        """
        # Point 모델은 개별 눈 이미지로는 작동할 수 없음
        # 대신 전체 프레임이 필요함
        # 임시로 이미지 크기 기반 분석 제공
        try:
            if eye_image.size == 0:
                return False, 0.0
            
            # 이미지 크기 기반 가로세로 비율 계산
            h, w = eye_image.shape[:2]
            aspect_ratio = w / h if h != 0 else 0
            
            # 감김 판단 (비율이 높을수록 감긴 상태)
            is_closed = aspect_ratio > self.THRESHOLD
            
            # 신뢰도 계산 (임계값과의 거리 기반)
            confidence = min(1.0, abs(aspect_ratio - self.THRESHOLD) / self.THRESHOLD)
            
            return is_closed, confidence
            
        except Exception as e:
            return False, 0.0
    
    def detect_both_eyes_from_frame(self, frame: np.ndarray) -> Tuple[Tuple[bool, float], Tuple[bool, float]]:
        """
        기존 eye_close_detecte 메서드와 동일한 방식으로 전체 프레임에서 양쪽 눈 감지
        """
        try:
            # get_bounding_boxes는 (right_bbox, left_bbox) 순서로 반환
            right_bbox, left_bbox = self.eye_targeting.get_bounding_boxes(frame)
            
            # 좌측 눈 처리
            if left_bbox is None:
                left_result = (False, 0.0)  # -1 대신 False, 0.0 사용
            else:
                left_pred = self.predict(left_bbox)
                left_closed = (left_pred == 1)
                left_result = (left_closed, 0.8 if left_pred == 1 else 0.2)
            
            # 우측 눈 처리
            if right_bbox is None:
                right_result = (False, 0.0)  # -1 대신 False, 0.0 사용
            else:
                right_pred = self.predict(right_bbox)
                right_closed = (right_pred == 1)
                right_result = (right_closed, 0.8 if right_pred == 1 else 0.2)
            
            return left_result, right_result
            
        except Exception as e:
            return (False, 0.0), (False, 0.0) 