#!/usr/bin/python
#
# Copyright (c) 2012-2013 Sergio Arroutbi Braojos <sarroutbi@gmail.com>
# 
# Permission to use, copy, modify, and/or distribute this software 
# for any purpose with or without fee is hereby granted, provided that 
# the above copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES 
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY 
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, 
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM 
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, 
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE 
# OR PERFORMANCE OF THIS SOFTWARE.
#
#
#
import _mysql
import sys
import getopt

default_db="guilty"
default_dbuser="root"
default_dbpasswd="root"
default_dbtable="blame"
default_hostname="localhost"
default_stat=""
default_extra=""

def parse_args(opts, args, app_name):
  database = default_db
  hostname = default_hostname
  dbuser   = default_dbuser
  dbpasswd = default_dbpasswd
  dbtable  = default_dbtable
  stat     = default_stat
  extra    = default_extra
  for opt, arg in opts:
    if opt == '-h':
      print_usage(app_name)
      sys.exit(0)
    elif opt in ("-d", "--database"):
      database = arg
    elif opt in ("-t", "--table"):
      dbtable = arg
    elif opt in ("-h", "--hostname"):
      hostname = arg
    elif opt in ("-u", "--dbuser"):
      dbuser = arg
    elif opt in ("-p", "--password"):
      dbpasswd = arg
    elif opt in ("-s", "--store"):
      store = arg
    elif opt in ("-e", "--extra_stat_data"):
      extra = arg
    elif opt in ("-S", "--stat"):
      stat = arg

  #print 'database is :', database
  #print 'table    is :', dbtable
  #print 'hostname is :', hostname
  #print 'dbuser   is :', dbuser
  #print 'password is :', dbpasswd
  #print 'stat     is :', stat
  #print 'extra    is :', extra

  if stat == '':
    print_usage(app_name)
 
  return database, dbtable, hostname, dbuser, dbpasswd, stat, extra
   
def print_usage(command):
  print 
  print command + ":" 
  print 
  print '             ' + command + ' [-d <database> -u <user> -h<dbhost> '\
'-S<stat> -e<extra_stat_data> -p<password>]'
  print 
  print '             Valid stats: all, timeLOCchanges' 
  print 
  print '             * timeLOCchanges stat data valid:' 
  print '               - Always   : dumps LOC changes that ever happened' 
  print '               - LastWeek : dumps LOC changes that happened last week'
  print '               - LastMonth: dumps LOC changes that happened last month'
  print '               - LastYear : dumps LOC changes that happened last year'
  print '               - Custom   : dumps LOC changes on a custom period'
  print '                          : Format : \"Custom,EndDate,StartDate\"'
  print '                          : Example: \"Custom,2013-12-27,2013-12-22\"'
  print 
  print '             * timeFileLOCchanges stat data will be same as timeLOCchanges, '
  print '               with the name of the file prepended :'
  print '               - file,Always   : dumps LOC changes that ever happened on file \'file\'' 
  print '               - file,LastWeek : dumps LOC changes that happened on last week on file \'file\''
  print '               - file,LastMonth: dumps LOC changes that happened last month on file \'file\''
  print '               - file,Last3Months: dumps LOC changes that happened on last 3 months on file \'file\''
  print '               - file,Last6Months: dumps LOC changes that happened on last 6 months on file \'file\''
  print '               - file,LastMonth: dumps LOC changes that happened last month on file \'file\''
  print '               - file,LastYear : dumps LOC changes that happened last year on file \'file\''
  print '               - file,Custom   : dumps LOC changes on a custom period on file \'file\''
  print '                               : Format : \"File,Custom,EndDate,StartDate\"'
  print '                               : Example: \"index.html,Custom,2013-12-27,2013-12-22\" on file \'file\''
  print 
  print '             * timeAuthorLOCchanges stat data will be same as timeLOCchanges, '
  print '               with the name of the file prepended :'
  print '               - author,Always   : dumps LOC changes that ever happened by author \'author\'' 
  print '               - author,LastWeek : dumps LOC changes that happened on last week by author \'author\''
  print '               - author,LastMonth: dumps LOC changes that happened last month by author \'author\''
  print '               - author,Last3Months: dumps LOC changes that happened on last 3 months by author \'author\''
  print '               - author,Last6Months: dumps LOC changes that happened on last 6 months by author \'author\''
  print '               - author,LastYear : dumps LOC changes that happened last year by author \'author\''
  print '               - author,Custom   : dumps LOC changes on a custom period by author \'author\''
  print '                                 : Format : \"Author,Custom,EndDate,StartDate\"'
  print '                                 : Example: \"sarroutbi,Custom,2013-12-27,2013-12-22\" by author \'author\''
  print 

def print_stat(cur, table, stat, extra):
  ok = False

  if stat == "timeLOCchanges":
    ok = getTimeLOCchanges(cur, table, extra, '', '')
  elif stat == "timeFileLOCchanges":
    ok = getTimeFileLOCchanges(cur, table, extra)
  elif stat == "timeAuthorLOCchanges":
    ok = getTimeAuthorLOCchanges(cur, table, extra)

  return ok

def parseCustomDates(string):
  tokens = string.split(',')
  if len(tokens) < 3:
    return tokens[0], tokens[0], False
  return tokens[1], tokens[2], True

def getDBFileId(cur, file):
  query = 'SELECT id from files WHERE path=\'' + file + '\';'
  cur.query(query)
  result = cur.use_result()
  file_id = 0
  row_list = result.fetch_row()
  if result and row_list and row_list[0]:
    file_id = row_list[0][0]
    return file_id, True
  else:
    return file_id, False

def getDBAuthorId(cur, author):
  query = 'SELECT id from authors WHERE name=\'' + author + '\';'
  cur.query(query)
  result = cur.use_result()
  author_id = 0
  row_list = result.fetch_row()
  if result and row_list and row_list[0]:
    author_id = row_list[0][0]
    return author_id, True
  else:
    return author_id, False

def getTimeFileLOCchanges(cur, table, extra):
  extra_nofile = ''
  tokens  = extra.split(',')
  file    = tokens[0]
  avoid   = True
  counter = 1
  for token in tokens:
    if not avoid:
      extra_nofile += token
      if counter < len(tokens):
        extra_nofile += ','  
    else:
      avoid = False
    counter += 1

  return getTimeLOCchanges(cur, table, extra_nofile, file, '')

def getTimeAuthorLOCchanges(cur, table, extra):
  extra_noauthor = ''
  tokens  = extra.split(',')
  author  = tokens[0]
  avoid   = True
  counter = 1
  for token in tokens:
    if not avoid:
      extra_noauthor += token
      if counter < len(tokens):
        extra_noauthor += ','  
    else:
      avoid = False
    counter += 1

  return getTimeLOCchanges(cur, table, extra_noauthor, '', author)

def getTimeLOCchanges(cur, table, time, file, author):

  if file == '' and author == '':
    basic_query = "SELECT COUNT(*) FROM " + table
    common_query = "SELECT COUNT(*) FROM " + table + " WHERE "
  elif file == '':
    author_id, ok = getDBAuthorId(cur, author)
    if ok:
      common_query = "SELECT COUNT(*) FROM " + table + " WHERE author_id=" + author_id + " AND "
    else:
      print "Error: %s author does not exist on databse" % (file)
      sys.exit(1)
  elif author == '':
    file_id, ok = getDBFileId(cur, file)
    if ok:
      common_query = "SELECT COUNT(*) FROM " + table + " WHERE file_id=" + file_id + " AND "
    else:
      print "Error: %s file does not exist on databse" % (file)
      sys.exit(1)
  else:
    return false
    
  if time == '':
    time  = 'Always'
  if time == 'Always':
    query = basic_query
  elif time == 'LastWeek':
    query = common_query + ' DATE BETWEEN DATE_SUB(NOW(), INTERVAL 1 WEEK) AND NOW();'
  elif time == 'LastMonth':
    query = common_query + ' DATE BETWEEN DATE_SUB(NOW(), INTERVAL 1 MONTH) AND NOW();'
  elif time == 'Last3Months':
    query = common_query + ' DATE BETWEEN DATE_SUB(NOW(), INTERVAL 3 MONTH) AND NOW();'
  elif time == 'Last6Months':
    query = common_query + ' DATE BETWEEN DATE_SUB(NOW(), INTERVAL 6 MONTH) AND NOW();'
  elif time == 'LastYear':
    query = common_query + ' DATE BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW();'
  elif time.startswith('Custom'):
    date1, date2, ok = parseCustomDates(time)
    if ok:
      query = common_query + ' DATE BETWEEN \'' + date2 + '\' AND \'' + date1 +'\';'
      time  = date2 + ' to ' + date1
    else:
      return False
  else:
    return False

  cur.query(query)
  result = cur.use_result()

  if result:
    print time + ', %s ' % result.fetch_row()[0]

  return True

def main(argv):
  try:
    opts, args = getopt.getopt(argv[1:],"hd:h:u:p:S:e:",["database=","hostname=","user=","password=","stat=", "extra="])
  except getopt.GetoptError:
    print "Exception!"
    print_usage(argv[0])
    sys.exit(1)
 
  db, table, hostname, dbuser, password, stat, extra = parse_args(opts, args, argv[0])
  try: 
    # Connect to an existing DB
    conn = _mysql.connect(hostname, dbuser, password, db)
    if not print_stat(conn, table, stat, extra):
      print_usage(argv[0])
  except _mysql.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)
  finally:
    if conn:
      conn.close()

if __name__ == "__main__":
   main(sys.argv[0:])
