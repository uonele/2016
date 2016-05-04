# -*- coding: utf-8 -*-
import abc

class Abstractimport():
    __metaclass__ = abc.ABCMeta
    #导入数据前的准备工作
    def data_prepare(self, filename, _filename):
        return