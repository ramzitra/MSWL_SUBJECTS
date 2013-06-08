#!/bin/bash
tmp_file=stats_monthweeks.txt

function error() {
  echo
  echo $1
  echo
  exit $2
}

function usage() {
  echo ""
  echo " $1 \"yearmonth\""
  echo ""
  echo "Example for April 2013:"
  echo ""
  echo " $1 201304"
  echo ""
  exit $2
}

test -z $1 && error "Please, provide a month and year in numeric format"
if [ $1 = '-h' ];
then
  usage $0 1
fi

> ${tmp_file}

YEARMONTH=$1
YEAR=$(echo ${YEARMONTH:0:4})
MONTH=$(echo ${YEARMONTH:4:2})
YEAR_MONTH=${YEAR}-${MONTH}

function dumpweek() {
  ./statsdb.py -StimeLOCchanges -eCustom,${YEAR_MONTH}-${2},${YEAR_MONTH}-${1}  >> ${tmp_file}
}

dumpweek "01" "07"
dumpweek "08" "14"
dumpweek "15" "21"
dumpweek "22" "31"

./plotmonthweeks

rm ${tmp_file}