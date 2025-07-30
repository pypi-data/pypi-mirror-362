#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
뼈대(Bone) 모듈 - 3ds Max용 뼈대 생성 관련 기능 제공
원본 MAXScript의 bone.ms를 Python으로 변환하였으며, pymxs 모듈 기반으로 구현됨
"""

from dataclasses import dataclass

from pymxs import runtime as rt
from .name import Name
from .anim import Anim
from .helper import Helper
from .constraint import Constraint


class Bone:
    """
    뼈대(Bone) 관련 기능을 제공하는 클래스.
    MAXScript의 _Bone 구조체 개념을 Python으로 재구현한 클래스이며,
    3ds Max의 기능들을 pymxs API를 통해 제어합니다.
    """
    
    def __init__(self, nameService=None, animService=None, helperService=None, constraintService=None):
        """
        클래스 초기화.
        
        Args:
            nameService: 이름 처리 서비스 (제공되지 않으면 새로 생성)
            animService: 애니메이션 서비스 (제공되지 않으면 새로 생성)
            helperService: 헬퍼 객체 서비스 (제공되지 않으면 새로 생성)
            constraintService: 제약 서비스 (제공되지 않으면 새로 생성)
        """
        self.name = nameService if nameService else Name()
        self.anim = animService if animService else Anim()
        self.helper = helperService if helperService else Helper(nameService=self.name)
        self.const = constraintService if constraintService else Constraint(nameService=self.name, helperService=self.helper)
    
    def remove_ik(self, inBone):
        """
        뼈대에서 IK 체인을 제거.
        
        Args:
            inBone: IK 체인을 제거할 뼈대 객체
        """
        # pos 또는 rotation 속성이 없는 경우에만 IK 체인 제거
        if (not rt.isProperty(inBone, "pos")) or (not rt.isProperty(inBone, "rotation")):
            rt.HDIKSys.RemoveChain(inBone)
    
    def get_bone_assemblyHead(self, inBone):
        """
        뼈대 어셈블리의 헤드를 가져옴.
        
        Args:
            inBone: 대상 뼈대 객체
            
        Returns:
            어셈블리 헤드 또는 None
        """
        tempBone = inBone
        while tempBone is not None:
            if tempBone.assemblyHead:
                return tempBone
            if not tempBone.assemblyMember:
                break
            tempBone = tempBone.parent
        
        return None
    
    def put_child_into_bone_assembly(self, inBone):
        """
        자식 뼈대를 어셈블리에 추가.
        
        Args:
            inBone: 어셈블리에 추가할 자식 뼈대
        """
        if inBone.parent is not None and inBone.parent.assemblyMember:
            inBone.assemblyMember = True
            inBone.assemblyMemberOpen = True
    
    def sort_bones_as_hierarchy(self, inBoneArray):
        """
        뼈대 배열을 계층 구조에 따라 정렬.
        
        Args:
            inBoneArray: 정렬할 뼈대 객체 배열
            
        Returns:
            계층 구조에 따라 정렬된 뼈대 배열
        """
        # BoneLevel 구조체 정의 (Python 클래스로 구현)
        @dataclass
        class BoneLevel:
            index: int
            level: int
        
        # 뼈대 구조체 배열 초기화
        bones = []
        
        # 뼈대 구조체 배열 채우기. 계층 수준을 0으로 초기화
        for i in range(len(inBoneArray)):
            bones.append(BoneLevel(i, 0))
        
        # 뼈대 배열의 각 뼈대에 대한 계층 수준 계산
        # 계층 수준은 현재 뼈대와 루트 노드 사이의 조상 수
        for i in range(len(bones)):
            node = inBoneArray[bones[i].index]
            n = 0
            while node is not None:
                n += 1
                node = node.parent
            bones[i].level = n
        
        # 계층 수준에 따라 뼈대 배열 정렬
        bones.sort(key=lambda x: x.level)
        
        # 정렬된 뼈대를 저장할 새 배열 준비
        returnBonesArray = []
        for i in range(len(inBoneArray)):
            returnBonesArray.append(inBoneArray[bones[i].index])
        
        return returnBonesArray
    
    def correct_negative_stretch(self, bone, ask=True):
        """
        뼈대의 음수 스케일 보정.
        
        Args:
            bone: 보정할 뼈대 객체
            ask: 사용자에게 확인 요청 여부 (기본값: True)
            
        Returns:
            None
        """
        axisIndex = 0
        
        # 뼈대 축에 따라 인덱스 설정
        if bone.boneAxis == rt.Name("X"):
            axisIndex = 0
        elif bone.boneAxis == rt.Name("Y"):
            axisIndex = 1
        elif bone.boneAxis == rt.Name("Z"):
            axisIndex = 2
        
        ooscale = bone.objectOffsetScale
        
        # 음수 스케일 보정
        if (ooscale[axisIndex] < 0) and ((not ask) or rt.queryBox("Correct negative scale?", title=bone.Name)):
            ooscale[axisIndex] = -ooscale[axisIndex]
            axisIndex = axisIndex + 2
            if axisIndex > 2:
                axisIndex = axisIndex - 3
            ooscale[axisIndex] = -ooscale[axisIndex]
            bone.objectOffsetScale = ooscale
    
    def reset_scale_of_selected_bones(self, ask=True):
        """
        선택된 뼈대들의 스케일 초기화.
        
        Args:
            ask: 음수 스케일 보정 확인 요청 여부 (기본값: True)
            
        Returns:
            None
        """
        # 선택된 객체 중 BoneGeometry 타입만 수집
        bones = [item for item in rt.selection if rt.classOf(item) == rt.BoneGeometry]
        
        # 계층 구조에 따라 뼈대 정렬
        bones = self.sort_bones_as_hierarchy(rt.selection)
        
        # 뼈대 배열의 모든 뼈대에 대해 스케일 초기화
        for i in range(len(bones)):
            rt.ResetScale(bones[i])
            if ask:
                self.correct_negative_stretch(bones[i], False)
    
    def is_nub_bone(self, inputBone):
        """
        뼈대가 Nub 뼈대인지 확인 (부모 및 자식이 없는 단일 뼈대).
        
        Args:
            inputBone: 확인할 뼈대 객체
            
        Returns:
            True: Nub 뼈대인 경우
            False: 그 외의 경우
        """
        if rt.classOf(inputBone) == rt.BoneGeometry:
            if inputBone.parent is None and inputBone.children.count == 0:
                return True
            else:
                return False
        return False
    
    def is_end_bone(self, inputBone):
        """
        뼈대가 End 뼈대인지 확인 (부모는 있지만 자식이 없는 뼈대).
        
        Args:
            inputBone: 확인할 뼈대 객체
            
        Returns:
            True: End 뼈대인 경우
            False: 그 외의 경우
        """
        if rt.classOf(inputBone) == rt.BoneGeometry:
            if inputBone.parent is not None and inputBone.children.count == 0:
                return True
            else:
                return False
        return False
    
    def create_nub_bone(self, inName, inSize, inBoneScaleType=rt.Name("none")):
        """
        Nub 뼈대 생성.
        
        Args:
            inName: 뼈대 이름
            inSize: 뼈대 크기
            inBoneScaleType: 뼈대 스케일 타입 (기본값: rt.Name("none"))
        Returns:
            생성된 Nub 뼈대
        """
        nubBone = None
        
        # 화면 갱신 중지 상태에서 뼈대 생성
        rt.disableSceneRedraw()
        
        # 뼈대 생성 및 속성 설정
        nubBone = rt.BoneSys.createBone(rt.Point3(0, 0, 0), rt.Point3(1, 0, 0), rt.Point3(0, 0, 1))
        
        nubBone.width = inSize
        nubBone.height = inSize
        nubBone.taper = 90
        nubBone.length = inSize
        nubBone.frontfin = False
        nubBone.backfin = False
        nubBone.sidefins = False
        nubBone.name = self.name.remove_name_part("Index", inName)
        nubBone.name = self.name.remove_name_part("Nub", nubBone.name)
        nubBone.name = self.name.replace_name_part("Nub", nubBone.name, self.name.get_name_part_value_by_description("Nub", "Nub"))
        
        nubBone.boneScaleType = inBoneScaleType
        
        # 화면 갱신 재개
        rt.enableSceneRedraw()
        rt.redrawViews()
        
        return nubBone
    
    def create_nub_bone_on_obj(self, inObj, inSize=1):
        """
        객체 위치에 Nub 뼈대 생성.
        
        Args:
            inObj: 위치를 참조할 객체
            inSize: 뼈대 크기 (기본값: 1)
            
        Returns:
            생성된 Nub 뼈대
        """
        boneName = self.name.get_string(inObj.name)
        newBone = self.create_nub_bone(boneName, inSize)
        newBone.transform = inObj.transform
        
        return newBone
    
    def create_end_bone(self, inBone):
        """
        뼈대의 끝에 End 뼈대 생성.
        
        Args:
            inBone: 부모가 될 뼈대 객체
            
        Returns:
            생성된 End 뼈대
        """
        parentBone = inBone
        parentTrans = parentBone.transform
        parentPos = parentTrans.translation
        boneName = self.name.get_string(parentBone.name)
        newBone = self.create_nub_bone(boneName, parentBone.width)
        
        newBone.transform = parentTrans
        
        # 로컬 좌표계에서 이동
        self.anim.move_local(newBone, parentBone.length, 0, 0)
        
        newBone.parent = parentBone
        self.put_child_into_bone_assembly(newBone)
        
        # 뼈대 속성 설정
        newBone.width = parentBone.width
        newBone.height = parentBone.height
        newBone.frontfin = False
        newBone.backfin = False
        newBone.sidefins = False
        newBone.taper = 90
        newBone.length = (parentBone.width + parentBone.height) / 2
        newBone.wirecolor = parentBone.wirecolor
        
        return newBone
    
    def create_bone(self, inPointArray, inName, end=True, delPoint=False, parent=False, size=2, normals=None):
        """
        포인트 배열을 따라 뼈대 체인 생성.
        
        Args:
            inPointArray: 뼈대 위치를 정의하는 포인트 배열
            inName: 뼈대 기본 이름
            end: End 뼈대 생성 여부 (기본값: True)
            delPoint: 포인트 삭제 여부 (기본값: False)
            parent: 부모 Nub 포인트 생성 여부 (기본값: False)
            size: 뼈대 크기 (기본값: 2)
            normals: 법선 벡터 배열 (기본값: None)
            
        Returns:
            생성된 뼈대 배열 또는 False (실패 시)
        """
        if normals is None:
            normals = []
            
        tempBone = None
        newBone = None
        
        returnBoneArray = []
        
        if len(inPointArray) != 1:
            for i in range(len(inPointArray) - 1):
                boneNum = i
                
                if len(normals) == len(inPointArray):
                    xDir = rt.normalize(inPointArray[i+1].transform.position - inPointArray[i].transform.position)
                    zDir = rt.normalize(rt.cross(xDir, normals[i]))
                    newBone = rt.BoneSys.createBone(inPointArray[i].transform.position, inPointArray[i+1].transform.position, zDir)
                else:
                    newBone = rt.BoneSys.createBone(inPointArray[i].transform.position, inPointArray[i+1].transform.position, rt.Point3(0, -1, 0))
                
                newBone.boneFreezeLength = True
                newBone.name = self.name.replace_name_part("Index", inName, str(boneNum))
                newBone.height = size
                newBone.width = size
                newBone.frontfin = False
                newBone.backfin = False
                newBone.sidefins = False
                
                returnBoneArray.append(newBone)
                
                if tempBone is not None:
                    tempTm = rt.copy(newBone.transform * rt.Inverse(tempBone.transform))
                    localRot = rt.quatToEuler(tempTm.rotation).x
                    
                    self.anim.rotate_local(newBone, -localRot, 0, 0)
                
                newBone.parent = tempBone
                tempBone = newBone
            
            if delPoint:
                for i in range(len(inPointArray)):
                    if (rt.classOf(inPointArray[i]) == rt.Dummy) or (rt.classOf(inPointArray[i]) == rt.ExposeTm) or (rt.classOf(inPointArray[i]) == rt.Point):
                        rt.delete(inPointArray[i])
            
            if parent:
                parentNubPointName = self.name.replace_type(inName, self.name.get_parent_str())
                parentNubPoint = self.helper.create_point(parentNubPointName, size=size, boxToggle=True, crossToggle=True)
                parentNubPoint.transform = returnBoneArray[0].transform
                returnBoneArray[0].parent = parentNubPoint
            
            rt.select(newBone)
            
            if end:
                endBone = self.create_end_bone(newBone)
                returnBoneArray.append(endBone)
                
                rt.clearSelection()
                
                return returnBoneArray
            else:
                return returnBoneArray
        else:
            return False
    
    def create_simple_bone(self, inLength, inName, end=True, size=1):
        """
        간단한 뼈대 생성 (시작점과 끝점 지정).
        
        Args:
            inLength: 뼈대 길이
            inName: 뼈대 이름
            end: End 뼈대 생성 여부 (기본값: True)
            size: 뼈대 크기 (기본값: 1)
            
        Returns:
            생성된 뼈대 배열
        """
        startPoint = self.helper.create_point("tempStart")
        endPoint = self.helper.create_point("tempEnd", pos=(inLength, 0, 0))
        returnBoneArray = self.create_bone([startPoint, endPoint], inName, end=end, delPoint=True, size=size)
        
        return returnBoneArray
    
    def create_stretch_bone(self, inPointArray, inName, size=2):
        """
        스트레치 뼈대 생성 (포인트를 따라 움직이는 뼈대).
        
        Args:
            inPointArray: 뼈대 위치를 정의하는 포인트 배열
            inName: 뼈대 기본 이름
            size: 뼈대 크기 (기본값: 2)
            
        Returns:
            생성된 스트레치 뼈대 배열
        """
        tempBone = []
        tempBone = self.create_bone(inPointArray, inName, size=size)
        
        for i in range(len(tempBone) - 1):
            self.const.assign_pos_const(tempBone[i], inPointArray[i])
            self.const.assign_lookat(tempBone[i], inPointArray[i+1])
        self.const.assign_pos_const(tempBone[-1], inPointArray[-1])
        
        return tempBone
    
    def create_simple_stretch_bone(self, inStart, inEnd, inName, squash=False, size=1):
        """
        간단한 스트레치 뼈대 생성 (시작점과 끝점 지정).
        
        Args:
            inStart: 시작 포인트
            inEnd: 끝 포인트
            inName: 뼈대 이름
            squash: 스쿼시 효과 적용 여부 (기본값: False)
            size: 뼈대 크기 (기본값: 1)
            
        Returns:
            생성된 스트레치 뼈대 배열
        """
        returnArray = []
        returnArray = self.create_stretch_bone([inStart, inEnd], inName, size=size)
        if squash:
            returnArray[0].boneScaleType = rt.Name("squash")
        
        return returnArray
    
    def get_bone_shape(self, inBone):
        """
        뼈대의 형태 속성 가져오기.
        
        Args:
            inBone: 속성을 가져올 뼈대 객체
            
        Returns:
            뼈대 형태 속성 배열
        """
        returnArray = []
        if rt.classOf(inBone) == rt.BoneGeometry:
            returnArray = [None] * 16  # 빈 배열 초기화
            returnArray[0] = inBone.width
            returnArray[1] = inBone.height
            returnArray[2] = inBone.taper
            returnArray[3] = inBone.length
            returnArray[4] = inBone.sidefins
            returnArray[5] = inBone.sidefinssize
            returnArray[6] = inBone.sidefinsstarttaper
            returnArray[7] = inBone.sidefinsendtaper
            returnArray[8] = inBone.frontfin
            returnArray[9] = inBone.frontfinsize
            returnArray[10] = inBone.frontfinstarttaper
            returnArray[11] = inBone.frontfinendtaper
            returnArray[12] = inBone.backfin
            returnArray[13] = inBone.backfinsize
            returnArray[14] = inBone.backfinstarttaper
            returnArray[15] = inBone.backfinendtaper
        
        return returnArray
    
    def pasete_bone_shape(self, targetBone, shapeArray):
        """
        뼈대에 형태 속성 적용.
        
        Args:
            targetBone: 속성을 적용할 뼈대 객체
            shapeArray: 적용할 뼈대 형태 속성 배열
            
        Returns:
            True: 성공
            False: 실패
        """
        if rt.classOf(targetBone) == rt.BoneGeometry:
            targetBone.width = shapeArray[0]
            targetBone.height = shapeArray[1]
            targetBone.taper = shapeArray[2]
            #targetBone.length = shapeArray[3]  # 길이는 변경하지 않음
            targetBone.sidefins = shapeArray[4]
            targetBone.sidefinssize = shapeArray[5]
            targetBone.sidefinsstarttaper = shapeArray[6]
            targetBone.sidefinsendtaper = shapeArray[7]
            targetBone.frontfin = shapeArray[8]
            targetBone.frontfinsize = shapeArray[9]
            targetBone.frontfinstarttaper = shapeArray[10]
            targetBone.frontfinendtaper = shapeArray[11]
            targetBone.backfin = shapeArray[12]
            targetBone.backfinsize = shapeArray[13]
            targetBone.backfinstarttaper = shapeArray[14]
            targetBone.backfinendtaper = shapeArray[15]
            
            if self.is_end_bone(targetBone):
                targetBone.taper = 90
                targetBone.length = (targetBone.width + targetBone.height) / 2
                targetBone.frontfin = False
                targetBone.backfin = False
                targetBone.sidefins = False
            
            return True
        return False
    
    def set_fin_on(self, inBone, side=True, front=True, back=False, inSize=2.0, inTaper=0.0):
        """
        뼈대의 핀(fin) 설정 활성화.
        
        Args:
            inBone: 핀을 설정할 뼈대 객체
            side: 측면 핀 활성화 여부 (기본값: True)
            front: 전면 핀 활성화 여부 (기본값: True)
            back: 후면 핀 활성화 여부 (기본값: False)
            inSize: 핀 크기 (기본값: 2.0)
            inTaper: 핀 테이퍼 (기본값: 0.0)
        """
        if rt.classOf(inBone) == rt.BoneGeometry:
            if not self.is_end_bone(inBone):
                inBone.frontfin = front
                inBone.frontfinsize = inSize
                inBone.frontfinstarttaper = inTaper
                inBone.frontfinendtaper = inTaper
                
                inBone.sidefins = side
                inBone.sidefinssize = inSize
                inBone.sidefinsstarttaper = inTaper
                inBone.sidefinsendtaper = inTaper
                
                inBone.backfin = back
                inBone.backfinsize = inSize
                inBone.backfinstarttaper = inTaper
                inBone.backfinendtaper = inTaper
    
    def set_fin_off(self, inBone):
        """
        뼈대의 모든 핀(fin) 비활성화.
        
        Args:
            inBone: 핀을 비활성화할 뼈대 객체
        """
        if rt.classOf(inBone) == rt.BoneGeometry:
            inBone.frontfin = False
            inBone.sidefins = False
            inBone.backfin = False
    
    def set_bone_size(self, inBone, inSize):
        """
        뼈대 크기 설정.
        
        Args:
            inBone: 크기를 설정할 뼈대 객체
            inSize: 설정할 크기
        """
        if rt.classOf(inBone) == rt.BoneGeometry:
            inBone.width = inSize
            inBone.height = inSize
            
            if self.is_end_bone(inBone) or self.is_nub_bone(inBone):
                inBone.taper = 90
                inBone.length = inSize
    
    def set_bone_taper(self, inBone, inTaper):
        """
        뼈대 테이퍼 설정.
        
        Args:
            inBone: 테이퍼를 설정할 뼈대 객체
            inTaper: 설정할 테이퍼 값
        """
        if rt.classOf(inBone) == rt.BoneGeometry:
            if not self.is_end_bone(inBone):
                inBone.taper = inTaper
    
    def delete_bones_safely(self, inBoneArray):
        """
        뼈대 배열을 안전하게 삭제.
        
        Args:
            inBoneArray: 삭제할 뼈대 배열
        """
        if len(inBoneArray) > 0:
            for targetBone in inBoneArray:
                self.const.collapse(targetBone)
                targetBone.parent = None
                rt.delete(targetBone)
            
            inBoneArray.clear()
    
    def select_first_children(self, inObj):
        """
        객체의 첫 번째 자식들을 재귀적으로 선택.
        
        Args:
            inObj: 시작 객체
            
        Returns:
            True: 자식이 있는 경우
            False: 자식이 없는 경우
        """
        rt.selectmore(inObj)
        
        for i in range(inObj.children.count):
            if self.select_first_children(inObj.children[i]):
                if inObj.children.count == 0 or inObj.children[0] is None:
                    return True
            else:
                return False
    
    def get_every_children(self, inObj):
        """
        객체의 모든 자식들을 가져옴.
        
        Args:
            inObj: 시작 객체
            
        Returns:
            자식 객체 배열
        """
        children = []
        
        if inObj.children.count != 0 and inObj.children[0] is not None:
            for i in range(inObj.children.count):
                children.append(inObj.children[i])
                children.extend(self.get_every_children(inObj.children[i]))
        
        return children
    
    def select_every_children(self, inObj, includeSelf=False):
        """
        객체의 모든 자식들을 선택.
        
        Args:
            inObj: 시작 객체
            includeSelf: 자신도 포함할지 여부 (기본값: False)
            
        Returns:
            선택된 자식 객체 배열
        """
        children = self.get_every_children(inObj)
        
        # 자신도 포함하는 경우
        if includeSelf:
            children.insert(0, inObj)
        
        rt.select(children)
    
    def get_bone_end_position(self, inBone):
        """
        뼈대 끝 위치 가져오기.
        
        Args:
            inBone: 대상 뼈대 객체
            
        Returns:
            뼈대 끝 위치 좌표
        """
        if rt.classOf(inBone) == rt.BoneGeometry:
            return rt.Point3(inBone.length, 0, 0) * inBone.objectTransform
        else:
            return inBone.transform.translation
    
    def link_skin_bone(self, inSkinBone, inOriBone):
        """
        스킨 뼈대를 원본 뼈대에 연결.
        
        Args:
            inSkinBone: 연결할 스킨 뼈대
            inOriBone: 원본 뼈대
        """
        self.anim.save_xform(inSkinBone)
        self.anim.set_xform(inSkinBone, space="World")
        
        self.anim.save_xform(inOriBone)
        
        rt.setPropertyController(inSkinBone.controller, "Scale", rt.scaleXYZ())
        
        linkConst = rt.link_constraint()
        linkConst.addTarget(inOriBone, 0)
        
        inSkinBone.controller = linkConst
        
        self.anim.set_xform(inSkinBone, space="World")
    
    def link_skin_bones(self, inSkinBoneArray, inOriBoneArray):
        """
        스킨 뼈대 배열을 원본 뼈대 배열에 연결.
        
        Args:
            inSkinBoneArray: 연결할 스킨 뼈대 배열
            inOriBoneArray: 원본 뼈대 배열
            
        Returns:
            True: 성공
            False: 실패
        """
        if len(inSkinBoneArray) != len(inOriBoneArray):
            print("Error: Skin bone array and original bone array must have the same length.")
            return False
        
        skinBoneDict = {}
        oriBoneDict = {}
        
        # 스킨 뼈대 딕셔너리 생성 (이름과 패턴화된 이름을 함께 저장)
        for item in inSkinBoneArray:
            # 아이템 저장
            skinBoneDict[item.name] = item
            # 언더스코어를 별표로 변환한 패턴 생성
            namePattern = self.name.remove_name_part("Base", item.name)
            namePattern = namePattern.replace("_", "*")
            skinBoneDict[item.name + "_Pattern"] = namePattern
        
        # 원본 뼈대 딕셔너리 생성 (이름과 패턴화된 이름을 함께 저장)
        for item in inOriBoneArray:
            # 아이템 저장
            oriBoneDict[item.name] = item
            # 공백을 별표로 변환한 패턴 생성
            namePattern = self.name.remove_name_part("Base", item.name)
            namePattern = namePattern.replace(" ", "*")
            oriBoneDict[item.name + "_Pattern"] = namePattern
        
        # 정렬된 배열 생성
        sortedSkinBoneArray = []
        sortedOriBoneArray = []
        
        # 같은 패턴을 가진 뼈대들을 찾아 매칭
        for skinName, skinBone in [(k, v) for k, v in skinBoneDict.items() if not k.endswith("_Pattern")]:
            skinPattern = skinBoneDict[skinName + "_Pattern"]
            
            for oriName, oriBone in [(k, v) for k, v in oriBoneDict.items() if not k.endswith("_Pattern")]:
                oriPattern = oriBoneDict[oriName + "_Pattern"]
                
                if rt.matchPattern(skinName, pattern=oriPattern):
                    sortedSkinBoneArray.append(skinBone)
                    sortedOriBoneArray.append(oriBone)
                    break
        # 링크 연결 수행
        for i in range(len(sortedSkinBoneArray)):
            self.link_skin_bone(sortedSkinBoneArray[i], sortedOriBoneArray[i])
        
        return True
    
    def unlink_skin_bone(self, inSkinBone):
        """
        스킨 뼈대를 원본 뼈대에서 연결 해제.
        
        Args:
            inSkinBone: 연결 해제할 스킨 뼈대
        """
        self.anim.save_xform(inSkinBone)
        self.anim.set_xform(inSkinBone)
        
        inSkinBone.controller = rt.prs()
        self.anim.set_xform(inSkinBone, space="World")
        
        return True
    
    def unlink_skin_bones(self, inSkinBoneArray):
        """
        스킨 뼈대 배열을 원본 뼈대에서 연결 해제.
        
        Args:
            inSkinBoneArray: 연결 해제할 스킨 뼈대 배열
        """
        for item in inSkinBoneArray:
            if rt.isValidObj(item):
                self.unlink_skin_bone(item)
        
        return True
    
    def create_skin_bone(self, inBoneArray, skipNub=True, mesh=True, link=True, skinBoneBaseName=""):
        """
        스킨 뼈대 생성.
        
        Args:
            inBoneArray: 원본 뼈대 배열
            skipNub: Nub 뼈대 건너뛰기 (기본값: True)
            mesh: 메시 스냅샷 사용 (기본값: True)
            link: 원본 뼈대에 연결 (기본값: True)
            skinBoneBaseName: 스킨 뼈대 기본 이름 (기본값: "b")
            
        Returns:
            생성된 스킨 뼈대 배열
        """
        bones = []
        skinBoneFilteringChar = "_"
        skinBonePushAmount = -0.02
        returnBones = []
        
        definedSkinBoneBaseName = self.name.get_name_part_value_by_description("Base", "SkinBone")
        
        for i in range(len(inBoneArray)):
            skinBoneName = self.name.replace_name_part("Base", inBoneArray[i].name, definedSkinBoneBaseName)
            skinBoneName = self.name.replace_filtering_char(skinBoneName, skinBoneFilteringChar)
            
            skinBone = self.create_nub_bone(f"{definedSkinBoneBaseName}_TempSkin", 2)
            skinBone.name = skinBoneName
            skinBone.wireColor = rt.Color(255, 88, 199)
            skinBone.transform = inBoneArray[i].transform
            
            if mesh:
                snapShotObj = rt.snapshot(inBoneArray[i])
                rt.addModifier(snapShotObj, rt.Push())
                snapShotObj.modifiers[rt.Name("Push")].Push_Value = skinBonePushAmount
                rt.collapseStack(snapShotObj)
                
                rt.addModifier(skinBone, rt.Edit_Poly())
                rt.execute("max modify mode")
                rt.modPanel.setCurrentObject(skinBone.modifiers[rt.Name("Edit_Poly")])
                skinBone.modifiers[rt.Name("Edit_Poly")].Attach(snapShotObj, editPolyNode=skinBone)
            
            skinBone.boneEnable = True
            skinBone.renderable = False
            skinBone.boneScaleType = rt.Name("None")
            
            bones.append(skinBone)
        
        for i in range(len(inBoneArray)):
            oriParentObj = inBoneArray[i].parent
            if oriParentObj is not None:
                skinBoneParentObjName = self.name.replace_name_part("Base", oriParentObj.name, definedSkinBoneBaseName)
                skinBoneParentObjName = self.name.replace_filtering_char(skinBoneParentObjName, skinBoneFilteringChar)
                bones[i].parent = rt.getNodeByName(skinBoneParentObjName)
            else:
                bones[i].parent = None
        
        for item in bones:
            item.showLinks = True
            item.showLinksOnly = True
        
        for item in bones:
            item.name = self.name.replace_name_part("Base", item.name, skinBoneBaseName)
        
        if link:
            self.link_skin_bones(bones, inBoneArray)
        
        if skipNub:
            for item in bones:
                if not rt.matchPattern(item.name, pattern=("*" + self.name.get_name_part_value_by_description("Nub", "Nub"))):
                    returnBones.append(item)
                else:
                    rt.delete(item)
        else:
            returnBones = bones.copy()
        
        bones.clear()
        
        return returnBones
    
    def create_skin_bone_from_bip(self, inBoneArray, skipNub=True, mesh=False, link=True, skinBoneBaseName=""):
        """
        바이페드 객체에서 스킨 뼈대 생성.
        
        Args:
            inBoneArray: 바이페드 객체 배열
            skipNub: Nub 뼈대 건너뛰기 (기본값: True)
            mesh: 메시 스냅샷 사용 (기본값: False)
            link: 원본 뼈대에 연결 (기본값: True)
            skinBoneBaseName: 스킨 뼈대 기본 이름 (기본값: "")
            
        Returns:
            생성된 스킨 뼈대 배열
        """
        # 바이페드 객체만 필터링, Twist 뼈대 제외, 루트 노드 제외
        targetBones = [item for item in inBoneArray 
                      if (rt.classOf(item) == rt.Biped_Object) 
                      and (not rt.matchPattern(item.name, pattern="*Twist*")) 
                      and (item != item.controller.rootNode)]
        
        returnSkinBones = self.create_skin_bone(targetBones, skipNub=skipNub, mesh=mesh, link=link, skinBoneBaseName=skinBoneBaseName)
        
        return returnSkinBones
    
    def create_skin_bone_from_bip_for_unreal(self, inBoneArray, skipNub=True, mesh=False, link=True, skinBoneBaseName=""):
        """
        언리얼 엔진용 바이페드 객체에서 스킨 뼈대 생성.
        
        Args:
            inBoneArray: 바이페드 객체 배열
            skipNub: Nub 뼈대 건너뛰기 (기본값: True)
            mesh: 메시 스냅샷 사용 (기본값: False)
            link: 원본 뼈대에 연결 (기본값: True)
            skinBoneBaseName: 스킨 뼈대 기본 이름 (기본값: "b")
            
        Returns:
            생성된 스킨 뼈대 배열 또는 False (실패 시)
        """
        genBones = self.create_skin_bone_from_bip(inBoneArray, skipNub=skipNub, mesh=mesh, link=link, skinBoneBaseName=skinBoneBaseName)
        if len(genBones) == 0:
            return False
        
        # 언리얼 엔진용으로 특정 뼈대 회전
        for item in genBones:
            if rt.matchPattern(item.name, pattern="*Pelvis*"):
                self.anim.rotate_local(item, 180, 0, 0)
            if rt.matchPattern(item.name, pattern="*Spine*"):
                self.anim.rotate_local(item, 180, 0, 0)
            if rt.matchPattern(item.name, pattern="*Neck*"):
                self.anim.rotate_local(item, 180, 0, 0)
            if rt.matchPattern(item.name, pattern="*Head*"):
                self.anim.rotate_local(item, 180, 0, 0)
        
        return genBones
    
    def gen_missing_bip_bones_for_ue5manny(self, inBoneArray):
        returnBones = []
        spine3 = None
        neck = None
        head = None
        
        handL = None
        handR = None
        
        fingerNames = ["index", "middle", "ring", "pinky"]
        knuckleName = "metacarpal"
        lKnuckleDistance = []
        rKnuckleDistance = []
        
        lFingers = []
        rFingers = []
        
        for item in inBoneArray:
            if rt.matchPattern(item.name, pattern="*spine 03"):
                spine3 = item
            if rt.matchPattern(item.name, pattern="*neck 01"):
                neck = item
            if rt.matchPattern(item.name, pattern="*head"):
                head = item
            if rt.matchPattern(item.name, pattern="*hand*l"):
                handL = item
            if rt.matchPattern(item.name, pattern="*hand*r"):
                handR = item
            
            for fingerName in fingerNames:
                if rt.matchPattern(item.name, pattern="*"+fingerName+"*01*l"):
                    lFingers.append(item)
                if rt.matchPattern(item.name, pattern="*"+fingerName+"*01*r"):
                    rFingers.append(item)
            for finger in lFingers:
                fingerDistance = rt.distance(finger, handL)
                lKnuckleDistance.append(fingerDistance)
            for finger in rFingers:
                fingerDistance = rt.distance(finger, handR)
                rKnuckleDistance.append(fingerDistance)
        
        filteringChar = self.name._get_filtering_char(inBoneArray[-1].name)
        isLower = inBoneArray[-1].name[0].islower()
        
        # Spine 4,5 생성
        spineName = self.name.get_name_part_value_by_description("Base", "Biped") + filteringChar + "Spine"
        
        spine4 = self.create_nub_bone(spineName, 2)
        spine5 = self.create_nub_bone(spineName, 2)
        
        spine4.name = self.name.replace_name_part("Index", spine4.name, "4")
        spine4.name = self.name.remove_name_part("Nub", spine4.name)
        spine5.name = self.name.replace_name_part("Index", spine5.name, "5")
        spine5.name = self.name.remove_name_part("Nub", spine5.name)
        if isLower:
            spine4.name = spine4.name.lower()
            spine5.name = spine5.name.lower()
        
        spineDistance = rt.distance(spine3, neck)/3.0
        rt.setProperty(spine4, "transform", spine3.transform)
        rt.setProperty(spine5, "transform", spine3.transform)
        
        self.anim.move_local(spine4, spineDistance, 0, 0)
        spine4PosConst = self.const.assign_pos_const_multi(spine4, [spine3, neck])
        spine4PosConst.setWeight(1, 100.0*(2.0/3.0))
        spine4PosConst.setWeight(2, 100.0 - (100.0*(2.0/3.0)))
        
        self.anim.move_local(spine5, spineDistance * 2, 0, 0)
        spine5PosConst = self.const.assign_pos_const_multi(spine5, [spine3, neck])
        spine5PosConst.setWeight(1, 100.0*(1.0/3.0))
        spine5PosConst.setWeight(2, 100.0 - (100.0*(1.0/3.0)))
        
        returnBones.append(spine4)
        returnBones.append(spine5)
        
        # 목 생성
        neckName = self.name.get_name_part_value_by_description("Base", "Biped") + filteringChar + "Neck"
        
        nekc2 = self.create_nub_bone(neckName, 2)
        
        nekc2.name = self.name.replace_name_part("Index", nekc2.name, "2")
        nekc2.name = self.name.remove_name_part("Nub", nekc2.name)
        if isLower:
            nekc2.name = nekc2.name.lower()
        
        neckDistance = rt.distance(neck, head)/2.0
        rt.setProperty(nekc2, "transform", neck.transform)
        self.anim.move_local(nekc2, neckDistance, 0, 0)
        neck2PosConst = self.const.assign_pos_const_multi(nekc2, [neck, head])
        
        returnBones.append(nekc2)
        
        # 손가락용 메타카팔 생성
        for i, finger in enumerate(lFingers):
            knuckleBoneName = self.name.add_suffix_to_real_name(finger.name, filteringChar+knuckleName)
            knuckleBoneName = self.name.remove_name_part("Index", knuckleBoneName)
            
            knuckleBone = self.create_nub_bone(knuckleBoneName, 2)
            knuckleBone.name = self.name.remove_name_part("Nub", knuckleBone.name)
            if isLower:
                knuckleBone.name = knuckleBone.name.lower()
                
            knuckleBone.transform = finger.transform
            lookAtConst = self.const.assign_lookat(knuckleBone, handL)
            lookAtConst.upnode_world = False
            lookAtConst.pickUpNode = handL
            lookAtConst.lookat_vector_length = 0.0
            lookAtConst.target_axisFlip = True
            self.const.collapse(knuckleBone)
            self.anim.move_local(knuckleBone, -lKnuckleDistance[i]*0.8, 0, 0)
            
            returnBones.append(knuckleBone)
        
        for i, finger in enumerate(rFingers):
            knuckleBoneName = self.name.add_suffix_to_real_name(finger.name, filteringChar+knuckleName)
            knuckleBoneName = self.name.remove_name_part("Index", knuckleBoneName)
            
            knuckleBone = self.create_nub_bone(knuckleBoneName, 2)
            knuckleBone.name = self.name.remove_name_part("Nub", knuckleBone.name)
            if isLower:
                knuckleBone.name = knuckleBone.name.lower()
                
            knuckleBone.transform = finger.transform
            lookAtConst = self.const.assign_lookat(knuckleBone, handR)
            lookAtConst.upnode_world = False
            lookAtConst.pickUpNode = handR
            lookAtConst.lookat_vector_length = 0.0
            lookAtConst.target_axisFlip = True
            self.const.collapse(knuckleBone)
            self.anim.move_local(knuckleBone, -rKnuckleDistance[i]*0.8, 0, 0)
            
            returnBones.append(knuckleBone)
        
        return returnBones
    
    def relink_missing_bip_bones_for_ue5manny(self, inBipArray, inMissingBoneArray):
        returnBones = []
        
        spine3 = None
        neck = None
        
        handL = None
        handR = None
        
        knuckleName = "metacarpal"
        
        for item in inBipArray:
            if rt.matchPattern(item.name, pattern="*spine 03"):
                spine3 = item
            if rt.matchPattern(item.name, pattern="*neck 01"):
                neck = item
            if rt.matchPattern(item.name, pattern="*hand*l"):
                handL = item
            if rt.matchPattern(item.name, pattern="*hand*r"):
                handR = item
        
        for item in inMissingBoneArray:
            if rt.matchPattern(item.name, pattern="*spine*"):
                item.parent = spine3
            if rt.matchPattern(item.name, pattern="*neck*"):
                item.parent = neck
            if rt.matchPattern(item.name, pattern=f"*{knuckleName}*l"):
                item.parent = handL
            if rt.matchPattern(item.name, pattern=f"*{knuckleName}*r"):
                item.parent = handR
        
        returnBones.append(inBipArray)
        returnBones.append(inMissingBoneArray)
        return returnBones
    
    def relink_missing_skin_bones_for_ue5manny(self, inSkinArray):
        returnBones = []
        spine3 = None
        spine4 = None
        spine5 = None
        
        neck = None
        neck2 = None
        head = None
        clavicleL = None
        clavicleR = None
        
        handL = None
        handR = None
        
        fingerNames = ["index", "middle", "ring", "pinky"]
        knuckleName = "metacarpal"
        
        lFingers = []
        rFingers = []
        
        for item in inSkinArray:
            if rt.matchPattern(item.name, pattern="*spine*03"):
                spine3 = item
            if rt.matchPattern(item.name, pattern="*neck*01"):
                neck = item
            if rt.matchPattern(item.name, pattern="*head*"):
                head = item
            if rt.matchPattern(item.name, pattern="*clavicle*l"):
                clavicleL = item
            if rt.matchPattern(item.name, pattern="*clavicle*r"):
                clavicleR = item
            
            if rt.matchPattern(item.name, pattern="*hand*l"):
                handL = item
            if rt.matchPattern(item.name, pattern="*hand*r"):
                handR = item
            
            for fingerName in fingerNames:
                if rt.matchPattern(item.name, pattern="*"+fingerName+"*01*l"):
                    lFingers.append(item)
                if rt.matchPattern(item.name, pattern="*"+fingerName+"*01*r"):
                    rFingers.append(item)
        
        for item in inSkinArray:
            if rt.matchPattern(item.name, pattern="*spine*04"):
                spine4 = item
                item.parent = spine3
            
            if rt.matchPattern(item.name, pattern="*spine*05"):
                spine5 = item
                item.parent = spine4
                neck.parent = spine5
                clavicleL.parent = spine5
                clavicleR.parent = spine5
                
            if rt.matchPattern(item.name, pattern="*neck*02"):
                neck2 = item
                item.parent = neck
                head.parent = neck2
            
            if rt.matchPattern(item.name, pattern=f"*{knuckleName}*l"):
                item.parent = handL
            if rt.matchPattern(item.name, pattern=f"*{knuckleName}*r"):
                item.parent = handR
                
        filteringChar = self.name._get_filtering_char(inSkinArray[-1].name)
        
        for item in lFingers:
            fingerNamePattern = self.name.add_suffix_to_real_name(item.name, filteringChar+knuckleName)
            fingerNamePattern = self.name.remove_name_part("Index", fingerNamePattern)
            for knuckle in inSkinArray:
                if rt.matchPattern(knuckle.name, pattern=fingerNamePattern):
                    item.parent = knuckle
                    break
        
        for item in rFingers:
            fingerNamePattern = self.name.add_suffix_to_real_name(item.name, filteringChar+knuckleName)
            fingerNamePattern = self.name.remove_name_part("Index", fingerNamePattern)
            for knuckle in inSkinArray:
                if rt.matchPattern(knuckle.name, pattern=fingerNamePattern):
                    item.parent = knuckle
                    break
        
        return returnBones
    
    def create_skin_bone_from_bip_for_ue5manny(self, inBoneArray, skipNub=True, mesh=False, link=True, isHuman=False, skinBoneBaseName=""):
        targetBones = [item for item in inBoneArray 
                      if (rt.classOf(item) == rt.Biped_Object) 
                      and (not rt.matchPattern(item.name, pattern="*Twist*")) 
                      and (item != item.controller.rootNode)]
        
        missingBipBones = []
        
        if isHuman:
            missingBipBones = self.gen_missing_bip_bones_for_ue5manny(targetBones)
            self.relink_missing_bip_bones_for_ue5manny(targetBones, missingBipBones)
        
        for item in missingBipBones:
            targetBones.append(item)
        
        sortedBipBones = self.sort_bones_as_hierarchy(targetBones)
        
        skinBones = self.create_skin_bone(sortedBipBones, skipNub=skipNub, mesh=mesh, link=False, skinBoneBaseName=skinBoneBaseName)
        if len(skinBones) == 0:
            return False
        
        pelvisBone = None
        lastSpineBone = None
        
        for item in skinBones:
            if rt.matchPattern(item.name.lower(), pattern="*pelvis*"):
                pelvisBone = item
            if rt.matchPattern(item.name.lower(), pattern="*spine*"):
                lastSpineBone = item
                foundChildren = self.get_every_children(item)
                for child in foundChildren:
                    if rt.matchPattern(child.name.lower(), pattern="*spine*"):
                        lastSpineBone = child
        
        if pelvisBone is not None and lastSpineBone is not None:
            for item in skinBones:
                if rt.matchPattern(item.name.lower(), pattern="*thigh*"):
                    item.parent = pelvisBone
                if rt.matchPattern(item.name.lower(), pattern="*clavicle*"):
                    item.parent = lastSpineBone
        
        for item in skinBones:
            if rt.matchPattern(item.name.lower(), pattern="*pelvis*"):
                self.anim.rotate_local(item, 180, 0, 0, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*spine*"):
                self.anim.rotate_local(item, 180, 0, 0, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*neck*"):
                self.anim.rotate_local(item, 180, 0, 0, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*head*"):
                self.anim.rotate_local(item, 180, 0, 0, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*thigh*l"):
                self.anim.rotate_local(item, 0, 0, 180, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*calf*l"):
                self.anim.rotate_local(item, 0, 0, 180, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*foot*l"):
                self.anim.rotate_local(item, 0, 0, 180, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*ball*r"):
                self.anim.rotate_local(item, 0, 0, 180, dontAffectChildren=True)
                
            if rt.matchPattern(item.name.lower(), pattern="*clavicle*r"):
                self.anim.rotate_local(item, 0, 0, -180, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*upperarm*r"):
                self.anim.rotate_local(item, 0, 0, -180, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*lowerarm*r"):
                self.anim.rotate_local(item, 0, 0, -180, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*hand*r"):
                self.anim.rotate_local(item, 0, 0, -180, dontAffectChildren=True)
            
            if rt.matchPattern(item.name.lower(), pattern="*thumb*r"):
                self.anim.rotate_local(item, 0, 0, 180, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*index*r"):
                self.anim.rotate_local(item, 0, 0, 180, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*middle*r"):
                self.anim.rotate_local(item, 0, 0, 180, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*ring*r"):
                self.anim.rotate_local(item, 0, 0, 180, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*pinky*r"):
                self.anim.rotate_local(item, 0, 0, 180, dontAffectChildren=True)
                
            if rt.matchPattern(item.name.lower(), pattern="*finger0*r"):
                self.anim.rotate_local(item, 0, 0, 180, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*finger1*r"):
                self.anim.rotate_local(item, 0, 0, 180, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*finger2*r"):
                self.anim.rotate_local(item, 0, 0, 180, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*finger3*r"):
                self.anim.rotate_local(item, 0, 0, 180, dontAffectChildren=True)
            if rt.matchPattern(item.name.lower(), pattern="*finger4*r"):
                self.anim.rotate_local(item, 0, 0, 180, dontAffectChildren=True)
            
            if rt.matchPattern(item.name.lower(), pattern="*metacarpal*"):
                tempArray = self.name._split_to_array(item.name)
                item.name = self.name._combine(tempArray, inFilChar="_")
                item.name = self.name.remove_name_part("Base", item.name)
            
            self.anim.save_xform(item)
            
        if isHuman:
            self.relink_missing_skin_bones_for_ue5manny(skinBones)
        
        self.link_skin_bones(skinBones, sortedBipBones)
        for item in skinBones:
            self.anim.save_xform(item)
        
        return (skinBones + missingBipBones)
    
    def set_bone_on(self, inBone):
        """
        뼈대 활성화.
        
        Args:
            inBone: 활성화할 뼈대 객체
        """
        if rt.classOf(inBone) == rt.BoneGeometry:
            inBone.boneEnable = True
    
    def set_bone_off(self, inBone):
        """
        뼈대 비활성화.
        
        Args:
            inBone: 비활성화할 뼈대 객체
        """
        if rt.classOf(inBone) == rt.BoneGeometry:
            inBone.boneEnable = False
    
    def set_bone_on_selection(self):
        """
        선택된 모든 뼈대 활성화.
        """
        selArray = list(rt.getCurrentSelection())
        for item in selArray:
            self.set_bone_on(item)
    
    def set_bone_off_selection(self):
        """
        선택된 모든 뼈대 비활성화.
        """
        selArray = list(rt.getCurrentSelection())
        for item in selArray:
            self.set_bone_off(item)
    
    def set_freeze_length_on(self, inBone):
        """
        뼈대 길이 고정 활성화.
        
        Args:
            inBone: 길이를 고정할 뼈대 객체
        """
        if rt.classOf(inBone) == rt.BoneGeometry:
            inBone.boneFreezeLength = True
    
    def set_freeze_length_off(self, inBone):
        """
        뼈대 길이 고정 비활성화.
        
        Args:
            inBone: 길이 고정을 해제할 뼈대 객체
        """
        if rt.classOf(inBone) == rt.BoneGeometry:
            inBone.boneFreezeLength = False
    
    def set_freeze_length_on_selection(self):
        """
        선택된 모든 뼈대의 길이 고정 활성화.
        """
        selArray = list(rt.getCurrentSelection())
        for item in selArray:
            self.set_freeze_length_on(item)
    
    def set_freeze_length_off_selection(self):
        """
        선택된 모든 뼈대의 길이 고정 비활성화.
        """
        selArray = list(rt.getCurrentSelection())
        for item in selArray:
            self.set_freeze_length_off(item)
            
    def turn_bone(self, inBone, inAngle):
        """
        입력된 각도만큼 입력된 본의 로컬 X 축을 회전 합니다.
        
        Args:
            inBone: 회전할 뼈대 객체
            inAngle: 회전할 각도
        """
        if rt.classOf(inBone) == rt.BoneGeometry:
            self.anim.rotate_local(inBone, inAngle, 0, 0, dontAffectChildren=True)