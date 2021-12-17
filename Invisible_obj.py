###############################################################################
# Name: 
#   Invisible Obj
#
# Description: 
#     By this script you can community easily with visibility and LOD visibility
#     attribute and faster see invisible obj and switch between show type obj . 
#
# Author: 
#   Ahmadreza Rezaei
#
# Copyright (C) 2022 Ahmadreza Rezaei. All rights reserved.
###############################################################################


import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

from operator import and_

def maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window),QtWidgets.QWidget)
    
class invisibleClass(QtWidgets.QDialog):
    
    dialog_window=None
    id_scriptjob = None
    
    def __init__(self,parent=maya_main_window()):
        
        super(invisibleClass,self).__init__(parent)
        
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)
        self.setWindowTitle("Visibility")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setMinimumSize(500,500)
        self.createaction()
        self.createwidget()
        self.createlayout()
        self.connectsignalslot()
        
    @classmethod
    def show_dialog(cls):
        if cls.dialog_window:
            if cls.dialog_window.isHidden():
                cls.dialog_window.show()
            else:
                cls.dialog_window.raise_()
                cls.dialog_window.activateWindow()
        else:
            cls.dialog_window = invisibleClass()
            cls.dialog_window.show()
    
    def createaction(self):
        
        self.A_mesh = QtWidgets.QAction(self)
        self.A_mesh.setText("mesh")
        self.A_mesh.setCheckable(True)
        self.A_mesh.setChecked(True)
        
        self.A_transform = QtWidgets.QAction(self)
        self.A_transform.setText("transform")
        self.A_transform.setCheckable(True)
        self.A_transform.setChecked(True)
        
        self.A_camera = QtWidgets.QAction(self)
        self.A_camera.setText("camera")
        self.A_camera.setCheckable(True)
        self.A_camera.setChecked(True)
        
        self.A_joint = QtWidgets.QAction(self)
        self.A_joint.setText("joint")
        self.A_joint.setCheckable(True)
        self.A_joint.setChecked(True)
        
        
    def createwidget(self):
        
        
        self.M_custom = QtWidgets.QMenu()
        self.M_custom.addAction(self.A_camera)
        self.M_custom.addAction(self.A_mesh)
        self.M_custom.addAction(self.A_transform)
        self.M_custom.addAction(self.A_joint)
        
        self.MB_1 = QtWidgets.QMenuBar()
        M_display = self.MB_1.addMenu("Display")
        M_display.addAction(self.A_camera)
        M_display.addAction(self.A_mesh)
        M_display.addAction(self.A_transform)
        M_display.addAction(self.A_joint)
        
        self.L_invisible = QtWidgets.QLabel("Invisible")

        self.LW_invisible = QtWidgets.QListWidget()
        self.LW_invisible.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.CB_visibility = QtWidgets.QCheckBox()
        self.CB_lodVisibility = QtWidgets.QCheckBox()
        
        self.PB_unvisible = QtWidgets.QPushButton("Invisible")
        self.PB_lodunvisible = QtWidgets.QPushButton("LOD Invisible")
        
        self.PB_cancel = QtWidgets.QPushButton("Cancel")
        self.PB_refresh = QtWidgets.QPushButton("Refresh")
    
        
    def createlayout(self):
        
        HBL_L = QtWidgets.QHBoxLayout()
        HBL_L.addWidget(self.L_invisible)
        
        HBL_LW = QtWidgets.QHBoxLayout()
        HBL_LW.addWidget(self.LW_invisible)
        
        VBL_CB = QtWidgets.QVBoxLayout()
        FL_CB_visibility = QtWidgets.QFormLayout()
        FL_CB_visibility.addRow("Visibility  ",self.CB_visibility)
        VBL_CB.addLayout(FL_CB_visibility)
        
        FL_CB_lodvisibility = QtWidgets.QFormLayout()
        FL_CB_lodvisibility.addRow("LOD Visibility  ",self.CB_lodVisibility)
        VBL_CB.addLayout(FL_CB_lodvisibility)
        
        HBL_PB = QtWidgets.QHBoxLayout()
        HBL_PB.addWidget(self.PB_unvisible)
        HBL_PB.addWidget(self.PB_lodunvisible)
        HBL_PB.addStretch()
        HBL_PB.addWidget(self.PB_refresh)
        HBL_PB.addWidget(self.PB_cancel)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10,10,10,10)
        main_layout.setSpacing(10)
        main_layout.setMenuBar(self.MB_1)
        main_layout.addLayout(HBL_L)
        main_layout.addLayout(HBL_LW)
        main_layout.addLayout(VBL_CB)
        main_layout.addLayout(HBL_PB)
        
    def connectsignalslot(self):
        
        self.A_camera.toggled.connect(self.toggle_action)
        self.A_joint.toggled.connect(self.toggle_action)
        self.A_transform.toggled.connect(self.toggle_action)
        self.A_mesh.toggled.connect(self.toggle_action)
        self.LW_invisible.itemPressed.connect(self.set_prepare_cb)
        self.CB_visibility.toggled.connect(self.chenge_visibility)
        self.CB_lodVisibility.toggled.connect(self.change_lodvisibility)
        self.PB_unvisible.clicked.connect(self.set_unvisible_selected)
        self.PB_lodunvisible.clicked.connect(self.set_lodunvisible_selected)
        self.PB_refresh.clicked.connect(self.refresh_list)
        self.PB_cancel.clicked.connect(self.close)
    
    def show_menu(self,point):
        
        self.M_custom.exec_(self.mapToGlobal(point))
        
    def toggle_action(self):

        bool_camera_check = self.A_camera.isChecked()
        bool_joint_check = self.A_joint.isChecked()
        bool_transform_check = self.A_transform.isChecked()
        bool_mesh_check = self.A_mesh.isChecked()

        self.set_type_show("camera",bool_camera_check)
        self.set_type_show("joint",bool_joint_check)
        self.set_type_show("transform",bool_transform_check)
        self.set_type_show("mesh",bool_mesh_check)
    
    def refresh_list(self):
        
        self.delete_lw()
        self.add_to_LW()
        self.toggle_action()
    
    def delete_lw(self):
        
        count = self.LW_invisible.count()
        for index in range(count):
            item = self.LW_invisible.itemAt(0,0)
            self.LW_invisible.takeItem(0)
            self.LW_invisible.removeItemWidget(item)
    
    def delete_item(self,item):
        
        row_item = self.LW_invisible.row(item)
        self.LW_invisible.takeItem(row_item)
        self.LW_invisible.removeItemWidget(item)
    
    def add_to_LW(self):
        
        all_obj = self.get_all_obj()
        for obj in all_obj:
            item = self.get_prepare_item(obj,self.get_absolute_name(obj))
            if item:
                self.set_to_lw(item)
          
    def chenge_visibility(self,bool_cb):
        
        longname_list = self.get_selectedlongname()
        items = self.LW_invisible.selectedItems()
        if longname_list:
            for index in range(len(longname_list)):
                self.set_visibility(longname_list[index],bool_cb)
                if and_(self.get_visibility(longname_list[index]),self.get_lodvisibility(longname_list[index])):
                    self.delete_item(items[index])
                
    def change_lodvisibility(self,bool_cb):
        
        longname_list = self.get_selectedlongname()
        items = self.LW_invisible.selectedItems()
        if longname_list:
            for index in range(len(longname_list)):
                self.set_lodvisibility(longname_list[index],bool_cb)
                if and_(self.get_visibility(longname_list[index]),self.get_lodvisibility(longname_list[index])):
                    self.delete_item(items[index])
        
    def get_prepare_item(self,data,text):
        item = QtWidgets.QListWidgetItem()
        self.set_text_item(item,text)
        self.set_data_item(item,data)        
        
        if not and_(self.get_lodvisibility(data),self.get_visibility(data)):
            item.setToolTip("Visibility  :  {0}  ,  LOD Visibility  :  {1}".format(self.get_visibility(data),self.get_lodvisibility(data)))
            return item
        else:
            return False
            
    def get_all_item(self):
        count_list = self.LW_invisible.count()
        list_items = []
        if count_list>0:
            for index in range(count_list):
                list_items.append(self.LW_invisible.item(index))
        return list_items
    
    def get_selectedlongname(self):
        long_names = []
        selected_items = self.LW_invisible.selectedItems()
        if selected_items:
            for item in selected_items:
                long_name = self.get_data_item(item)
                long_names.append(long_name)
            return long_names
        else:
            return False
            
    def get_data_item(self,item):
        return item.data(QtCore.Qt.UserRole)
            
    def get_absolute_name(self,obj):
        obj_list = obj.split("|")
        return obj_list[-1]
 
    def get_all_obj(self):
        return cmds.ls(dagObjects=True,long=True)

    def get_visibility(self,obj):
        return cmds.getAttr("{0}.visibility".format(obj))
        
    def get_lodvisibility(self,obj):
        return cmds.getAttr("{0}.lodVisibility".format(obj))
        
    def set_type_show(self,type_node,bool_check):
        items = self.get_all_item()
        for item in items:
            long_name = self.get_data_item(item)
            if cmds.objectType(long_name)==type_node:
                if bool_check:
                    item.setHidden(False)
                else:
                    item.setHidden(True)
        
    def set_prepare_cb(self):
        selected_items = self.get_selectedlongname()
        index =0
        if selected_items:
            for long_name in selected_items:
                bool_vis = self.get_visibility(long_name)
                bool_lodvis = self.get_lodvisibility(long_name)
                if index==0:
                    self.set_lodvis_and_vis_cb(bool_vis,bool_lodvis)
                index+=1
        
    def set_lodvis_and_vis_cb(self,bool_vis,bool_lodvis):
        self.CB_visibility.setChecked(bool_vis)
        self.CB_lodVisibility.setChecked(bool_lodvis)
        
    def set_to_lw(self,item):
        self.LW_invisible.addItem(item)
            
    def set_text_item(self,item,text):
        item.setText(text)
            
    def set_data_item(self,item,data):
        item.setData(QtCore.Qt.UserRole,data)
        
    def set_visibility(self,longname,bool_cb):
        cmds.setAttr("{0}.visibility".format(longname),bool_cb)
    
    def set_lodvisibility(self,longname,bool_cb):
        cmds.setAttr("{0}.lodVisibility".format(longname),bool_cb)
        
    def set_unvisible_selected(self):
        
        list_selected = cmds.ls(sl=True,long=True)
        if list_selected:
            for select in list_selected:
                try:
                    self.set_visibility(select,False)
                except:
                    om.MGlobal.displayWarning("Can't do unvisible {0}".format(self.get_absolute_name(select)))
        self.refresh_list()
        
    def set_lodunvisible_selected(self):
        
        list_selected = cmds.ls(sl=True,long=True)
        if list_selected:
            for select in list_selected:
                try:
                    self.set_lodvisibility(select,False)
                except:
                    om.MGlobal.displayWarning("Can't do unvisible {0}".format(self.get_absolute_name(select)))
        
        self.refresh_list()
        
    def selection_changed(self):
        
        list_selected = cmds.ls(sl=True,long=True)
        items = self.get_all_item()
        self.LW_invisible.setCurrentRow(-1,QtCore.QItemSelectionModel.Clear)
        if items and list_selected:
            for item in items:
                long_name = self.get_data_item(item)
                for selected in list_selected:
                    if long_name == selected:
                        self.LW_invisible.setCurrentItem(item,QtCore.QItemSelectionModel.Select)
            self.set_prepare_cb()                
            

    def closeEvent(self,e):
        
        cmds.scriptJob(kill = self.id_scriptjob,force=True)
        
    def showEvent(self,e):
        
        super(invisibleClass,self).showEvent(e)
        e.accept()
        self.add_to_LW()
        self.id_scriptjob = cmds.scriptJob(event=["SelectionChanged",self.selection_changed])
        self.refresh_list()
        
