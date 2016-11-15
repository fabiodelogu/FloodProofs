#!/bin/bash

__myname=$(basename $0)
__mydir=$(dirname $0)
((__upTo = 3600 * 4))
__nowAsSecs=$(date +%s)
__toGet="$(date +%Y-%m-%d)_dati_prev.csv"
((__endAsSecs = $__nowAsSecs + $__upTo))
while (($__nowAsSecs < $__endAsSecs)); do
    if wget "http://10.6.26.123/db_vig/dati/$__toGet" -O /hydro/data/dynamic_data/source/subjective-forecast/$__toGet ;then
        exit 0
    fi
    sleep 300
    __nowAsSecs=$(date +%s)
done

exit 0
