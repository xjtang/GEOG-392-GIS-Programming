# -*- coding: utf-8 -*-

import arcpy
import time

def progressorStart(progressorTime):
    # Increment the progressor and change the label; add message to the results pane
    arcpy.SetProgressorPosition(progressorTime['start'] + progressorTime['step'])
    arcpy.SetProgressorLabel("start to update render...")
    time.sleep(progressorTime['readTime'])
    arcpy.AddMessage("start to update render...")
    return

def progressIncrement(progressorTime):
    # Increment the progressor and change the label; add message to the results pane
    arcpy.SetProgressorPosition(progressorTime['start'] + progressorTime['step'] +
                                 progressorTime['step'])
    arcpy.SetProgressorLabel("setting render...")
    time.sleep(progressorTime['readTime'])
    arcpy.AddMessage("setting render...")
    return

def progressorEnd(progressorTime):
    # Increment the progressor and change the label; add message to the results pane
    arcpy.SetProgressorPosition(progressorTime['max'])
    arcpy.SetProgressorLabel("saving project...")
    time.sleep(progressorTime['readTime'])
    arcpy.AddMessage("saving project...")
    return

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Lab6RenderTool]


class Lab6RenderTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            # code here
        )


        param1 = arcpy.Parameter(
            # code here
        )


        param2 = arcpy.Parameter(
            # code here
        )
        params = [param0, param1, param2]
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
        #progressor variables
        progressorTime = {
            'readTime': 2.5,
            'start': 0,
            'max':100,
            'step':25,
        }

        # Setup the progressor
        arcpy.SetProgressor("step", "Checking project and layer...", progressorTime['start'], 
        progressorTime['max'], progressorTime['step'])
        time.sleep(progressorTime['readTime'])
        # Add message to the results pane
        arcpy.AddMessage("Checking project and layer...")

        # Reference to our .aprx
        aprxFileAddress = parameters[0].valueAsText
        project = arcpy.mp.ArcGISProject(aprxFileAddress)
        layername = parameters[1].valueAsText
        outputFileAddr = parameters[2].valueAsText

        layers = project.listMaps('Map')[0].listLayers()
        for layer in layers:
            if layer.name != layername:
                continue
            if layer.isFeatureLayer:
                symbology = layer.symbology
                progressorStart(progressorTime)
                
                if hasattr(symbology, 'renderer'):
                    if layername == 'Trees':
                        # Update the copy's renderer to be 'GraduatedColorsRenderer'
                        symbology.updateRenderer('#####') # REPLACE #####
                        # Tell arcpy which field we want to base our choropleth off of
                        symbology.renderer.classificationField = "#####" # REPLACE #####
                        progressIncrement(progressorTime)
                        # Set how many classes we'll have
                        symbology.renderer.breakCount = 5
                        # Set the color ramp
                        symbology.renderer.colorRamp = project.listColorRamps('#####')[0] #REPLACE #####
                        # Set the layer's actual symbology equal to the copy's
                        layer.symbology = symbology # Very important step
                        progressorEnd(progressorTime)
                        
                    elif layername == 'Structures':
                        # Update the copy's renderer to be "UniqueValueRenderer"
                        symbology.updateRenderer('#####') #REPLACE #####
                        progressIncrement(progressorTime)
                        # Tells arcpy that we want to use "Type" as our unique value
                        symbology.renderer.fields = ["Type"]
                        # Set the layer's actual symbology equal to the copy's
                        layer.symbology = symbology # Very important step
                        progressorEnd(progressorTime)
                        
                    else:
                        print("We can't work with this layer")
            
        project.saveACopy(outputFileAddr)
        return
