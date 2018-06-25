from abc import ABCMeta, abstractmethod

import psutil
import operator
import subprocess
import random
import time

from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
from token_telegram import CMD
from matplotlib import pyplot



class WorkInServer(metaclass=ABCMeta):

    def init(self, inp, out):
        self.inp = inp
        self.out = out

    @abstractmethod
    def work(self, *args, **kwargs):
        pass

    @classmethod
    def get_instance(cls, name, *args, **kwargs):
        klass = cls.types.get(name)
        if klass is None:
            raise WorkException('Work with name "{}" not found!'.format(name))
        return klass(*args, **kwargs)

    types = {}

    @classmethod
    def add_work(cls, name, klass):
        if not name:
            raise WorkException('Work must have a name!')
        if not issubclass(klass, WorkInServer):
            raise WorkException('Class "{}" is not Work!'.format(klass))
        cls.types[name] = klass

class WorkException(Exception):
    def init(self, ext):
        pass

def add_Work(type):
    def decorator(cls):
        WorkInServer.add_work(type, cls)
        return cls
    return decorator\

@add_Work('status_system')
class StatusServer(WorkInServer):
    def work(self):
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        boottime = datetime.fromtimestamp(psutil.boot_time())
        now = datetime.now()
        timedif = "Online for: %.1f Hours" % (((now - boottime).total_seconds()) / 3600)
        memtotal = "Total memory: %.2f GB " % (memory.total / 1000000000)
        memuseperc = "Used memory: " + str(memory.percent) + " %"
        diskused = "Disk used: " + str(disk.percent) + " %"
        pids = psutil.pids()
        pidsreply = ''
        procs = {}
        for pid in pids:
            p = psutil.Process(pid)
            try:
                pmem = p.memory_percent()
                if pmem > 0.5:
                    if p.name() in procs:
                        procs[p.name()] += pmem
                    else:
                        procs[p.name()] = pmem
            except:
                print("...")
        sortedprocs = sorted(procs.items(), key=operator.itemgetter(1), reverse=True)
        for proc in sortedprocs:
            pidsreply += proc[0] + " " + ("%.2f" % proc[1]) + " %\n"
        reply = timedif + "\n" + \
                memtotal + "\n" + \
                memuseperc + "\n" + \
                diskused + "\n\n" + \
                pidsreply
        print(reply)
        return reply

@add_Work('shell')
class StatusServer(WorkInServer):
    def work(self, inp='pwd', status=True):
        if inp == 'exit':
            status = False
            return status, 'Shell closed!'
        else:
            p = Popen(inp, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            out = p.stdout.read()
            if out == b'': out = 'Not output'
            return status, out

@add_Work('conn_client_proxy')
class StatusProxyNow(WorkInServer):
    def work(self, inp=CMD):
        p = Popen(str(inp), shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        out = p.stdout.read()
        return int(out)

@add_Work('log_client_proxy')
class LogStatusProxyNow(WorkInServer):
    def __init__(self):
        self.start = datetime.now()
        write_status = WorkInServer.get_instance('conn_client_proxy')

    def work(self):
        end = datetime.now()

        with open('status_proxy.txt') as f:
            self.people_list = [int(i) for i in f.read().split()]

        yaxis = self.people_list
        xaxis = [int(i) for i in range(1,len(yaxis)+1)]
        #print(yaxis,xaxis, len(yaxis), len(xaxis))
        return self.myplotgraph(yaxis, xaxis)

    def myplotgraph(self, yaxis, xaxis):
        pyplot.ylabel('User')
        pyplot.plot(xaxis, yaxis, 'r-.')
        pyplot.axis([0, len(xaxis) - 1, 0, 100])
        pyplot.savefig('graph.png')
        #pyplot.show()
        pyplot.close()
        f = open('graph.png', 'rb')  # some file on local disk
        return f



































