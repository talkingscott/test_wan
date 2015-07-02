import datetime
import re
import sys

with open('test_wan.txt', 'r') as f:
  consecutive_errors = 0
  for line in f:
    fields = re.split(' - ', line)
    try:
      dt = datetime.datetime.strptime(fields[0], '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
      dt = datetime.datetime.strptime(fields[0], '%Y-%m-%d %H:%M:%S')
    if len(fields) == 2:
      m = re.match('(\S+) \(([\d\.]+)\)', fields[1])
      if m is not None:
        status = m.group(1)
        duration = float(m.group(2))
      else:
        status = 'ERROR'
        duration = 0.0
        exc = fields[1]
    else:
      duration = float(fields[1])
      status = fields[2]
      if len(fields) > 3:
        exc = fields[3].strip()

    if status != 'OK':
      if consecutive_errors == 0:
        error_start_dt = dt
      consecutive_errors += 1
      print >>sys.stderr, '{0} {1}'.format(dt, exc)
    else:
      if consecutive_errors > 0:
        if consecutive_errors > 1:
          print 'Outage started {0} lasted {1}'.format(error_start_dt.strftime('%Y-%m-%d %H:%M:%S'), str(dt - error_start_dt).split('.')[0])
        consecutive_errors = 0

  if consecutive_errors > 1:
    print 'Outage started {0} lasted {1}'.format(error_start_dt.strftime('%Y-%m-%d %H:%M:%S'), str(dt - error_start_dt).split('.')[0])
