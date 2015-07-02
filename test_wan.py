import datetime
import urllib2
import time
import sys

def log(elapsed, status, exc=None):
  if exc is not None:
    msg = '{0} - {1:.3f} - {2} - {3}'.format(datetime.datetime.now(), elapsed, status, exc)
  else:
    msg = '{0} - {1:.3f} - {2} - '.format(datetime.datetime.now(), elapsed, status)

  print msg
  sys.stdout.flush()
  print >>sys.stderr, msg
  sys.stderr.flush()

while True:
  try:
    start = time.time()
    f = urllib2.urlopen('http://www.msn.com/en-us/tv/tv-listings', timeout=30)
    try:
      f.read()
    finally:
      f.close()
    end = time.time()
    log(end - start, 'OK')
  except Exception, e:
    end = time.time()
    log(end - start, 'ERROR', e)
  time.sleep(5)
