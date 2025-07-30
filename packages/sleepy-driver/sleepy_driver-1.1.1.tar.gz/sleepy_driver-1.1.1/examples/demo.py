#!/usr/bin/env python3
"""
SleepyDriver 라이브러리 데모

새로운 API를 사용한 간단하고 깔끔한 졸음 감지 예제입니다.
"""

import cv2
import time
import sys
import os

# 상위 디렉토리의 sleepy_driver 모듈을 import할 수 있도록 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sleepy_driver import quick_detector, list_available_models

def main():
    """메인 데모 함수"""
    print("🚗 SleepyDriver Demo Started!")
    print("=" * 50)
    
    # 사용 가능한 모델 표시
    models = list_available_models()
    print(f"Available models: {models}")
    
    # 모델 선택
    print("\nSelect a model:")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    
    try:
        choice = int(input("Choice (number): ")) - 1
        if 0 <= choice < len(models):
            selected_model = models[choice]
        else:
            print("Invalid choice. Using opencv model.")
            selected_model = "opencv"
    except ValueError:
        print("Invalid input. Using opencv model.")
        selected_model = "opencv"
    
    print(f"\n🔍 Starting drowsiness detection with {selected_model} model...")
    
    # 감지기 생성 (매우 간단!)
    try:
        detector = quick_detector(selected_model, threshold_ms=1000)  # 1초 임계값
        print(f"✅ Detector created successfully: {detector.get_model_info()}")
    except Exception as e:
        print(f"❌ Model load failed: {e}")
        if "joblib" in str(e):
            print("💡 Solution: pip install joblib scikit-learn")
        elif "torch" in str(e):
            print("💡 Solution: pip install torch torchvision")
        return
    
    # 카메라 시작
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    if not cap.isOpened():
        print("❌ Cannot open camera.")
        return
    
    print("\n📹 Camera started!")
    print("👀 Please position your face in front of the camera")
    print("😴 Close your eyes for 2+ seconds to trigger drowsiness alert")
    print("🚪 Press 'q' to quit")
    
    # 감지 루프
    frame_count = 0
    start_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)  # 좌우 반전
        frame_count += 1
        
        # 🔥 핵심: 한 줄로 졸음 감지!
        result = detector.detect(frame)
        
        # 결과 표시
        if result.success:
            # 눈 상태 결정 (영어로, 더 명확하게)
            eyes_status = "CLOSED" if result.both_eyes_closed else "OPEN"
            drowsy_status = "DROWSY ALERT!" if result.is_drowsy else "AWAKE"
            
            # 좌우 눈 개별 상태 (화면 기준으로 올바르게 표시)
            left_status = "CLOSED" if result.right_eye_closed else "OPEN"  # 화면 왼쪽은 사용자 오른쪽 눈
            right_status = "CLOSED" if result.left_eye_closed else "OPEN"  # 화면 오른쪽은 사용자 왼쪽 눈
            
            # 색상 설정
            color = (0, 0, 255) if result.is_drowsy else (0, 255, 0)
            
            # 정보 표시 (초대형! 멀리서도 확실히 보이도록!)
            cv2.putText(frame, f"{selected_model.upper()} MODEL", (25, 80),
                       cv2.FONT_HERSHEY_SIMPLEX, 2.2, (255, 255, 0), 6)
            cv2.putText(frame, f"EYES: {eyes_status}", (25, 160),
                       cv2.FONT_HERSHEY_SIMPLEX, 2.2, (0, 255, 0), 6)
            cv2.putText(frame, f"L:{left_status[:1]} R:{right_status[:1]}", (25, 240),
                       cv2.FONT_HERSHEY_SIMPLEX, 2.2, (255, 255, 0), 6)
            cv2.putText(frame, f"STATUS: {drowsy_status}", (25, 320),
                       cv2.FONT_HERSHEY_SIMPLEX, 2.2, color, 6)
            cv2.putText(frame, f"DURATION: {result.closed_duration_ms:.0f}ms", (25, 400),
                       cv2.FONT_HERSHEY_SIMPLEX, 2.2, (100, 255, 255), 6)
            
            # 졸음 경고 - 매우 강한 시각적 효과!
            if result.is_drowsy:
                # 1. 전체 화면에 깜빡이는 빨간색 배경
                alpha = 0.3 if int(time.time() * 10) % 2 == 0 else 0.1  # 깜빡임 효과
                overlay = frame.copy()
                cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), -1)
                cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
                
                # 2. 두꺼운 빨간색 테두리 (깜빡임)
                border_thickness = 15 if int(time.time() * 5) % 2 == 0 else 10
                cv2.rectangle(frame, (0, 0), (frame.shape[1]-1, frame.shape[0]-1), (0, 0, 255), border_thickness)
                
                # 3. 중앙에 거대한 경고 메시지
                warning_text = "DROWSINESS DETECTED!"
                text_size = cv2.getTextSize(warning_text, cv2.FONT_HERSHEY_SIMPLEX, 4.0, 12)[0]
                text_x = (frame.shape[1] - text_size[0]) // 2
                text_y = frame.shape[0] // 2
                
                # 텍스트 배경 (검은색 반투명, 거대한 박스)
                cv2.rectangle(frame, (text_x-60, text_y-100), (text_x+text_size[0]+60, text_y+60), 
                             (0, 0, 0), -1)
                cv2.rectangle(frame, (text_x-60, text_y-100), (text_x+text_size[0]+60, text_y+60), 
                             (0, 0, 255), 12)
                
                # 경고 텍스트 (거대한 글씨)
                cv2.putText(frame, warning_text, (text_x, text_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 4.0, (255, 255, 255), 12)
                
                # 4. 상단에 추가 경고 (거대하게)
                cv2.putText(frame, "TAKE A BREAK!", (frame.shape[1]//2 - 250, 120),
                           cv2.FONT_HERSHEY_SIMPLEX, 3.5, (0, 0, 255), 8)
                
                # 5. 터미널에도 경고 메시지 + 다양한 소리 시도
                if int(time.time() * 2) % 2 == 0:  # 0.5초마다
                    print(f"🚨 DROWSINESS ALERT! Duration: {result.closed_duration_ms}ms")
                    
                    # 여러 소리 방법 시도
                    try:
                        # 방법 1: 시스템 벨 (여러 번)
                        for _ in range(3):
                            print('\a', end='', flush=True)
                            time.sleep(0.1)
                        
                        # 방법 2: 터미널에서 소리 (macOS/Linux)
                        import os
                        import subprocess
                        if os.name == 'posix':  # macOS/Linux
                            try:
                                subprocess.run(['afplay', '/System/Library/Sounds/Ping.aiff'], 
                                             check=False, timeout=1)
                            except:
                                try:
                                    subprocess.run(['paplay', '/usr/share/sounds/alsa/Front_Left.wav'], 
                                                 check=False, timeout=1)
                                except:
                                    pass
                        elif os.name == 'nt':  # Windows
                            try:
                                import winsound
                                winsound.Beep(1000, 500)  # 1000Hz, 0.5초
                            except:
                                pass
                    except:
                        pass  # 소리 재생 실패 시 무시
                
        # FPS 표시 (거대하게!)
        elapsed = time.time() - start_time
        if elapsed > 0:
            fps = frame_count / elapsed
            cv2.putText(frame, f"FPS: {fps:.1f}", (frame.shape[1] - 280, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 255, 255), 5)
        
        # 사용법 안내 (거대하게!)
        cv2.putText(frame, "Press 'Q' to QUIT", (25, frame.shape[0] - 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.8, (200, 200, 200), 5)
        
        # 화면 표시
        cv2.imshow("🚗 SleepyDriver Demo", frame)
        
        # 키 입력 확인
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    # 정리
    cap.release()
    cv2.destroyAllWindows()
    
    # 통계 출력
    print(f"\n📊 Session Statistics:")
    print(f"  - Runtime: {elapsed:.1f}s")
    print(f"  - Total frames: {frame_count}")
    print(f"  - Average FPS: {frame_count/elapsed:.1f}")
    print(f"  - Model used: {selected_model}")
    
    print("\n🎉 SleepyDriver demo finished!")

if __name__ == "__main__":
    main() 