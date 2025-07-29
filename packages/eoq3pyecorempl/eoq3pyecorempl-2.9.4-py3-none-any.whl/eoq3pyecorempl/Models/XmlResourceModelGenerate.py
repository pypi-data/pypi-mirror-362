import os
import shutil

from pyecore.resources import ResourceSet, URI

from pyecoregen.ecore import EcoreGenerator

pyeoqProject = "./" #must be changed on different pc
# modelProject = "../../model" #must be changed on different pc
modelName = "xmlresourcemodel"
#modelBackupName = "workspacemdbmodel_autobackup.ecore"

# modelSrcFolder = os.path.join(modelProject,'.')
modelDestFolder = os.path.join(pyeoqProject,'.')
# outfolder = os.path.join(pyeoqProject,'Models')
outfolder = os.path.join(pyeoqProject,'Generated')

#Backup an existing code model file
modelfile = os.path.join(modelDestFolder,modelName+'.ecore')
# backupfile = os.path.join(modelDestFolder,modelBackupName)
# if(os.path.isfile(backupfile)):
#     os.remove(backupfile)
# if(os.path.isfile(modelfile)):
#     shutil.copy(modelfile, backupfile)
#     os.remove(modelfile)
# modelsource = os.path.join(modelSrcFolder,modelName)
# shutil.copy(modelsource, modelfile)

#Delete existing generated code
oldmodel = os.path.join(outfolder,modelName)
if(os.path.isdir(oldmodel)):
    shutil.rmtree(oldmodel)

#Generate the python implementation
#outfolder = os.path.join(pyeoqProject,"pyeoq")
rset = ResourceSet()
resource = rset.get_resource(URI(modelfile))
root = resource.contents[0]  # We get the root (an EPackage here)
generator = EcoreGenerator(auto_register_package=True)
generator.generate(root, outfolder)