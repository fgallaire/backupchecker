# -*- coding: utf-8 -*-
# Copyright © 2011 Carl Chenet <chaica@ohmytux.com>
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



from brebis.generatelist import GenerateList

# Generate a list of files from a tree
'''Generate a list of files from a tree'''

class GenerateListForTree(GenerateList):
    '''Generate a list of files from a tree'''

    def __init__(self, __arcpath):
        '''The constructor for the GenerateListForTree class'''
        __listoffiles = ['[files]\n']
        __oneline = '{}: size:{} uid:{} gid:{} mode:{} type:{}\n'
        
        for __dirpath, __dirnames, __filenames, in os.walk(__arcpath):
            __dirinfo = os.lstat(__dirpath)
            __dirmode = stat.S_IMODE(__dirinfo.st_mode)
            # Translate file type in brebis intern file type
            __type = self.__translate_type(__dirinfo.st_mode)
            # Extract file data
            __listoffiles.append(__oneline.format(os.path.relpath(__dirpath, __arcpath),
                                                    str(__dirinfo.st_size),
                                                    str(__dirinfo.st_uid),
                                                    str(__dirinfo.st_gid),
                                                    __dirmode,
                                                    __type))
            for __filename in __filenames:
                __filepath = os.path.join(__dirpath, __filename)
                __filepath = self._normalize_path(__filepath)
                __fileinfo = os.lstat(__filepath)
                __filemode = stat.S_IMODE(__fileinfo.st_mode)
                __type = self.__translate_type(__fileinfo.st_mode)
            # Extract file data
            __listoffiles.append(__oneline.format(os.path.relpath(__filepath, __arcpath),
                                                    str(__fileinfo.st_size),
                                                    str(__fileinfo.st_uid),
                                                    str(__fileinfo.st_gid),
                                                    __filemode,
                                                    __type))
        # call the method to write information in a file
        self._generate_list(__arcpath, __listoffiles)

    def __translate_type(self, __mode):
        '''Translate the type of the file to a generic name'''
        if stat.S_ISREG(__mode):
            return 'f'
        elif stat.S_ISDIR(__mode):
            return 'd'
        elif stat.S_ISCHR(__mode):
            return 'c'
        elif stat.S_ISLNK(__mode):
            return 's' 
        elif stat.S_BLK(__mode):
            return 'b'
        elif stat.S_ISSOCK(__mode):
            return 'k'
        elif stat.S_ISFIFO(__mode):
            return 'o'
        pass
