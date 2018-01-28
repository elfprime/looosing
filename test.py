# coding=utf-8
import Utils as ut
from pandas import ExcelWriter

file = ExcelWriter('perf.xlsx')
a = ut.getPerf(['2017-01-03', '2018-01-02'])
a.to_excel(file)
