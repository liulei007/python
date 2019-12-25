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
    def pvcreate(self):
        pvcreate = call(["pvcreate", "/dev/%s1" % (self.drive)])
    def vgcreate(self):
	vgcreate = 'vgcreate  %s /dev/%s1' %(basename(normpath(self.vgfolder)),self.drive)
	status,output = getstatusoutput(vgcreate)
	print status,output
	print "This is for vgcreate: ", vgcreate
    def extend_lv(self):
	extend_lv = 'lvcreate --name {0} -l "100%FREE" {1}' .format(basename(normpath(self.lvfolder)),basename(normpath(self.vgfolder)))
	status,output = getstatusoutput(extend_lv)
	print status
	print output
	print "This is for lvcreate", self.vgfolder,self.lvfolder
    def resizefs(self):
	diskcmd = ("cat /etc/fstab | grep %s | awk '{print $3}'" % self.lvfolder) 
        diskcmd2 = subprocess.Popen(diskcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	diskfs,diskfs2 = diskcmd2.communicate()[0].split("\n")
	print diskfs
	if diskfs ==  "xfs":             	    
	   rs = call(["xfs_growfs", "/dev/%s/%s" % (basename(normpath(self.vgfolder)),basename(normpath(self.lvfolder)))])
	elif diskfs == "ext4":
	   print "This is ext4"
	   #rs = call(["resize2fs", "/dev/%s/%s" % (basename(normpath(self.vgfolder)),basename(normpath(self.lvfolder)))])
	   rs = call(["mkfs.ext4", "/dev/%s/%s" % (basename(normpath(self.vgfolder)),basename(normpath(self.lvfolder)))])
	elif diskfs == "ext3":
	   print "This is ext3"
	   rs = call(["mkfs.ext3", "/dev/%s/%s" % (basename(normpath(self.vgfolder)),basename(normpath(self.lvfolder)))])
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
		x1.pvcreate()
		x1.vgcreate()
                x1.pvcreate()
                time.sleep(5)
                x1.extend_lv()
                x1.resizefs()
if __name__ == "__main__":
    Usage = "Usage: python lvm.python -d sdb -v VolGroup -l lv_root "
    print '\033[1;31m %s "variables:  -d : disk, -v :volume, -l : logical volume"\033[1;m' %Usage
    main()
