#!/bin/sh
cd `dirname $0`/../src
cp -r ./* $HOME/Library/Application\ Support/XBMC/addons/script.pulsar.rutracker/

rm -f $HOME/.xbmc/temp/xbmcup/script.pulsar.rutracker/cache.sql
