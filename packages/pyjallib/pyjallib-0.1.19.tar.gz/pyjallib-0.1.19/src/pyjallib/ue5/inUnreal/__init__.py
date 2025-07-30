#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UE5 inUnreal 패키지
Unreal Engine 5가 실행 중일 때만 사용 가능한 모듈들

주의: 이 패키지의 모든 모듈은 Unreal Engine이 실행 중일 때만 임포트 가능합니다.
"""

# UE5 가용성 확인
def is_ue5_available() -> bool:
    """
    Unreal Engine 5가 사용 가능한지 확인합니다.
    
    Returns:
        bool: UE5가 사용 가능하면 True, 그렇지 않으면 False
    """
    try:
        import unreal
        return True
    except ImportError:
        return False

# 기본적으로 사용 가능한 모듈들
__all__ = ['is_ue5_available']

# UE5가 사용 가능한 경우에만 모듈들을 임포트
if is_ue5_available():
    try:
        from .importerSettings import ImporterSettings
        __all__.append('ImporterSettings')
    except ImportError as e:
        ImporterSettings = None
        print(f"[PyJalLib] ImporterSettings 임포트 실패: {e}")

    try:
        from .baseImporter import BaseImporter
        __all__.append('BaseImporter')
    except ImportError as e:
        BaseImporter = None
        print(f"[PyJalLib] BaseImporter 임포트 실패: {e}")

    try:
        from .skeletonImporter import SkeletonImporter
        __all__.append('SkeletonImporter')
    except ImportError as e:
        SkeletonImporter = None
        print(f"[PyJalLib] SkeletonImporter 임포트 실패: {e}")

    try:
        from .skeletalMeshImporter import SkeletalMeshImporter
        __all__.append('SkeletalMeshImporter')
    except ImportError as e:
        SkeletalMeshImporter = None
        print(f"[PyJalLib] SkeletalMeshImporter 임포트 실패: {e}")

    try:
        from .animationImporter import AnimationImporter
        __all__.append('AnimationImporter')
    except ImportError as e:
        AnimationImporter = None
        print(f"[PyJalLib] AnimationImporter 임포트 실패: {e}")

else:
    # UE5가 사용 불가능한 경우 모든 모듈을 None으로 설정
    ImporterSettings = None
    BaseImporter = None
    SkeletonImporter = None
    SkeletalMeshImporter = None
    AnimationImporter = None
    print("[PyJalLib] Unreal Engine이 실행되지 않았습니다. inUnreal 모듈들을 사용할 수 없습니다.")

def get_available_modules() -> list:
    """
    현재 사용 가능한 모듈 목록을 반환합니다.
    
    Returns:
        list: 사용 가능한 모듈 이름 목록
    """
    available = []
    if 'ImporterSettings' in __all__ and ImporterSettings is not None:
        available.append('ImporterSettings')
    if 'BaseImporter' in __all__ and BaseImporter is not None:
        available.append('BaseImporter')
    if 'SkeletonImporter' in __all__ and SkeletonImporter is not None:
        available.append('SkeletonImporter')
    if 'SkeletalMeshImporter' in __all__ and SkeletalMeshImporter is not None:
        available.append('SkeletalMeshImporter')
    if 'AnimationImporter' in __all__ and AnimationImporter is not None:
        available.append('AnimationImporter')
    return available

# 헬퍼 함수도 __all__에 추가
__all__.append('get_available_modules') 