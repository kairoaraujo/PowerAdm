#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
PowerAdm
cachefile.py

Copyright (c) 2015 Kairo Araujo

It was created for personal use. There are no guarantees of the author.
Use at your own risk.

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

IBM, Power, PowerVM (a.k.a. VIOS) are registered trademarks of IBM Corporation in
the United States, other countries, or both.
VMware, vCenter, vCenter Orchestrator are registered trademarks of VWware Inc in the United
States, other countries, or both.
'''

# Imports
###############################################################################################
import os
import time
###############################################################################################

class CacheFile():
    '''It's is a simple cache file.

       Attributes:
       filename         the file you want store
       time_refresh     time of the refresh in seconds
       cmd_update       the output you want store in the cache file
       return_type      t_return to return and t_print to print

       Sample to use:

       def lsnports_cmd():
           lsnports_data = commands.getoutput('ssh -l xxxx command_foo_bar')

       lsnports = cachefile.CacheFile('lsnports.cache', '600', lsnports_cmd, 't_print')
       lsnports.cache()
    '''

    def __init__(self, filename, time_refresh, cmd_update, return_type):
        self.filename = filename
        self.time_refresh = int(time_refresh)
        self.cmd_update = cmd_update
        self.return_type = return_type

    def cache(self):
        ''' Main of Class CacheFile.
            It's get the cache or update if cache don't exists or depracieted
        '''

        def cacheUpdate():
            ''' Update the file cache '''

            global text_file
            self.cmd_update
            text_file = open(self.filename, 'w')
            text_file.write('%s ' % self.cmd_update())
            text_file.close()

        def readCache():
            ''' Read the file cache content '''

            with open(self.filename, 'r') as content_file:
                content = content_file.read()
            if self.return_type == 't_print':
                print content
            elif self.return_type == 't_return':
                return content
            else:
                print 'Return type error'


        # verify if cache file exists
        if os.path.isfile(self.filename):

            if (time.time() - os.path.getmtime(self.filename)) > self.time_refresh:
                # if time to refresh is > then file it'll be updated
                cacheUpdate()
                return readCache()

            else:
                # if time to refresh is < just use the file
                return readCache()

        # if file don't exists the file is created
        else:
            cacheUpdate()
            return readCache()

