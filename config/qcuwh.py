# -*- coding: utf8 -*-
from config import _Report


class QCUWHHealthReport(_Report):
    """
    2023/2/13
    
    """
    def __init__(self, username, password, school_id=''):
        _Report.__init__(self, username, password, school_id)

        self._form_id = '7185'
        self._enc = 'f837c93e0de9d9ad82db707b2c27241e'
        self._reporter_name = 'QCUWH健康表单'

        self._day_id = -1
        self._report_time_id = -1
        self._temperature_ids = []
        self._options_ids = [74]
        self._hasAuthority_ids = []
        self._isShow_ids = [63]



    def _clean_form_data(self):
        form_data = self._last_form_data
        for f in form_data:
            if f['id'] in self._options_ids:
                if not f['fields'][0]['values']:  # 没数据，不显示,处理56,57,58
                    f['isShow'] = False
                else:
                    # 下拉项选择改写为 true
                    for option in f['fields'][0]['options']:
                        if f['fields'][0]['values'][0]['val'] == option['title']:
                            option['checked'] = True
            elif f['id'] in self._isShow:
                f['isShow'] = False
            elif f['id'] in self._hasAuthority_ids:
                f['hasAuthority'] = False
            # 这个是文本填写,处理45
            elif f['id'] in self._edittext_area:
                if not f['fields'][0]['values']:  # 没数据，不显示
                    f['isShow'] = False

        self._today_form_data = form_data
        return form_data
