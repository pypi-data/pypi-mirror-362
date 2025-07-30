import unittest
from dotenv import load_dotenv
from msfabricpysdkcore import FabricClientCore
from datetime import datetime
load_dotenv()

class TestFabricClientCore(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFabricClientCore, self).__init__(*args, **kwargs)
        self.fcc = FabricClientCore()
                  
    def test_sql_endpoint(self):
        fcc = self.fcc

        workspace_id = "05bc5baa-ef02-4a31-ab20-158a478151d3"
        item_id = "d21012a1-f306-4cf1-a21b-f8ae55c17642"

        response = fcc.refresh_sql_endpoint_metadata(workspace_id=workspace_id, sql_endpoint_id=item_id, wait_for_completion=False)
        self.assertIn(response.status_code, [200, 202])








