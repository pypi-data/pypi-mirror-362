"""
눈 타겟팅 - MediaPipe를 사용한 90x90 눈 영역 추출

전체 프레임에서 얼굴을 감지하고 눈 영역을 90x90 크기로 추출합니다.
"""

import mediapipe as mp
import cv2
import numpy as np
from typing import Optional, Tuple

class EyeTargeting:
    """
    MediaPipe를 사용한 눈 영역 감지 및 추출
    
    얼굴에서 좌우 눈의 위치를 감지하고 90x90 크기로 추출합니다.
    """
    
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            refine_landmarks=True,
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # MediaPipe 좌/우 눈 랜드마크 인덱스
        self.RIGHT_EYE_IDX = [33, 133, 160, 159, 158, 157, 173, 246]
        self.LEFT_EYE_IDX = [362, 263, 387, 386, 385, 384, 398, 466]
    
    def get_bounding_boxes(self, frame: np.ndarray) -> Tuple[Optional[Tuple], Optional[Tuple]]:
        """
        이미지 프레임에서 얼굴을 탐지하고 좌우 눈의 bounding box를 반환
        
        Args:
            frame: BGR 형식의 이미지 프레임
            
        Returns:
            Tuple: (right_eye_box, left_eye_box)
                각 box는 (x, y, w, h) 형태의 튜플
                None이면 해당 눈을 찾지 못한 경우
        """
        try:
            # BGR to RGB 변환
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            if not results.multi_face_landmarks:
                return None, None
            
            face_landmarks = results.multi_face_landmarks[0]
            h, w, _ = frame.shape
            
            # 우측 눈 bounding box 계산
            right_eye_box = self._calculate_eye_bbox(face_landmarks, self.RIGHT_EYE_IDX, w, h)
            
            # 좌측 눈 bounding box 계산  
            left_eye_box = self._calculate_eye_bbox(face_landmarks, self.LEFT_EYE_IDX, w, h)
            
            return right_eye_box, left_eye_box
            
        except Exception as e:
            return None, None
    
    def _calculate_eye_bbox(self, face_landmarks, eye_indices: list, img_w: int, img_h: int) -> Optional[Tuple]:
        """
        특정 눈의 랜드마크로부터 bounding box 계산
        
        Args:
            face_landmarks: MediaPipe 얼굴 랜드마크
            eye_indices: 눈 랜드마크 인덱스 리스트
            img_w, img_h: 이미지 크기
            
        Returns:
            Tuple: (x, y, w, h) bounding box 또는 None
        """
        try:
            # 눈 랜드마크 좌표 추출
            eye_points = []
            for idx in eye_indices:
                landmark = face_landmarks.landmark[idx]
                x = int(landmark.x * img_w)
                y = int(landmark.y * img_h)
                eye_points.append((x, y))
            
            # bounding box 계산
            xs = [point[0] for point in eye_points]
            ys = [point[1] for point in eye_points]
            
            x_min, x_max = min(xs), max(xs)
            y_min, y_max = min(ys), max(ys)
            
            # 여백 추가 (10%)
            margin_x = int((x_max - x_min) * 0.1)
            margin_y = int((y_max - y_min) * 0.1)
            
            x = max(0, x_min - margin_x)
            y = max(0, y_min - margin_y)
            w = min(img_w - x, x_max - x_min + 2 * margin_x)
            h = min(img_h - y, y_max - y_min + 2 * margin_y)
            
            return (x, y, w, h)
            
        except Exception as e:
            return None
    
    def crop_eye(self, frame: np.ndarray, bbox: Tuple[int, int, int, int], size: int = 90) -> np.ndarray:
        """
        기존 EyeDetector.crop_and_resize와 100% 동일한 방식으로 눈 영역 추출
        
        Args:
            frame: 원본 이미지 프레임
            bbox: (x, y, w, h) bounding box
            size: 출력 이미지 크기 (기본값: 90)
            
        Returns:
            np.ndarray: 90x90 크기의 눈 이미지
        """
        try:
            if bbox is None:
                return None

            x, y, w, h = bbox
            
            # 기존과 정확히 동일한 여백 계산
            x1 = max(x - h//2, 0)
            y1 = max(y - w//2, 0)
            x2 = min(x + w + h//2, frame.shape[1])
            y2 = min(y + h + w//2, frame.shape[0])
            
            # 영역 추출
            eye_crop = frame[y1:y2, x1:x2]
            
            # 90x90으로 리사이즈
            eye_resized = cv2.resize(eye_crop, (size, size))
            
            return eye_resized
            
        except Exception as e:
            # 에러 발생 시 빈 90x90 이미지 반환
            return np.zeros((size, size, 3), dtype=np.uint8)
    
    def extract_both_eyes(self, frame: np.ndarray) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """
        한 번에 양쪽 눈을 추출하는 편의 메서드
        
        Args:
            frame: 입력 이미지 프레임
            
        Returns:
            Tuple: (right_eye_90x90, left_eye_90x90)
                None이면 해당 눈을 추출하지 못한 경우
        """
        right_box, left_box = self.get_bounding_boxes(frame)
        
        right_eye = None
        left_eye = None
        
        if right_box is not None:
            right_eye = self.crop_eye(frame, right_box)
            
        if left_box is not None:
            left_eye = self.crop_eye(frame, left_box)
        
        return right_eye, left_eye 