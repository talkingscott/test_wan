import datetime
import urllib2
import time
import sys

def _log(elapsed, status, exc=None):
  '''Log a message to stderr and stdout'''
  if exc is not None:
    msg = '{0} - {1:.3f} - {2} - {3}'.format(datetime.datetime.now(), elapsed, status, exc)
  else:
    msg = '{0} - {1:.3f} - {2} - '.format(datetime.datetime.now(), elapsed, status)

  print msg
  sys.stdout.flush()
  print >>sys.stderr, msg
  sys.stderr.flush()

def get_urls(urls, pause_time):
  '''Continuously retrieve the URLs in a list, pausing after each'''
  url_index = 0
  while True:
    url = urls[url_index]
  
    try:
      start = time.time()
      f = urllib2.urlopen(url, timeout=30)
      try:
        f.read()
      finally:
        f.close()
      end = time.time()
      _log(end - start, 'OK')
    except Exception, e:
      end = time.time()
      _log(end - start, 'ERROR', url + ': ' + str(e))
  
    time.sleep(pause_time)
    url_index = (url_index + 1) % len(urls)

if __name__ == '__main__':
  # TODO: allow the user to specify his/her own list of URLs and pause time
  urls = ['http://www.msn.com/en-us/tv/tv-listings', 'http://www.macrumors.com/', 'http://aws.amazon.com/', 'https://cloud.google.com/compute/', 'http://www.cnet.com/']
  get_urls(urls, 5.0)
