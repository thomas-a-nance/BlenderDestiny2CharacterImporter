from pathlib import Path
import bpy
import re
import os
import shutil
import subprocess
from ..methods import helpermethods
import traceback

searchResultImageCount = 0

@helpermethods.background
def RipModelAndExport(context):
    selectedObj = bpy.types.WindowManager.d2ci_search_results_manager.SelectedSearchResultEntry
    try:
        context.window_manager.d2ci.IsRippingExport = True
        context.window_manager.d2ci.RippingExportText = f"Exporting {selectedObj.get('displayProperties').get('name')}..."

        successfulExtract = False
        for idx, hashNum in enumerate(selectedObj.get('customAttributes').get('hashList')):
            itemObjForMDE = {
                'hash': hashNum,
                'name': selectedObj.get('displayProperties').get('name'),
                'shader': 'shader' in selectedObj.get('customAttributes').get('categories'),
                'class': selectedObj.get('customAttributes').get('class') or ''
            }
            
            exitCode = RunMDE(itemObjForMDE,context)
            if exitCode == 0:
                successfulExtract = True
                break

        if successfulExtract:
            context.window_manager.d2ci.RippingExportText = f"Successfully exported {selectedObj.get('displayProperties').get('name')}."
        else:
            context.window_manager.d2ci.RippingExportText = f"Failed to export {selectedObj.get('displayProperties').get('name')}."

        context.window_manager.d2ci.IsRippingExport = False
    except Exception as e:
        context.window_manager.d2ci.IsRippingExport = False
        context.window_manager.d2ci.RippingExportText = f"Failed to export {selectedObj.get('displayProperties').get('name')} (Exception)."
        print(traceback.format_exc())

def RunMDE(item, context):
    configMgr = bpy.types.WindowManager.d2ci_config
    packagesFolder = Path(configMgr.GetConfigItem('General','Destiny2PackageFileLocation'))
    mdeFilePath = Path(os.path.join(helpermethods.GetProjectMDEPath(), "MontevenDynamicExtractorv1.9.3.exe"))
    outputFolder = configMgr.GetConfigItem('General','Destiny2OutputFileLocation')

    fileName = re.sub('[ -\"\']', '_', (item.get('class')+'_' if len(item.get('class')) > 0 else '') + item.get('name').lower())
    foldersuffix = str(len([i for i in os.listdir(outputFolder) if os.path.isdir(os.path.join(outputFolder,i))]))
    os.makedirs(os.path.join(outputFolder, fileName+'_'+foldersuffix), mode=0o777, exist_ok=True)
    finalOutputFolder = Path(os.path.join(outputFolder, fileName+'_'+foldersuffix))

    context.window_manager.d2ci.RippingExportText = f"Attempting to export item {str(item.get('hash'))}..."
    mdeArgs = ['--pkgspath', packagesFolder, '--outputpath', finalOutputFolder]
    if not item.get('shader'):
        mdeArgs = mdeArgs + ['--filename', fileName]
    mdeArgs = mdeArgs + ['--textures', ('--shader' if item.get('shader') else '--api'), str(item.get('hash'))]
    fullCmdArgs = [mdeFilePath] + mdeArgs
    exitCode = subprocess.Popen(fullCmdArgs, shell=False).wait()
    if exitCode != 0:
        shutil.rmtree(finalOutputFolder, ignore_errors=True)

    return exitCode

def FixFilePathForArgs(path):
    return path.replace("\\","/")

#hash: item.id,
#name: item.getAttribute('name'),
#shader: item.dataset.itemcategories.includes('shader'),
#class: item.dataset?.class || null,
#gameGeneration: item.dataset.gameGeneration,