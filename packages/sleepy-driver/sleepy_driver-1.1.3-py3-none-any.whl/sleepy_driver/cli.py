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
        version="SleepyDriver 1.1.3"
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
    """데모 실행 - 새로운 원라이너 API 사용"""
    try:
        # 새로운 원라이너 API 사용!
        from . import start_detection
        
        print(f"🎬 원라이너 API로 데모 시작!")
        start_detection(model_name, threshold_ms, mirror=True, show_info=True)
        
    except ImportError as e:
        print(f"❌ 모듈 로드 실패: {e}")
        print("💡 해결: pip install sleepy-driver[all]")
    except Exception as e:
        print(f"❌ 데모 실행 실패: {e}")

if __name__ == "__main__":
    main() 