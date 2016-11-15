#!/bin/sh
users="dpc-marche"
for user in "${users[@]}"
do 
    ps -eo pid,cmd,etime | grep "HMC_Model_V2_realtime"
    #ps -o etime,euid,pid,tty,comm -u "$user" | while read etime euid pid tty comm
    do 
        [ "$etime" = ELAPSED ] && continue
        [ "$tty" = '?' ] && continue
        do_kill=$(echo "$etime" | awk -F'[-:]' 'NF==3{sub(/^/,"0-")} $1>0 || $2>0 ||$3>=400 {print "Kill"}')
        [ "$do_kill" ] || continue
        kill -HUP "$pid"
    done
done
