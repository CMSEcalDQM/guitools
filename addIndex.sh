#!/bin/bash

date

guidir=/data/ecalod-disk01/dqm-gui
datadir=/data/ecalod-disk01/dqm-data

lock=$datadir/.addIndex.lock

if [ -e $lock ]; then
    echo "addIndex already running"
    exit 1
fi

touch $lock

ix=$guidir/state/dqmgui/online/ix
tmp=$datadir/tmp/closed
dest=$datadir/root

cd $guidir

. $PWD/current/apps/dqmgui/etc/profile.d/env.sh

for file in $(ls -t --color=never $tmp/DQM* 2> /dev/null); do
    echo "Adding index for "$(echo $file | sed 's|^.*/\([^\/]*\)$|\1|')

    visDQMIndex add $ix $file && mv $file $dest/
done

rm $lock
