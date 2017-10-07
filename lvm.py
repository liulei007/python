    #! /usr/bin/python

from optparse import OptionParser
from subprocess import Popen, call, PIPE
from shlex import split
    #to import getstatusoutput from commands lib
from commands import getstatusoutput
import os
from os.path import basename, normpath
import shlex, subprocess
import time
import re

devnull = open(os.devnull, 'w')
parser = OptionParser()
parser.add_option('-d', '--drive', dest='drive')
parser.add_option('-v', '--vgfolder1', dest='vgfolder')
parser.add_option('-l', '--lvfolder', dest='lvfolder')
(opts, args) = parser.parse_args()

class addDrive(object):

    def __init__(self, drive, vgfolder, lvfolder):
        self.drive = str(drive)
        self.vgfolder = str(vgfolder)
        self.lvfolder = str(lvfolder)

    def check_disk(self):
        flags=False
        cmd = "cat /proc/partitions | awk '{print $4}'"
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output= ps.communicate()[0].split(", \n")
        drives = self.drive+"1"
        if drives in str(output):
            print "Disk has been added to lvm, please double check disk partitions table %s" % output
            exit(-1)
            flags = True
        else:
            flags = False
            print "Starting next job"
    def fdisk(self):
        before_format_cmd = split('echo -e "n\np\n1\n\n\nt\n8e\\nw\n"')
        #before_format_arg = split(before_format_cmd)
        after_format_cmd = split("fdisk /dev/%s" %self.drive)
        #after_format_arg = split(after_format_cmd)
        p1 = Popen(before_format_cmd, stdout=PIPE)
        p2 = call(after_format_cmd, stdin=p1.stdout, stderr=devnull)
        #p2 = call(after_format_arg, stdin=p1.stdout)
        if p2 != 0:
            print 'disk not valid /dev/%s' %self.drive
            exit(-1)
        else:
            print 'formated disk /dev/%s' %self.drive

    def partprobe(self):
        pprobe = "partprobe"
        pprobe1 = split(pprobe)
        part = call(pprobe1)
    def pvcreate(self):
        pvcreate = call(["pvcreate", "/dev/%s1" % self.drive],stderr=devnull)
    def extend_vg(self):
        vgextend = 'vgextend %s /dev/%s1' % (basename(normpath(self.vgfolder)),self.drive)
        status,output = getstatusoutput(vgextend)
        print "This is for vg"
        print  status,output
    def extend_lv(self):
        lvextend = call(["lvextend", "-l", "+100%FREE", "/dev/%s/%s" % (basename(normpath(self.vgfolder)),basename(normpath(self.lvfolder)))])
    def resizefs(self):
        rs = call(["xfs_growfs", "/dev/%s/%s" % (basename(normpath(self.vgfolder)),basename(normpath(self.lvfolder)))])
def main():
        x = addDrive(opts.drive, opts.vgfolder, opts.lvfolder)
        x.check_disk()
        x.fdisk()
        x.partprobe()
        x.pvcreate()
        time.sleep(5)
        x.extend_vg()
        x.extend_lv()
        x.resizefs()
if __name__ == "__main__":
    print "Usage: python lvm.python -d sdb -v cl -l root, which means -d : disk, -v : volume, -l : logical volume"
main()
