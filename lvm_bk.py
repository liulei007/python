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

    devnull = open(os.devnull, 'w')
    parser = OptionParser()
    parser.add_option('-d', '--drive', dest='drive', help='this is the name of the drive like sda,hdd')
    parser.add_option('-v', '--vgfolder1', dest='vgfolder', help='this is the volume group name')
    parser.add_option('-l', '--lvfolder', dest='lvfolder', help='this is the logical volume group name')
    (opts, args) = parser.parse_args()
    class addDrive(object):
        def __init__(self, drive, vgfolder, lvfolder):
            self.drive = str(drive)
            #self.folder = str(folder)
            self.vgfolder = str(vgfolder)
            self.lvfolder = str(lvfolder)

        def fdisk(self):
            #if self.drive =
    	#before_format_cmd = 'echo -e "n\np\n1\n\nt\\n8e\nw"'
            #devnull = open(os.devnull, 'w')
    	before_format_cmd = 'echo -e "n\np\n1\n\n\nt\n8e\\nw\n"'
            before_format_arg = split(before_format_cmd)
            after_format_cmd = "fdisk /dev/%s" %self.drive
            after_format_arg = split(after_format_cmd)
            p1 = Popen(before_format_arg, stdout=PIPE)
            p2 = call(after_format_arg, stdin=p1.stdout, stderr=devnull)
            if p2 != 0:
               print 'disk not valid /dev/%s' %self.drive
            else:
               print 'formated disk /dev/%s' %self.drive

        def partprobe(self):
            pprobe = "partprobe"
            pprobe1 = split(pprobe)
            part = call(pprobe1)
        def pvcreate(self):
            pvcreate = call(["pvcreate", "/dev/%s1" % self.drive], stderr=devnull)
        def extend_vg(self):
            vgextend = 'vgextend %s /dev/%s1' % (basename(normpath(self.vgfolder)),self.drive)
            status,output = getstatusoutput(vgextend)
            print "This is for vg"
            print  status,output

            #vgextend = 'vgextend %s /dev/%s' % (basename(normpath(self.vgfolder)), self.drive)
            #vgextend = call(["vgextend", "%s", "/dev/%s1" % (basename(normpath(self.vgfolder)),self.drive)])
        def extend_lv(self):
            lvextend = call(["lvextend", "-l", "+100%FREE", "/dev/%s/%s" % (basename(normpath(self.vgfolder)),basename(normpath(self.lvfolder)))])
        #def volgroup(self):
            #vgcreate = 'vgcreate -v vg_%s /dev/%s1' % (basename(normpath(self.folder)), self.drive)
         #   vgcreate = 'vgcreate -v %s /dev/%s1' % (basename(normpath(self.folder)), self.drive)
         #   status,output = getstatusoutput(vgcreate)
        #def lvm(self):
         #   lvcreate = 'lvcreate -v -l "100%FREE" -n lv_{0} vg_{1}' . format(basename(normpath(self.folder)), basename(normpath(self.folder)))
          #  status,output = getstatusoutput(lvcreate)
          #  print status
          #  print output
    #myaddDrive = addDrive(object)
    #myaddDrive.fdisk()
    #/dev/vg/lv
        def resizefs(self):
            #rs = 'xfs_growfs /dev/%s/%s' % (basename(normpath(self.vgfolder)),basename(normpath(self.lvfolder)))
            rs = call(["xfs_growfs", "/dev/%s/%s" % (basename(normpath(self.vgfolder)),basename(normpath(self.lvfolder)))])
    def main():
        x = addDrive(opts.drive, opts.vgfolder, opts.lvfolder)
        x.fdisk()
        x.partprobe()
        x.pvcreate()
        time.sleep(5)
        x.extend_vg()
        x.extend_lv()
        x.resizefs()
        if __name__ == "__main__":

        print "Usage: python 1_fdisk.py -d sdb -v cl -l root, which means -d : disk, -v : volume, -l : logical volume"
        main()
