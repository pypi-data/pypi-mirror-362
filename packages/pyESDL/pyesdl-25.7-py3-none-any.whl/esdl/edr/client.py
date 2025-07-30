#  This work is based on original code developed and copyrighted by TNO 2022.
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
import base64
import json
import urllib
from dataclasses import dataclass

import requests

from esdl.esdl_handler import EnergySystemHandler

EDR_URL="https://drive.esdl.hesi.energy"


@dataclass
class EDRInfo:
    """
    Represents information about an object in the Energy Data Repository (EDR)
    """
    id: str
    """ the ID (or path) of the object in the EDR """
    title: str
    """ the title of the object in the EDR """
    description: str
    """ the description of the object in the EDR """
    esdl_type: str
    """ the ESDL type of the object in the EDR """


class EDRClient:
    """
    Implements an interface to the Energy Data Repository (EDR)
    """
    def __init__(self, host=None, port=None):
        """
        Constructor of the EDR client. Uses the public EDR URL by default, but allows to specify a different "host" and
        "port" for using a local EDR instance

        :param host: alternative hostname of a EDR instance
        :param port: alternative port of a EDR instance
        """
        if host:
            self.EDR_URL = host + ":" + port
        else:
            self.EDR_URL = EDR_URL

    def get_objects_list(self, esdl_type):
        """
        Retrieves a list of objects from the EDR of a given type. The input parameter esdl_type can for example be
        "EnergyAsset", "Sectors", "Carriers" or "InfluxDBProfile". Each element in the returned list is of type EDRInfo
        and has id, title, description and esdl_type fields. The ESDL type of the elements in the list can be subtypes
        of the input esdl_type, e.g. you ask for objects of type "EnergyAsset" and get back objects of type
        "WindTurbine".

        :param esdl_type: the type of the ESDL class
        :return: list of objects of the given type
        """
        url = self.EDR_URL + "/store/edr/query?addESDL=false&addImageData=false&esdlType="+esdl_type+"&maxResults=-1"

        obj_list = list()

        r = requests.get(url)
        if r.status_code == 200:
            result = json.loads(r.text)

            for item in result:
                obj = EDRInfo(
                    id=item["id"],
                    title=item["title"],
                    description=item["description"] if "description" in item else "",
                    esdl_type=item["esdlType"] if "esdlType" in item else None,
                )
                obj_list.append(obj)

        return obj_list

    def get_object_esdl(self, edr_path):
        """
        Retrieves a specific ESDL object from the EDR

        :param edr_path: the path in the EDR to the specific ESDL object
        :return: the ESDL object
        """
        url = self.EDR_URL + "/store/edr/query?addESDL=true&path=" + urllib.parse.quote(edr_path, safe='')

        headers = {
            'Accept': "application/json",
            'User-Agent': "pyESDL/EDRClient"
        }

        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            result = json.loads(r.text)

            if result:
                if 'esdl' in result[0]:
                    esdl_str_b64 = result[0]['esdl']
                    esdl_str_b64_bytes = esdl_str_b64.encode('utf-8')
                    esdl_str_bytes = base64.b64decode(esdl_str_b64_bytes)
                    esdl_str = esdl_str_bytes.decode('utf-8')

                    esh = EnergySystemHandler()
                    esdl_obj = esh.load_from_string(esdl_string=esdl_str)
                    return esdl_obj

        # return None in all other cases
        return None



