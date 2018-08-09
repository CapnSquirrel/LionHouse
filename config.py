#!/usr/bin/env python
  
## Logging
import logging as log
import coloredlogs

## Logging Setup
FORMAT = '%(asctime)-15s %(filename)s %(lineno)d: %(message)s'
coloredlogs.install(fmt=FORMAT,level=log.DEBUG)

## Pretty Printing
from pprint import pprint
from pprint import pformat

## Environment variables
import os
PROJECT_HOME = os.environ['PROJECT_HOME']

config = {
  "blah": "blah"
}

