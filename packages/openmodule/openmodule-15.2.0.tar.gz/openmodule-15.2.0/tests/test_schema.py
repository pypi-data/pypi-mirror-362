import json
import os
from functools import partial
from unittest import TestCase

from openmodule.config import override_context
from openmodule.health import HealthPongMessage
from openmodule.models.access_service import AccessCheckRequest, AccessCheckResponse
from openmodule.rpc.server import RPCServer
from openmodule.utils.schema import Schema
from openmodule_test.core import OpenModuleCoreTestMixin
from openmodule_test.rpc import RPCServerTestMixin

file_name = "../schemas.json"


def test(*args, **kwargs):
    """
    Test
    """
    return None


def test2(*args, **kwargs):
    """
    Test
    """
    return None


def test1(*args, **kwargs):
    return None


def test3(*args, **kwargs):
    return None


class SchemaTest(TestCase):
    def tearDown(self) -> None:
        super().setUp()
        try:
            os.remove(file_name)
        except:
            pass
        Schema.clear()
        super().tearDown()

    def setUp(self) -> None:
        super().setUp()
        os.environ["TESTING"] = "True"
        try:
            os.remove(file_name)
        except:
            pass
        Schema.clear()

    def test_models(self):
        Schema.save_model(AccessCheckRequest)
        schema = Schema.render_schema()
        length = len(schema["components"]["schemas"])
        self.assertEqual(1, len(Schema.models))
        self.assertIn("AccessCheckRequest", schema["components"]["schemas"])
        self.assertEqual(None, schema.get("paths"))

        # same model
        Schema.save_model(AccessCheckRequest)
        schema = Schema.render_schema()
        self.assertEqual(1, len(Schema.models))
        self.assertIn("AccessCheckRequest", schema["components"]["schemas"])
        self.assertEqual(None, schema.get("paths"))
        self.assertEqual(length, len(schema["components"]["schemas"]))

        Schema.save_model(AccessCheckResponse)
        schema1 = Schema.render_schema()
        self.assertEqual(2, len(Schema.models))
        self.assertIn("AccessCheckRequest", schema["components"]["schemas"])
        self.assertIn("AccessCheckResponse", schema1["components"]["schemas"])
        self.assertGreaterEqual(len(schema1["components"]["schemas"]), length)

    def test_rpcs(self):
        Schema.save_rpc("access_service", "auth", AccessCheckRequest, AccessCheckResponse, test)
        self.assertEqual(1, len(Schema.rpcs))

        schema = Schema.render_schema()
        self.assertIn("/access_service/auth", schema["paths"])
        self.assertEqual(len(schema["paths"]), 1)

        Schema.save_rpc("access_service", "auth", AccessCheckRequest, AccessCheckResponse, test)
        schema = Schema.render_schema()
        self.assertIn("/access_service/auth", schema["paths"])
        self.assertEqual(1, len(Schema.rpcs))
        self.assertEqual(len(schema["paths"]), 1)

        Schema.save_rpc("access_service", "abc", AccessCheckRequest, AccessCheckResponse, test)
        schema = Schema.render_schema()
        self.assertIn("/access_service/abc", schema["paths"])
        self.assertIn("/access_service/auth", schema["paths"])
        self.assertEqual(2, len(Schema.rpcs))
        self.assertEqual(len(schema["paths"]), 2)

    def test_messages(self):
        Schema.save_message("message_topic", AccessCheckRequest, test)
        self.assertEqual(1, len(Schema.messages))
        schema = Schema.render_schema()
        self.assertIn("/message_topic/test", schema["paths"])
        self.assertEqual(len(schema["paths"]), 1)

        Schema.save_message("message_topic", AccessCheckRequest, test)
        self.assertEqual(1, len(Schema.messages))
        schema = Schema.render_schema()
        self.assertIn("/message_topic/test", schema["paths"])
        self.assertEqual(len(schema["paths"]), 1)

        with self.assertRaises(AssertionError):
            Schema.save_message("message_topic", AccessCheckRequest, test1)

        Schema.save_message("message_topic", AccessCheckRequest, test2)
        schema = Schema.render_schema()
        self.assertIn("/message_topic/test", schema["paths"])
        self.assertIn("/message_topic/test2", schema["paths"])
        self.assertEqual(2, len(schema["paths"]))
        self.assertEqual(2, len(Schema.messages))

    def test_message_filters(self):
        Schema.save_message("message_topic", AccessCheckRequest, test, {"a": 1})
        Schema.save_message("message_topic", AccessCheckRequest, test, {"a": 2})
        self.assertEqual(1, len(Schema.messages))
        self.assertEqual(2, len(Schema.messages["/message_topic/test"]))

        schema = Schema.render_messages()
        self.assertIn("/message_topic/test - 2", schema)
        self.assertIn("/message_topic/test - 2", schema)

    def test_file(self):
        def get_file_data():
            with open(file_name, "r") as file:
                return json.loads(file.read())

        Schema.to_file(file_name)
        with self.assertRaises(FileNotFoundError):
            data = get_file_data()

        Schema.save_rpc("access_service", "auth", AccessCheckRequest, AccessCheckResponse, test)
        Schema.to_file(file_name)
        data = get_file_data()
        self.assertEqual(1, len(data["paths"]))

        Schema.save_rpc("access_service", "auth", AccessCheckRequest, AccessCheckResponse, test)
        Schema.to_file(file_name)
        data = get_file_data()
        self.assertEqual(1, len(data["paths"]))

        Schema.save_rpc("access_service", "abc", AccessCheckRequest, AccessCheckResponse, test)
        Schema.to_file(file_name)
        data = get_file_data()
        self.assertEqual(2, len(data["paths"]))

        # add empty Schema
        Schema.clear()
        Schema.to_file(file_name)
        data = get_file_data()

        self.assertEqual(2, len(data["paths"]))
        self.assertGreaterEqual(len(data["components"]["schemas"]), 2)
        data = get_file_data()
        self.assertEqual(2, len(data["paths"]))
        self.assertGreaterEqual(len(data["components"]["schemas"]), 2)

    def test_clear(self):
        self.assertEqual(0, len(Schema.models))
        self.assertEqual(0, len(Schema.rpcs))
        Schema.save_rpc("access_service", "auth", AccessCheckRequest, AccessCheckResponse, test)

        self.assertEqual(2, len(Schema.models))
        self.assertEqual(1, len(Schema.rpcs))

        Schema.clear()
        self.assertEqual(0, len(Schema.models))
        self.assertEqual(0, len(Schema.rpcs))

    def test_rpc_doc(self):
        with self.assertRaises(AssertionError):
            Schema.save_rpc("access_service", "auth", AccessCheckRequest, AccessCheckResponse, test1)
        Schema.save_rpc("access_service", "auth", AccessCheckRequest, AccessCheckResponse, test1, False)

    def test_partial_functions(self):
        func = partial(test, x=1)
        Schema.save_message("message_topic", AccessCheckRequest, func)
        self.assertIn("/message_topic/test", Schema.render_messages())

    def test_save(self):
        Schema.save_rpc("access_service", "abc", AccessCheckRequest, AccessCheckRequest, test)
        Schema.save_message("abc", AccessCheckRequest, test)
        self.assertEqual(1, len(Schema.messages))
        self.assertEqual(1, len(Schema.rpcs))
        num_models = len(Schema.models)

        with override_context(TESTING=False):
            Schema.save_rpc("access_service", "abc", AccessCheckRequest, AccessCheckResponse, test)
            Schema.save_message("abc", AccessCheckRequest, test)
            self.assertEqual(1, len(Schema.messages))
            self.assertEqual(1, len(Schema.rpcs))
            self.assertEqual(num_models, len(Schema.models))


class LiveTest(RPCServerTestMixin, OpenModuleCoreTestMixin):
    rpc_channels = ["access_service"]
    topics = ["access_service"]

    def setUp(self):
        super().setUp()
        try:
            os.remove(file_name)
        except:
            pass
        Schema.clear()
        self.server = RPCServer(context=self.zmq_context())
        self.server.run_as_thread()

    def tearDown(self) -> None:
        super().tearDown()
        try:
            os.remove(file_name)
        except:
            pass
        Schema.clear()

    def test_save(self):
        self.server.register_handler("session", "start", AccessCheckRequest, AccessCheckResponse, test)
        self.core.messages.register_handler("io", HealthPongMessage, test)
        self.wait_for_rpc_server(self.server)
        self.wait_for_dispatcher(self.core.messages)
        self.assertEqual(1, len(Schema.messages))
        self.assertEqual(1, len(Schema.rpcs))

        self.server.register_handler("access_service", "abc", AccessCheckRequest, AccessCheckResponse, test3,
                                     register_schema=False)
        self.core.messages.register_handler("abc", HealthPongMessage, test3, register_schema=False)
        self.wait_for_rpc_server(self.server)
        self.wait_for_dispatcher(self.core.messages)
        self.assertEqual(1, len(Schema.messages))
        self.assertEqual(1, len(Schema.rpcs))
