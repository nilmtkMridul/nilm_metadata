NILM METADATA
=============

NILM Metadata is a framework for
modelling appliances, meters, measurements, buildings and datasets.
Default properties for appliances and meters are also provided.

NILM Metadata aims to provide:

* a schema for describing:
  * domestic appliances
    * a controlled vocabulary for appliance names and categories
    * a list of time periods when each appliance was active
    * each appliance can contain any number of components (e.g. a
      light fitting can contain multiple lamps and a dimmer)
    * prior knowledge about the distribution of variables such as:
      * on power
      * on duration
      * usage in terms of hour per day
      * appliance correlations (e.g. that the TV is usually on if the
        games console is on)
  * electricity meters (whole-home and individual appliance meters)
    * a controlled vocabulary for measurements
    * wiring hierarchy of meters
  * a mapping of which appliances are connected to which meters

NILM Metadata uses [JSON Schema](http://json-schema.org/) to define
the syntactic elements of the schema and then uses a simple but
powerful inheritance mechanism to allow 'objects' (e.g. a
specification of an appliance) to inherit from an existing object.
For example, `laptop computer` is a specialisation of `computer`
and the two share several properties (e.g. both are in the `ICT`
category).  So `laptop computer` inherits from `computer` and modifies
and adds any properties it needs.  In this way, we can embrace the
["don't repeat yourself (DRY)"](http://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
principal by exploiting the relationship between appliances.

The metadata itself is [YAML](http://en.wikipedia.org/wiki/YAML).

The aim is that NILM Metadata can be used as a stand-alone project to
specify the metadata for any NILM dataset; and that metadata can then
be used with the open-source energy disaggregation and analytics
framework [NILMTK](http://nilmtk.github.io/).

Example
=======

Below is a snippet of the metadata for the UKPD dataset.  The snippet
first describes the dataset itself, then describes the first building
and describes the boiler and one meter in the building.

```yaml
name: UKPD
full_name: UK Power Dataset
institution: Imperial College London
contact: jack.kelly@imperial.ac.uk
description: Recording from 4 domestic homes in or near to London, UK.
number_of_buildings: 4
timezone: Europe/London
urls: ['http://www.doc.ic.ac.uk/~dk3810/data']
buildings:
  1:
    geo_location:
      city: London
      country: UK
      latitude: 51.464462
      longitude: -0.076544}
      
    timezone: Europe/London
    
    timeframe:
      start: 2012-11-09
      end: 2014-03-11
      
    utilities:
    
      electric:
      
        mains_voltage:
          nominal: 230
          tolerance_lower_bound: 10
          tolerance_upper_bound: 6

        appliances:
        - name: boiler
          instance: 1
          model: Greenstar 30CDi Conventional natural gas
          manufacturer: Worcester
          fuel: natural gas
          subtype: regular
          meter_ids: [2]
          nominal_consumption: 
            on_power: 70   # watts
          part_number: 41-311-71
          room:
            name: bathroom
            instance: 1
          year_of_purchase: 2011
          control:
            system: [manual, thermostat, timer]
          energy_rating: A
          categories:
            size: large
            traditional: heating
            google_shopping:
            - climate control
            - furnaces and boilers
            electrical:
            - single-phase induction motor
          components:
          - name: water pump
            parent: water pump
            categories:
              electrical: [single-phase induction motor]
          distributions:
            on_power:
            - model:
              distribution_name: normal
              mu: 73   # watts
              sigma: 12

        meters:
        - model: EcoManager Whole House Transmitter
          manufacturer: Current Cost / Sailwider        
          id: 1
          sample_period: 6          
          max_sample_period: 120
          measurements:
          - physical_quantity: power
            type: apparent           
            cummulative: false
            minimum: 0
            maximum: 25000            
          dates_active:
          - start: 2012-11-09        
            end: 2014-03-11
          model_url: https://shop.edfenergy.com/Item.aspx?id=547
          site_meter: true
          wireless: true
```


Version numbering and contributing
==================================

The current release is version 0.1.  There are definitely plenty of
improvements that can be made so please submit pull requests for the
dev version!


Validating a new JSON file against the schema
=============================================

TODO


Related projects
================

* [Project Haystack](http://project-haystack.org/), to quote their
  website, "*is an open source initiative to develop tagging
  conventions and taxonomies for building equipment and operational
  data. We define standardized data models for sites, equipment, and
  points related to energy, HVAC, lighting, and other environmental
  systems.*"  Haystack is an awesome project but it does not specify a
  controlled vocabulary for appliances, which is the meat of the
  `nilm_metadata` project.  Where appropriate, `nilm_metadata` does
  use similar properties to Haystack (e.g. the "site_meter" property
  is borrowed directly from Haystack).
* [WikiEnergy](http://wiki-energy.org/) "*A Universe of Energy Data,
  Available Around the World*".

Testing
=======

```
nosetests --nocapture
```


Validating without network access
=================================

To maximise code re-use, individual schema files reference other
schema files.  Files referred to from
each schema are loaded from github.

If you need to do validation without network
access then it should be possible but will require a bit of hacking.
I think you would first need to remove all the "id" properties from
every schema file and then use a code snippet like
[this one](https://github.com/Julian/jsonschema/issues/98#issuecomment-17531405).
