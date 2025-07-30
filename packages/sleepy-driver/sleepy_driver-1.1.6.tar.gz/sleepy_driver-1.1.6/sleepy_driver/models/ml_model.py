"""
RandomForest 기반 눈 상태 감지 모델 (MLEye)

사전 훈련된 RandomForest 모델을 사용하여 눈의 개폐 상태를 판단합니다.
입력: 90x90 크기의 눈 이미지 (64x64로 리사이즈됨)
출력: (is_closed: bool, confidence: float)
"""

import os
import cv2
import numpy as np
from typing import Tuple
from .base import EyeStateDetector

class MLEyeModel(EyeStateDetector):
    """
    RandomForest 기반 눈 감지 모델
    
    사전 훈련된 scikit-learn RandomForest 모델을 사용합니다.
    """
    
    def __init__(self):
        super().__init__()
        self.model = None
        self.model_path = os.path.join(os.path.dirname(__file__), "rf_model.pkl")
    
    def initialize(self) -> bool:
        """RandomForest 모델 로드"""
        try:
            import joblib
            import sklearn
            
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {self.model_path}")
            
            self.model = joblib.load(self.model_path)
            self.is_initialized = True
            return True
            
        except ImportError:
            raise ImportError(
                "MLEye 모델을 사용하려면 다음 라이브러리가 필요합니다: "
                "pip install joblib scikit-learn"
            )
        except Exception as e:
            raise Exception(f"모델 로드 실패: {str(e)}")
    
    def detect_eye_state(self, eye_image: np.ndarray) -> Tuple[bool, float]:
        """
        RandomForest 기반 눈 상태 감지
        
        Args:
            eye_image: 90x90 크기의 눈 이미지
            
        Returns:
            Tuple[bool, float]: (is_closed, confidence)
        """
        if not self.is_initialized or self.model is None:
            raise RuntimeError("모델이 초기화되지 않았습니다. initialize()를 먼저 호출하세요.")
        
        try:
            # 1. 이미지 전처리
            processed_image = self._preprocess_image(eye_image)
            
            # 2. 예측 실행
            prediction = self.model.predict(processed_image)[0]  # 0 or 1
            
            # 3. 확률 예측 (가능한 경우)
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(processed_image)[0]
                confidence = max(probabilities)  # 가장 높은 확률을 신뢰도로 사용
            else:
                confidence = 0.8  # 기본 신뢰도
            
            # 4. 결과 변환 (모델 출력이 반대일 수 있으므로 확인 필요)
            # 원래 코드에서 1 - prediction을 했으므로 그대로 적용
            is_closed = bool(1 - prediction)
            
            return is_closed, confidence
            
        except Exception as e:
            # 에러 발생 시 안전하게 처리
            return False, 0.0
    
    def _preprocess_image(self, eye_image: np.ndarray) -> np.ndarray:
        """
        이미지 전처리: 64x64 리사이즈 후 flatten
        
        Args:
            eye_image: 입력 눈 이미지
            
        Returns:
            np.ndarray: 전처리된 이미지 (1, 4096) 형태
        """
        # 흑백 변환 (필요한 경우)
        if len(eye_image.shape) == 3:
            gray = cv2.cvtColor(eye_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = eye_image.copy()
        
        # 64x64로 리사이즈
        resized = cv2.resize(gray, (64, 64))
        
        # flatten하여 1차원 배열로 변환
        flattened = resized.flatten().reshape(1, -1)
        
        return flattened 