"""
SleepyDriver - 졸음 감지 라이브러리

사용 예시:
    # 초간단 사용법 (1줄!)
    from sleepy_driver import start_detection
    start_detection()  # 기본 설정으로 바로 시작!
    
    # 모델 선택 (2줄!)
    from sleepy_driver import start_detection
    start_detection('mlp')  # MLP 모델로 바로 시작!

    # 기존 사용법
    from sleepy_driver import quick_detector
    
    detector = quick_detector("opencv")
    result = detector.detect(frame)
    
    if result.is_drowsy:
        print(f"졸음 감지! {result.duration_ms}ms")

    # 고급 사용법
    from sleepy_driver import EyeStateDetector, TimeBased
    
    class MyCustomModel(EyeStateDetector):
        def detect_eye_state(self, eye_image):
            # 사용자 구현
            return is_closed, confidence
    
    detector = DrowsinessDetector.create_with_custom_components(
        eye_detector=MyCustomModel(),
        drowsiness_analyzer=TimeBased(threshold_ms=2000)
    )
"""

from .core.detector import Detector, DetectionResult
from .core.results import EyeDetectionResult, DrowsinessResult
from .drowsiness.detector import DrowsinessDetector
from .drowsiness.analyzer import TimeBased, MLBased
from .models.base import EyeStateDetector
from .eye.targeting import EyeTargeting
from .models.registry import ModelRegistry

__version__ = "1.1.2"
__author__ = "SleepyDriver Team"

# 사용자가 주로 사용할 클래스들을 노출
__all__ = [
    # 메인 API
    "DrowsinessDetector",
    
    # 원라이너 API
    "start_detection", 
    "webcam_detection",
    "simple_detector",
    
    # 결과 클래스들
    "DetectionResult",
    "EyeDetectionResult", 
    "DrowsinessResult",
    
    # 컴포넌트 인터페이스
    "EyeStateDetector",
    "EyeTargeting",
    
    # 졸음 분석기들
    "TimeBased",
    "MLBased",
    
    # 모델 관리
    "ModelRegistry",
    
    # 기본 클래스
    "Detector",
    
    # 편의 함수들
    "quick_detector",
    "list_available_models"
]

# 편의 함수들
def list_available_models():
    """사용 가능한 모든 모델 목록 반환"""
    return ModelRegistry.list_models()

def quick_detector(model_name="opencv", threshold_ms=1000):
    """빠른 설정을 위한 편의 함수"""
    return DrowsinessDetector.create_with_model(model_name, threshold_ms)

def simple_detector(model_name="opencv"):
    """가장 간단한 감지기 생성 (기본 설정)"""
    return quick_detector(model_name, 1000)

def start_detection(model_name="opencv", threshold_ms=1000, mirror=True, show_info=True):
    """
    🚀 원라이너! 바로 웹캠 졸음 감지 시작
    
    Args:
        model_name: 사용할 모델 ('opencv', 'ml', 'mlp', 'point')
        threshold_ms: 졸음 판단 임계값 (밀리초)
        mirror: 좌우 반전 여부 (거울 모드)
        show_info: 화면에 정보 표시 여부
    """
    import cv2
    import os
    
    print(f"🚗 SleepyDriver 시작! (모델: {model_name})")
    
    try:
        # 감지기 생성
        detector = quick_detector(model_name, threshold_ms)
        print(f"✅ {model_name} 모델 로드 완료!")
        
        # 카메라 설정
        cap = cv2.VideoCapture(0)
        
        # 윈도우 환경에서 DirectShow 사용
        if os.name == 'nt':  # Windows
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            print("❌ 카메라를 열 수 없습니다!")
            print("💡 해결 방법:")
            print("  1. 다른 앱에서 카메라 사용 중인지 확인")
            print("  2. 윈도우: 설정 > 개인정보 > 카메라 권한 확인")
            return
        
        print("📹 카메라 연결 성공!")
        print("사용법: 'q' 키로 종료, 스페이스바로 일시정지")
        
        paused = False
        
        while True:
            if not paused:
                ret, frame = cap.read()
                if not ret:
                    print("⚠️ 프레임 읽기 실패!")
                    continue
                
                # 좌우 반전 (거울 모드)
                if mirror:
                    frame = cv2.flip(frame, 1)
                
                # 졸음 감지 (핵심!)
                result = detector.detect(frame)
                
                if show_info and result.success:
                    # 졸음 상태에 따른 표시
                    if result.is_drowsy:
                        status_text = f"DROWSY ALERT! ({result.closed_duration_ms}ms)"
                        color = (0, 0, 255)  # 빨간색
                        
                        # 강력한 졸음 경고 효과!
                        # 1. 깜빡이는 빨간 배경
                        import time
                        alpha = 0.3 if int(time.time() * 10) % 2 == 0 else 0.1
                        overlay = frame.copy()
                        cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), -1)
                        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
                        
                        # 2. 두꺼운 경고 테두리 (깜빡임)
                        border_thickness = 15 if int(time.time() * 5) % 2 == 0 else 8
                        cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), color, border_thickness)
                        
                        # 3. 중앙 경고 메시지
                        warning_text = "DROWSINESS DETECTED!"
                        text_size = cv2.getTextSize(warning_text, cv2.FONT_HERSHEY_SIMPLEX, 3.0, 8)[0]
                        text_x = (frame.shape[1] - text_size[0]) // 2
                        text_y = frame.shape[0] // 2
                        
                        # 경고 배경
                        cv2.rectangle(frame, (text_x-40, text_y-60), (text_x+text_size[0]+40, text_y+40), 
                                     (0, 0, 0), -1)
                        cv2.rectangle(frame, (text_x-40, text_y-60), (text_x+text_size[0]+40, text_y+40), 
                                     (0, 0, 255), 6)
                        
                        # 경고 텍스트
                        cv2.putText(frame, warning_text, (text_x, text_y),
                                   cv2.FONT_HERSHEY_SIMPLEX, 3.0, (255, 255, 255), 8)
                    else:
                        status_text = "AWAKE"
                        color = (0, 255, 0)  # 초록색
                    
                    # 정보 표시 (거대한 글씨로!)
                    cv2.putText(frame, status_text, (25, 80), 
                               cv2.FONT_HERSHEY_SIMPLEX, 2.2, color, 6)
                    cv2.putText(frame, f"Model: {model_name.upper()}", (25, 160), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 255, 0), 5)
                    
                    # 눈 상태 표시 (화면 기준으로 올바르게 매핑, 거대하게!)
                    left_eye = "C" if result.right_eye_closed else "O"   # 화면 왼쪽 = 사용자 오른쪽 눈
                    right_eye = "C" if result.left_eye_closed else "O"   # 화면 오른쪽 = 사용자 왼쪽 눈
                    cv2.putText(frame, f"Eyes: L:{left_eye} R:{right_eye}", (25, 240), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 255, 255), 5)
                    
                    # 지속 시간 표시 (추가)
                    cv2.putText(frame, f"Duration: {result.closed_duration_ms:.0f}ms", (25, 320), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1.8, (100, 255, 255), 5)
            
            # 화면 표시
            if 'frame' in locals():
                window_title = f'SleepyDriver ({model_name}) - Press Q to quit'
                cv2.imshow(window_title, frame)
            
            # 키 입력 처리
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # 'q' 또는 ESC
                break
            elif key == ord(' '):  # 스페이스바
                paused = not paused
                print("⏸️ 일시정지" if paused else "▶️ 재생")
        
        cap.release()
        cv2.destroyAllWindows()
        print("👋 SleepyDriver 종료!")
        
    except KeyboardInterrupt:
        print("\n⚠️ 사용자가 중단했습니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        if "joblib" in str(e) or "sklearn" in str(e):
            print("💡 해결: pip install sleepy-driver[ml]")
        elif "torch" in str(e):
            print("💡 해결: pip install sleepy-driver[dl]")

def webcam_detection(model_name="opencv", **kwargs):
    """
    웹캠 감지 별칭 (start_detection과 동일)
    """
    return start_detection(model_name, **kwargs) 