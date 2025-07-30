"""
새로운 SleepyDriver 라이브러리 테스트

sleepy_driver 모듈을 사용한 졸음 감지 테스트입니다.
"""

import cv2
import time
import sys
import os

# 상위 디렉토리의 sleepy_driver 모듈을 import할 수 있도록 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sleepy_driver.models.registry import ModelRegistry
from sleepy_driver.models.base import EyeStateDetector
from sleepy_driver.drowsiness.analyzer import TimeBased
from sleepy_driver.core.results import EyeDetectionResult, DrowsinessResult

# 임시로 눈 타겟팅을 위한 기존 모듈 사용
from eyeDetection.EyeDetection import EyeDetector as EyeTargeting

def install_dependencies():
    """필요한 의존성 설치 안내"""
    print("=== 새로운 SleepyDriver 라이브러리 ===")
    print("OpenCV 모델: 추가 의존성 없음")
    print("ML 모델: pip install joblib scikit-learn")
    print("MLP 모델: pip install torch torchvision")
    print("Point 모델: 추가 의존성 없음")
    print("\n모든 의존성 설치: pip install joblib scikit-learn torch torchvision")
    print("="*50)

class SimpleDrowsinessDetector:
    """
    간단한 졸음 감지기 (임시 구현)
    """
    def __init__(self, model_name: str = "opencv", threshold_ms: float = 1000.0):
        self.model_name = model_name
        self.eye_model = None
        self.eye_targeting = EyeTargeting()
        self.drowsiness_analyzer = TimeBased(threshold_ms)
        
    def initialize(self):
        """감지기 초기화"""
        try:
            self.eye_model = ModelRegistry.create(self.model_name)
            print(f"✓ {self.model_name} 모델 로드 성공")
            return True
        except Exception as e:
            print(f"✗ {self.model_name} 모델 로드 실패: {e}")
            return False
    
    def detect(self, frame) -> DrowsinessResult:
        """프레임에서 졸음 감지"""
        try:
            # 1. 눈 영역 추출 (90x90)
            right_box, left_box = self.eye_targeting.get_bounding_boxes(frame)
            
            if right_box is None or left_box is None:
                return DrowsinessResult(
                    success=False,
                    message="얼굴 또는 눈을 찾을 수 없습니다"
                )
            
            # 2. 눈 이미지 추출
            right_eye = self.eye_targeting.crop_eye(frame, right_box)
            left_eye = self.eye_targeting.crop_eye(frame, left_box)
            
            # 3. 각 눈의 상태 감지
            left_closed, left_conf = self.eye_model.detect_eye_state(left_eye)
            right_closed, right_conf = self.eye_model.detect_eye_state(right_eye)
            
            # 4. 눈 감지 결과 생성
            eye_result = EyeDetectionResult(
                success=True,
                message="눈 감지 완료",
                left_eye_closed=left_closed,
                right_eye_closed=right_closed,
                left_confidence=left_conf,
                right_confidence=right_conf
            )
            
            # 5. 졸음 분석
            drowsiness_result = self.drowsiness_analyzer.analyze(eye_result)
            
            return drowsiness_result
            
        except Exception as e:
            return DrowsinessResult(
                success=False,
                message=f"감지 오류: {str(e)}"
            )

def test_single_model(model_name: str, duration: int = 30):
    """단일 모델 테스트"""
    print(f"\n=== {model_name} 모델 테스트 ===")
    
    # 감지기 초기화
    detector = SimpleDrowsinessDetector(model_name, 1000.0)
    if not detector.initialize():
        return
    
    # 카메라 초기화
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return
    
    print(f"{model_name} 모델로 테스트 중... 'q'를 누르면 종료됩니다.")
    
    start_time = time.time()
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        frame_count += 1
        
        # 감지 실행
        result = detector.detect(frame)
        
        # 결과 표시
        if result.success:
            status = "DROWSY!" if result.is_drowsy else "AWAKE"
            color = (0, 0, 255) if result.is_drowsy else (0, 255, 0)
            
            cv2.putText(frame, f"Model: {model_name}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame, f"Status: {status}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            cv2.putText(frame, f"Duration: {result.closed_duration_ms:.0f}ms", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Level: {result.drowsiness_level}", (10, 120),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            if result.is_drowsy:
                cv2.putText(frame, "WAKE UP!", (50, 200),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        else:
            cv2.putText(frame, f"Error: {result.message}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # FPS 표시
        elapsed = time.time() - start_time
        if elapsed > 0:
            fps = frame_count / elapsed
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, frame.shape[0] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        cv2.imshow(f"SleepyDriver - {model_name}", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif duration > 0 and elapsed > duration:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # 통계 출력
    if elapsed > 0:
        avg_fps = frame_count / elapsed
        print(f"\n{model_name} 모델 성능:")
        print(f"  - 평균 FPS: {avg_fps:.2f}")
        print(f"  - 총 프레임: {frame_count}")
        print(f"  - 실행 시간: {elapsed:.1f}초")

if __name__ == "__main__":
    while True:
        print("=== SleepyDriver 라이브러리 테스트 ===")
        
        # 의존성 안내
        install_dependencies()
        
        print("\n사용 가능한 모델들:")
        try:
            available_models = ModelRegistry.list_models()
            for i, model in enumerate(available_models, 1):
                print(f"{i}. {model}")
        except Exception as e:
            print(f"모델 목록 로드 실패: {e}")
            break
        
        print(f"{len(available_models) + 1}. 종료")
        
        choice = input(f"\n모델 선택 (1-{len(available_models) + 1}): ").strip()
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_models):
                selected_model = available_models[choice_num - 1]
                print(f"{selected_model} 모델 선택됨")
                test_single_model(selected_model)
            elif choice_num == len(available_models) + 1:
                print("프로그램을 종료합니다.")
                break
            else:
                print("잘못된 선택입니다.")
        except ValueError:
            print("숫자를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            break 