#!/usr/bin/env python3
"""
SleepyDriver CLI - 명령행 인터페이스

설치 후 `sleepy-driver-demo` 명령으로 실행할 수 있습니다.
"""

import sys
import os
import argparse
from pathlib import Path

def main():
    """CLI 메인 함수"""
    parser = argparse.ArgumentParser(
        description="SleepyDriver - AI 기반 졸음 감지 시스템",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  sleepy-driver-demo                    # 기본 OpenCV 모델로 데모 실행
  sleepy-driver-demo --model mlp        # MLP 모델로 실행
  sleepy-driver-demo --threshold 2000   # 2초 임계값으로 실행
  sleepy-driver-demo --list-models      # 사용 가능한 모델 목록 표시

지원 모델:
  - opencv: 전통적인 컴퓨터 비전 (기본값)
  - ml: RandomForest 기반 머신러닝
  - mlp: CNN 기반 딥러닝
  - point: MediaPipe 랜드마크 기반
        """
    )
    
    parser.add_argument(
        "--model", "-m",
        choices=["opencv", "ml", "mlp", "point"],
        default="opencv",
        help="사용할 감지 모델 (기본값: opencv)"
    )
    
    parser.add_argument(
        "--threshold", "-t",
        type=int,
        default=1000,
        help="졸음 판단 임계값 (밀리초, 기본값: 1000)"
    )
    
    parser.add_argument(
        "--list-models", "-l",
        action="store_true",
        help="사용 가능한 모델 목록 표시"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="SleepyDriver 1.0.0"
    )
    
    args = parser.parse_args()
    
    # 모델 목록 표시
    if args.list_models:
        try:
            from . import list_available_models
            models = list_available_models()
            print("🚗 SleepyDriver - 사용 가능한 모델:")
            for i, model in enumerate(models, 1):
                print(f"  {i}. {model}")
        except ImportError as e:
            print(f"❌ 모델 목록을 가져올 수 없습니다: {e}")
        return
    
    # 데모 실행
    try:
        print(f"🚗 SleepyDriver 시작!")
        print(f"📊 모델: {args.model}")
        print(f"⏱️  임계값: {args.threshold}ms")
        print(f"🚪 종료하려면 'q'를 누르세요")
        print()
        
        # 데모 실행
        run_demo(args.model, args.threshold)
        
    except KeyboardInterrupt:
        print("\n👋 SleepyDriver를 종료합니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        print("💡 해결 방법:")
        print("  1. 카메라가 연결되어 있는지 확인")
        print("  2. 필요한 의존성 설치: pip install sleepy-driver[all]")
        print("  3. 다른 모델 시도: sleepy-driver-demo --model opencv")

def run_demo(model_name: str, threshold_ms: int):
    """데모 실행"""
    try:
        # 동적으로 데모 모듈 import
        from . import quick_detector
        import cv2
        import time
        
        # 감지기 생성
        detector = quick_detector(model_name, threshold_ms=threshold_ms)
        print(f"✅ {detector.get_model_info()} 모델 로드 완료!")
        
        # 카메라 시작
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("카메라를 열 수 없습니다")
        
        print("📹 카메라 시작됨! 졸음 감지 중...")
        
        frame_count = 0
        start_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame = cv2.flip(frame, 1)  # 좌우 반전
            frame_count += 1
            
            # 졸음 감지
            result = detector.detect(frame)
            
            # 결과 표시
            if result.success:
                # 상태 정보
                status = "DROWSY!" if result.is_drowsy else "Normal"
                color = (0, 0, 255) if result.is_drowsy else (0, 255, 0)
                
                # 정보 표시
                cv2.putText(frame, f"SleepyDriver - {model_name.upper()}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                cv2.putText(frame, f"Status: {status}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                cv2.putText(frame, f"Duration: {result.closed_duration_ms:.0f}ms", (10, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # 졸음 경고
                if result.is_drowsy:
                    cv2.putText(frame, "DROWSY ALERT!", (50, 150),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
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
            cv2.imshow("SleepyDriver CLI Demo", frame)
            
            # 키 입력 확인
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        
        # 정리
        cap.release()
        cv2.destroyAllWindows()
        
        # 통계
        print(f"\n📊 세션 통계:")
        print(f"  - 실행 시간: {elapsed:.1f}초")
        print(f"  - 총 프레임: {frame_count}")
        print(f"  - 평균 FPS: {frame_count/elapsed:.1f}")
        
    except ImportError as e:
        print(f"❌ 모듈 로드 실패: {e}")
        print("💡 해결: pip install sleepy-driver[all]")
    except Exception as e:
        print(f"❌ 데모 실행 실패: {e}")

if __name__ == "__main__":
    main() 