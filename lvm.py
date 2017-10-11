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
parser.add_option('-d', '--drive', dest='drive', help='This is drives you are try to partition')
parser.add_option('-v', '--vgfolder', dest='vgfolder', help='This option is for volume group')
parser.add_option('-l', '--lvfolder', dest='lvfolder', help='This option is for logical volume')
(opts, args) = parser.parse_args()


class addDrive(object):

    def __init__(self, drive, vgfolder, lvfolder):
        self.drive = str(drive)
        self.vgfolder = str(vgfolder)
        self.lvfolder = str(lvfolder)

    def check_disk(self):
        cmd = "cat /proc/partitions | awk '{print $4}'"
        d1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = d1.communicate()[0].split("\n")
        drives = self.drive+"1"
	vg1 = self.vgfolder
	lv1 = self.lvfolder
        if drives in str(output):
            print "Disk already added to lvm group, please double check disk partitions table: %s" % output
            exit(-1)
	else:
	    print "Normal"
    def fdisk(self):
            before_format_cmd = split('echo -e "n\np\n1\n\n\nt\n8e\\nw\n"')
            after_format_cmd = split("fdisk /dev/%s" %self.drive)
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
        if basename(normpath(self.vgfolder)) is None:
            exit(-1)
        else:
            vgextend = 'vgextend %s /dev/%s1' % (basename(normpath(self.vgfolder)),self.drive)
            status,output = getstatusoutput(vgextend)
            print "This is for vg"
            print status,output
    def extend_lv(self):
        if basename(normpath(self.lvfolder)) is None:
            exit(-1)
        else:
            lvextend = call(["lvextend", "-l", "+100%FREE", "/dev/%s/%s" % (basename(normpath(self.vgfolder)),basename(normpath(self.lvfolder)))])
    def resizefs(self):
	diskcmd = ("cat /etc/fstab | grep %s | awk '{print $3}'" % self.lvfolder) 
        diskcmd2 = subprocess.Popen(diskcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	diskfs,diskfs2 = diskcmd2.communicate()[0].split("\n")
	print diskfs
	if diskfs ==  "xfs":             	    
	   rs = call(["xfs_growfs", "/dev/%s/%s" % (basename(normpath(self.vgfolder)),basename(normpath(self.lvfolder)))])
	elif diskfs == "ext4":
	   print "This is ext4"
	   rs = call(["resize2fs", "/dev/%s/%s" % (basename(normpath(self.vgfolder)),basename(normpath(self.lvfolder)))])
	else:
	   print "Unknown partitions"
def main():
            x1 = addDrive(opts.drive, opts.vgfolder, opts.lvfolder)
	    if opts.drive == None or opts.vgfolder == None or opts.lvfolder == None:
	    	print "Too little arguments, here is manual:"
		pcal = call(["python", "lvm.py", "-h"])
                exit(-1)
            else:
                x1.check_disk()
                x1.fdisk()
                x1.partprobe()
                x1.pvcreate()
                time.sleep(5)
                x1.extend_vg()
                x1.extend_lv()
                x1.resizefs()
if __name__ == "__main__":
    Usage = "Usage: python lvm.python -d sdb -v VolGroup -l lv_root "
    print '\033[1;31m %s "variables:  -d : disk, -v :volume, -l : logical volume"\033[1;m' %Usage
    main()
