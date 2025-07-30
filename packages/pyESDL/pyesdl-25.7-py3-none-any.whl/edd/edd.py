"""Definition of meta model 'edd'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'edd'
nsURI = 'http://www.tno.nl/edr/edd'
nsPrefix = 'edd'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)


class EnergyDataDescription(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EString, unique=True, derived=False, changeable=True, iD=True)
    title = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    description = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    tags = EAttribute(eType=EString, unique=True, derived=False, changeable=True, upper=-1)
    version = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    graphURL = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    esdlType = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    lastChanged = EAttribute(eType=EDate, unique=True, derived=False,
                             changeable=True, transient=True)
    publicationDate = EAttribute(eType=EDate, unique=True, derived=False,
                                 changeable=True, transient=True)
    esdl = EReference(ordered=True, unique=True, containment=True, derived=False)
    image = EReference(ordered=True, unique=True, containment=True, derived=False)

    def __init__(self, *, id=None, title=None, description=None, tags=None, esdl=None, image=None, version=None, graphURL=None, esdlType=None, lastChanged=None, publicationDate=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if tags:
            self.tags.extend(tags)

        if version is not None:
            self.version = version

        if graphURL is not None:
            self.graphURL = graphURL

        if esdlType is not None:
            self.esdlType = esdlType

        if lastChanged is not None:
            self.lastChanged = lastChanged

        if publicationDate is not None:
            self.publicationDate = publicationDate

        if esdl is not None:
            self.esdl = esdl

        if image is not None:
            self.image = image


class Image(EObject, metaclass=MetaEClass):

    contentType = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    imageData = EAttribute(eType=EByteArray, unique=True, derived=False, changeable=True)

    def __init__(self, *, contentType=None, imageData=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if contentType is not None:
            self.contentType = contentType

        if imageData is not None:
            self.imageData = imageData
