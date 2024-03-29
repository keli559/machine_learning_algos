import sys
import os.path
import time
import datetime
import commands

# For Macs:
# LOCALMACHINEROOT = "/Volumes" 
#For Linux machines:
LOCALMACHINEROOT = "" 

TRMMroot = LOCALMACHINEROOT + "/data2b/TRMM" 
TMIroot =  TRMMroot + "/TMI"
PRroot =  TRMMroot + "/PR"
TMIHDFroot = TMIroot + "/HDF/"
PRHDFroot = PRroot + "/HDF/"
TMIindexpath = TMIroot + "/1B11.index"
PRindexpath = PRroot + "/2A25.index"

class orbitloc:
  pass

# Declare dictionaries for TMI and PR indexes
tmiorb = {}
prorb = {}
  
default = orbitloc()
default.orbitno = -999
default.path = ""
default.localpath = ""
default.startdatetime = ""
default.enddatetime = ""
default.startepochsec = 0.0
default.endepochsec = 0.0
default.slat = -999.9
default.exists = False

def initindex(indexpath, orb):
  findex = open(indexpath)
  try:
    for line in findex:
      line = line.rstrip('\n')
   
      HDFpath = line[0:line.index(".HDF")+4]
      basename = HDFpath[-25:]
      iorbit = int(basename[14:19])

      slat = float(line[-10:-2])

      startdatetime = line[line.index(".HDF")+5:line.index(".HDF")+28]
      startfracsec = 0.001*int(startdatetime[-3:])
      startepochsec = time.mktime(time.strptime(startdatetime[0:19],"%Y-%m-%d %H:%M:%S"))+startfracsec

      enddatetime = line[line.index(".HDF")+29:line.index(".HDF")+52]
      endfracsec = 0.001*int(enddatetime[-3:])
      endepochsec = time.mktime(time.strptime(enddatetime[0:19],"%Y-%m-%d %H:%M:%S"))+endfracsec

      tmporbit = orbitloc()
      tmporbit.orbitno = iorbit
      tmporbit.localpath = LOCALMACHINEROOT + HDFpath
      tmporbit.path = HDFpath
      tmporbit.startdatetime = datetime.datetime.fromtimestamp(startepochsec)
      tmporbit.enddatetime = datetime.datetime.fromtimestamp(endepochsec)
      tmporbit.startepochsec = startepochsec
      tmporbit.endepochsec = endepochsec
      tmporbit.slat = slat
      tmporbit.exists = True
    
      orb[iorbit] = tmporbit
  finally:
    findex.close
  return

initindex(TMIindexpath, tmiorb)  
initindex(PRindexpath, prorb)  

def orbitquery(orbitno,orb):
  iorbitno = int(orbitno)
  result = orb.get(iorbitno,default)
  return result

def TMIquery(orbitno):
  return orbitquery(orbitno,tmiorb)

def PRquery(orbitno):
  return orbitquery(orbitno,prorb)


def orbitfetch(orbitno,sensor):
  # get orbit info

  if sensor=="TMI":
    orbitinfo = TMIquery(orbitno)
    HDFroot = TMIHDFroot
    remotesubdir = "TRMM_L1/TRMM_1B11/"
    filesuffix = ""
  elif sensor=="PR":
    orbitinfo = PRquery(orbitno)
    HDFroot = PRHDFroot
    remotesubdir = "TRMM_L2/TRMM_2A25/"
    filesuffix = ".Z"
  else:
    return default

  # check whether orbit exists
  if not orbitinfo.exists:
    return orbitinfo

  # check whether file already exists on local server, including
  # possible compressed forms

  localcopy = os.path.exists(orbitinfo.localpath)
  if localcopy:
    return orbitinfo

  localcopy = os.path.exists(orbitinfo.localpath+".Z")
  if localcopy:
    orbitinfo.localpath = orbitinfo.localpath+".Z"
    return orbitinfo

  localcopy = os.path.exists(orbitinfo.localpath+".gz")
  if localcopy:
    orbitinfo.localpath = orbitinfo.localpath+".gz"
    return orbitinfo

  
  # if it does not, fetch it from NASA server

  # FUTURE: First check for sufficient space; delete oldest files if
  # needed to make space
  # /FUtURE

  #get filename and relative path
  orbitpath = orbitinfo.localpath
#  print 'orbitpath ',orbitpath
  relpath = orbitpath[len(HDFroot):]
#  print 'relpath ',relpath
  subdir = relpath[0:9]
#  print 'subdir ',subdir
  subdir1 = relpath[0:4]
#  print 'subdir1 ',subdir1
  fname = relpath[len(subdir):]
#  print 'fname ',fname

  # create target subdirectories, if needed
  targetdir1 = HDFroot + subdir1
#  print "targetdir1 ",targetdir1 
  if not os.path.exists(targetdir1):
    comstring = 'mkdir ' + targetdir1
#    print comstring
    commands.getoutput(comstring)
    comstring = 'chmod a+rwx ' + targetdir1
#    print comstring
    commands.getoutput(comstring)

  targetdir2 = HDFroot + subdir
#  print 'targetdir2 ',targetdir2
  if not os.path.exists(targetdir2):
    comstring = 'mkdir ' + targetdir2
#    print comstring
    commands.getoutput(comstring)
    comstring = 'chmod a+rwx ' + targetdir2
#    print comstring
    commands.getoutput(comstring)


  relpath = relpath + filesuffix
  comstring = '/sw/bin/lftp -c "user anonymous gwpetty@wisc.edu ; get ftp://disc2.nascom.nasa.gov/ftp/data/s4pa/'+ remotesubdir + relpath + ' -o ' + HDFroot + relpath +'"'
#  print comstring
  commands.getoutput(comstring)


  # check for all possible variations on local filename
  localcopy = os.path.exists(orbitinfo.localpath)
  if localcopy:
    return orbitinfo

  localcopy = os.path.exists(orbitinfo.localpath+".Z")
  if localcopy:
    orbitinfo.localpath = orbitinfo.localpath+".Z"
    return orbitinfo

  localcopy = os.path.exists(orbitinfo.localpath+".gz")
  if localcopy:
    orbitinfo.localpath = orbitinfo.localpath+".gz"
    return orbitinfo

  return default



def TMIfetch(orbitno):
  return orbitfetch(orbitno,"TMI")

def PRfetch(orbitno):
  return orbitfetch(orbitno,"PR")
