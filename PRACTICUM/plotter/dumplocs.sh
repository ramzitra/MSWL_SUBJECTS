#!/bin/bash
tmp_file=stats_locs.txt

> ${tmp_file}

./statsdb.py -StimeLOCchanges -eLastWeek     >> ${tmp_file}
./statsdb.py -StimeLOCchanges -eLastMonth    >> ${tmp_file}
./statsdb.py -StimeLOCchanges -eLast3Months  >> ${tmp_file}
./statsdb.py -StimeLOCchanges -eLast6Months  >> ${tmp_file}
./statsdb.py -StimeLOCchanges -eLastYear     >> ${tmp_file}
./plotlocs

rm ${tmp_file}