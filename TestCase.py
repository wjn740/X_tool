#!/usr/bin/python

import urllib.request

import re

import io

from benchmark import benchmark

class TestCase():
    def __init__(self, submission_id="", arch="", product="", release="", host="", log_url="", testsuite="", test_time="", testcase="", kernel_version=""):
        self.submission_id=submission_id
        self.arch = arch
        self.product = product
        self.release = release
        self.host = host
        self.log_url = log_url
        self.testsuite = testsuite
        self.test_time = test_time
        self.testcase = testcase
        self.kernel_version = kernel_version
        self.kernel_long_version = self.read_kernel_long_version()
        self.testcase_benchmark()



    def __repr__(self):
        return "<"+self.testcase+">"

    def read_testcase(self):
        f = urllib.request.urlopen(self.log_url+"/"+self.testcase)
        for line in f:
            print(line)

    def testcase_benchmark(self):
        """
        The following functions will call corresponding constructor function.
        These functions will add a benchmark attribute to TestCase object.
        The benchmark attribute is a set of benchmark objects. each benchmark
        object indicate represents a checkpoint. for instance, "random read",
        "sequnce write".
        """
        f = urllib.request.urlopen(self.log_url+"/"+self.testcase)
        if self.testcase == 'reaim-ioperf':
            self.benchmark_reaim_ioperf()
            return
        if self.testcase == 'sysbench-cpu':
            return
        if self.testcase == 'sysbench-threads':
            return
        if self.testcase == 'sysbench-memory':
            return
        if self.testcase == 'sysbench-mutex':
            return
        if self.testcase == 'sysbench-oltp':
            return
        if self.testcase == 'tiobench-doublemem-async':
            return
        if self.testcase == 'bonnie++-async':
            self.benchmark_bonniepp()
            return
        if self.testcase == 'bonnie++-fsync':
            self.benchmark_bonniepp()
            return
            return
        if self.testcase == 'dbench4-async':
            return
        if self.testcase == 'dbench4-fsync':
            return
        if self.testcase == 'kernbench':
            self.benchmark_kernbench()
            return
        if self.testcase == 'libmicro-contextswitch':
            return
        if self.testcase == 'libmicro-file':
            return
        if self.testcase == 'libmicro-memory':
            return
        if self.testcase == 'libmicro-process':
            return
        if self.testcase == 'libmicro-regular':
            return
        if self.testcase == 'libmicro-socket':
            return
        if self.testcase == 'lmbench-bcopy':
            return
        if self.testcase == 'lmbench-ctx':
            return
        if self.testcase == 'lmbench-file':
            return
        if self.testcase == 'lmbench-local':
            return
        if self.testcase == 'lmbench-mem':
            return
        if self.testcase == 'lmbench-ops':
            return
        if self.testcase == 'lmbench-syscall':
            return
        if self.testcase == 'netperf-fiber-tcp':
            return
        if self.testcase == 'netperf-fiber-udp':
            return
        if self.testcase == 'netperf-fiber-tcp6':
            return
        if self.testcase == 'netperf-fiber-udp6':
            return
        if self.testcase == 'netperf-loop-tcp':
            return
        if self.testcase == 'netserver-start':
            return
        if self.testcase == 'netperf-loop-udp':
            return
        if self.testcase == 'pgbench-small-ro':
            return
        if self.testcase == 'pgbench-small-rw':
            return
        if self.testcase == 'iozone-doublemem-async':
            return
        if self.testcase == 'iozone-doublemem-fsync':
            return
        if self.testcase == 'qa_siege_performance':
            return


    def read_kernel_long_version(self):
        with urllib.request.urlopen(self.log_url+"/"+'kernel') as response:
            for line in response:
                line = line.decode('utf-8')
                patten=re.compile(r'(Name) *: .*(kernel)-(default)*')
                match1 = patten.match(line)
                if match1:
                    flavor=match1.group(3)
                    continue
                patten=re.compile(r'(Version) *: (.*)')
                match1 = patten.match(line)
                if match1:
                    major=match1.group(2)
                    continue
                patten=re.compile(r'(Release) *: ([0-9][0-9]*)\.([0-9]*)\.*([0-9].*)*')
                match1 = patten.match(line)
                if match1:
                    if match1.group(4):
                        minor='.'.join([match1.group(2), match1.group(3)])
                        continue
                    else:
                        minor='.'.join([match1.group(2)])
                        continue
                if flavor and major and minor:
                    break
            return "-".join([major, minor, flavor ])

    def benchmark_dbench4(self):
        self.benchmark = list()
        with urllib.request.urlopen(self.log_url+"/"+self.testcase) as page:
            g = io.BufferedReader(page)
            t = io.TextIOWrapper(g, 'utf-8')
            pattern1 = re.compile('^Throughput (\d+\.*\d*) MB/sec  (\d+\.*\d*) clients  (\d+\.*\d*) procs  max_latency=(\d+\.*\d*) ms')
            for line in t:
                m1 = pattern1.match(line)
                if m1:
                    self.benchmark.append(benchmark("{} processes Throughput(MB/sec)".format(m1.group(3)), m1.group(1), 1)
                    self.benchmark.append(benchmark("{} processes max_latency(ms)".format(m1.group(3)), m1.group(4), -1)

    def benchmark_kernbench(self):
        self.benchmark = list()
        with urllib.request.urlopen(self.log_url+"/"+self.testcase) as page:
            g = io.BufferedReader(page)
            t = io.TextIOWrapper(g, 'utf-8')
            for line in t:
                pattern1=re.compile('^Elapsed Time *(\d*)')
                pattern2=re.compile('^Context Switches *(\d*)')
                pattern3=re.compile('^Half load -j (\d*) run number')
                pattern4=re.compile('^Optimal load -j (\d*) run number')
                m1 = pattern1.match(line)
                m2 = pattern2.match(line)
                m3 = pattern3.match(line)
                m4 = pattern4.match(line)
                if m3:
                    jobs=str(m3.group(1))
                    continue
                if m4:
                    jobs=str(m4.group(1))
                    continue
                if m1:
                    #print(m1.group(1))
                    self.benchmark.append(benchmark('Jobs'+jobs+'/'+'Elapsed_Time', float(m1.group(1)), -1))
                    continue
                if m2:
                    #print(m2.group(1))
                    self.benchmark.append(benchmark('Jobs'+jobs+'/'+'Context_Switch', float(m2.group(1)), 1))
                    continue



    def benchmark_reaim_ioperf(self):
        self.benchmark = list()
        pattern=re.compile(b'Max Jobs per Minute ([0-9].*\.*[0-9]*)')
        for line in urllib.request.urlopen(self.log_url+"/"+self.testcase):
            m = pattern.match(line)
            if m:
                value=str(m.group(1), 'utf-8')
                self.benchmark.append(benchmark('Jobs_per_Minute', value, 1))
                continue

    def benchmark_netperf_tcp(self):
        """
        group(1):Recv socket size bytes
        group(2):Send socket size bytes
        group(3):Send message szie bytes
        group(4):Elapsed Time secs
        group(5):Throughput 10^6bits/sec
        """
        pattern = re.compile(" (\d+) +(\d+) +(\d+) +(\d+\.*\d*) +(\d+\.*\d*)")
        for line in sys.stdin:
            m1 = pattern.match(line)
            if m1:
                print("Throughput: {} (10^6bits/sec)".format(m1.group(5)));
                break

    def benchmark_netperf_udp(self):
        """
        Socket  Message  Elapsed      Messages
        Size    Size     Time         Okay Errors   Throughput
        bytes   bytes    secs            #      #   10^6bits/sec

        212992   65507   60.00     2133018      0    18630.23    <--------m0
        212992           60.00     1690587           14765.95    <--------m1
        """
        pattern0 = re.compile("(\d+) +(\d+) +(\d+\.*\d*) +(\d+) +(\d+) +(\d+\.*\d*)")
        pattern1 = re.compile("(\d+) +(\d+\.*\d*) +(\d+) +(\d+\.*\d*)")
#pattern = re.compile(" (\d+) +(\d+) +(\d+\.*\d*) +(\d+) +(\d+) +(\d+\.*\d*)")
        for line in sys.stdin:
            m0 = pattern0.match(line)
            m1 = pattern1.match(line)
            if m0:
                print(line)
                continue
            if m1:
                print(line)
                break


    def benchmark_bonniepp(self):
        """
        Create a benchmark attribute for each Testcase object.
        This attribute will use to compare subsystem.
        This function could be called 'parser' for testing log.
        """
        self.benchmark = list()
        pattern=re.compile(b'^Machine')
        with urllib.request.urlopen(self.log_url+"/"+self.testcase) as page:
            g = io.BufferedReader(page)
            t = io.TextIOWrapper(g, 'utf-8')
            for line in t:
                pattern=re.compile('Machine .*Size')
                m = pattern.match(line)
                if m:
                    line=next(t).split()
                    self.benchmark.append(benchmark('Sequential_Output#Per_char#K/s', line[2], 1))
                    self.benchmark.append(benchmark('Sequential_Output#Block#K/s', line[4], 1))
                    self.benchmark.append(benchmark('Sequential_Output#Rewrite#K/s', line[6], 1))
                    self.benchmark.append(benchmark('Sequential_Input#Per_char#K/s', line[8], 1))
                    self.benchmark.append(benchmark('Sequential_Input#Block#K/s', line[10], 1))
                    self.benchmark.append(benchmark('Random#Seeks#sec', line[12], -1))
                    break
