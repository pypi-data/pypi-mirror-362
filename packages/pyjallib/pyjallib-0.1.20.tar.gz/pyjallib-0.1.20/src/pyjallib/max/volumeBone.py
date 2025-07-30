#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
관절 부피 유지 본(Volume preserve Bone) 모듈 - 3ds Max용 관절의 부피를 유지하기 위해 추가되는 중간본들을 위한 모듈

이 모듈은 3ds Max에서 캐릭터 애니메이션 과정에서 관절 변형 시 발생하는 부피 감소 문제를 해결하기 위한
부피 유지 본 시스템을 제공합니다. 관절이 회전할 때 볼륨감을 자동으로 유지하는 보조 본을 생성하여
더 자연스러운 캐릭터 애니메이션을 구현할 수 있습니다.
"""

from pymxs import runtime as rt

# Import necessary service classes for default initialization
from .name import Name
from .anim import Anim
from .helper import Helper
from .bone import Bone
from .constraint import Constraint

from .boneChain import BoneChain


class VolumeBone:  # Updated class name to match the new file name
    """
    관절 부피 유지 본(Volume preserve Bone) 클래스
    
    3ds Max에서 관절의 부피를 유지하기 위해 추가되는 중간본들을 위한 클래스입니다.
    이 클래스는 관절이 회전할 때 자동으로 부피감을 유지하도록 하는 보조 본 시스템을 생성하고
    관리합니다. 부모 관절과 자식 관절 사이에 부피 유지 본을 배치하여 관절 변형 시 부피 감소를
    방지하고 더 자연스러운 움직임을 구현합니다.
    """
    def __init__(self, nameService=None, animService=None, constraintService=None, boneService=None, helperService=None):
        """
        클래스 초기화.
        
        필요한 서비스 객체들을 초기화하거나 외부에서 제공받습니다. 
        각 서비스 객체들은 본 생성, 이름 관리, 애니메이션 제어, 제약 조건 적용 등의 
        기능을 담당합니다.
        
        Args:
            nameService: 이름 처리 서비스 (제공되지 않으면 새로 생성)
            animService: 애니메이션 서비스 (제공되지 않으면 새로 생성)
            constraintService: 제약 서비스 (제공되지 않으면 새로 생성)
            boneService: 뼈대 서비스 (제공되지 않으면 새로 생성)
            helperService: 헬퍼 서비스 (제공되지 않으면 새로 생성)
        """
        # 서비스 인스턴스 설정 또는 생성
        self.name = nameService if nameService else Name()
        self.anim = animService if animService else Anim()
        
        # 종속성이 있는 서비스들은 이미 생성된 서비스들을 전달
        self.const = constraintService if constraintService else Constraint(nameService=self.name)
        self.bone = boneService if boneService else Bone(nameService=self.name, animService=self.anim)
        self.helper = helperService if helperService else Helper(nameService=self.name)
        
        self.rootBone = None
        self.rotHelper = None
        self.limb = None
        self.limbParent = None
        self.bones = []
        self.rotAxises = []
        self.transAxises = []
        self.transScales = []
        self.volumeSize = 5.0
        self.rotScale = 0.5
        
        self.posScriptExpression = (
            "localLimbTm = limb.transform * inverse limbParent.transform\n"
            "localDeltaTm = localLimbTm * inverse localRotRefTm\n"
            "\n"
            "q = localDeltaTm.rotation\n"
            "\n"
            "eulerRot = (quatToEuler q order:5)\n"
            "swizzledRot = (eulerAngles eulerRot.y eulerRot.z eulerRot.x)\n"
            "saturatedTwist = abs ((swizzledRot.x*axis.x + swizzledRot.y*axis.y + swizzledRot.z*axis.z)/180.0)\n"
            "\n"
            "trAxis * saturatedTwist * volumeSize * transScale\n"
        )
    
    def reset(self):
        """
        클래스의 주요 컴포넌트들을 초기화합니다.
        서비스가 아닌 클래스 자체의 작업 데이터를 초기화하는 함수입니다.
        
        Returns:
            self: 메소드 체이닝을 위한 자기 자신 반환
        """
        self.rootBone = None
        self.rotHelper = None
        self.limb = None
        self.limbParent = None
        self.bones = []
        self.rotAxises = []
        self.transAxises = []
        self.transScales = []
        self.volumeSize = 5.0
        self.rotScale = 0.5
        
        return self
    
    def create_root_bone(self, inObj, inParent, inRotScale=0.5):
        if rt.isValidNode(inObj) == False or rt.isValidNode(inParent) == False:
            return False
        
        if rt.isValidNode(self.rootBone) and rt.isValidNode(self.rotHelper):
            return self.rootBone
        
        rootBoneName = inObj.name
        filteringChar = self.name._get_filtering_char(rootBoneName)
        rootBoneName = self.name.add_suffix_to_real_name(rootBoneName, filteringChar+"Vol"+filteringChar+"Root")
        
        rootBone = self.bone.create_nub_bone(rootBoneName, 2)
        rootBone.name = self.name.remove_name_part("Nub", rootBone.name)
        if rootBone.name[0].islower():
            rootBone.name = rootBone.name.lower()
            rootBoneName = rootBoneName.lower()
            
        rt.setProperty(rootBone, "transform", inObj.transform)
        rootBone.parent = inObj
        
        rotHelper = self.helper.create_point(rootBoneName)
        rotHelper.name = self.name.replace_name_part("Type", rotHelper.name, self.name.get_name_part_value_by_description("Type", "Dummy"))
        rt.setProperty(rotHelper, "transform", inObj.transform)
        rotHelper.parent = inParent
        self.const.assign_pos_const(rotHelper, inObj)
        
        oriConst = self.const.assign_rot_const_multi(rootBone, [inObj, rotHelper])
        oriConst.setWeight(1, inRotScale * 100.0)
        oriConst.setWeight(2, (1.0 - inRotScale) * 100.0)
        
        self.rootBone = rootBone
        self.rotHelper = rotHelper
        self.limb = inObj
        self.limbParent = inParent
        
        return self.rootBone
    
    def create_bone(self, inObj, inParent, inRotScale=0.5, inVolumeSize=5.0, inRotAxis="Z", inTransAxis="PosY", inTransScale=1.0, useRootBone=True, inRootBone=None):
        if rt.isValidNode(inObj) == False or rt.isValidNode(inParent) == False:
            return False
        
        if useRootBone:
            if rt.isValidNode(self.rootBone) == False and rt.isValidNode(self.rotHelper) == False:
                return False
            self.rootBone = inRootBone if inRootBone else self.create_root_bone(inObj, inParent, inRotScale)
        else:
            self.create_root_bone(inObj, inParent, inRotScale)
        
        self.limb = inObj
        self.limbParent = inParent
        
        volBoneName = inObj.name
        filteringChar = self.name._get_filtering_char(volBoneName)
        volBoneName = self.name.add_suffix_to_real_name(volBoneName, filteringChar + "Vol" + filteringChar + inRotAxis + filteringChar+ inTransAxis)
        volBoneIndex = self.name.get_name("Index", volBoneName)
        
        volBone = self.bone.create_nub_bone(volBoneName, 2)
        volBone.name = self.name.remove_name_part("Nub", volBone.name)
        volBone.name = self.name.replace_name_part("Index", volBone.name, volBoneIndex)
        
        if volBone.name[0].islower():
            volBone.name = volBone.name.lower()
            volBoneName = volBoneName.lower()
        rt.setProperty(volBone, "transform", self.rootBone.transform)
        
        volBoneTrDir = rt.Point3(0.0, 0.0, 0.0)
        if inTransAxis == "PosX":
            volBoneTrDir = rt.Point3(1.0, 0.0, 0.0)
        elif inTransAxis == "NegX":
            volBoneTrDir = rt.Point3(-1.0, 0.0, 0.0)
        elif inTransAxis == "PosY":
            volBoneTrDir = rt.Point3(0.0, 1.0, 0.0)
        elif inTransAxis == "NegY":
            volBoneTrDir = rt.Point3(0.0, -1.0, 0.0)
        elif inTransAxis == "PosZ":
            volBoneTrDir = rt.Point3(0.0, 0.0, 1.0)
        elif inTransAxis == "NegZ":
            volBoneTrDir = rt.Point3(0.0, 0.0, -1.0)
        
        self.anim.move_local(volBone, volBoneTrDir[0]*inVolumeSize, volBoneTrDir[1]*inVolumeSize, volBoneTrDir[2]*inVolumeSize)
        volBone.parent = self.rootBone
        
        rotAxis = rt.Point3(0.0, 0.0, 0.0)
        if inRotAxis == "X":
            rotAxis = rt.Point3(1.0, 0.0, 0.0)
        elif inRotAxis == "Y":
            rotAxis = rt.Point3(0.0, 1.0, 0.0)
        elif inRotAxis == "Z":
            rotAxis = rt.Point3(0.0, 0.0, 1.0)
        
        # localRotRefTm = self.limb.transform * rt.inverse(self.limbParent.transform)
        localRotRefTm = self.limb.transform * rt.inverse(self.rotHelper.transform)
        volBonePosConst = self.const.assign_pos_script_controller(volBone)
        volBonePosConst.addNode("limb", self.limb)
        # volBonePosConst.addNode("limbParent", self.limbParent)
        volBonePosConst.addNode("limbParent", self.rotHelper)
        volBonePosConst.addConstant("axis", rotAxis)
        volBonePosConst.addConstant("transScale", rt.Float(inTransScale))
        volBonePosConst.addConstant("volumeSize", rt.Float(inVolumeSize))
        volBonePosConst.addConstant("localRotRefTm", localRotRefTm)
        volBonePosConst.addConstant("trAxis", volBoneTrDir)
        volBonePosConst.setExpression(self.posScriptExpression)
        volBonePosConst.update()
        
        return True
    
    def create_bones(self, inObj, inParent, inRotScale=0.5, inVolumeSize=5.0, inRotAxises=["Z"], inTransAxises=["PosY"], inTransScales=[1.0]):
        """
        여러 개의 부피 유지 본을 생성합니다.
        
        Args:
            inObj: 본을 생성할 객체
            inParent: 부모 객체
            inRotScale: 회전 비율
            inVolumeSize: 부피 크기
            inRotAxises: 회전 축 리스트
            inTransAxises: 변환 축 리스트
            inTransScales: 변환 비율 리스트
        
        Returns:
            BoneChain: 생성된 볼륨 본 체인 객체
        """
        if rt.isValidNode(inObj) == False or rt.isValidNode(inParent) == False:
            return None
        
        if len(inRotAxises) != len(inTransAxises) or len(inRotAxises) != len(inTransScales):
            return None
        
        rootBone = self.create_root_bone(inObj, inParent, inRotScale=inRotScale)
        
        # rootBone이 None이면 실패
        if not rootBone:
            return None
        
        # 볼륨 본들 생성
        bones = []
        for i in range(len(inRotAxises)):
            self.create_bone(inObj, inParent, inRotScale, inVolumeSize, inRotAxises[i], inTransAxises[i], inTransScales[i], useRootBone=True, inRootBone=rootBone)
            
            # 생성된 본의 이름 패턴으로 찾기
            volBoneName = inObj.name
            filteringChar = self.name._get_filtering_char(volBoneName)
            volBoneName = self.name.add_suffix_to_real_name(volBoneName, 
                          filteringChar + "Vol" + filteringChar + inRotAxises[i] + 
                          filteringChar + inTransAxises[i])
            
            if volBoneName[0].islower():
                volBoneName = volBoneName.lower()
                
            final_volBoneName = self.name.remove_name_part("Nub", volBoneName)
            volBone = rt.getNodeByName(final_volBoneName)
            if rt.isValidNode(volBone):
                bones.append(volBone)
        
        # 모든 생성된 본들 모음
        all_bones = [rootBone] + bones
        rotHelper = self.rotHelper
        
        # BoneChain에 필요한 형태의 결과 딕셔너리 생성
        result = {
            "Bones": all_bones,
            "Helpers": [rotHelper],
            "SourceBones": [inObj, inParent],
            "Parameters": [inRotScale, inVolumeSize] + inRotAxises + inTransAxises + inTransScales
        }
        
        # 메소드 호출 후 데이터 초기화
        self.reset()
        
        rt.redrawViews()
        
        return BoneChain.from_result(result)
    
    def create_bones_from_chain(self, inBoneChain: BoneChain):
        """
        기존 BoneChain 객체에서 볼륨 본을 생성합니다.
        기존 설정을 복원하거나 저장된 데이터에서 볼륨 본 셋업을 재생성할 때 사용합니다.
        
        Args:
            inBoneChain (BoneChain): 볼륨 본 정보를 포함한 BoneChain 객체
        
        Returns:
            BoneChain: 업데이트된 BoneChain 객체 또는 실패 시 None
        """
        if not inBoneChain or inBoneChain.is_empty():
            return None
            
        # 기존 객체 삭제 (delete_all 대신 delete 사용)
        # delete는 bones와 helpers만 삭제하고 sourceBones와 parameters는 유지함
        inBoneChain.delete()
            
        # BoneChain에서 필요한 정보 추출
        sourceBones = inBoneChain.sourceBones
        parameters = inBoneChain.parameters
        
        # 필수 소스 본 확인
        if len(sourceBones) < 2 or not rt.isValidNode(sourceBones[0]) or not rt.isValidNode(sourceBones[1]):
            return None
        
        # 최소 필요 파라미터 확인
        if len(parameters) < 2:
            return None
            
        # 파라미터 가져오기
        inRotScale = parameters[0]
        inVolumeSize = parameters[1]
        
        # 회전축, 변환축, 변환비율을 파라미터에서 추출
        # 최소한 하나의 축 세트는 필요
        param_count = len(parameters)
        if param_count <= 2:
            # 기본 값 사용
            inRotAxises = ["Z"]
            inTransAxises = ["PosY"]
            inTransScales = [1.0]
        else:
            # 파라미터 중간을 3등분하여 각 목록 추출
            axis_count = (param_count - 2) // 3
            
            inRotAxises = parameters[2:2+axis_count]
            inTransAxises = parameters[2+axis_count:2+axis_count*2]
            inTransScales = parameters[2+axis_count*2:2+axis_count*3]
            
            # 리스트 길이가 일치하지 않으면 기본값으로 보완
            if len(inRotAxises) != len(inTransAxises) or len(inRotAxises) != len(inTransScales):
                min_len = min(len(inRotAxises), len(inTransAxises), len(inTransScales))
                inRotAxises = inRotAxises[:min_len] if min_len > 0 else ["Z"]
                inTransAxises = inTransAxises[:min_len] if min_len > 0 else ["PosY"]
                inTransScales = inTransScales[:min_len] if min_len > 0 else [1.0]
            
        # 새로운 볼륨 본 생성
        inObj = sourceBones[0]
        inParent = sourceBones[1]
        
        return self.create_bones(inObj, inParent, inRotScale, inVolumeSize, inRotAxises, inTransAxises, inTransScales)
