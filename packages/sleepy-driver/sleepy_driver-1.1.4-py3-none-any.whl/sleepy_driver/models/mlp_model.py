"""
CNN(MLP) 기반 눈 상태 감지 모델 - 기존 MLPEyeCloseDetector와 100% 동일

PyTorch 기반 CNN 모델을 사용하여 눈의 개폐 상태를 판단합니다.
"""

import torch
import torch.nn as nn
import torchvision.transforms as transforms
import os
from typing import Tuple
import numpy as np
from .base import EyeStateDetector

class EyeCNN(nn.Module):
    """기존과 정확히 동일한 CNN 아키텍처"""
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )

        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 5 * 5, 128),
            nn.ReLU(),
            nn.Linear(128, 2)
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

class MLPEyeModel(EyeStateDetector):
    """기존 MLPEyeCloseDetector를 100% 그대로 복사한 구현"""
    
    def __init__(self):
        super().__init__()
        # 기존과 동일한 초기화
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "eye_cnn_model_early_stopping.pth")

        self.model = EyeCNN().to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
    
        self.transform = transforms.Compose([
            transforms.ToPILImage(),      # OpenCV 이미지 (numpy) → PIL 이미지
            transforms.Grayscale(),
            transforms.Resize((90, 90)),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])
        self.is_initialized = True
    
    def initialize(self) -> bool:
        """기존에는 __init__에서 바로 초기화"""
        return True
    
    def predict(self, eye_img):
        """기존 MLPEyeCloseDetector.predict와 100% 동일"""
        if eye_img.size == 0:
            return None

        input_tensor = self.transform(eye_img).unsqueeze(0).to(self.device)
    
        with torch.no_grad():
            output = self.model(input_tensor)
            pred_raw = torch.argmax(output, dim=1).item()  # 0: closed, 1: open
            pred = 1 - pred_raw  # 0 → 1, 1 → 0 (반전)
        return pred

    def detect_eye_state(self, eye_image: np.ndarray) -> Tuple[bool, float]:
        """새로운 인터페이스를 위한 wrapper - 기존 predict 결과를 정확히 변환"""
        try:
            result = self.predict(eye_image)
            
            if result is None:
                return False, 0.0
            
            # 기존 로직: pred=1이면 눈 감음, pred=0이면 눈 뜸
            is_closed = (result == 1)
            confidence = 0.8
            
            return is_closed, confidence
            
        except Exception as e:
            return False, 0.0 