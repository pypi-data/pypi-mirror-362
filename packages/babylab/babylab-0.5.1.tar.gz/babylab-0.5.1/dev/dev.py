"""
Fixtures for testing.
"""

from babylab import api
from tests import conftest


token = conftest.get_api_key()
records = api.Records(token=token)
data_dict = api.get_data_dict(token=token)
ppt = conftest.create_record_ppt()
apt = conftest.create_record_apt()
que = conftest.create_record_que()
ppt_finput = conftest.create_finput_ppt()
apt_finput = conftest.create_finput_apt()
que_finput = conftest.create_finput_que()
