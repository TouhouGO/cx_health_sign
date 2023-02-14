# -*- coding: utf8 -*-
from config import _Report


class QCUWHHealthReport(_Report):
    """
    QCUWH Health Report
    该脚本由他人贡献，本人未充分测试，不保证其可用性
    """
    def __init__(self, username, password, school_id=''):
        _Report.__init__(self, username, password, school_id)

        self._form_id = '7185'
        self._enc = 'f837c93e0de9d9ad82db707b2c27241e'
        self._reporter_name = 'QCUWH健康表单'

        self._temperature_ids = [73]
        self._options_ids = [73, 74, 62, 60, 61, 66, 67, 68]
        self._isShow_ids = [63, 61, 64, 68, 69]
        self._day_id = -1
        self._report_time_id = -1
        self._hasAuthority_ids = []

        """
        56:三针是否龙泉卫生院接种
        57:两针
        58:一针
        同时只出现在一个，val可能不存在
        45选项为未接种原因，当有57或58时候才会显示
        """

    def _clean_form_data(self):
        form_data = self._last_form_data
        for f in form_data:
            if f['id'] == self._day_id:
                # 打卡日期
                today = self._t.today
                if f['fields'][0]['values'][0]['val'] == today:
                    # 如果获取到上次的打卡时间是今天的，则不需要再次填报
                    self._result = '%s今日%s已填报过%s' % (self._username_masked, today, self._reporter_name)
                    raise Exception(self._result)
                else:
                    f['fields'][0]['values'][0]['val'] = today
            elif f['id'] == self._report_time_id:
                # 打卡时间
                today = self._t.today
                report_time = self._t.report_time
                if f['fields'][0]['values'][0]['val'].startswith(today):
                    # 同上
                    self._result = '%s今日%s已填报过%s' % (self._username_masked, today, self._reporter_name)
                    raise Exception(self._result)
                else:
                    f['fields'][0]['values'][0]['val'] = report_time
            elif f['id'] in self._temperature_ids and f['id'] not in self._options_ids:
                # 体温
                temperature = self._random_temperature()
                f['fields'][0]['values'][0]['val'] = temperature
            elif f['id'] in self._options_ids and f['id'] not in self._isShow_ids:
                # 下拉项选择改写为 true
                for option in f['fields'][0]['options']:
                    if f['fields'][0]['values'][0]['val'] == option['title']:
                        option['checked'] = True
            elif f['id'] in self._hasAuthority_ids:
                # 内部使用的id
                f['hasAuthority'] = False
            elif f['id'] in self._isShow_ids:
                # 内部使用的id
                f['isShow'] = False

        self._today_form_data = form_data
        return form_data
