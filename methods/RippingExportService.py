import bpy
import re
import os
import subprocess
from ..methods import helpermethods
import traceback

searchResultImageCount = 0

@helpermethods.background
def RipModelAndExport(context):
    selectedObj = bpy.types.WindowManager.d2ci_search_results_manager.SelectedSearchResultEntry
    try:
        context.window_manager.d2ci.IsRippingExport = True
        context.window_manager.d2ci.RippingExportText = "Exporting..."

        itemObjForMDE = {
            'hash': selectedObj.get('hash'),
            'name': selectedObj.get('displayProperties').get('name'),
            'shader': 'shader' in selectedObj.get('customAttributes').get('categories'),
            'class': selectedObj.get('customAttributes').get('class')
        }

        RunMDE(itemObjForMDE)

        context.window_manager.d2ci.IsRippingExport = False
        context.window_manager.d2ci.RippingExportText = f"Successfully exported {selectedObj.get('displayProperties').get('name')}."
    except Exception as e:
        context.window_manager.d2ci.IsRippingExport = False
        context.window_manager.d2ci.RippingExportText = f"Failed to export {selectedObj.get('displayProperties').get('name')}."
        print(traceback.format_exc())

def RunMDE(item):
    configMgr = bpy.types.WindowManager.d2ci_config
    packagesFolder = FixFilePathForArgs(configMgr.GetConfigItem('General','Destiny2PackageFileLocation'))
    mdeFilePath = FixFilePathForArgs(helpermethods.GetProjectMDEPath())
    outputFolder = configMgr.GetConfigItem('General','Destiny2OutputFileLocation')

    fileName = re.sub('[ -\"\']', '_', (item.get('class')+'_' if len(item.get('class')) > 0 else '') + item.get('name').lower())
    foldersuffix = str(len([i for i in os.listdir(outputFolder) if os.path.isdir(os.path.join(outputFolder,i))]))
    os.makedirs(os.path.join(outputFolder, fileName+'_'+foldersuffix), mode=0o777, exist_ok=True)
    finalOutputFolder = FixFilePathForArgs(os.path.join(outputFolder, fileName+'_'+foldersuffix))

    mdeArgs = ['--pkgspath', r'"%s"' % packagesFolder, '--outputpath', r'"%s"' % finalOutputFolder]
    if not item.get('shader'):
        mdeArgs = mdeArgs + ['--filename', fileName]
    mdeArgs = mdeArgs + ['--textures', ('--shader' if item.get('shader') else '--api'), str(item.get('hash'))]
    cmdArgs = ' '.join(mdeArgs)

    exitCode = subprocess.Popen("MontevenDynamicExtractorv1.9.3.exe" + " " + cmdArgs, shell=False, cwd=mdeFilePath).wait()
    if exitCode != 0:
        raise Exception("MDE Failed")
    return

def FixFilePathForArgs(path):
    return path.replace("\\","/")

#hash: item.id,
#name: item.getAttribute('name'),
#shader: item.dataset.itemcategories.includes('shader'),
#class: item.dataset?.class || null,
#gameGeneration: item.dataset.gameGeneration,