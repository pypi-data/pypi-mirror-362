#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
자동 쇄골(AutoClavicle) 모듈 - 3ds Max용 자동화된 쇄골 기능 제공
원본 MAXScript의 autoclavicle.ms를 Python으로 변환하였으며, pymxs 모듈 기반으로 구현됨
"""

from pymxs import runtime as rt

# Import necessary service classes for default initialization
from .name import Name
from .anim import Anim
from .helper import Helper
from .bone import Bone
from .constraint import Constraint
from .bip import Bip

from .boneChain import BoneChain


class AutoClavicle:
    """
    자동 쇄골(AutoClavicle) 관련 기능을 제공하는 클래스.
    MAXScript의 _AutoClavicleBone 구조체 개념을 Python으로 재구현한 클래스이며,
    3ds Max의 기능들을 pymxs API를 통해 제어합니다.
    """
    
    def __init__(self, nameService=None, animService=None, helperService=None, boneService=None, constraintService=None, bipService=None):
        """
        클래스 초기화
        
        Args:
            nameService: 이름 처리 서비스 (제공되지 않으면 새로 생성)
            animService: 애니메이션 서비스 (제공되지 않으면 새로 생성)
            helperService: 헬퍼 객체 서비스 (제공되지 않으면 새로 생성)
            boneService: 뼈대 서비스 (제공되지 않으면 새로 생성)
            constraintService: 제약 서비스 (제공되지 않으면 새로 생성)
            bipService: Biped 서비스 (제공되지 않으면 새로 생성)
        """
        # 서비스 인스턴스 설정 또는 생성
        self.name = nameService if nameService else Name()
        self.anim = animService if animService else Anim()
        # 종속성이 있는 서비스들은 이미 생성된 서비스들을 전달
        self.helper = helperService if helperService else Helper(nameService=self.name)
        self.bone = boneService if boneService else Bone(nameService=self.name, animService=self.anim)
        self.const = constraintService if constraintService else Constraint(nameService=self.name)
        self.bip = bipService if bipService else Bip(nameService=self.name, animService=self.anim)
        
        self.boneSize = 2.0
        self.rotTargetUpperArmPosConstExpression = ""
        self.rotTargetUpperArmPosConstExpression += "local clavicleDistance = distance clavicle upperArm\n"
        self.rotTargetUpperArmPosConstExpression += "local xPos = (clavicleDistance/2.0) * distanceDir * liftScale\n"
        self.rotTargetUpperArmPosConstExpression += "[xPos, 0.0, 0.0]\n"
        
        # 초기화된 결과를 저장할 변수들
        self.genBones = []
        self.genHelpers = []
        self.clavicle = None
        self.upperArm = None
        self.liftScale = 0.8
        
    def reset(self):
        """
        클래스의 주요 컴포넌트들을 초기화합니다.
        서비스가 아닌 클래스 자체의 작업 데이터를 초기화하는 함수입니다.
        
        Returns:
            self: 메소드 체이닝을 위한 자기 자신 반환
        """
        self.genBones = []
        self.genHelpers = []
        self.clavicle = None
        self.upperArm = None
        self.liftScale = 0.8
        
        return self
    
    def create_bones(self, inClavicle, inUpperArm, liftScale=0.8):
        """
        자동 쇄골 뼈를 생성하고 설정합니다.
        
        Args:
            inClavicle: 쇄골 뼈 객체
            inUpperArm: 상완 뼈 객체
            liftScale: 들어올림 스케일 (기본값: 0.8)
            
        Returns:
            생성된 자동 쇄골 뼈대 배열 또는 AutoClavicleChain 클래스에 전달할 수 있는 딕셔너리
        """
        if not rt.isValidNode(inClavicle) or not rt.isValidNode(inUpperArm):
            return False
        
        # 리스트 초기화
        genBones = []
        genHelpers = []
        
        # 쇄골과 상완 사이의 거리 계산
        clavicleLength = rt.distance(inClavicle, inUpperArm)
        facingDirVec = inUpperArm.transform.position - inClavicle.transform.position
        inObjXAxisVec = inClavicle.objectTransform.row1
        distanceDir = 1.0 if rt.dot(inObjXAxisVec, facingDirVec) > 0 else -1.0
        clavicleLength *= distanceDir
        
        # 자동 쇄골 이름 생성 및 뼈대 생성
        autoClavicleName = self.name.replace_name_part("RealName", inClavicle.name, "Auto" + self.name._get_filtering_char(inClavicle.name) + "Clavicle")
        if inClavicle.name[0].islower():
            autoClavicleName = autoClavicleName.lower()
        
        autoClavicleBone = self.bone.create_nub_bone(autoClavicleName, 2)
        autoClavicleBone.name = self.name.remove_name_part("Nub", autoClavicleBone.name)
        autoClavicleBone.transform = inClavicle.transform
        autoClavicleBone.parent = inClavicle
        autoClvaiclePosConst = self.const.assign_pos_const_multi(autoClavicleBone, [inClavicle, inUpperArm])
        genBones.append(autoClavicleBone)
        
        # 타겟 헬퍼 포인트 생성 (쇄골과 상완용)
        rotTargetClavicle = self.helper.create_point(self.name.replace_name_part("Type", autoClavicleName, self.name.get_name_part_value_by_description("Type", "Target")))
        rotTargetClavicle.name = self.name.replace_name_part("Index", rotTargetClavicle.name, "0")
        rotTargetClavicle.transform = inClavicle.transform
        rotTargetClavicle.parent = inClavicle
        rotTargetClaviclePosConst = self.const.assign_pos_const(rotTargetClavicle, inUpperArm)
        genHelpers.append(rotTargetClavicle)
        
        rotTargetUpperArm = self.helper.create_point(self.name.replace_name_part("Type", autoClavicleName, self.name.get_name_part_value_by_description("Type", "Target")))
        rotTargetUpperArm.name = self.name.add_suffix_to_real_name(rotTargetUpperArm.name, self.name._get_filtering_char(inClavicle.name) + "arm")
        rotTargetUpperArm.transform = inUpperArm.transform
        rotTargetUpperArm.parent = inUpperArm
        rotTargetUpperArmPosConst = self.const.assign_pos_script_controller(rotTargetUpperArm)
        rotTargetUpperArmPosConst.addConstant("distanceDir", distanceDir)
        rotTargetUpperArmPosConst.addConstant("liftScale", liftScale)
        rotTargetUpperArmPosConst.addNode("clavicle", inClavicle)
        rotTargetUpperArmPosConst.addNode("upperArm", inUpperArm)
        rotTargetUpperArmPosConst.setExpression(self.rotTargetUpperArmPosConstExpression)
        genHelpers.append(rotTargetUpperArm)
        
        # 회전 헬퍼 포인트 생성
        autoClavicleRotHelper = self.helper.create_point(self.name.replace_name_part("Type", autoClavicleName, self.name.get_name_part_value_by_description("Type", "Rotation")))
        autoClavicleRotHelper.transform = autoClavicleBone.transform
        autoClavicleRotHelper.parent = inClavicle
        autoClavicleRotHelperPosConst = self.const.assign_pos_const_multi(autoClavicleRotHelper, [inClavicle, inUpperArm])
        
        lookAtConst = self.const.assign_lookat_multi(autoClavicleRotHelper, [rotTargetClavicle, rotTargetUpperArm])
        
        lookAtConst.upnode_world = False
        lookAtConst.pickUpNode = inClavicle
        lookAtConst.lookat_vector_length = 0.0
        if distanceDir < 0:
            lookAtConst.target_axisFlip = True
        
        genHelpers.append(autoClavicleRotHelper)
        
        # ik 헬퍼 포인트 생성
        ikGoal = self.helper.create_point(autoClavicleName, boxToggle=False, crossToggle=True)
        ikGoal.transform = inClavicle.transform
        self.anim.move_local(ikGoal, clavicleLength, 0.0, 0.0)
        ikGoal.name = self.name.replace_name_part("Type", autoClavicleName, self.name.get_name_part_value_by_description("Type", "Target"))
        ikGoal.name = self.name.replace_name_part("Index", ikGoal.name, "1")
        
        ikGoal.parent = autoClavicleRotHelper
        
        autClavicleLookAtConst = self.const.assign_lookat(autoClavicleBone, ikGoal)
        if clavicleLength < 0:
            autClavicleLookAtConst.target_axisFlip = True
        autClavicleLookAtConst.upnode_world = False
        autClavicleLookAtConst.pickUpNode = inClavicle
        autClavicleLookAtConst.lookat_vector_length = 0.0
        genHelpers.append(ikGoal)
        
        # 결과를 멤버 변수에 저장
        self.genBones = genBones
        self.genHelpers = genHelpers
        self.clavicle = inClavicle
        self.upperArm = inUpperArm
        self.liftScale = liftScale
        
        # AutoClavicleChain에 전달할 수 있는 딕셔너리 형태로 결과 반환
        result = {
            "Bones": genBones,
            "Helpers": genHelpers,
            "SourceBones": [inClavicle, inUpperArm],
            "Parameters": [liftScale]
        }
        
        # 메소드 호출 후 데이터 초기화
        self.reset()
        
        rt.redrawViews()
        
        return BoneChain.from_result(result)
    
    def create_bones_from_chain(self, inBoneChain: BoneChain):
        """
        기존 BoneChain 객체에서 자동 쇄골 뼈를 생성합니다.
        기존 설정을 복원하거나 저장된 데이터에서 쇄골 셋업을 재생성할 때 사용합니다.
        
        Args:
            inBoneChain (BoneChain): 자동 쇄골 정보를 포함한 BoneChain 객체
        
        Returns:
            BoneChain: 업데이트된 BoneChain 객체 또는 실패 시 None
        """
        if not inBoneChain or inBoneChain.is_empty():
            return None
        
        inBoneChain.delete()
            
        # BoneChain에서 필요한 정보 추출
        sourceBones = inBoneChain.sourceBones
        parameters = inBoneChain.parameters
        
        # 필수 소스 본 확인
        if len(sourceBones) < 2 or not rt.isValidNode(sourceBones[0]) or not rt.isValidNode(sourceBones[1]):
            return None
            
        # 파라미터 가져오기 (또는 기본값 사용)
        liftScale = parameters[0] if len(parameters) > 0 else 0.8
        
        # 쇄골 생성
        inClavicle = sourceBones[0]
        inUpperArm = sourceBones[1]
        
        # 새로운 쇄골 생성
        return self.create_bones(inClavicle, inUpperArm, liftScale)
