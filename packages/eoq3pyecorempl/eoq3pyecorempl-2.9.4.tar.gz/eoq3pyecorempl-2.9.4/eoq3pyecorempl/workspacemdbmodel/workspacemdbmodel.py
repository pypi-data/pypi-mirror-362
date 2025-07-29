"""Definition of meta model 'workspacemdbmodel'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'workspacemdbmodel'
nsURI = 'http://www.eoq.de/workspacemdbmodel/v3.0'
nsPrefix = 'de.eoq'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)


@abstract
class PathElementA(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True, default_value='.')

    def __init__(self, *, name=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name


class Directory(PathElementA):

    subdirectories = EReference(ordered=True, unique=True, containment=True, upper=-1)
    resources = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, subdirectories=None, resources=None, **kwargs):

        super().__init__(**kwargs)

        if subdirectories:
            self.subdirectories.extend(subdirectories)

        if resources:
            self.resources.extend(resources)


class Resource(PathElementA):

    info = EAttribute(eType=EString, derived=False, changeable=True, default_value='.')
    isLoaded = EAttribute(eType=EBoolean, derived=False, changeable=True)
    content = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, content=None, info=None, isLoaded=None, **kwargs):

        super().__init__(**kwargs)

        if info is not None:
            self.info = info

        if isLoaded is not None:
            self.isLoaded = isLoaded

        if content is not None:
            self.content = content


class Workspace(Directory):

    actualPathAbs = EAttribute(eType=EString, derived=False, changeable=True)
    actualPath = EAttribute(eType=EString, derived=False, changeable=True)
    actualPathCwd = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, actualPathAbs=None, actualPath=None, actualPathCwd=None, **kwargs):

        super().__init__(**kwargs)

        if actualPathAbs is not None:
            self.actualPathAbs = actualPathAbs

        if actualPath is not None:
            self.actualPath = actualPath

        if actualPathCwd is not None:
            self.actualPathCwd = actualPathCwd
