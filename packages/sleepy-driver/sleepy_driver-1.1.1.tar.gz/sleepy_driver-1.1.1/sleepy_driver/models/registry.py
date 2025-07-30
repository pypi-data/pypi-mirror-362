"""
모델 레지스트리 - 팩토리 패턴을 사용한 모델 관리

다양한 눈 감지 모델들을 등록하고 관리하는 시스템입니다.
지연 로딩을 통해 의존성 문제를 해결합니다.
"""

from typing import Dict, Callable, List
from .base import EyeStateDetector

class ModelRegistry:
    """
    모델 레지스트리 - 팩토리 패턴
    
    모델을 지연 로딩 방식으로 등록하고 관리합니다.
    """
    _factories: Dict[str, Callable[[], EyeStateDetector]] = {}
    
    @classmethod
    def register(cls, name: str, factory: Callable[[], EyeStateDetector]):
        """
        모델 팩토리 함수 등록
        
        Args:
            name: 모델 이름
            factory: 모델 인스턴스를 생성하는 팩토리 함수
        """
        cls._factories[name] = factory
        print(f"✓ {name} 모델이 등록되었습니다")
    
    @classmethod
    def create(cls, name: str) -> EyeStateDetector:
        """
        등록된 모델 인스턴스 생성
        
        Args:
            name: 모델 이름
            
        Returns:
            EyeStateDetector: 모델 인스턴스
            
        Raises:
            ValueError: 모델이 등록되지 않은 경우
            ImportError: 모델 의존성이 없는 경우
        """
        if name not in cls._factories:
            available = list(cls._factories.keys())
            raise ValueError(f"모델 '{name}'이 등록되지 않았습니다. 사용 가능한 모델: {available}")
        
        try:
            factory = cls._factories[name]
            model = factory()
            model.initialize()  # 모델 초기화
            return model
        except Exception as e:
            raise ImportError(f"모델 '{name}' 생성 실패: {str(e)}")
    
    @classmethod
    def list_models(cls) -> List[str]:
        """등록된 모든 모델 이름 반환"""
        return list(cls._factories.keys())
    
    @classmethod
    def is_registered(cls, name: str) -> bool:
        """모델이 등록되어 있는지 확인"""
        return name in cls._factories
    
    @classmethod
    def clear(cls):
        """모든 등록된 모델 제거 (테스트용)"""
        cls._factories.clear()

# =============================================================================
# 기본 모델들 등록
# =============================================================================

def _create_opencv_model():
    """OpenCV 모델 팩토리"""
    from .opencv_model import OpenCVEyeModel
    return OpenCVEyeModel()

def _create_ml_model():
    """MLEye 모델 팩토리"""
    from .ml_model import MLEyeModel
    return MLEyeModel()

def _create_mlp_model():
    """MLP 모델 팩토리"""
    from .mlp_model import MLPEyeModel
    return MLPEyeModel()

def _create_point_model():
    """Point 모델 팩토리"""
    from .point_model import PointEyeModel
    return PointEyeModel()

# 모델들을 자동 등록
def _register_default_models():
    """기본 제공 모델들을 레지스트리에 등록"""
    ModelRegistry.register("opencv", _create_opencv_model)
    ModelRegistry.register("ml", _create_ml_model)
    ModelRegistry.register("mlp", _create_mlp_model)
    ModelRegistry.register("point", _create_point_model)
    
    print(f"등록된 모델들: {ModelRegistry.list_models()}")

# 모듈 import 시 자동 등록
_register_default_models() 