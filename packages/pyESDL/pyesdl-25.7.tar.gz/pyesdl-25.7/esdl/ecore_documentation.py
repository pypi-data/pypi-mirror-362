#  This work is based on original code developed and copyrighted by TNO 2023.
#  Subsequent contributions are licensed to you by the developers of such code and are
#  made available to the Project under one or several contributor license agreements.
#
#  This work is licensed to you under the Apache License, Version 2.0.
#  You may obtain a copy of the license at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Contributors:
#      TNO         - Initial implementation
#  Manager:
#      TNO

from pyecore.resources import ResourceSet, URI
from pyecore.utils import DynamicEPackage
from pyecore.ecore import EModelElement, EAnnotation
from pyecore.resources.resource import HttpURI

import esdl
from esdl.resources.xmlresource import XMLResource


esdlVersion = "unknown"

class EcoreDocumentation:
    """This class loads the dynamic meta-model and returns the documentation for attributes as these are
    not present in the static meta-model (e.g. in the classes that are generated in esdl.py)"""
    def __init__(self, esdlEcoreFile=None):
            self.esdl = None
            self.rset = None
            self.esdl_model = None
            self.resource = None
            if esdlEcoreFile is None:
                self.esdlEcoreFile = 'https://raw.githubusercontent.com/EnergyTransition/ESDL/master/esdl/model/esdl.ecore'
            else:
                self.esdlEcoreFile = esdlEcoreFile
            self._init_metamodel()
            global esdlVersion
            esdlVersion = self.get_esdl_version()

    def _init_metamodel(self):
            self.rset = ResourceSet()

            # Assign files with the .esdl extension to the XMLResource instead of default XMI
            self.rset.resource_factory['esdl'] = lambda uri: XMLResource(uri)

            # Read esdl.ecore as meta model
            mm_uri = URI(self.esdlEcoreFile)
            if self.esdlEcoreFile[:4] == 'http':
                mm_uri = HttpURI(self.esdlEcoreFile)
            try:
                esdl_model_resource = self.rset.get_resource(mm_uri)
            except Exception as e:
                self.esdl = esdl.esdl # use imported esdl packages (that miss attribute documentation)
                self.esdl_model = esdl.eClass
                return

            esdl_model = esdl_model_resource.contents[0]
            self.esdl_model = esdl_model
            # logger.debug('Namespace: {}'.format(esdl_model.nsURI))
            self.rset.metamodel_registry[esdl_model.nsURI] = esdl_model

            # Create a dynamic model from the loaded esdl.ecore model, which we can use to build Energy Systems
            self.esdl = DynamicEPackage(esdl_model)


    def get_doc(self, className, attributeName):
        """ Returns the documentation of an attribute from the dynamic meta model,
        because the static meta model does not contain attribute documentation"""
        ecoreClass = self.esdl_model.getEClassifier(className)
        if ecoreClass is None: return None
        attr = ecoreClass.findEStructuralFeature(attributeName)
        if attr is None: return None
        # logger.debug('Retrieving doc for {}: {}'.format(attributeName, attr.__doc__))
        return attr.__doc__

    def get_unit(self, className:str, attributeName:str) -> str:
        """
        :value: EmodelElement (e.g. EObject) that has an annotation attached
        :returns: The unit attached to this annotation or empty string
        """
        ecoreClass = self.esdl_model.getEClassifier(className)
        if ecoreClass is None: return None
        attr = ecoreClass.findEStructuralFeature(attributeName)
        if attr is None: return None

        annotation: EAnnotation = attr.getEAnnotation('http://www.tno.nl/esdl/attribute/unit')
        unit = annotation.details.get('unit', '') if annotation else None
        return unit if unit else ''

    def get_esdl_version(self):
        annotation: EAnnotation = self.esdl_model.getEAnnotation('http://www.tno.nl/esdl/version')
        version = annotation.details.get('version', '') if annotation else None
        return version if version else 'unknown'
