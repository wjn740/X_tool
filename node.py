#!/usr/bin/python

from collections import OrderedDict

import statistics


def build_statistic_data(a_list):
    '''
    The data looks like:
    #data = {
    #        'adfas': [123,123,123,123,123],
    #        'axxxdfas': [123,123,123,123,123],
    #        'a234s': [123,123,123,123,123],
    #        'ad__s': [123,123,123,123,123],
    #        }
    '''
    data = OrderedDict()
    for l in a_list:
        data[l.name] = l.values()
    return data

class statistics_node():
    """this class will make a statistics node for the list, the list will be use for statistics table"""
    def __init__(self, _list):
        try:
            self.name = "/".join([_list[0].product, _list[0].release, _list[0].kernel_long_version])
        except IndexError as err:
            return


        self.data = _list
        self.benchmarks = OrderedDict()
        self.benchmarks_init()
        #self.print_benchmarks()

    def benchmarks_init(self):
        """
        benchmarks attribute looks like:
        benchmarks = {
            'random write' : {
                              'mean': value,
                              'sum' : value,
                              'max' : value,
                              'min' : value,
                              'stddev' : value,
                              'count' : value
                              }

            'random read' : {
                              'mean': value,
                              'sum' : value,
                              'max' : value,
                              'min' : value,
                              'stddev' : value,
                              'count' : value
                              }

            }
        """
        _tmp_dict=dict()
        for tc in self.data:
            for bm in tc.benchmark:
                if bm.name in _tmp_dict:
                    _tmp_dict[bm.name].append(float(bm.value))
                else:
                    _tmp_dict[bm.name] = [float(bm.value)]

        for k, v in _tmp_dict.items():
            self.benchmarks[k]=OrderedDict()
            self.benchmarks[k]['mean']=statistics.mean(v)
            self.benchmarks[k]['sum']=sum(v)
            self.benchmarks[k]['max']=max(v)
            self.benchmarks[k]['min']=min(v)
            if len(v) >= 2:
                self.benchmarks[k]['stddev']=statistics.stdev(v)
            else:
                self.benchmarks[k]['stddev']=0
            self.benchmarks[k]['count']=len(v)


    def print_benchmarks(self):
        print(self.benchmarks)
    def __repr__(self):
        return self.name

    def values(self):
        self.indexs=list()
        values=list()
        for k,v in self.benchmarks.items():
            for k1,v1 in v.items():
                self.indexs.append(str(k)+'/'+str(k1))
                values.append(v1)

        #print(','.join(str(self.benchmarks[k] for k in self.benchmarks.keys())))
        return values

    def __str__(self):
        self.indexs=list()
        values=list()
        for k,v in self.benchmarks.items():
            for k1,v1 in v.items():
                self.indexs.append(str(k)+str(k1))
                values.append(v1)

        #print(','.join(str(self.benchmarks[k] for k in self.benchmarks.keys())))
        return str(values)

    def mean(self):
        pass

    def _sum(self, _list):
        pass
    def stddev(self, _list):
        pass
    def cov(self, _list):
        pass
    def _min(self, _list):
        pass
    def _max(self, _list):
        pass
