# pyESDL

![PyPI - Version](https://img.shields.io/pypi/v/pyesdl)  ![PyPI - Downloads](https://img.shields.io/pypi/dm/pyESDL)  ![ReadTheDocs status](https://readthedocs.org/projects/pyesdl/badge/?version=latest)


pyESDL is a library for using ESDL in python programs. ESDL stands for Energy System Description
Language and is created to support developers creating, parsing, generating ESDL-files with the 
goal to create interoperable energy system transition tooling.

This package contains all the ESDL classes of the ESDL language and an `EnergySystemHandler`
that helps the developer to read and write ESDL-files.

The PyESDL documentation can be found here: [https://pyesdl.readthedocs.io/](https://pyesdl.readthedocs.io/)

More information about ESDL can be found at:
1. [ESDL gitbook documentation](https://energytransition.gitbook.io/esdl/) with a general introduction,
   example applications and some code samples.
2. [ESDL Model Reference documentation](https://energytransition.github.io/) that describes all the 
   classes and definitions in detail using a clickable UML diagram.

## Support functions:

PyESDL now comes with a lot of support functions for:

- handling profiles:
  - ProfileManager: reading profiles from a CSV, converting to and from esdl.DateTimeProfile or esdl.TimeSeriesProfile.
  - ExcelProfileManager: reading from and writing profiles to Excel files
  - InfluxDBProfileManager: reading from and writong profiles to InfluxDB (version 1.7)
- handling geometries: conversion to and from esdl geometries, WKT, WKB, GeoJSON, ...
- qunatity and units: unit conversion, converting a QuantityAndUnit to a string, building a QuantityAndUnit from a string

## Installing
PyESDL now comes with a lot of support functions for handling profiles, geometries and qunatity and units. This requires
additional dependencies. As not all users might need all functionalities, there are several ways to install pyESDL.

Use the following command to install the pyESDL python module including all dependencies from the PyPi registry:

`pip install pyESDL[all]`

To install the minimal version of pyESDL:

`pip install pyESDL`

To install the dependencies for additional profile functionalities (only required for support for Excel and InfluxDB):

`pip install pyESDL[profiles]`

To install the dependencies for handling geometries:

`pip install pyESDL[geometry]`

## Documentation

We will start soon with generating more documentation on [readthedocs](https://pyesdl.readthedocs.io/).

## Usage

### Example 1 - Creating an ESDL-file and saving it to disk
```python
from esdl.esdl_handler import EnergySystemHandler
from esdl import esdl
esh = EnergySystemHandler()
es = esh.create_empty_energy_system(name="ES1", es_description='Nice Energy System',
                                   inst_title='instance 1', area_title="Area 51")
print(es)
esh.save(filename="test.esdl")
```

### Example 2 - Loading an ESDL file and adding a WindTurbine to an area
```python
from esdl.esdl_handler import EnergySystemHandler
from esdl import esdl
from pprint import pprint

esh = EnergySystemHandler()
# load an ESDL file and use type hinting to help the IDE to do auto completion
es: esdl.EnergySystem = esh.load_file('test.esdl')
print(es)
# Create a WindTurbine
wind_turbine = esdl.WindTurbine(name='WindTurbine at coast', rotorDiameter=50.0, height=100.0,
                               type=esdl.WindTurbineTypeEnum.WIND_ON_COAST)

# print the wind turbines properties in ESDL as a dict
pprint(esh.attr_to_dict(wind_turbine))

# Get the area where this windturbine should be added
area51: esdl.Area = es.instance[0].area
# add the WindTurbine to the area
area51.asset.append(wind_turbine)
# save the file
esh.save()

# Give the WindTurbine a location on the map
location = esdl.Point(lat=52.6030475337285, lon=4.729614257812501)
wind_turbine.geometry = location

esh.save()
# Convert the Energy System to an XML string and print it
xml_string = esh.to_string()
print(xml_string)
```

### Converting ESDL units
Example:
```python
from esdl.units.conversion import convert_to_unit, ENERGY_IN_J, ENERGY_IN_MWh

converted = convert_to_unit(5, ENERGY_IN_MWh, ENERGY_IN_J)
18E9 == converted
>> True
```

## Changes

## Version 25.7
- Add support for ESDL release 25.7
- Small bugfix in generating a QuantityAndUnitType instance from a string
- Fix bug in unit conversion when physical quantities are not the same

## Version 25.5.2
- Fix bug in unit conversion when physical quantities are not the same

## Version 25.5.1
- Add support for ESDL release 25.5.1

## Version 25.5
- Add support for ESDL release 25.5

## Version 25.2
- Add support for ESDL release 25.2

## Version 24.11.2
- Add link to documentation of pyESDL on readthedocs
- Fix geojson dependency 

## Version 24.11.1
- Downgrade pyEcore to 0.13.2 again, due to error with rows in tables

## Version 24.11
- Update build system and dependencies
- Fix wrong import in `support_functions` on Python > 3.12
- Update pyEcore to 0.15.1

## Version 24.9
- Add support for ESDL release 24.09
- Upgrade shapely and geojson versions

## Version 24.2
- Fix bug when no tags are given for an InfluxDBProfile
- Fix issue with multi-valued attribute values (such as values in TableRow)
- Start with the ReadTheDocs documentation

### Version 24.1
- Add support for ESDL release 24.01 

### Version 23.12.1
- Fix bug in ProfileManager
- InfluxDBProfileManager.load_influxdb now returns an esdl.InfluxDBProfile
- InfluxDBProfileManager: improved handling of situations where no data is returned

### Version 23.12
- Bug fixes in InfluxDBProfileManager

### Version 23.11.2
- Add support for ESDL release 23.11 (with powerCurveTable for WindTurbine)

### Version 23.11.1
- Fix bug in determining the end_datetime of profiles

### Version 23.11
- Implement EDR client
- Added more predefined QaUs
- Support for tags in InfluxDBProfileManager

### Version 23.10.1
- Implement set_profile function
- Corrected some bugs (datetime_utils missing, support for fields with '-')

### Version 23.10
- Add support functions for handling profiles, geometries and qunatity and units.

### Version 23.03
- Add support for ESDL release 23.03 (added 2 PowerPlant types, referenceYear for CostInformation, added fullLoadHours and operationalHours attributes to Consumer and Transport classes)

### Version 22.11.1
- Add support for ESDL release 22.11 (with KPI-KPI and Sector-Sector relation, ElectricBoiler, PowerPlant types, ...)

### Version 22.11
- Add support for Energy Data Repository files (*.edd)
- Add supoprt for linking to external files (e.g. stored in the EDR) using `get_external_reference(url, object_id)`
- Add function to instantiate a class by its class name (`instantiate_esdltype(className)`) 

### Version 22.10.0
- Add support for ESDL release 22.10 (with Port-Constraint relation, support for modelling material flows, added powerFactor attribute for electricity related assets, DataSourceList)

### Version 22.7.0
- Add support for ESDL release 22.07 (with ConnectableAsset, ExposedPortsAsset, PumpedHydroPower and CAES assets, restructured some LabelJump information, asset Constraints)

### Version 21.12.0
- Add support for ESDL release 21.12 (with quantity and unit information for InputOutputRelation, renaming of some distribution information classes of AggregatedBuildings)

### Version 21.11.0
- Add support for ESDL release 21.11 (with HybridHeatpump, developmentCosts, Commodity emission attribute)

 ### Version 21.10.0
- Add support for ESDL release 21.10 (with storage volumes)

### Version 21.9.1
- Add support for ESDL release 21.9 (with pipe and cable relations)

### Version 21.9.0
- Fix pyecore 0.12.1 dependency issue

### Version 21.7.1
- Add support for ESDL release 21.7 (with BufferDistance, ATES)

#### Version 21.6.2
- Fix issue with version definition, making the EnergySystemHandler unusable.
- Add get_all_instances_of_type() to EnergySystemHandler to retrieve all the instances of a certain type in an EnergySystem.
  
  E.g. ```esh.get_all_instances_of_type(esdl.GenericProfile)``` will give you all the profiles defined in the EnergySystem.

#### Version 21.6.1
- Add support for InputOutputRelation 


## Releasing
The release process is as follows:
1. Do a `git tag` with the new version number
2. Do `python setup.py sdist bdist_wheel` to create the tarball and wheel in the `dist` folder
3. upload to PyPi: `python3 -m twine upload --repository pyESDL dist/*`

