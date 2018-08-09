# Copyright 2015 Google Inc
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

# Explanation:
# https://cloud.google.com/appengine/docs/standard/python/tools/localunittesting

# Code:
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/standard/localtesting/datastore_test.py

# [START imports]
import unittest
import logging as log
#import coloredlogs

from config import config

## Logging Setup
#FORMAT = '%(asctime)-15s %(filename)s %(lineno)d: %(message)s'
#coloredlogs.install(fmt=FORMAT,level=log.DEBUG)


from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
# [END imports]

from LionHouse_models import User

# [START datastore_example_1]
class TestModel(ndb.Model):
    """A model class used for testing."""
    number = ndb.IntegerProperty(default=42)
    text = ndb.StringProperty()


class TestEntityGroupRoot(ndb.Model):
    """Entity group root"""
    pass


def GetEntityViaMemcache(entity_key):
    """Get entity from memcache if available, from datastore if not."""
    entity = memcache.get(entity_key)
    if entity is not None:
        return entity
    key = ndb.Key(urlsafe=entity_key)
    entity = key.get()
    if entity is not None:
        memcache.set(entity_key, entity)
    return entity
# [END datastore_example_1]


# [START datastore_example_test]
class DatastoreTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

# [END datastore_example_test]

    # [START datastore_example_teardown]
    def tearDown(self):
        self.testbed.deactivate()
    # [END datastore_example_teardown]

    # [START datastore_example_insert]
    def testInsertEntity(self):
        User(name = "Test Name", username = "Test Username", email = "test@email.com").put()
        self.assertEqual(1, len(User.query().fetch(2)))
    # [END datastore_example_insert]

    def testGetEntity(self):
        #self.assertEqual(1, len(User.query().filter(User.name == "Test Name").get()))
        print(User.query().filter(User.name == "Test Name").get())
        print("HELLO")
        log.info("HELLO")


# [START main]
if __name__ == '__main__':
    unittest.main()
# [END main]
