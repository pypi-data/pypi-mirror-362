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

__version__ = "1.1.4"
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
                        
                        # 3. 중앙 대형 경고 메시지 (demo.py와 동일하게!)
                        warning_text = "DROWSINESS DETECTED!"
                        text_size = cv2.getTextSize(warning_text, cv2.FONT_HERSHEY_SIMPLEX, 4.0, 12)[0]
                        text_x = (frame.shape[1] - text_size[0]) // 2
                        text_y = frame.shape[0] // 2
                        
                        # 경고 배경 (더 큰 박스)
                        cv2.rectangle(frame, (text_x-60, text_y-100), (text_x+text_size[0]+60, text_y+60), 
                                     (0, 0, 0), -1)
                        cv2.rectangle(frame, (text_x-60, text_y-100), (text_x+text_size[0]+60, text_y+60), 
                                     (0, 0, 255), 12)
                        
                        # 경고 텍스트 (검은 테두리로 더 선명하게!)
                        # 검은 테두리 (8방향)
                        for dx in [-3, 0, 3]:
                            for dy in [-3, 0, 3]:
                                if dx != 0 or dy != 0:
                                    cv2.putText(frame, warning_text, (text_x + dx, text_y + dy),
                                               cv2.FONT_HERSHEY_SIMPLEX, 4.0, (0, 0, 0), 15)
                        # 메인 텍스트 (밝은 청록색)
                        cv2.putText(frame, warning_text, (text_x, text_y),
                                   cv2.FONT_HERSHEY_SIMPLEX, 4.0, (0, 255, 255), 12)
                        
                        # 상단 추가 경고 (테두리 효과)
                        break_x = frame.shape[1]//2 - 250
                        break_y = 120
                        for dx in [-2, 0, 2]:
                            for dy in [-2, 0, 2]:
                                if dx != 0 or dy != 0:
                                    cv2.putText(frame, "TAKE A BREAK!", (break_x + dx, break_y + dy),
                                               cv2.FONT_HERSHEY_SIMPLEX, 3.5, (0, 0, 0), 10)
                        cv2.putText(frame, "TAKE A BREAK!", (break_x, break_y),
                                   cv2.FONT_HERSHEY_SIMPLEX, 3.5, (0, 255, 0), 8)
                    else:
                        status_text = "AWAKE"
                        color = (0, 255, 0)  # 초록색
                    
                    # demo.py와 동일한 스타일로 정보 표시!
                    # 눈 상태 결정
                    eyes_status = "CLOSED" if result.both_eyes_closed else "OPEN"
                    drowsy_status = "DROWSY ALERT!" if result.is_drowsy else "AWAKE"
                    
                    # 좌우 눈 개별 상태 (화면 기준으로 올바르게 표시)
                    left_status = "CLOSED" if result.right_eye_closed else "OPEN"   # 화면 왼쪽 = 사용자 오른쪽 눈
                    right_status = "CLOSED" if result.left_eye_closed else "OPEN"   # 화면 오른쪽 = 사용자 왼쪽 눈
                    
                    # 정보 표시 (배경에 관계없이 잘 보이도록 검은 테두리 추가!)
                    def draw_text_with_outline(img, text, pos, font, size, color, thickness, outline_color=(0, 0, 0), outline_thickness=2):
                        """텍스트에 검은 테두리를 추가하여 가독성 향상"""
                        x, y = pos
                        # 1. 검은 테두리 그리기 (8방향)
                        for dx in [-outline_thickness, 0, outline_thickness]:
                            for dy in [-outline_thickness, 0, outline_thickness]:
                                if dx != 0 or dy != 0:
                                    cv2.putText(img, text, (x + dx, y + dy), font, size, outline_color, thickness + outline_thickness)
                        # 2. 메인 텍스트 그리기
                        cv2.putText(img, text, pos, font, size, color, thickness)
                    
                    # 모든 텍스트에 테두리 효과 적용
                    draw_text_with_outline(frame, f"{model_name.upper()} MODEL", (25, 80),
                                         cv2.FONT_HERSHEY_SIMPLEX, 2.2, (255, 255, 0), 6)
                    draw_text_with_outline(frame, f"EYES: {eyes_status}", (25, 160),
                                         cv2.FONT_HERSHEY_SIMPLEX, 2.2, (0, 255, 0), 6)
                    draw_text_with_outline(frame, f"L:{left_status[:1]} R:{right_status[:1]}", (25, 240),
                                         cv2.FONT_HERSHEY_SIMPLEX, 2.2, (255, 255, 0), 6)
                    draw_text_with_outline(frame, f"STATUS: {drowsy_status}", (25, 320),
                                         cv2.FONT_HERSHEY_SIMPLEX, 2.2, color, 6)
                    draw_text_with_outline(frame, f"DURATION: {result.closed_duration_ms:.0f}ms", (25, 400),
                                         cv2.FONT_HERSHEY_SIMPLEX, 2.2, (0, 255, 255), 6)
            
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