#!/usr/bin/python2.7
#
# Copyright 
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from pprint import pprint
import socket
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from splunklib.client import connect
import splunklib.results as results
from Crypto.Cipher import *
import base64
import ConfigParser
#import encrypt

try:
    import utils
except ImportError:
    raise Exception("Add the SDK repository to your PYTHONPATH")

def splunkreader(response,metric):
    #print (response)
    reader = results.ResultsReader(response)
    la = open (metric+'.csv', 'w')
    for result in reader:
          #print(result)
          if len(result.keys()) == 2:
	           la.write(result['query']+';@'+result[metric])
          la.write('\n')
    print (metric+'.csv is complete')
    la.close()	    

def getEncryptionPassphrase(fn):
    f=open(fn)
    passphrase=f.readline()[:64]
    f.close()
    return passphrase

def getEncryptionIV(fn):
    f=open(fn)
    iv=f.readline()[-16:]
    f.close()
    return iv


def main():
 
    username = base64.b64decode('cmR1cmJoYQ==')
    password = base64.b64decode('Uk9tdWxhbjEyIUA=')
    connect_string=['--username=rdurbha', '--host=splunk.sciquest.com', '--password=FErengi12!@']
    kwargs_oneshot = { 
                      "earliest_time": "-60m",
                      "count":0
                     }
    usage = "usage: oneshot.py <search>"
    opts = utils.parse(connect_string[0:], {}, ".splunkrc", usage=usage)
    service = connect(**opts.kwargs)
    

    #searchquery = "search index=db2 sourcetype=*dyn* source=*trans* host=extractor* |eval exec_time= stmt_exec_time/num_executions | rex field=stmt_text \"(?<workload_type>[^( ]+)\" | table stmt_exec_time"
    #response = service.jobs.oneshot(searchquery, **kwargs_oneshot)
    #print (response) 
    #splunkreader(response,'exec_time')

    searchquery = "search index=db2 sourcetype=*dyn* source=*trans* host=extractor* | eval exec_time= stmt_exec_time/num_executions|rex \"stmt_text=(?<query>[^\n]+)\" | table query,exec_time"
    response = service.jobs.oneshot(searchquery, **kwargs_oneshot)
    #print (response) 
    splunkreader(response,'exec_time')

    

if __name__ == "__main__":
    main()
