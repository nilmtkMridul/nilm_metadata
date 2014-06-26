.. highlight:: yaml

**********************************
Central appliance metadata
**********************************

Manual
======

Common info about appliances is stored in NILM Metadata.  This includes:

* Categories for each appliance type
* prior knowledge about the distribution of variables such as:

  * on power
  * on duration
  * usage in terms of hour per day
  * appliance correlations (e.g. that the TV is usually on if the games console is on)
* valid additional properties for each appliance
* mapping from country codes to nominal mains voltage ranges

The central info about appliances uses a simple but powerful
inheritance mechanism to allow appliances to inherit from a other
appliances.  For example, 'laptop computer' is a specialisation of
'computer' and the two share several properties (e.g. both are in the
'ICT' category).  So 'laptop computer' inherits from 'computer' and
modifies and adds any properties it needs.  In this way, we can
embrace the
`don't repeat yourself (DRY) <http://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`_
principal by exploiting the relationship between appliances.


Inheritance
-----------

* protypical inheritance; like JavaScript
* dicts are updated; lists are extended; other properties are overwritten
* arbitrary inheritance depth

Components
----------

* recursive
* categories of appliance is updated with categories from each component

Subtypes versus a new child object
----------------------------------

Appliance specification objects can take a 'subtype' property.  Why
not use inheritance for all subtypes?  The rule of thumb is that if a
subtype is functionally different to its parent then it should be
specified as a separate o child bject (for example, a gas hob and an electric
hob clearly have radically different electricity usage profiles) but
if the differences are minor (e.g. a digital radio versus an analogue
radio) then the appliances should be specified as subtypes of the same object.

Naming conventions
------------------

* properties are lowercase with underscores, e.g. `main_room_light`
* object names (not specific makes and models) are lowercase with
  spaces, unless they are acronyms in which case they are uppercase
  (e.g. 'LED')
* object names of specific makes and models are uppercase with a tilde
  to separate the manufacturer from the model e.g. `Samsung~RSU1R`
* category names are lowercase with spaces
* ambersands are replaced with 'and'

Categories
----------

:Traditional: wet, cold, consumer electronics, ICT, cooking, heating
:Misc: misc, sockets
:Size: small, large
:Electrical: 
  - lighting, incandescent, fluorescent, compact, linear, LED
  - resistive
  - power electronics
  - SMPS, no PFC, passive PFC, active PFC
  - single-phase induction motor, capacitor start-run, constant torque


Example
-------

To demonstrate the inheritance system, let's look at specifying a
boiler.

First, NILM Metadata specifies a 'heating appliance' object, which is
can be considered the 'base class'::

  heating appliance:
    parent: appliance
    categories:
      traditional: heating
      size: large

Next, we specify a 'boiler' object, which inherits from 'heating appliance'::


  #------------- BOILERS ------------------------

  boiler: # all boilers except for electric boilers

    parent: heating appliance

    synonyms: [furnace]

    # Categories of the child object are appended
    # to existing categories in the parent.
    categories:
      google_shopping:
        - climate control
        - furnaces and boilers

    # Here we specify that boilers have a component
    # which is itself an object whose parent
    # is `water pump`.
    components:
      - parent: water pump

    # Boilers have a property which most other appliances
    # do not have: a fuel source.  We specify additional
    # properties using the JSON Schema syntax.
    additional_properties:
      fuel:
        enum: [natural gas, coal, wood, oil, LPG]

    subtypes:
      - combi
      - regular

    # We can specify the different mechanisms that
    # control the boiler.  This is useful, for example,
    # if we want to find all appliances which 
    # must be manually controlled (e.g. toasters)
    control: [manual, timer, thermostat]

    # We can also declare prior knowledge about boilers.
    # For example, we know that boilers tend to be in
    # bathrooms, utility rooms or kitchens
    distributions:
      room:
        distribution_of_data:
          categories: [bathroom, utility, kitchen]
          values: [0.3, 0.2, 0.2]
          # If the values do not add to 1 then the assumption
          # is that the remaining probability mass is distributed equally to
          # all other rooms.
        source: subjective # These values are basically guesses!


Finally, in the metadata for the dataset itself, we can do::

  type: boiler
  manufacturer: Worcester
  model: Greenstar 30CDi Conventional natural gas
  room: bathroom
  year_of_purchase: 2011
  fuel: natural gas
  subtype: regular
  part_number: 41-311-71
  efficiency_rating: 
    certification_name: SEDBUK
    rating: A
  nominal_consumption:
    on_power: 70


Schema details
==============

Below is a UML Class Diagram
showing all the classes and the relationships between classes:

.. image:: schema.svg

(Please see the :doc:`manual` for more background about the NILM
Metadata schema)

Below we describe all the classes and their attributes and possible values.

ApplianceType
-------------

Has many of the attributes that :ref:`appliance-schema` has, with the addition
of:

:distributions: (dict) Distribution of random variables.

   :on_power: (array of priors, see below) bin_edges in units of watts
   :on_duration: (array of priors, see below) bin_edges in units of seconds
   :off_duration: (array of priors, see below) bin_edges in units of seconds
   :usage_hour_per_day: (array of priors, see below) bin_edges = [0,1,2,...,24]
   :usage_day_per_week: (array of priors, see below) categories =
                        ['mon', 'tue', ..., 'sun']
   :usage_month_per_year: (array of priors, see below) bin_edges are
                          in units of days (we need bin edges because
                          months are not equal lengths).  The first
                          bin represents January.
   :rooms: (array of priors, see below) Categorical distribution over
           the rooms where this appliance is likely to be
           used. e.g. for a fridge this might be 'kitchen:0.9,
           garage:0.1'.  Please use the standard room names defined in
           room.json (category names in distributions are not
           automatically validated).
   :subtypes: (array of priors, see below) Categorical distribution
              over the subtypes.
   :appliance_correlations: (array of priors, see below) list of other
                            appliances. Probability of this appliance
                            being on given that the other appliance is
                            on. e.g. 'tv:0.1, amp:0.4, ...' means that
                            there is a 10% probability of this
                            appliance being on if the TV is on.  Each
                            category name can either be just an
                            appliance name (e.g. 'fridge') or
                            <appliance name>,<appliance instance>
                            e.g. 'fridge,1'
   :ownership_per_country: (array of priors, see below) Probability of
                           this appliance being owned by a household
                           in each country (i.e. a categorical
                           distribution where categories are standard
                           two-letter country code defined by ISO
                           3166-1 alpha-2. e.g. 'GB' or 'US'.
                           http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2). If
                           the probability refers to the entire globe
                           then use 'GLOBAL' as the country code.
   :ownership_per_continent: (array of priors, see below) Probability
                             of this appliance being owned by a
                             household in each country (i.e. a
                             categorical distribution where categories
                             are standard two-letter continent code
                             defined at
                             http://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_by_continent_%28data_file%29

Country
-------

One large dict specifying country-specific information.

Each key is a 'country' (string). Please use a
standard two-letter country code defined by `ISO 3166-1 alpha-2
<http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>`_. e.g. 'GB' or
'US'.

Each value is a dict with the following attributes:

:mains_voltage: (dict):

   :nominal: (number) (required) volts
   :upper_limit: (number) volts
   :lower_limit: (number) volts

.. _prior-schema:

Priors
------

Represent prior knowledge. For continuous variables, specify either
the distribution of data (i.e. the data represented in a histogram),
or a density estimate (a model fitted to the data), or both.  For
categorical variables, specify the categorical distribution.

:distribution_of_data: (dict) Distribution of the data expressed as
                       normalised frequencies per discrete bin (for
                       continuous variables) or per category (for
                       categorical variables).  'categories' can be
                       used instead of 'bin_edges' for continuous
                       variables where it makes sense; e.g. where each
                       bin represents a day of the week

  :bin_edges: (list of numbers of list of strings) (required) \|bin_edges\| ==
              \|values\| + 1        
  :categories: (list of strings) (required) \|bin_edges\| == \|values\|
  :values: (list of numbers) (required) The normalised frequencies.
           For continuous variables, in integral over the range must
           be 1.  For categorical variables, the sum of frequences can
           be <= 1.  If < 1 then the system will assume that the
           remaining mass is distributed equaly across all other
           categories.  For example, for the probability of a fridge
           being in a specific room, it is sufficient to just state
           that the probability is 0.9 for a fridge to be in the
           kitchen.

:model: (dict) A fitted model to describe the probability density
        function (for continuous variables) or the probability mass
        function (for discrete variables).  Use additional properties
        for the relevant parameters, written as Greek letters spelt
        out in lowercase English e.g. 'mu' and 'lambda' except for
        summary stats where we use some combination of 'min', 'max',
        'mean', 'mode'.

  :distribution_name: (enum) one of {'normal', 'inverse gaussian',
                      'summary stats'}
  :sum_of_squared_error: (number)

:n_datapoints: (int)
:date_prepared: (string) ISO 8601 date format
:source: (enum) one of {'subjective', 'empirical from data',
         'empirical from publication'}. What is the source of this
         prior?  If from publication then use ``related_documents`` to
         provide references.  If from data then provide details using
         the ``software`` and ``training_data`` properties.
:related_documents: (list of strings) If 'source==empirical from
                    publication' then enter the reference(s) here.
:software: (string) the software used to generate the prior from data.
:specific_to": (dict):

  :country: (string) standard two-letter country code defined by 
            `ISO 3166-1 alpha-2
            <http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>`_
            e.g. 'GB' or 'US'.
  :continent: (string) standard 
              `two-letter continent code defined on WikiPedia
              <http://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_by_continent_%28data_file%29>`_
:distance: (int) this is filled in by the
           ``concatenate_complete_object`` function and reports the
           distance (in numbers of generations) between this prior and
           the most-derived object.  In other words, the larger this
           number, the less specific to the object this prior is.  If
           this is not set the the prior applies to the current
           object.
:description: (string)
:training_data: (array of dicts).  Each element is a dict with these properties:

  :dataset: (string) Short name of dataset
  :buildings: (list of dicts):

    :building_id: (int)
    :dates: (list of :ref:`interval-schema` objects)
    :country: (string) standard two-letter country code defined by 
            `ISO 3166-1 alpha-2
            <http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>`_
            e.g. 'GB' or 'US'.

ApplianceModel
--------------

This is not especially well defined yet. Just an initial sketch.  The
basic idea is that we would be able to specify models for each
appliance type.

:appliance_type: (string) Reference to the specific `ApplianceType`_
                 that we are modelling.
:model_type: (enum) one of {'HMM', 'FHMM', 'gubernatorial
             optimisation'}
:parameters: (dict) Parameters specific to each model type.

ApplianceModel re-uses several properties from :ref:`prior-schema` :

* training_data
* specific_to
* software
* related_documents
* date_prepared
* description