#!/usr/bin/env python3
"""
🚀 SleepyDriver 원라이너 사용 예제

이 파일은 SleepyDriver의 가장 간단한 사용법을 보여줍니다.
복잡한 코드 없이 바로 졸음 감지를 시작할 수 있어요!
"""

def example1_simplest():
    """가장 간단한 예제 - 1줄로 시작!"""
    print("📝 예제 1: 가장 간단한 사용법")
    print("="*50)
    
    from sleepy_driver import start_detection
    
    # 이게 전부에요! 1줄로 끝!
    start_detection()

def example2_choose_model():
    """모델 선택 예제"""
    print("📝 예제 2: 모델 선택하기")
    print("="*50)
    
    from sleepy_driver import start_detection
    
    # 원하는 모델로 시작
    start_detection('mlp')  # 가장 정확한 CNN 모델

def example3_custom_settings():
    """설정 변경 예제"""
    print("📝 예제 3: 설정 변경하기")
    print("="*50)
    
    from sleepy_driver import start_detection
    
    # 설정을 바꿔서 시작
    start_detection(
        model_name='opencv',    # 빠른 모델
        threshold_ms=2000,      # 2초 임계값 (더 관대하게)
        mirror=False,           # 좌우 반전 안 함
        show_info=True          # 화면에 정보 표시
    )

def example4_webcam_alias():
    """웹캠 감지 별칭 사용"""
    print("📝 예제 4: 웹캠 감지 별칭")
    print("="*50)
    
    from sleepy_driver import webcam_detection
    
    # start_detection과 동일하지만 이름이 더 명확
    webcam_detection('ml')

def example5_traditional_way():
    """기존 방식과의 비교"""
    print("📝 예제 5: 기존 방식 vs 새로운 방식")
    print("="*50)
    
    print("🟡 기존 방식 (복잡):")
    print("""
    from sleepy_driver import quick_detector
    import cv2
    
    detector = quick_detector('opencv')
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        result = detector.detect(frame)
        
        if result.is_drowsy:
            print(f"졸음 감지! {result.closed_duration_ms}ms")
            cv2.putText(frame, "DROWSY!", (20, 50), ...)
        else:
            cv2.putText(frame, "AWAKE", (20, 50), ...)
        
        cv2.imshow('Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    """)
    
    print("\n🟢 새로운 방식 (간단!):")
    print("""
    from sleepy_driver import start_detection
    start_detection()  # 끝!
    """)
    
    # 실제로 실행해보기
    print("실제로 새로운 방식 실행:")
    from sleepy_driver import start_detection
    start_detection()

def show_all_models():
    """사용 가능한 모든 모델 보기"""
    print("📝 사용 가능한 모델들")
    print("="*50)
    
    from sleepy_driver import list_available_models
    
    models = list_available_models()
    print("🎯 지원되는 모델:")
    for i, model in enumerate(models, 1):
        print(f"  {i}. {model}")
    
    print("\n💡 사용법:")
    for model in models:
        print(f"  start_detection('{model}')")

def main():
    """메인 함수 - 예제 선택"""
    print("🚗 SleepyDriver 원라이너 예제 모음")
    print("="*60)
    
    examples = [
        ("가장 간단한 사용법 (1줄!)", example1_simplest),
        ("모델 선택하기", example2_choose_model), 
        ("설정 변경하기", example3_custom_settings),
        ("웹캠 감지 별칭", example4_webcam_alias),
        ("기존 vs 새로운 방식", example5_traditional_way),
        ("사용 가능한 모델 보기", show_all_models),
    ]
    
    print("실행할 예제를 선택하세요:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    try:
        choice = int(input("\n선택 (1-6): ")) - 1
        if 0 <= choice < len(examples):
            name, func = examples[choice]
            print(f"\n🎬 {name} 실행 중...\n")
            func()
        else:
            print("❌ 잘못된 선택입니다.")
    except ValueError:
        print("❌ 숫자를 입력하세요.")
    except KeyboardInterrupt:
        print("\n👋 종료합니다.")

if __name__ == "__main__":
    main() 