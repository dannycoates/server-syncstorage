# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from webtest import TestApp

from syncstorage.storage import get_storage
from syncstorage.tests.support import StorageTestCase


class TestWSGIApp(StorageTestCase):

    TEST_INI_FILE = "tests-hostname.ini"

    def test_host_specific_config(self):
        req = self.make_request(environ={"HTTP_HOST": "localhost"})
        sqluri = get_storage(req).sqluri
        self.assertEquals(sqluri, "sqlite:///:memory:")

        req = self.make_request(environ={"HTTP_HOST": "some-test-host"})
        sqluri = get_storage(req).sqluri
        self.assertTrue(sqluri.startswith("sqlite:////tmp/some-test-host-"))

        req = self.make_request(environ={"HTTP_HOST": "some-test-host:8000"})
        sqluri = get_storage(req).sqluri
        self.assertTrue(sqluri.startswith("sqlite:////tmp/some-test-host-"))

        req = self.make_request(environ={"HTTP_HOST": "another-test-host"})
        sqluri = get_storage(req).sqluri
        self.assertTrue(sqluri.startswith("sqlite:////tmp/another-test-host-"))

    def test_the_it_works_page(self):
        app = TestApp(self.config.make_wsgi_app())
        r = app.get("/")
        self.assertTrue("It Works!" in r.body)
