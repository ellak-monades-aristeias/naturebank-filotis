naturenank-filotis
====================

Version 1.0 (2015-10-01)

naturenank-filotis is a Database for the Natural Environment of Greece,
powered by [NatureBank](https://github.com/ellak-monades-aristeias/naturebank),


Requirements
------------
 * Python v.2.7
 * PostreSQL v.9.0
 * PostGIS v.2.1

Additional requirements related with Django and its applications are
documented in file requirements.txt.
NatureBank has been successfully tested with PostreSQL v.9.0,
spatially enabled with PostGIS v.2.1. Other versions of the above
software or other spatially enabled databases may work as well.


Installation
------------

(to be completed)

#### Install Python, PostreSQL and PostGIS
#### Install Django and dependencies
#### Create a database user
#### Create a spatially enabled database

`createdb filotis -U postgres -W -h localhost -O filotis
     -T template_postgis`

#### Populate the database

`pg_restore -i -h localhost -U postgres -d filotis -v
     <path>/db/filotis.dump`

#### Create the configuration file

Copy file /naturebank_project/settings/local-example.py to
/naturebank_project/settings/local.py making the appropriate adjustments.

#### Configure your web server


License
-------
    naturenank-filotis is a database for the Natural Environment of Greece.
    Copyright (C) 2005-2015 National Technical University of Athens

    naturenank-filotis is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public
    License along with this program. If not, see
    <http://www.gnu.org/licenses/>.

naturenank-filotis is powered by NatureBank, which is
Copyright (C) 2005-2015 National Technical University of Athens.

All additional 3rd party software provided with this release and/or used
by naturenank-filotis are AGPLv3 compatible as their licenses ensure the
freedoms to run, study, share (copy), and modify the software. Additionally,
some of them are copylefted.


Acknowledgements
----------------
naturenank-filotis is based on Filotis, a database for the natural environment
of Greece, developed between 2005-2015 by the National Technical University
of Athens. Main authors of Filotis are Anthony Christophides and Stefanos
Kozanis. Theodore Kargas was the main author of the initial version of Filotis.
