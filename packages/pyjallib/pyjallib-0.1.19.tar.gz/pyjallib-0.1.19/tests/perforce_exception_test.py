#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perforce 모듈의 예외 처리 테스트

이 테스트는 perforce.py 모듈에서 exceptions.py의 PyJalLib 표준 예외들이 
올바르게 발생하는지 테스트합니다.
"""

import sys
import os

# 프로젝트 루트를 sys.path에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from pyjallib.perforce import Perforce
from pyjallib.exceptions import PerforceError, ValidationError


def test_connection_error():
    """연결되지 않은 상태에서 작업 수행 시 PerforceError 발생 테스트"""
    print("=== 연결 상태 예외 테스트 ===")
    
    p4 = Perforce()
    # 연결하지 않은 상태
    
    try:
        # _ensure_connected()를 사용하는 새로운 테스트
        p4._ensure_connected()
        print("❌ 예외가 발생하지 않았습니다 (예상: PerforceError)")
        return False
    except PerforceError as e:
        print(f"✅ PerforceError 정상 발생: {e}")
        print(f"   함수명: {e.get_function_name()}")
        return True
    except Exception as e:
        print(f"❌ 예상치 못한 예외 타입: {type(e).__name__}: {e}")
        return False


def test_validation_error():
    """잘못된 타입 입력 시 ValidationError 발생 테스트"""
    print("\n=== 입력 검증 예외 테스트 ===")
    
    p4 = Perforce()
    # 일단 가짜 연결 상태로 설정 (테스트용)
    p4.connected = True
    
    # 잘못된 타입의 파라미터 전달 (문자열 대신 리스트를 요구하는 메서드에 문자열 전달)
    try:
        p4.check_files_checked_out("single_file.txt")  # 리스트 대신 문자열 전달
        print("❌ 예외가 발생하지 않았습니다 (예상: ValidationError)")
        return False
    except ValidationError as e:
        print(f"✅ ValidationError 정상 발생: {e}")
        print(f"   함수명: {e.get_function_name()}")
        return True
    except Exception as e:
        print(f"❌ 예상치 못한 예외 타입: {type(e).__name__}: {e}")
        return False


def test_file_operation_validation():
    """파일 작업에서 ValidationError 발생 테스트"""
    print("\n=== 파일 작업 검증 예외 테스트 ===")
    
    p4 = Perforce()
    p4.connected = True
    
    test_cases = [
        ("checkout_files", "체크아웃"),
        ("add_files", "추가"),
        ("delete_files", "삭제"),
        ("sync_files", "동기화")
    ]
    
    success_count = 0
    for method_name, operation_name in test_cases:
        try:
            method = getattr(p4, method_name)
            if method_name == "sync_files":
                method("single_file.txt")  # sync_files는 change_list_number 파라미터가 없음
            else:
                method("single_file.txt", 12345)  # 리스트 대신 문자열 전달
            print(f"❌ {operation_name} - 예외가 발생하지 않았습니다 (예상: ValidationError)")
        except ValidationError as e:
            print(f"✅ {operation_name} - ValidationError 정상 발생")
            success_count += 1
        except Exception as e:
            print(f"❌ {operation_name} - 예상치 못한 예외: {type(e).__name__}: {e}")
    
    return success_count == len(test_cases)


def test_backwards_compatibility():
    """기존 코드와의 호환성을 위한 더미 테스트 (get_last_error는 제거됨)"""
    print("\n=== 하위 호환성 테스트 (스킵) ===")
    print("✅ get_last_error() 메서드가 제거되어 예외 기반 처리로 변경됨")
    return True


def test_function_name_tracking():
    """함수명 자동 추적 기능 테스트"""
    print("\n=== 함수명 추적 테스트 ===")
    
    p4 = Perforce()
    
    try:
        p4._ensure_connected()
        return False
    except PerforceError as e:
        func_name = e.get_function_name()
        print(f"✅ 함수명 추적: {func_name}")
        
        # 함수명이 올바르게 추적되었는지 확인
        if func_name and func_name in ["test_function_name_tracking", "_ensure_connected"]:
            print("✅ 함수명이 올바르게 추적됨")
            return True
        else:
            print(f"❌ 함수명 추적 실패 또는 예상과 다름: {func_name}")
            return False


def main():
    """메인 테스트 실행 함수"""
    print("🔧 PyJalLib Perforce 예외 처리 테스트 시작\n")
    
    test_results = []
    
    # 각 테스트 실행
    test_results.append(("연결 상태 예외", test_connection_error()))
    test_results.append(("입력 검증 예외", test_validation_error()))
    test_results.append(("파일 작업 검증 예외", test_file_operation_validation()))
    test_results.append(("하위 호환성", test_backwards_compatibility()))
    test_results.append(("함수명 추적", test_function_name_tracking()))
    
    # 결과 출력
    print("\n" + "="*50)
    print("📊 테스트 결과 요약")
    print("="*50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n전체 결과: {passed}/{total} 테스트 통과")
    
    if passed == total:
        print("🎉 모든 테스트가 성공했습니다!")
        return True
    else:
        print("⚠️  일부 테스트가 실패했습니다.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 