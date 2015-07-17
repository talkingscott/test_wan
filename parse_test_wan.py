import datetime
import re
import sys

def parse_datetime(dt_string):
  try:
    dt = datetime.datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S.%f')
  except ValueError:
    dt = datetime.datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S')
  return dt

def parse_file(path):
  with open(path, 'r', 0x8000) as f:
    consecutive_errors = 0
    for line in f:
      fields = re.split(' - ', line)
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
        dt = parse_datetime(fields[0])
        if consecutive_errors == 0:
          error_start_dt = dt
        consecutive_errors += 1
        print >>sys.stderr, '{0} {1}'.format(dt, exc)
      else:
        if consecutive_errors > 0:
          if consecutive_errors > 1:
            dt = parse_datetime(fields[0])
            print 'Outage started {0} lasted {1}'.format(error_start_dt.strftime('%Y-%m-%d %H:%M:%S'), str(dt - error_start_dt).split('.')[0])
          consecutive_errors = 0
  
    if consecutive_errors > 1:
      dt = parse_datetime(fields[0])
      print 'Outage started {0} lasted {1}'.format(error_start_dt.strftime('%Y-%m-%d %H:%M:%S'), str(dt - error_start_dt).split('.')[0])

if __name__ == '__main__':
  parse_file('test_wan.txt' if len(sys.argv) <= 1 else sys.argv[1])
