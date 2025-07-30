from pyecore.resources import global_registry
from .edd import getEClassifier, eClassifiers
from .edd import name, nsURI, nsPrefix, eClass
from .edd import EnergyDataDescription, Image

from pyecore.ecore import EObject

from . import edd

__all__ = ['EnergyDataDescription', 'Image']

eSubpackages = []
eSuperPackage = None
edd.eSubpackages = eSubpackages
edd.eSuperPackage = eSuperPackage

EnergyDataDescription.esdl.eType = EObject
EnergyDataDescription.image.eType = Image

otherClassifiers = []

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)

register_packages = [edd] + eSubpackages
for pack in register_packages:
    global_registry[pack.nsURI] = pack
