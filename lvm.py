#! /usr/bin/python

from optparse import OptionParser
from subprocess import Popen, call, PIPE
from shlex import split
from commands import getstatusoutput
from os.path import basename, normpath
import subprocess
import time
import os

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
        cmd = "cat /proc/partitions | awk '{print $4}'"
        d1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = d1.communicate()[0].split(", \n")
        drives = self.drive+"1"
        if drives in str(output):
            print "Disk already added to lvm group, please double check disk partitions table %s" % output
            exit(-1)
    def fdisk(self):
        before_format_cmd = split('echo -e "n\np\n1\n\n\nt\n8e\\nw\n"')
        #before_format_arg = split(before_format_cmd)
        after_format_cmd = split("fdisk /dev/%s" %self.drive)
        #after_format_arg = split(after_format_cmd)
        p1 = Popen(before_format_cmd, stdout=PIPE)
        p2 = call(after_format_cmd, stdin=p1.stdout, stderr=devnull)
        if p2 != 0:
            print 'disk not valid /dev/%s' %self.drive
            exit(-1)
        else:
            print 'partitioning disk /dev/%s' %self.drive

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
        print status,output
    def extend_lv(self):
        lvextend = call(["lvextend", "-l", "+100%FREE", "/dev/%s/%s" % (basename(normpath(self.vgfolder)),basename(normpath(self.lvfolder)))])
    def resizefs(self):
        rs = call(["xfs_growfs", "/dev/%s/%s" % (basename(normpath(self.vgfolder)),basename(normpath(self.lvfolder)))])
def main():
        x1 = addDrive(opts.drive, opts.vgfolder, opts.lvfolder)
        x1.check_disk()
        x1.fdisk()
        x1.partprobe()
        x1.pvcreate()
        time.sleep(5)
        x1.extend_vg()
        x1.extend_lv()
        x1.resizefs()
if __name__ == "__main__":
    Usage = "Usage: python lvm.python -d sdb -v cl -l root"
    print "%s which means -d : disk, -v : volume, -l : logical volume" %Usage
    if opts.drive == None and opts.vgfolder == None and opts.lvfolder == None:
        print Usage
        exit(-1)
    main()
