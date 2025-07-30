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
            # 눈 상태 결정
            eyes_status = "Closed" if result.both_eyes_closed else "Open"
            drowsy_status = "DROWSY!" if result.is_drowsy else "Normal"
            
            # 좌우 눈 개별 상태 (화면 기준으로 올바르게 표시)
            left_status = "C" if result.right_eye_closed else "O"  # 화면 왼쪽은 사용자 오른쪽 눈
            right_status = "C" if result.left_eye_closed else "O"  # 화면 오른쪽은 사용자 왼쪽 눈
            
            # 색상 설정
            color = (0, 0, 255) if result.is_drowsy else (0, 255, 0)
            
            # 정보 표시 (기존 스타일과 유사하게)
            cv2.putText(frame, f"{selected_model} Model", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame, f"Eyes: {eyes_status}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"L:{left_status} R:{right_status}", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame, f"Status: {drowsy_status}", (10, 120),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            cv2.putText(frame, f"Time: {result.closed_duration_ms:.0f}ms", (10, 150),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # 졸음 경고만 빨간색으로 강조
            if result.is_drowsy:
                cv2.putText(frame, "DROWSY ALERT!", (50, 200),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                # 전체 화면에 빨간색 테두리
                cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 8)
                
        # FPS 표시
        elapsed = time.time() - start_time
        if elapsed > 0:
            fps = frame_count / elapsed
            cv2.putText(frame, f"FPS: {fps:.1f}", (frame.shape[1] - 120, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # 사용법 안내
        cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 128, 128), 2)
        
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