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
from typing import Dict, Any

from pyecore.resources import ResourceSet, URI
from pyecore.ecore import EEnum, EAttribute, EOrderedSet, EObject
from pyecore.utils import alias
from pyecore.resources.resource import HttpURI, Resource
from esdl.resources.xmlresource import XMLResource
from esdl import esdl
from uuid import uuid4
from io import BytesIO
from esdl import support_functions


class EnergySystemHandler:

    def __init__(self, energy_system=None):
        if energy_system is not None:
            self.energy_system = energy_system
        self.resource = None
        self.rset = ResourceSet()

        # Assign files with the .esdl extension to the XMLResource instead of default XMI
        self.rset.resource_factory['esdl'] = lambda uri: XMLResource(uri)

        # fix python builtin 'from' that is also used in ProfileElement as attribute
        # use 'start' instead of 'from' when using a ProfileElement
        # alias('start', esdl.ProfileElement.findEStructuralFeature('from'))
        esdl.ProfileElement.from_.name = 'from'
        setattr(esdl.ProfileElement, 'from', esdl.ProfileElement.from_)
        alias('start', esdl.ProfileElement.from_)

        setattr(EObject, '__copy__', support_functions.clone)
        setattr(EObject, 'clone', support_functions.clone)
        setattr(EObject, '__deepcopy__', support_functions.deepcopy)
        setattr(EObject, 'deepcopy', support_functions.deepcopy)

        # have a nice __repr__ for the EnergySystem class when printing. As most objects are linked together
        # we don't do this for other classes, due to recursion.
        esdl.EnergySystem.__repr__ = lambda x: '{}({})'.format(type(x).__name__, EnergySystemHandler.attr_to_dict(x))

    def _new_resource_set(self):
        """Resets the resourceset and removes all files that are loaded before (e.g. when loading a new file)"""
        self.rset = ResourceSet()
        self.resource = None
        # Assign files with the .esdl extension to the XMLResource instead of default XMI
        self.rset.resource_factory['esdl'] = lambda uri: XMLResource(uri)

    def load_file(self, uri_or_filename: str) -> esdl.EnergySystem:
        """Loads a file in a new resource set"""
        if uri_or_filename[:4] == 'http':
            uri = HttpURI(uri_or_filename)
        else:
            uri = URI(uri_or_filename)
        return self.load_uri(uri)

    def load_uri(self, uri) -> esdl.EnergySystem:
        """Loads a new resource in a new resourceSet"""
        self._new_resource_set()
        self.resource = self.rset.get_resource(uri)
        # At this point, the model instance is loaded!
        self.energy_system = self.resource.contents[0]
        return self.energy_system

    def add_uri(self, uri) -> esdl.EnergySystem:
        """Adds the specified URI to the resource set, i.e. load extra resources that the resource can refer to."""
        self.resource = self.rset.get_resource(uri)
        # At this point, the model instance is loaded!
        self.energy_system = self.resource.contents[0]
        return self.energy_system

    def load_from_string(self, esdl_string) -> esdl.EnergySystem:
        uri = StringURI('from_string.esdl', esdl_string)
        # self._new_resource_set()
        self.resource = self.rset.create_resource(uri)
        self.resource.load()
        self.energy_system = self.resource.contents[0]
        return self.energy_system

    def to_string(self) -> str:
        """
        To serialize an energy system in a resource, we use a StringURI to save it to a string instead of a file
        :return: XML string of the current resource/ESDL file that is loaded.
        """
        uri = StringURI('to_string.esdl')
        self.resource.save(uri)
        # return the string
        return uri.getvalue()

    def to_bytesio(self) -> BytesIO:
        """Returns a BytesIO stream for the energy system"""
        uri = StringURI('to_string.esdl')
        self.resource.save(uri)
        return uri.get_stream()

    def get_external_reference(self, url: str, object_id: str = None):
        """
        Support function to create a reference to an external ESDL/EDD file.

        :param url: web address e.g. a URL from the EDR, https://drive.esdl.hesi.energy/store/resource/edr/Public/Key figures/Emissiefactoren energiedragers 2017.edd
        :param object_id: Optional, the id of the object in the file to refer to, if not specified, it will return the root of the file.
        :return: EObject returning the root of the document, or the object that is specified by the id found in that file

        Be aware that when assigning an external reference to a containment relation, the content from the external reference
        will be moved (not copied) to the resource that it is assigned to. If you want the reference to be external,
        only use this for references (no diamond), not containment relations (a diamond in the ESDL UML diagram)
        """
        remote_resource = self.rset.get_resource(url)
        if object_id is not None and object_id in remote_resource.uuid_dict:
            return remote_resource.uuid_dict[object_id]
        else:
            return remote_resource.contents[0]

    def save(self, filename=None):
        """Add the resource to the resourceSet when saving"""
        if filename is None:
            self.resource.save()
        else:
            uri = URI(filename)
            fileresource = self.rset.create_resource(uri)
            # add the current energy system
            fileresource.append(self.energy_system)
            # save the resource
            fileresource.save()
            self.rset.remove_resource(fileresource)

    def save_as(self, filename):
        """Saves the resource under a different filename"""
        self.resource.save(output=filename)

    def get_energy_system(self) -> esdl.EnergySystem:
        return self.energy_system

    # Using this function you can query for objects by ID
    # When loading an ESDL-file, all objects that have an ID defined are stored in resource.uuid_dict automatically
    # Note: If you add things later to the resource, it won't be added automatically to this dictionary though.
    # Use get_by_id_slow() for that
    def get_by_id(self, object_id) -> EObject:
        if object_id in self.resource.uuid_dict:
            return self.resource.uuid_dict[object_id]
        else:
            print('Can\'t find object for id={} in uuid_dict of the ESDL model'.format(object_id))
            raise KeyError('Can\'t find object for id={} in uuid_dict of the ESDL model'.format(object_id))
            return None

    def get_by_id_slow(self, object_id) -> EObject:
        for o in self.energy_system.eAllContents():
            if hasattr(o, 'id'):
                if o.id == object_id:
                    return o

    def update_uuid_dict(self, es: esdl.EnergySystem = None) -> None:
        """
        Update the Resource's uuid_dict of a specific energy system
        This might be necessary when e.g. deepcopying an object in an resource that has references to other parts of that
        resource that are not being deepcopied.
        :param es: energy system that needs a uuid_dict update, if None, the current self.energy_system is used
        """
        if not es:
            es = self.energy_system
        for o in es.eAllContents():
            if hasattr(o, 'id'):
                es.eResource.uuid_dict[o.id] = o

    def add_object(self, obj):
        if hasattr(obj, 'id'):
            if id is not None:
                self.resource.uuid_dict[obj.id] = obj
            else:
                print('Id has not been set for object {}({})', obj.eClass.name, obj)

    def remove_object(self, obj):
        if hasattr(obj, 'id'):
            if id is not None:
                del self.resource.uuid_dict[obj.id]

    def remove_obj_by_id(self, obj_id):
        del self.resource.uuid_dict[obj_id]

    def get_all_instances_of_type(self, esdl_type):
        all_instances = list()
        for esdl_element in self.get_energy_system().eAllContents():
            if isinstance(esdl_element, esdl_type):
                all_instances.append(esdl_element)
        return all_instances

    @staticmethod
    def instantiate_esdltype(className: str) -> EObject:
        """
        Instantiates a new instance of an ESDL class className and returns it.
        E.g. ip:InPort = instantiate_esdltype("InPort")
        """
        return esdl.getEClassifier(className)()

    @staticmethod
    def resolve_fragment(resource: Resource, fragment: str):
        """
        Resolves a URI fragment (e.g. '//@instance.0/@area/@asset.0/@port.0') to the associated object
        and returns the object.
        This is used for objects that have no ID attribute
        """
        return resource.resolve(fragment)

    @staticmethod
    def attr_to_dict(esdl_object) -> Dict[str, Any]:
        """ Creates a dict of all the attributes of an ESDL object, useful for printing/debugging"""
        d = dict()
        d['esdlType'] = esdl_object.eClass.name
        for attr in dir(esdl_object):
            attr_value = esdl_object.eGet(attr)
            if attr_value is not None:
                d[attr] = attr_value
        return d

    @staticmethod
    def generate_uuid() -> str:
        ''' Creates a uuid: useful for generating unique IDs'''
        return str(uuid4())

    def create_empty_energy_system(self, name, es_description=None, inst_title="Instance0", area_title="Main Area") -> esdl.EnergySystem:
        """
        Creates a new empty Energy System (EnergySystem + Instance + Area) and adds it to the resource set
        :param name:
        :param es_description: Optional
        :param inst_title: optional, default "Instance0"
        :param area_title:
        :return: the created empty Energy System
        """
        es_id = self.generate_uuid()
        self.energy_system = esdl.EnergySystem(id=es_id, name=name, description=es_description)

        instance = esdl.Instance(id=self.generate_uuid(), name=inst_title)
        self.energy_system.instance.append(instance)

        # TODO: check if this (adding scope) solves error????
        area = esdl.Area(id=self.generate_uuid(), name=area_title, scope=esdl.AreaScopeEnum.from_string('UNDEFINED'))
        instance.area = area

        self.resource = self.rset.create_resource(StringURI('new_energy_system.esdl'))
        # add the current energy system
        self.resource.append(self.energy_system)
        return self.energy_system

    # Support for Pickling when serializing the energy system in a session
    # The pyEcore classes by default do not allow for simple serialization for Session management in Flask.
    # Internally Flask Sessions use Pickle to serialize a data structure by means of its __dict__. This does not work.
    # Furthermore, ESDL can contain cyclic relations. Therefore we serialize to XMI and back if necessary.
    # This is not efficient with large ESDLs
    def __getstate__(self):
        state = dict()
        state['energySystem'] = self.to_string();
        return state

    def __setstate__(self, state):
        self.__init__()
        self.load_from_string(state['energySystem'])

    @staticmethod
    def version():
        '''Returns the version of pyESDL'''
        return __version__


'''Version information about pyESDL'''
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


"""
Allows to convert a model to an XML string and vice versa
"""
class StringURI(URI):
    def __init__(self, uri, text=None):
        """
        Creates a new StringURI to be used for a resource. By setting text it can convert that XML text to a
        python class model, when doing a resource.load(uri). If text is empty and the associated resource is not,
        resource.save(uri) will convert the resource to XML. Use uri.getvalue() to return the string representation of
        this resource.
        :param uri: the file name of this ESDL, should be unique in this resource set.
        :param text: XML string to convert to a resource (pyEcore classes)
        """
        super(StringURI, self).__init__(uri)
        if text is not None:
            self.__stream = BytesIO(text.encode('UTF-8'))

    def getvalue(self):
        """
        :return: the XML as a string of this ESDL resource
        """
        readbytes = self.__stream.getvalue()
        # somehow stringIO does not work, so we use BytesIO
        string = readbytes.decode('UTF-8')
        return string

    def create_instream(self):
        return self.__stream

    def create_outstream(self):
        self.__stream = BytesIO()
        return self.__stream

    def get_stream(self):
        return self.__stream
