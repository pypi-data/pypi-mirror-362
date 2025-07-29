"""
 Workspace model persistence layer (MPL)
 The features of an MPL are:
 - Load a local directory structure into a workspace model in the domain
 - Store a workspace model in the domain to an empty local directory structure
 - In both cases the MPL can listen to domain changes and apply them to the workspace model
 Bjoern Annighoefer 2021
"""

from .workspacemdbmodel import Directory, Resource, Workspace, PathElementA
from .xmlresourcemodel import Document, Element, Attribute

from eoq3.concepts import CONCEPTS
from eoq3.config import Config, EOQ_DEFAULT_CONFIG
from eoq3.logger import GetLoggerInstance
from eoq3.error import EOQ_ERROR_RUNTIME
from eoq3.value import LST, QRY
from eoq3.command import Cmp, EVT_TYPES, EVT_KEYS
from eoq3.query import Qry, Obj, His
from eoq3.domain import Domain, DomainConnector
from eoq3pyecoreutils.pyecoretoeoq import EPackageStructureToCmd, EPackageRefsToCmd, EUserModelToCmd, EObjectRefsToCmd, EcoreConversionOptions
from eoq3pyecoreutils.crudforpyecore import CreateEObject, UpdateEObject, DeleteEObject

from pyecore.resources import ResourceSet, URI
from pyecore.ecore import EObject, EPackage

from collections import deque
import os
import shutil
import time
import xml.etree.ElementTree
import xml.dom.minidom
from timeit import default_timer
from threading import Lock,Semaphore,Thread
import traceback
#type checking
from typing import Callable
    

ECORE_FILE_EXTENTION = '.ecore'
   
### MAIN CLASS     
class PyEcoreWorkspaceMpl(DomainConnector):
    """Loads a directory of ecore models as a workspace model into a domain.
    """
    modelRoot:QRY
    modelRootFeature:str
    trackDomainChanges:bool
    progressCallback:Callable[[int], None]
    workspaceRoot:QRY

    def __init__(self, baseDir:str, target:Qry=None, featureName:str=None, trackDomainChanges:bool=False, progressCallback:Callable[[int],None]=None, config:Config=EOQ_DEFAULT_CONFIG):
        super().__init__(config)
        #parameters
        self.baseDir = os.path.normpath(baseDir)
        self.modelRoot = target
        self.modelRootFeature = featureName
        self.trackDomainChanges = trackDomainChanges
        self.progressCallback = progressCallback
        #internals
        self.logger = GetLoggerInstance(config)
        self.baseDirAbs = os.path.join(os.getcwd(),self.baseDir)
        self.baseDirUri = URI(self.baseDir) 
        self.rset = ResourceSet()
        self.modelResourceLut = {}  #a look-up table between eResources and ModelResource objects
        self.eResourceLut = {}  #a look-up table between ModelResource and eResources objects
        
        self.builtinMetamodels = [Directory.eClass.eContainer(),Document.eClass.eContainer()] #metamodel not loaded from the files, but existing, e.g. by code generation
        self.loadedMetamodels = [] #collects all metamodel files known
        
        self.lastPersistentPaths = {}  # dir or resources -> path
        self.dirtyResources = []  #stores all modified resources, such that they can be saved
        self.deletedResources = {}  #stores all resources marked for deletion
        #self.dirtyObjects = []  #stores all objects that have been modified in order to do not mark them twice
        
        self.knownModelExtensions = []  #this is used to identify the model files to be loaded. ecore files are known as model files by default.
        self.knownXmlExtensions = ['xml']
        
        self.domain = None  # is set during coupling
        self.objectToIdLookup = {}
        self.idToObjectLookup = {}

        self.updateQueue = deque()
        self.updateQueueLock = Lock()
        self.updateSignal = Semaphore(0)

        self.isDirty = False
        self.lastUpdate = 0.0
        self.lastSave = 0.0
                
        self.modelLock = Lock() #this prevents model modifications during saving
        
        self.shallRun = True
        
        self.updateThread = None
        
    #@Override
    def Connect(self,domain:Domain,sessionId:str=None)->None:
        super().Connect(domain, sessionId)
        # set conversion options
        options = EcoreConversionOptions()
        options.muteUpdate = True #this speeds up execution
        options.packageIdFeature = "name"
        #load build in models 
        # 1. loop loads the structure
        for mm in self.builtinMetamodels:
            self.logger.Info('Uploading built-in package %s[%s]...'%(mm.name,mm.nsURI))
            start = default_timer()
            cmd = Cmp()
            importedObjs = EPackageStructureToCmd(mm, None, cmd, self.objectToIdLookup, 0, options, self.logger)
            res = self.domain.Do(cmd,self.sessionId,asDict=True)
            self.__UpdateObjectLutFromUploadCmd(importedObjs,res)
            end = default_timer()
            self.logger.Info('ok (%.5f s)'%(end-start))
        #2. loop resolves the references, because, meta-models might have cross-references
        for mm in self.builtinMetamodels:
            self.logger.Info('Uploading built-in package references for %s[%s]...'%(mm.name,mm.nsURI))
            start = default_timer()
            cmd = Cmp()
            importedObjs = EPackageRefsToCmd(mm, cmd, self.objectToIdLookup, 0, options, self.logger)
            res = self.domain.Do(cmd,self.sessionId,asDict=True)
            self.__UpdateObjectLutFromUploadCmd(importedObjs,res)
            end = default_timer()
            self.logger.Info('ok (%.5f s)'%(end-start))
        #upload workspace model
        self.logger.Info('Converting workspace model...')
        start = default_timer()
        cmd = Cmp()
        importedObjs = EUserModelToCmd(self.workspaceModel, cmd, self.objectToIdLookup, 0, options, self.baseDir, self.logger)
        EObjectRefsToCmd(self.workspaceModel, cmd, self.objectToIdLookup, options, self.logger)
        #add the workspace root to an existing element MDB if given
        if(None != self.modelRoot and None != self.modelRootFeature):
            cmd.Upd(self.modelRoot,self.modelRootFeature,self.objectToIdLookup[importedObjs[-1]])
        res = self.domain.Do(cmd,self.sessionId,asDict=True)
        workspaceRoot = res["o0"] #o0 is the first created object
        self.__UpdateObjectLutFromUploadCmd(importedObjs,res)
        end = default_timer()
        self.logger.Info('ok (%.5f s)'%(end-start))
        if(self.progressCallback): self.progressCallback(self.__CalcProgress(1, 1, 0, 10))
        #upload meta models
        #1. loop upload the structure and attaches to the workspace model
        uploadedMms = []
        for r in self.workspaceModel.eAllContents():
            if(Resource == type(r) and r.isLoaded):
                mm = self.__ResourceGetContent(r)
                if(isinstance(mm,EPackage)): #upload only meta-models
                    self.logger.Info('Uploading package structure %s[%s] from %s...'%(mm.name,mm.nsURI,r.name))
                    start = default_timer()
                    cmd = Cmp()
                    importedObjs = EPackageStructureToCmd(mm, None, cmd, self.objectToIdLookup, 0, options, self.logger)
                    uploadedMms.append(mm) #remember, because we need a second loop for the internal dependencies
                    resource = self.objectToIdLookup[r]
                    resourceContentAssocStrId = 'content'
                    #resourceContentAssocStrId = r.eClass.ePackage.eGet(options.packageIdFeature)+ECORE_CLASSID_SEPERATOR+r.eClass.name+ECORE_CLASSID_SEPERATOR+'content'
                    cmd.Crt(CONCEPTS.M1COMPOSITION,1,[resourceContentAssocStrId,resource,self.objectToIdLookup[importedObjs[-1]]])
                    #TODO cmd.Upd(resource,'content',self.objectToIdLookup[importedObjs[-1]])
                    res = self.domain.Do(cmd,self.sessionId,asDict=True)
                    self.__UpdateObjectLutFromUploadCmd(importedObjs,res)
                    end = default_timer()
                    self.logger.Info('ok (%.5f s)'%(end-start))
        #2.loop updates the internal dependencies
        for mm in uploadedMms:
            self.logger.Info('Uploading package references for %s[%s]...'%(mm.name,mm.nsURI))
            start = default_timer()
            cmd = Cmp()
            importedObjs = EPackageRefsToCmd(mm, cmd, self.objectToIdLookup, 0, options, self.logger)
            res = self.domain.Do(cmd,self.sessionId,asDict=True)
            self.__UpdateObjectLutFromUploadCmd(importedObjs,res)
            end = default_timer()
            self.logger.Info('ok (%.5f s)'%(end-start))
        if(self.progressCallback): self.progressCallback(self.__CalcProgress(1, 1, 10, 10))
        #upload model resources
        #1. loop uploads the structure and attaches it to the workspace model
        uploadedModels = []
        nModels = sum(1 for x in self.workspaceModel.eAllContents())
        i = 0
        for r in self.workspaceModel.eAllContents():
            if(Resource == type(r) and r.isLoaded):
                m = self.__ResourceGetContent(r)
                if(not isinstance(m,EPackage)): #upload any user model
                    name = 'INSTANCE'
                    try: name = m.name 
                    except AttributeError: pass
                    className = m.eClass.name
                    self.logger.Info('Uploading model %s : %s from %s...'%(name,className,r.name))
                    start = default_timer()
                    cmd = Cmp()
                    importedObjs = EUserModelToCmd(m, cmd, self.objectToIdLookup, 0, options, r.name, self.logger)
                    uploadedModels.append(m) #remember, because we need a second loop for the internal dependencies
                    resource = self.objectToIdLookup[r]
                    resourceContentAssocStrId = 'content'
                    #resourceContentAssocStrId = r.eClass.ePackage.eGet(options.packageIdFeature)+ECORE_CLASSID_SEPERATOR+r.eClass.name+ECORE_CLASSID_SEPERATOR+'content'
                    cmd.Crt(CONCEPTS.M1COMPOSITION,1,[resourceContentAssocStrId,resource,self.objectToIdLookup[importedObjs[-1]]])
                    #cmd.Upd(resource,'content',self.objectToIdLookup[importedObjs[-1]])
                    res = self.domain.Do(cmd,self.sessionId,asDict=True)
                    self.__UpdateObjectLutFromUploadCmd(importedObjs,res)
                    end = default_timer()
                    self.logger.Info('ok (%.5f s)'%(end-start))
            i = i+1
            if(self.progressCallback): self.progressCallback(self.__CalcProgress(nModels, i, 20, 60))
        #2.loop updates the internal dependencies
        nModels = len(uploadedModels)
        i = 0
        for m in uploadedModels:
            name = 'INSTANCE'
            try: name = m.name 
            except AttributeError: pass
            className = m.eClass.name
            self.logger.Info('Uploading model references for %s : %s...'%(name,className))
            start = default_timer()
            cmd = Cmp()
            EObjectRefsToCmd(m, cmd, self.objectToIdLookup, options, self.logger)
            self.domain.Do(cmd,self.sessionId)
            end = default_timer()
            self.logger.Info('ok (%.5f s)'%(end-start))
            i = i+1
            if(self.progressCallback): self.progressCallback(self.__CalcProgress(nModels, i, 60, 100))
        #listen to all domain changes
        if(self.trackDomainChanges):
            self.domain.Observe(self.__OnDomainChanges, self.sessionId, self.sessionId)
            cmd = Cmp().Obs(EVT_TYPES.CRT,EVT_KEYS.ALL).Obs(EVT_TYPES.UPD,EVT_KEYS.ALL).Obs(EVT_TYPES.UPD,EVT_KEYS.ALL)
            self.domain.Do(cmd, self.sessionId)
            self.updateThread = Thread(target=self.__UpdateThread)
            self.updateThread.start()
            
        self.workspaceRoot = workspaceRoot

    #@Override
    def Disconnect(self) ->None:
        if(self.trackDomainChanges):
            cmd = Cmp().Ubs(EVT_TYPES.CRT,EVT_KEYS.ALL).Ubs(EVT_TYPES.UPD,EVT_KEYS.ALL).Ubs(EVT_TYPES.UPD,EVT_KEYS.ALL)
            self.domain.Do(cmd, self.sessionId)
            self.domain.Unobserve(self.__OnDomainChanges, self.sessionId, self.sessionId)
            self.shallRun = False
            self.updateThread.join()
        super().Disconnect()

    #@Override    
    def Close(self)->None:
        self.logger.Info("Closing workspace MDB ...") #makes problems when main thread has ended already
        #stop observing
        if(self.trackDomainChanges):
            cmd = Cmp().Ubs(EVT_TYPES.CRT,EVT_KEYS.ALL).Ubs(EVT_TYPES.UPD,EVT_KEYS.ALL).Ubs(EVT_TYPES.UPD,EVT_KEYS.ALL)
            self.domain.Do(cmd, self.sessionId)
            self.domain.Unobserve(self.__OnDomainChanges, self.sessionId, self.sessionId)
            self.shallRun = False
            self.updateThread.join()
        super().Close()
        self.logger.Info("ok")

    ### ADDITIONAL FUNCTIONS ###

    def GetWorkspaceRoot(self)->QRY:
        return self.workspaceRoot

    ### STORE FUNCTIONS ###

    def Store(self):
        raise NotImplemented()
        
    ### LOAD FUNCTIONS ###

    def Load(self)->None:
        self.workspaceModel = self.__LoadWorkspace(self.baseDirAbs)
            
    def __LoadWorkspace(self,baseDirAbs:str)->Workspace:
        workspaceModel = self.__BuildWorkspaceModel(baseDirAbs)
        # load meta models first
        self.__LoadAllMetaModelsInDir(workspaceModel)
        # load other resources
        self.__LoadAllResourcesInDir(workspaceModel)
        return workspaceModel
        
            
    def __BuildWorkspaceModel(self,workspaceAbsPath:str)->Workspace:
        workspaceModel = Workspace()
        workspaceModel.actualPathAbs = workspaceAbsPath
        workspaceModel.actualPathCwd = self.__GetRelativeCwdPath(workspaceAbsPath)
        (directories,files) = self.__ScanForFilesAndDirectories(workspaceAbsPath)
        #create directories (this includes empty ones)
        for dirpath in directories:
            directory = self.__GetOrCreateDir(dirpath,workspaceModel)
        #create model files
        for f in files:
            head,tail = os.path.split(f)
            directory = self.__GetOrCreateDir(head,workspaceModel)
            resource = Resource(name=tail)
            self.__SetLastPersistentPath(resource, f)
            #self.__InitPathElementA(resource, f)
            resource.isLoaded = False
            directory.resources.add(resource)
        return workspaceModel
    
    
    def __ScanForFilesAndDirectories(self,absPath:str)->(str,list):
        directories = []
        ressourceFiles = []
        for root, dirs, files in os.walk(absPath, topdown=True):
            for d in dirs:
                path = os.path.join(root,d)
                directories.append(path)
            for f in files:
                    path = os.path.join(root,f)
                    ressourceFiles.append(path)
        return (directories,ressourceFiles)
        
                
    def __LoadAllMetaModelsInDir(self,workspaceModel:Directory)->None:
        ''' Opens all metamodels from the given workspace model and tries to load and register them
        '''
        # filter out the resources to be loaded
        for r in workspaceModel.resources:
            if(r.name.lower().endswith(ECORE_FILE_EXTENTION)):
                self.__LoadMetaModelResource(r)
        # recurse in subdirectories
        for d in workspaceModel.subdirectories:
            self.__LoadAllMetaModelsInDir(d)
       
            
    def __LoadMetaModelResource(self,resource:Resource)->None:
        path = self.__GetLastPersitentPath(resource)
        self.logger.Info("Loading meta-model %s ..."%(path))
        start = default_timer() 
        try:
            eResource = self.rset.get_resource(path)
            gcmRoot = eResource.contents[0]
            self.rset.metamodel_registry[gcmRoot.nsURI] = gcmRoot
            # register all possible subpackages
            for child in gcmRoot.eAllContents():
                if(isinstance(child,EPackage)):
                    self.rset.metamodel_registry[child.nsURI] = child
            #remember the file extension, which is the file name (without extension) of the model file
            metaModelFileName = os.path.basename(path)
            modelExtension = os.path.splitext(metaModelFileName)[0]
            self.knownModelExtensions += [modelExtension]
            # link resource and eResource
            self.__LinkResourceAndEResource(resource, eResource)
            self.__ResourceSetContent(resource,gcmRoot) #hidden root must be set
            end = default_timer()
            self.logger.Info("ok (%f s)"%(end-start))
        except Exception as e:
            self.logger.Info("failed: %s"%(str(e)))
            resource.info = "Load failed: %s"%(str(e))
        self.__SetResourceClean(resource)
                        
            
    def __LoadAllResourcesInDir(self,workspaceModel:Directory)->None:
        # filter out the resources to be loaded
        for r in workspaceModel.resources:
            if( not r.name.lower().endswith(ECORE_FILE_EXTENTION)):
                self.__LoadResource(r)
        # recurse in subdirectories
        for d in workspaceModel.subdirectories:
            self.__LoadAllResourcesInDir(d)
          
            
    def __LoadResource(self, resource:Resource)->None:
        path = self.__GetLastPersitentPath(resource)
        self.logger.Info("Loading resource %s ..."%(path))
        start = default_timer() 
        try:
            extension = os.path.splitext(path)[1].replace('.','') #remove the point in the extension     
            if(extension in self.knownModelExtensions):
                self.__LoadModelResource(resource)
                end = default_timer()
                self.logger.Info("ok (%f s)"%(end-start))
            elif(extension in self.knownXmlExtensions):
                self.__LoadXmlResource(resource)
                end = default_timer()
                self.logger.Info("ok (%f s)"%(end-start))
            else:
                self.logger.Info("skipped: Unknown extension")
                resource.info = "skipped: Unknown extension"
        except Exception as e:
            self.logger.Info("failed: %s"%(str(e)))
            resource.info = "Load failed: %s"%(str(e))
            if(self.config.printUnexpectedExceptionTraces):
                traceback.print_exc()
        self.__SetResourceClean(resource)
            
      
    def __LoadModelResource(self, resource:Resource)->None:
        path = self.__GetLastPersitentPath(resource)
        eResource = self.rset.get_resource(path)
        if not eResource:
            raise EOQ_ERROR_RUNTIME(0,'Could not read %s as a model. Corrupted?'%(path))
        self.__LinkResourceAndEResource(resource, eResource)
        content = None if (0==len(eResource.contents)) else eResource.contents[0] #eResources with multiple contents are not supported
        self.__ResourceSetContent(resource,content) #hidden root must be set
    
    
    def __LoadXmlResource(self, resource:Resource)->None:
        path = self.__GetLastPersitentPath(resource)
        #parse input-xml
        xmlparse = xml.etree.ElementTree
        tree = xmlparse.parse(path)
        root = tree.getroot()
        ldfile = Document(name=resource.name, version="1.0")
        rootelement = Element(name=root.tag, content=root.text.strip())
#         resource.document = ldfile
        ldfile.rootelement = rootelement
        #resource.contents.add(ldfile)
        for attr in root.attrib:
            newAttr = Attribute(name=attr, value=root.attrib[attr])
            rootelement.attributes.add(newAttr)
        # find first layer
        for element in root:
            if(element.text == None):
                element.text = ""
            #find all subclasses within first layer
            self.__LoadXmlFindChildElems(element, rootelement)    
        self.__ResourceSetContent(resource, ldfile)
        
        
    def __LoadXmlFindChildElems(self, element, parent):
        ''' Support function for __LoadXmlResource
        '''
        if(element.text == None):
            element.text = ""
        newChild = Element(name = element.tag, content = element.text.strip())
        parent.subelements.add(newChild)
        #create attribute class for each attribute
        for attr in element.attrib:
            newAttr = Attribute(name = attr, value = element.attrib[attr])
            newChild.attributes.add(newAttr)
        #find all child elements
        for child in element:
            self.__LoadXmlFindChildElems(child, newChild)
        return parent
        
    def __GetOrCreateDir(self, path:str, workspaceModel:Directory):
        relPath = os.path.relpath(path, self.baseDirAbs)
        directory = workspaceModel
        if(relPath and relPath != '.'): #only proceed for non empty strings
            segments = relPath.split(os.path.sep)
            for segment in segments: 
                subdirexists = False
                for subdir in directory.subdirectories:
                    if(subdir.name == segment):
                        directory = subdir
                        subdirexists = True
                        break
                if(not subdirexists):
                    newsubdir = Directory(name=segment)
                    #self.__InitPathElementA(newsubdir, path)
                    self.__SetLastPersistentPath(newsubdir, path)
                    directory.subdirectories.add(newsubdir)
                    directory = newsubdir
        return directory
    
    ### PATH HELPER FUNCTIONS ###
                
    def __GetElementPath(self,directory:PathElementA)->str:
        workspaceFound = False #indicates if the element is attached correctly somewhere below the root
        path = directory.name
        if(isinstance(directory,Workspace)):
            return path
        parent = directory.eContainer()
        while(isinstance(parent,Directory)):
            path = os.path.join(parent.name,path)
            if(isinstance(parent,Workspace)):
                workspaceFound = True
                break #exit because there should not be an element further down.
            parent = parent.eContainer()
        if(workspaceFound):
            return path
        else:
            return None
    
    def __GetAbsElementPath(self,directory:PathElementA)->str:
        path = self.__GetElementPath(directory)
        if(None != path):
            path = path[2:]
            return os.path.join(self.baseDirAbs,path)
        else:
            return None
       
    def __GetLastPersitentPath(self,dirOrResource:PathElementA)->str:
        lastPersistentPath = None
        try:
            lastPersistentPath = self.lastPersistentPaths[dirOrResource]
        except KeyError:
            lastPersistentPath = None
        return lastPersistentPath
    
    def __SetLastPersistentPath(self,dirOrResource,lastPersistentPath)->None:
        self.lastPersistentPaths[dirOrResource] = lastPersistentPath
        
    def __DeleteLastPeristentPath(self,dirOrResource:PathElementA)->None:
        try:
            self.lastPersistentPaths.pop(dirOrResource)
        except:
            pass  # fail silent if element does not has no path so far

    def __GetRelativeCwdPath(self,absPath:str)->str:
        return os.path.relpath(absPath, os.getcwd())
    
    ### RESOURCE CONTENT HELPERS ###
    
    def __ResourceSetContent(self,resource:Resource,content:EObject)->None:
        '''Sets the content of an resources without making a direct relation ship,
        which would cause the link between EResources and content to break.
        ''' 
        resource._content = content
        content._resource = resource #establish a backwards link to the model
        resource.isLoaded = True #if a content is set this resource must be loaded
        
    def __ResourceGetContent(self,resource:Resource)->EObject:
        try:
            return resource._content
        except AttributeError:
            return None
        
    def __ObjectGetResource(self,eObj:EObject)->Resource:
        '''Retrieves the resource this eObject belongs to.
        If it does not belong to any resource, None is returned
        '''
        #look for the upper-most parent
        parent = eObj
        while(parent.eContainer()):
            parent = parent.eContainer()
        #look if the parent is linked to a resources
        try:
            return parent._resource
        except AttributeError:
            return None
    
    ### OBJECT LUT HELPER FUNCTIONDS ###     
        
    def __UpdateObjLut(self,eObj:EObject,obj:Qry)->None:
        self.objectToIdLookup[eObj] = obj
        self.idToObjectLookup[obj] = eObj    
        
    def __RemoveFromObjLut(self,eObj:EObject,obj:Qry)->None:
        del self.objectToIdLookup[eObj]
        del self.idToObjectLookup[obj] 
    
    def __UpdateObjectLutFromUploadCmd(self,eObjs:list,res:LST):
        '''Updates His entries in the internal object lookup table by Obj entries 
        from a commands result. 
        In addition the reverse look-up table is build
        '''
        for o in eObjs:
            e = self.objectToIdLookup[o]
            if(isinstance(e,His)):
                i = e.v[0].v[0].GetVal()
                elem = res[i]
                self.objectToIdLookup[o] = elem #replace His entry with the object reference from the command
                self.idToObjectLookup[elem] = o #reverse look-up
                
    ### ERESOURCE HELPER FUNCTIONS ###        
            
    def __LinkResourceAndEResource(self, resource:Resource, eResource)->None:
        ''' Establish a connection between workspace resources and pyecore resources
        '''
        eResource._eoqResource = resource
        resource._eResource = eResource
        
    def __UnlinkResourceAndEResource(self, resource)->None:
        ''' Release the connection between workspace resources and pyecore resources
        '''
        eResource = resource._eResource
        eResource._eoqResource = None
        resource._eResource = None
        
    def __GetModelsEResource(self, resource:Resource)->object:
        ''' Return the eResource for a workspace resource.
        Only works if resource and eResource have been linked 
        before.
        If no eResource is linked, None is returned.
        '''
        eResource = None
        #check if an eResource exists for this file
        try: 
            eResource = resource._eResource
        except AttributeError:
            pass #equal a None eResource
        return eResource
                
    ### DOMAIN CHANGE LISTENER ###
        
    def __OnDomainChanges(self,evts,context,src):
        #copy the events to the event queue
        self.updateQueueLock.acquire()
        #self.updateQueue.appendleft(evts) #TODO: is disabled until the update processing is fixed
        self.updateQueueLock.release()
        # and signals the event thread to process the events
        #self.updateSignal.release() #TODO: is disabled until the update processing is fixed
    
    ### UPDATE THREAD ###
    
    def __UpdateThread(self)->None:
        while(self.shallRun):
            newEvents = self.updateSignal.acquire(timeout=0.5)
            if(newEvents):
                self.__ProcessNextEvent()
            else: #if no event was caused, see if we need to save the local resources
                if(self.isDirty):
                    now = time.time()
                    if(now - self.lastUpdate > self.config.mplMinSaveTimeout or\
                       now - self.lastSave > self.config.mplMaxSaveTimeout):
                        self.__SaveWorkspace()
        #make sure all changes are applied before closing
        queuedEvents = self.updateSignal.acquire(timeout=0.0)
        while(queuedEvents):
            self.__ProcessNextEvent()
            queuedEvents = self.updateSignal.acquire(timeout=0.0)
        #finally save the workspace if it was modified
        if(self.isDirty):
            self.__SaveWorkspace()
            
    def __ProcessNextEvent(self)->None:
        '''Pops the next event from the event queue and processes it
        Is thread-safe.
        '''
        self.updateQueueLock.acquire()
        evts = self.updateQueue.pop()
        self.updateQueueLock.release()
        self.__ApplyDomainUpdates(evts)
        
                    
    def __ApplyDomainUpdates(self,evts:list)->None:
        ''' This applies crt, upd and del events 
        received from the domain to the local models
        and marks the workspace as dirty after changes
        '''
        #TODO: this code has not been updated after the introduction of CONCEPTS. IS CURRENTLY BROKEN
        for evt in evts:
            evtType = evt.a[0].GetVal()
            if(evtType == EVT_TYPES.CRT):
                evtData = evt.a[1]
                target = evtData[1]
                classId = evtData[2].GetVal()
                name = evtData[3].GetVal()
                try:
                    eTarget = self.__CrudCreate(target, classId, name)
                    if(isinstance(eTarget,Resource)):
                        pass
                    elif(isinstance(eTarget,Directory)):
                        pass
                except Exception as e:
                    self.logger.Error("Create failed: %s"%str(e))
                    if(self.config.printUnexpectedExceptionTraces):
                        traceback.print_exc()
            elif(evtType == EVT_TYPES.UPD):
                evtData = evt.a[1]
                target = evtData[1]
                try:
                    eTarget = self.idToObjectLookup[target]
                    featureName = evtData[2].GetVal()
                    value = evtData[3]
                    eValue = self.idToObjectLookup[value] if isinstance(value,Qry) else value.GetVal()
                    position = evtData[4].GetVal()
                    #update the model element
                    (eFeatureName,oldEValue,oldEParent) = self.__CrudUpdate(eTarget, featureName, eValue, position)
                    #consider special cases like resources, directories or packages
                    if(isinstance(eTarget,Resource)):
                        if(eFeatureName=="name"):
                            self.__RenameResource(eTarget)
                        elif(eFeatureName=="content"):
                            newContent = eTarget.content
                            eTarget.content = None #the content internally is always none
                            self.__ResourceSetContent(eTarget, newContent)
                    elif(isinstance(eTarget,Directory)): #moved or added workspace resources
                        if(eFeatureName=="name"):
                            self.__RenameDirectory(eTarget)
                        elif(eFeatureName=="resources"):
                            #1. check if a new resource is added or moved
                            if(isinstance(eValue,Resource)):
                                if(isinstance(oldEParent,Directory)):
                                    self.__MoveResource(eValue)
                                elif(None == oldEParent):
                                    self.__AddResource(eValue)
                            #2. check if an old resource needs deletion
                            if(isinstance(oldEValue,Resource)):
                                self.__DeleteResource(oldEValue)
                        elif(eFeatureName=="subdirectories"):
                            #1. check if a new dir is added or moved
                            if(isinstance(eValue,Directory)):
                                if(isinstance(oldEParent,Directory)):
                                    self.__MoveDirectory(eValue)
                                elif(None == oldEParent):
                                    self.__AddDirectory(eValue)
                            #2. check if an old dir needs deletion
                            if(isinstance(oldEValue,Directory)):
                                self.__DeleteDirectory(oldEValue)
                    elif(isinstance(eTarget,EPackage) and eFeatureName == "nsURI"):
                        self.rset.metamodel_registry[eValue] = eTarget
                        if(None != oldEValue):
                            del self.rset.metamodel_registry[oldEValue]
                except KeyError:
                    #should never go here because all elements are tracked 
                    self.logger.Warn("Event target unknown: %s"%(target))
                except Exception as e:
                    self.logger.Error("Update failed: %s"%(str(e)))
                    if(self.config.printUnexpectedExceptionTraces):
                        traceback.print_exc()
            elif(evtType == EVT_TYPES.DEL):
                evtData = evt.a[1]
                target = evtData[1]
                try:
                    eTarget = self.idToObjectLookup[target]
                    self.__CrudDelete(eTarget, target)
#                     if(isinstance(eTarget,Resource)):
#                         pass
#                     elif(isinstance(eTarget,Directory)):
#                         pass
#                     elif(isinstance(eTarget,EObject)):
#                         self.__Delete(eTarget, target)
#                     else:
#                         self.logger.Error("Object decoding error: %s",target)
                except KeyError:
                    #should never go here because all elements are tracked 
                    self.logger.Warn("Event target unknown: %s"%(target))
                except Exception as e:
                    self.logger.Error("Delete failed: %s"%(str(e)))
                    if(self.config.printUnexpectedExceptionTraces):
                        traceback.print_exc()
            else:
                #should never go here, because other events are not registered, but somebody from the outside could register other events for the mpl
                self.logger.Warn("Unexpected event type: %s"%(evtType))
                
                
    ### INTERNAL CRUD INTERFACE USED FOR UPDATES ###            
    
    def __CrudCreate(self,target:Qry,classId:str,name:str)->None:
        eObj = CreateEObject(classId, name, self.rset.metamodel_registry)
        #a new object was created. register and return it
        self.__UpdateObjLut(eObj, target)
        return eObj
            
    def __CrudUpdate(self,eTarget:EObject,featureName:str,eValue,position:int):
        (eFeatureName,oldEValue,oldEParent) = UpdateEObject(eTarget, featureName, eValue, position)
        self.__SetObjectDirty(eTarget) #every update will make the workspace dirty
        return (eFeatureName,oldEValue,oldEParent)
    
    def __CrudDelete(self,eTarget:EObject,target:Qry):
        self.__RemoveFromObjLut(eTarget,target)
        DeleteEObject(eTarget)
        pass

    ### UPDATE METHODS FOR FILE AND DIRECTORY CHANGES ####
       
    def __AddResource(self,resource:Resource):
        #get the new path
        newPath = self.__GetAbsElementPath(resource)
        if(None != newPath): #in case the Resource is attached to a directory that is not attached to the workspace no path can be determined and file creation must be post-poned
            #create a file placeholder
            open(newPath, 'w').close() #create and empty file. The content is created later
            self.__SetLastPersistentPath(resource, newPath)
            self.__SetResourceDirty(resource)
            relPath = os.path.relpath(newPath,self.baseDir)
            self.logger.Info("Created resource %s ."%(relPath))          
                    
    def __RenameResource(self,resource:Resource)->None:
        lastPersistentPath = self.__GetLastPersitentPath(resource)
        newName = resource.name
        if(lastPersistentPath): #otherwise this is a new resource and needs no renaming
            oldPath = lastPersistentPath
            filePath, oldName = os.path.split(oldPath)
            if(newName!=oldName):
                newPath = os.path.join(filePath,newName)
                os.rename(oldPath,newPath) 
                self.__SetLastPersistentPath(resource, newPath)
                #self.__RefreshResourceOrDirectoryPath(resource)
                # inform about action
                oldRelPath = os.path.relpath(oldPath,self.baseDir)
                newRelPath = os.path.relpath(newPath,self.baseDir)
                self.logger.Info("Renamed resource %s to %s."%(oldRelPath,newRelPath))
                 
    def __MoveResource(self,resource:Resource)->None:
        lastPersistentPath = self.__GetLastPersitentPath(resource)
        if(lastPersistentPath): #otherwise there is no need to move the resource
            oldPath = lastPersistentPath
            newPath = self.__GetAbsElementPath(resource)
            if(newPath!=oldPath):
                #move the file 
                os.rename(oldPath,newPath) 
                self.__SetLastPersistentPath(resource, newPath)
                #inform about action
                oldRelPath = os.path.relpath(oldPath,self.baseDir)
                newRelPath = os.path.relpath(newPath,self.baseDir)
                self.logger.Info("Moved resource %s to %s."%(oldRelPath,newRelPath))
                 
    def __DeleteResource(self,resource:Resource):
        lastPersistentPath = self.__GetLastPersitentPath(resource)
        if(lastPersistentPath):
            oldPath = lastPersistentPath
            #delete resource
            os.remove(oldPath)
            #self.__DeleteResourceOrDirectoryPath(resource)
            self.__DeleteLastPeristentPath(resource)
            #inform about action
            oldRelPath = os.path.relpath(oldPath,self.baseDir)
            self.logger.Info("Deleted resource %s."%(oldRelPath))
                 
    def __AddDirectory(self,directory):
        newPath = self.__GetAbsElementPath(directory)
        if(newPath): #if this is false, then the dir was added to a directory not attached to the workspace
            #create new dir file
            os.mkdir(newPath)
            self.__SetLastPersistentPath(directory, newPath)
            #recursively consider all contained resources and subdirs 
            for res in directory.resources:
                self.__AddResource(res)
            for subdir in directory.subdirectories:
                self.__AddDirectory(subdir)
            # inform about action
            newRelPath = os.path.relpath(newPath,self.baseDir)
            self.logger.Info("Added directory %s."%(newRelPath))
                 
     
    def __RenameDirectory(self,directory:Directory)->None:
        lastPersistentPath = self.__GetLastPersitentPath(directory)
        newName = directory.name
        if(lastPersistentPath): #otherwise this is a new resource and needs no renaming
            oldPath = lastPersistentPath
            filePath, oldName = os.path.split(oldPath)
            if(newName!=oldName):
                newPath = os.path.join(filePath,newName)
                #create the new dir
                os.rename(oldPath,newPath) 
                self.__RefreshResourceOrDirectoryPath(directory)
                #inform about action
                oldRelPath = os.path.relpath(oldPath,self.baseDir)
                newRelPath = os.path.relpath(newPath,self.baseDir)
                self.logger.Info("Renamed directory %s to %s."%(oldRelPath,newRelPath))
                     
    def __MoveDirectory(self,directory:Directory)->None:
        lastPersistentPath = self.__GetLastPersitentPath(directory)
        if(lastPersistentPath): #otherwise there is no need to move the directory
            oldPath = lastPersistentPath
            newPath = self.__GetAbsElementPath(directory)
            if(newPath!=oldPath):
                #move the directory 
                shutil.move(oldPath,newPath) 
                self.__RefreshResourceOrDirectoryPath(directory)
                #inform about action
                oldRelPath = os.path.relpath(oldPath,self.baseDir)
                newRelPath = os.path.relpath(newPath,self.baseDir)
                self.logger.Info("Moved directory %s to %s."%(oldRelPath,newRelPath))
                 
    def __DeleteDirectory(self,directory:Directory)->None:
        lastPersistentPath = self.__GetLastPersitentPath(directory)
        if(lastPersistentPath):
            oldPath = lastPersistentPath
            #delete resource
            shutil.rmtree(oldPath)
            self.__DeleteResourceOrDirectoryPath(directory)
            #inform about action
            oldRelPath = os.path.relpath(oldPath,self.baseDir)
            self.logger.Info("Deleted directory %s."%(oldRelPath))
                 
    def __RefreshResourceOrDirectoryPath(self,element:PathElementA)->None:
        ''' Updates the last persistent path for this element and all children.
        Should be called if a parent has obtained a new path.
        '''
        newPath = self.__GetAbsElementPath(element)
        if(newPath):
            self.__SetLastPersistentPath(element, newPath)
            if(isinstance(element, Directory)):
                #update contained elements
                for subres in element.resources:
                    self.__RefreshResourceOrDirectoryPath(subres)
                for subdir in element.subdirectories:
                    self.__RefreshResourceOrDirectoryPath(subdir)
                     
    def __DeleteResourceOrDirectoryPath(self,element:PathElementA)->None:
        ''' Removes the last persistent path from this and all child elements
        '''
        self.__DeleteLastPeristentPath(element)
        if(isinstance(element, Directory)):
            #update contained elements
            for subres in element.resources:
                self.__DeleteResourceOrDirectoryPath(subres)
            for subdir in element.subdirectories:
                self.__DeleteResourceOrDirectoryPath(subdir)
                
    ### SAVE FUNCTIONS ###
    
    def __SetObjectDirty(self,eObj:EObject)->None:
        resource = None
        if(isinstance(eObj,Resource)):
            resource = eObj
        else:
            resource = self.__ObjectGetResource(eObj)
        if(None != resource):
            self.__SetResourceDirty(resource)
    
    def __SetResourceDirty(self,resource:Resource)->None:
        resource._isDirty = True
        self.__SetWorkspaceDirty() #if one resource is dirty, the MPL is dirty
    
    def __SetResourceClean(self,resource:Resource)->None:
        resource._isDirty = False #set a hidden attribute not known by the MDB
        
    def __IsResourceDirty(self,resource:Resource)->None:
        return resource._isDirty
        

    def __SetWorkspaceDirty(self)->None:
        ''' Sets the MPL dirty. 
        This marks it to be saved in the next save loop.
        The time of setting dirty is remembered to calculate 
        if the autosafe timeout is triggered.
        '''
        self.isDirty = True
        self.lastUpdate = time.time()
        
    def __SetWorkspaceClean(self)->None:
        ''' Sets the MPL clean, i.e.
        no saving of resources is required 
        The time setting the MPL clean is rembered.
        '''
        self.isDirty = False
        self.lastSave = time.time()
        
    def __SaveWorkspace(self)->None:
        ''' Persists the workspace model in the file system.
        Changes are adapted as good as possible.
        After saving the workspace is clean again.
        '''        
        self.__SaveDirectory(self.workspaceModel)
        self.__SetWorkspaceClean() #mare the workspace as clean again.
        
    def __SaveDirectory(self,directory:Directory)->None:
        ''' Save all resources in a directory and
        all subdirectories.
        '''        
        for r in directory.resources:
            self.__SaveResource(r)
        # recurse in subdirectories
        for d in directory.subdirectories:
            self.__SaveDirectory(d)
            
    def __SaveResource(self,resource:Resource)->None:
        ''' Saves a workspace resource.
        Based on the content of the resource it is decided what
        file format and save routine is used.
        If the resource is detached from the workspace model, nothing will happen.
        '''
        if(self.__IsResourceDirty(resource)):
            actualPath = self.__GetAbsElementPath(resource)
            if(None != actualPath):
                try:
                    actualRelPath = os.path.relpath(actualPath, self.baseDirAbs)
                    self.logger.Info("Saving %s ..."%(actualRelPath))
                    start = default_timer()
                    content = self.__ResourceGetContent(resource)
                    if(isinstance(content,Document)): #XML file
                        self.__SaveXmlResource(resource, content, actualPath)
                    elif(isinstance(content,EObject)): #All that remains is tried to save as EResource
                        self.__SaveModelResource(resource, content, actualPath)
                    else:
                        self.logger.Warn('Do not know how to save %s.'%(actualPath))
        
                    #self.__SetLastPersistentPath(resource, actualPath)
                    end = default_timer()
                    self.__SetResourceClean(resource) #the resource was saved, so it is clean again now
                    self.logger.Info("ok (%f s)"%(end-start))
                except Exception as e: #catch exceptions to prevent that one failed resource does not stop the saving of the others. 
                    self.logger.Error("Failed to save %s: %s"%(actualRelPath,str(e)))
                    if(self.config.printUnexpectedExceptionTraces):
                        traceback.print_exc()
        
    
    def __SaveModelResource(self, resource:Resource, content:EObject, newPath:str)->None:
        ''' Saves a model in the ECORE XMI format
        '''
        eResource = self.__GetModelsEResource(resource)
        if(None==eResource): #create an new eResource
            eResource = self.rset.create_resource(newPath)
            self.__LinkResourceAndEResource(resource,eResource)
        else: #make sure the URI is up to date
            newUri = URI(newPath)
            eResource.uri = newUri
        #make sure the content is up to date
        if(0 == len(eResource.contents) or eResource.contents[0] != content):
            eResource.contents.clear()
            eResource.contents.append(content) #should not destroy the model because it has not father
        #finally save the content
        eResource.save()
        self.__SetLastPersistentPath(resource, newPath)
        
    def __SaveXmlResource(self, resource:Resource, content:Document, newPath:str)->None:
        ''' Saves the plain XML files based on the XML model
        '''
        ET = xml.etree.ElementTree
        parser = xml.dom.minidom
        #get root element
        rootElement = content.rootelement
        rootTag = ET.Element(rootElement.name)
        rootTag.text = rootElement.content
        #get attributes
        for attrib in rootElement.attributes:
                rootTag.set(attrib.name, attrib.value)
        #find all elements in root
        self.__SaveXmlFindSubElems(ET, rootTag, rootElement)
        #create output string
        xmlstr = parser.parseString(ET.tostring(rootTag)).toprettyxml(indent = "   ")
        with open(newPath, "w") as f:
            #comment: replace is not necessary
            f.write(xmlstr.replace('<?xml version="1.0" ?>',
                                 '<?xml version="1.0" encoding="utf-8"?>'))
        self.__SetLastPersistentPath(resource, newPath)    

    def __SaveXmlFindSubElems(self, ET, parentTag, Element)->None:
        ''' A support function of __SaveXmlResource
        '''
        for subelement in Element.subelements:
            #add to parent
            subTag = ET.SubElement(parentTag, subelement.name)
            subTag.text = subelement.content
            #get attributes
            for attrib in subelement.attributes:
                subTag.set(attrib.name, attrib.value)
            # find (sub)subelement
            self.__SaveXmlFindSubElems(ET, subTag, subelement)
            
    def __CalcProgress(self,totalSteps:int, currentStep:int, percentageOffset:int, percentageLimit:int)->int:
        percentageRange = percentageLimit-percentageOffset
        progress = round(percentageOffset+(currentStep/totalSteps)*percentageRange)
        return progress

        
    
                
                
