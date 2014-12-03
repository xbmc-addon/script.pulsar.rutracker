#!/bin/sh
cd `dirname $0`/../src

OLD=`cat ./addon.xml | grep '<addon' | grep 'version="' | grep -E -o 'version="[0-9\.]+"' |  grep -E -o '[0-9\.]+'`
echo "Old version: $OLD"
echo -n 'New version: '
read NEW

sed -e "s/Pulsar\" version=\"$OLD\"/Pulsar\" version=\"$NEW\"/g" ./addon.xml > ./addon2.xml
mv ./addon2.xml ./addon.xml

rm -rf ../script.pulsar.rutracker
rm -f ./script.pulsar.rutracker.zip
mkdir ../script.pulsar.rutracker
cp -r ./* ../script.pulsar.rutracker/

cd ../
zip -rq ./script.pulsar.rutracker.zip ./script.pulsar.rutracker

cp ./script.pulsar.rutracker.zip ../repository.hal9000/repo/script.pulsar.rutracker/script.pulsar.rutracker-$NEW.zip

rm -rf ./script.pulsar.rutracker
rm -f ./script.pulsar.rutracker.zip

`../repository.hal9000/build/build.sh`
