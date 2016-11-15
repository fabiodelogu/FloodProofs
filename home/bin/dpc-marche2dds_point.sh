#!/bin/bash

#
# Script che trasferisce dati da locale ad un server remoto
#

#source_base_path=/hydro/archive/realtime_nwp-lami-i7


DATE=$(echo $1)
YEAR=$(echo $1 | cut -c1-4)
MONTH=$(echo $1 | cut -c5-6)
DAY=$(echo $1 | cut -c7-8)
HH=$(echo $1 | cut -c9-10)

#source_base_path=/hydro/archive/realtime_nwp-lami-i7
#dds_base_path=/share/series/damsdeterministicecmwf 
#data_path=/timeseries/section_q
source_base_path=$2
dds_base_path=$3
data_path=$4

log_file="/home/dpc-marche/log/dpc-marche2dds.log"

echo "Running script dpc-marche2dds_point with Parameters: $1 $2 $3 $4" >> $log_file


dds_host=10.198.26.11
dds_usr=root
dds_psw=rootroot

#echo "$YEAR $MONTH $DAY $HH" >> $log_file

FILES=$(ls $source_base_path/$YEAR/$MONTH/$DAY/$HH$data_path)

for FILE in ${FILES}; do
    #echo $FILE
    filename_datepart=${FILE##*_}
    #echo $filename_datepart
    filename_year=$(echo $filename_datepart | cut -c1-4)
    filename_month=$(echo $filename_datepart | cut -c5-6)
    filename_day=$(echo $filename_datepart | cut -c7-8)
    echo "$FILE $filename_datepart $filename_year $filename_month $filename_day" >> $log_file
    #if [ ! -d sshpass -p $dds_psw ssh $dds_usr@$dds_host  $dds_base_path/$filename_year/$filename_month/$filename_day ]
    if ! (sshpass -p $dds_psw ssh $dds_usr@$dds_host  [ -d $dds_base_path/$filename_year/$filename_month/$filename_day ])
    then
	#echo "creating path: $dds_base_path/$filename_year/$filename_month/$filename_day" >> $log_file
	    sshpass -p $dds_psw ssh $dds_usr@$dds_host "mkdir -p $dds_base_path/$filename_year/$filename_month/$filename_day"
	    #sshpass -p $dds_psw ssh $dds_usr@$dds_host "chown -R rdp:rdp $dds_base_path/$filename_year"
    fi
    #echo "transferring file $FILE" >> $log_file
    sshpass -p $dds_psw rsync -ue ssh  $source_base_path/$filename_year/$filename_month/$filename_day/$HH$data_path/$FILE $dds_usr@$dds_host:$dds_base_path/$YEAR/$MONTH/$DAY/$FILE
    #echo "changing owner to rdp" >> $log_file
    sshpass -p $dds_psw ssh $dds_usr@$dds_host "chown -R rdp:rdp $dds_base_path/$filename_year"
    #echo $remote_usr@$remote_host$remote_base_path/$YEAR/$MONTH/$DAY/$HH$series_path/$FILE
    #echo $local_base_path/$filename_year/$filename_month/$filename_day
done

echo "End running script dpc-marche2dds_point\n\n\n" >> $log_file
