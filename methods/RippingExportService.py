import bpy
import os
import re
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
    packagesFolder = replaceBackslashes(wrapFilePathInQuotes(configMgr.GetConfigItem('General','Destiny2PackageFileLocation')))
    outputFolder = replaceBackslashes(wrapFilePathInQuotes(configMgr.GetConfigItem('General','Destiny2OutputFileLocation')))
    mdeFilePath = wrapFilePathInQuotes(helpermethods.GetProjectMDEPath())
    mdeArgs = ['--pkgspath', packagesFolder, '--outputpath', outputFolder]

    if not item.get('shader'):
        mdeArgs = mdeArgs + ['--filename', re.sub('[ -\"\']', '_', (item.get('class')+'_' if len(item.get('class')) > 0 else '') + item.get('name').lower())]

    mdeArgs = mdeArgs + ['--textures', ('--shader' if item.get('shader') else '--api'), str(item.get('hash'))]

    cmdArgs = ' '.join(mdeArgs)
    cmd = 'MontevenDynamicExtractorv1.9.3.exe'
    fullCmdWithArgs = cmd + ' ' + cmdArgs
    os.chdir(mdeFilePath)
    subprocess.check_call([fullCmdWithArgs])
    return

def replaceBackslashes(path):
    return path.replace('\\', '/')

def wrapFilePathInQuotes(path):
    return '"' + path + '"'

#hash: item.id,
#name: item.getAttribute('name'),
#shader: item.dataset.itemcategories.includes('shader'),
#class: item.dataset?.class || null,
#gameGeneration: item.dataset.gameGeneration,