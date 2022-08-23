import adsk.core, adsk.fusion, traceback
import os
import decimal

#Define Limits
MinLength = 50
MaxLength = 70
PrecisionLength = 10      #rounding precision

MinWidth = 25
MaxWidth = 40
PrecisionWidth = 5

MinHeight = 25
MaxHeight = 40
PrecisionHeight = 5




def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface        
        des = adsk.fusion.Design.cast(app.activeProduct)

        #Choose Where to Put the Files
        SavePath = SetFileLocation("ChooseOutPutFolder","ThisDoesntMatter.png",'*.png')
        OutputPath = os.path.split(SavePath)[0]  #get just folder path, without file name

        for Length in frange(MinLength,MaxLength+PrecisionLength,PrecisionLength):
            ChangeParameterValue('Length',str(Length))

            for Width in frange(MinWidth,MaxWidth+PrecisionWidth,PrecisionWidth):
                ChangeParameterValue('Width',Width)

                for Height in frange(MinHeight,MaxHeight+PrecisionHeight,PrecisionHeight):
                    ChangeParameterValue('Height',Height)

                    FileName = OutputPath + "/" + str(Length) + "&" + str(Width) + "&" + str(Height) + "&"  + ".png"
                    #ui.messageBox(FileName)
                    ScreenShot(FileName)             
                    stlexporter(context, FileName)

        ui.messageBox('Finished.')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))




#This function is used to change the value of a given parameter.
def ChangeParameterValue(ParameterName,ParameterNewValue):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        ui.workspaces.itemById("FusionSolidEnvironment").activate() #Open Design Workspace

        des = adsk.fusion.Design.cast(app.activeProduct)

        userParams = des.userParameters
        userParams.itemByName(ParameterName).expression = ParameterNewValue #actually change the value
           
            
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            end



#This function prompts a user for a file location, using the file location dialog box. this would be used for Saving a file.
def SetFileLocation(Message,Initial,Suffex):
    #use '*.*' for extension if you want all files selectable

    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        fileDlg = ui.createFileDialog()
        fileDlg.title = Message

          # Show file save dialog
        fileDlg.title = Message
        fileDlg.initialFilename = Initial
        fileDlg.filter = Suffex
        fileDlg.showSave()
        Result = fileDlg.filename

        return Result

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            end



def ScreenShot(FileName):
    app = adsk.core.Application.get()
    adsk.doEvents()
    app.activeViewport.saveAsImageFile(FileName, 0, 0)
    pass

def frange(A, L=None, D=None):
    #Use float number in range() function
    # if L and D argument is null set A=0.0 and D = 1.0
    if L == None:
        L = A + 0.0
        A = 0.0
    if D == None:
        D = 1.0
    while True:
        if D > 0 and A >= L:
            break
        elif D < 0 and A <= L:
            break
        yield ("%g" % A) # return float number
        A = A + D


def stlexporter(context, filename):

    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        
        # get active design        
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        
        # get root component in this design
        rootComp = design.rootComponent
        
        # create a single exportManager instance
        exportMgr = design.exportManager
        
        # export the root component to printer utility
        stlRootOptions = exportMgr.createSTLExportOptions(rootComp)

        # get all available print utilities
        printUtils = stlRootOptions.availablePrintUtilities

        # export the root component to the print utility, instead of a specified file            
        #for printUtil in printUtils:
            #stlRootOptions.sendToPrintUtility = True
            #stlRootOptions.printUtility = printUtil

            #exportMgr.execute(stlRootOptions)
            
        # get the script location
        scriptDir = os.path.dirname(os.path.realpath(__file__))  
        
        # export the occurrence one by one in the root component to a specified file
       # allOccu = rootComp.allOccurrences
       # for occ in allOccu:
        #    fileName = scriptDir + "/" + occ.component.name
            
            # create stl exportOptions
          #  stlExportOptions = exportMgr.createSTLExportOptions(occ, fileName)
          #  stlExportOptions.sendToPrintUtility = False
            
           # exportMgr.execute(stlExportOptions)

        # export the body one by one in the design to a specified file
        allBodies = rootComp.bRepBodies
        for body in allBodies:
            # fileName = scriptDir + "/" + body.parentComponent.name + '-' + body.name
            
            # create stl exportOptions
            stlExportOptions = exportMgr.createSTLExportOptions(body, filename)
            stlExportOptions.sendToPrintUtility = False
            
            exportMgr.execute(stlExportOptions)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            end