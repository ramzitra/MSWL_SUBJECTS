/**
 * Copyright © 2012-2013 Sergio Arroutbi Braojos <sarroutbi@gmail.com>
 * 
 * Permission to use, copy, modify, and/or distribute this software 
 * for any purpose with or without fee is hereby granted, provided that 
 * the above copyright notice and this permission notice appear in all copies.
 * 
 * THE SOFTWARE IS PROVIDED “AS IS” AND THE AUTHOR DISCLAIMS ALL WARRANTIES 
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY 
 * AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, 
 * INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM 
 * LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, 
 * NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE 
 * OR PERFORMANCE OF THIS SOFTWARE.
 **/

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include "libstat.h"

const char* STATSDB_DUMPER = "./statsdb.py";

LibStat::LibStat()
{
  memset(m_author, 0, MAX_AUTHOR);
  memset(m_file, 0, MAX_FILE);
  memset(m_date, 0, MAX_DATE);
}

LibStat::LibStat(const char* date, const char* file, const char* author)
{
  if(author)
    strncpy(m_author, author, MAX_AUTHOR);
  else
    memset(m_author, 0, MAX_AUTHOR);

  if(file)
    strncpy(m_file, file, MAX_FILE);
  else
    memset(m_file, 0, MAX_FILE);

  strncpy(m_date, date, MAX_DATE);
}

bool LibStat::empty(const char* str)
{
  return ((!str) || (!strlen(str)));
}

const uint64_t LibStat::getLOCs()
{
  uint64_t locs = 0;
  const char* fileDumped = dump();
  if(!getLOCs(fileDumped, &locs))
    locs = 0;
  unlink(fileDumped);
  return locs;
}

const bool LibStat::getLOCs(const char* file, uint64_t* read)
{
  bool ok = true;
  FILE* ff = NULL;
  char line[MAX_LINE];
  memset(line, 0, MAX_LINE);

  if(!read) {
    ok = false;
  }
  else if(empty(file)) {
    ok = false;
  }
  else if(!(ff = fopen(file, "r"))) {
    ok = false;
  }
  else {
    *read = 0;
    while(fgets(line, MAX_LINE, ff)) {
      char extra[MAX_LINE];
      uint64_t loc;
      memset(extra, 0, MAX_LINE);
      if(sscanf(line, "%[^','], %lld", extra, &loc) == 2) {
        ok = true;
        *read = loc;
        break;
      }
    }
  }
  return ok;
}

const char* LibStat::dump()
{
  const char* file = NULL;
  char command[MAX_COMMAND];
  memset(command, 0, MAX_COMMAND);
  strncpy(m_dumpfile, const_cast<char*>("/tmp/libstat.XXXXXX"), MAX_FILE);
  mkstemp(m_dumpfile);

  if(empty(m_author) && empty(m_file)) {
    snprintf(command, MAX_COMMAND, "%s -StimeLOCchanges -e%s > %s",
             STATSDB_DUMPER, m_date, m_dumpfile);
  }
  else if(empty(m_author)) {
    snprintf(command, MAX_COMMAND, "%s -StimeFileLOCchanges -e%s,%s > %s",
             STATSDB_DUMPER, m_file, m_date, m_dumpfile);
  }
  else if(empty(m_file)) {
    snprintf(command, MAX_COMMAND, "%s -StimeAuthorLOCchanges -e%s,%s > %s",
             STATSDB_DUMPER, m_author, m_date, m_dumpfile);
  }
  if(system(command) != 0)
    file = NULL;
  else 
    file = m_dumpfile;

  return file;
}
