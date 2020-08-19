#!/bin/bash
time=$1
iterations=$2
times_run=$(($1*60))
echo "$times_run"
for(( i=0;i<$iterations;i++ ));do
    index_page='https://finance.yahoo.com/most-active/'
    cdate=`date +"%Y_%m_%d_%H_%M_%S"`
    hfn=yahoo_${cdate}.html
    wget -O yahoo_${cdate}.html $index_page
    python3 stock-extraction.py $hfn
    sleep $times_run
done;