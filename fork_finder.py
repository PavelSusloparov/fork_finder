#!/usr/bin/python

import logging
import os
import re
import signal
import subprocess

logging.basicConfig(format = u'%(filename)s [LINE:%(lineno)d]# %(levelname)-0s [%(asctime)s]  %(message)s', level = logging.DEBUG, filename = u'%s/fork.log' %  '/'.join(os.path.abspath(__file__).split('/')[:-1]))

MAX_FORKS = 10


class SignalToManyForkSender(object):
    """
    Class send signal to processes with more than child_num_limit forks.

    @childs_num_limit: If process has more than childs_num_limit forks, it gets signal
    @sig: type of signal, whiich send to processes
    """
    def __init__(self, childs_num_limit, sig):
        self.childs_num_limit = childs_num_limit
        self.sig = sig
        self.all_pids = []
        self.many_forks = []

    def run(self):
        """
        Start process
        """
        self._get_all_pids()
        self._find_fork_process()
        self._send_signal()

    def _get_all_pids(self):
        """
        Get all pids in system.

        @return: None
        """
        #Use Linux 'ps ax' command for getting list of all processes
        raw_ps = subprocess.Popen(['ps', 'ax'], stdout=subprocess.PIPE).communicate()[0]
        processes = raw_ps.split('\n')
        # this specifies the number of splits, so the splitted lines
        # will have (nfields+1) elements
        nfields = len(processes[0].split()) - 1
        #Parce list of all processes
        for row in processes[1:]:
            if row:
                self.all_pids.append(row.split(None, nfields)[0])
        logging.debug("All process pids in system: %s" % self.all_pids)

    def _find_fork_process(self):
        """
        Get list of processes with more than childs_num_limit forks.

        @return: None
        """
        for pid in self.all_pids:
            #Use pstree -p <pid> command for getting pid process tree.
            pstree_raw = subprocess.Popen("pstree -p %s" % pid, shell=True, stdout=subprocess.PIPE).communicate()[0]
            #Use regular expression for getting all pid process childs from pstree_raw
            childs = re.findall(r'\-\{.*\}\((\d+)\)', pstree_raw)
            childs_num = len(childs)
            #Compare current number of child process and childs limit by user
            if childs_num > self.childs_num_limit:
                logging.debug("Pid %s has %s forks" % (pid, childs_num))
                self.many_forks.append(pid)

    def _send_signal(self):
        """
        Send signal sig to processes wtih more than childs_num_limit forks.

        @sig: type of signal, whiich send to processes
        @return: None
        """
        for pid in self.many_forks:
            try:
                logging.info("Send signal with code %s to %s." % (self.sig, pid))
                #Uncomment for sending signal sig to process pid
                #os.kill(pid, sig)
            except OSError:
                logging.error("Process %s has more than %s forks, but you do not have permission for send %s signal to it." % (pid, sig))

def main():
    print os.path.basename
    SignalToManyForkSender(MAX_FORKS, signal.SIGHUP).run()

if __name__ == "__main__":
    main()
