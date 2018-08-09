#!/usr/bin/env python

from config import config

import logging as log

from pprint import pprint
from pprint import pformat

from LionHouse_models import Post, User

log.info(pformat(config))

def fetch_posts():
  return Post.query().fetch()

posts = fetch_posts()
#log.info(pformat(posts))
