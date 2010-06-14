# -*- coding: utf-8 -*-
# Copyright © 2009 Carl Chenet <chaica@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Check a database
'''Check a database'''

import logging

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import OperationalError, ProgrammingError, NoSuchTableError
import sqlalchemy

from expecteddbobjects import ExpectedDbObjects

class CheckDb(object):
    '''Check a database'''

    def __init__(self, __cfgvalues):
        self.__main(__cfgvalues)

    def __main(self, __cfgvalues):
        '''The main for the CheckDb class'''
        __db_objects = ExpectedDbObjects(__cfgvalues['dbobjects']).db_objects
        # sqlite connection
        if __cfgvalues['dbtype'] == 'sqlite':
            __engine = create_engine(''.join([__cfgvalues['dbtype'], ':///', __cfgvalues['dbpath']]))
        # mysql connection
        elif __cfgvalues['dbtype'] == 'mysql':
            __engine = create_engine(''.join([__cfgvalues['dbtype'], '+mysqlconnector://', __cfgvalues['dbuser'], ':', __cfgvalues['dbpass'], '@', __cfgvalues['dbhost'], '/', __cfgvalues['dbname']]))
        # postgresql connection
        elif __cfgvalues['dbtype'] == 'postgresql':
            __engine = create_engine(''.join([__cfgvalues['dbtype'], '+pg8000://', __cfgvalues['dbuser'], ':', __cfgvalues['dbpass'], '@', __cfgvalues['dbhost'], '/', __cfgvalues['dbname']]))
        __metadata = MetaData()
        try:
            for __db_object in __db_objects:
                __key, __value = __db_object, __db_objects[__db_object]
                for __element in __value:
                    __db_backtrace = getattr(sqlalchemy, ''.join([__key[0].upper(),__key[1:-1]]))(__element, __metadata, autoload=True, autoload_with=__engine)
        except (OperationalError, ProgrammingError) as __err:
            logging.warn('The following error occured: {}'.format(__err))
        except NoSuchTableError as __err:
            if __cfgvalues['dbtype'] == 'sqlite':
                logging.warn('The following table was not found in {}: {}'.format(__cfgvalues['dbpath'], __err))
            else:
                logging.warn('The following table was not found in the {} database: {}'.format(__cfgvalues['dbname'], __err))
