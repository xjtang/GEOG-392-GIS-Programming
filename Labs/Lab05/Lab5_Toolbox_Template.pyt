# -*- coding: utf-8 -*-

import arcpy
import os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Lab5_Toolbox"
        self.alias = "Lab5_Toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Lab5_Tool]


class Lab5_Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Lab5_Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param_GDB_folder = arcpy.Parameter(
            displayName="GDB Folder",
            name="gdbfolder",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_GDB_Name = arcpy.Parameter(
            displayName="GDB Name",
            name="gdbname",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_Garage_CSV_File = arcpy.Parameter(
            displayName="Garage CSV File",
            name="garagecsvfile",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_Garage_Layer_Name = arcpy.Parameter(
            displayName="Garage Layer Name",
            name="garagelayername",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_Campus_GDB = arcpy.Parameter(
            displayName="Campus GDB",
            name="campusGDB",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_Selected_Garage_Name = arcpy.Parameter(
            displayName="Selected Garage Name",
            name="selectedgaragename",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_buffer_radius = arcpy.Parameter(
            displayName="Buffer Radius",
            name="bufferradius",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )
        params = [
            param_GDB_folder, 
            param_GDB_Name, 
            param_Garage_CSV_File, 
            param_Garage_Layer_Name, 
            param_Campus_GDB, 
            param_Selected_Garage_Name, 
            param_buffer_radius
            ]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #query user input
        #Edit the code by yourself, 
        #see Page 15 of Lab5 instructions.ppt for answers

        print("User Input:")
        print("GDBFolder:" + GDB_Folder)
        print("GDB_Name: " + GDB_Name)
        print("Garage_CSV_File" + Garage_CSV_File)
        print("Garage_layer_Name: " + Garage_Layer_Name)
        print("Campus_GDB: " + Campus_GDB)
        print("Selected_Garage_Name: " + Selected_Garage_Name)
        print("Buffer_Radius: " + Buffer_Radius)

        #create gdb
        arcpy.CreateFileGDB_management(GDB_Folder, GDB_Name)
        GDB_Full_Path = GDB_Folder + "/" + GDB_Name

        #import garage csv
        garages = arcpy.management.MakeXYEventLayer(Garage_CSV_File, "x", "y", Garage_Layer_Name)
        arcpy.FeatureClassToGeodatabase_conversion(garages, GDB_Full_Path)

        #search surcor
        structures = Campus_GDB + "/Structures"
        where_clause = "BldgName = '%s'" % Selected_Garage_Name
        cursor = arcpy.SearchCursor(structures, where_clause=where_clause)

        #import layers into created GDB


        shouldProceed = False

        for row in cursor:
            if row.getValue("BldgName") == Selected_Garage_Name:
                shouldProceed = True
                break

        if shouldProceed:
            #select garage as feature layer
            selected_garage_layer_name = GDB_Full_Path+"/garage_selected"
            garage_feature = arcpy.Select_analysis(structures, selected_garage_layer_name, 
            where_clause)

            # Buffer the selected building
            garage_buff_name = "/building_buffed_%s" % (Buffer_Radius)
            arcpy.Buffer_analysis(garage_feature, GDB_Full_Path + garage_buff_name, 
            Buffer_Radius + " meter")

            #clip
            arcpy.Clip_analysis(structures, GDB_Full_Path + garage_buff_name, 
            GDB_Full_Path + "/clip")

            arcpy.AddMessage("Success")
            print("success")
        else:
            arcpy.AddError("Seems we couldn’t find the building name you entered")
            print("error")

        return
