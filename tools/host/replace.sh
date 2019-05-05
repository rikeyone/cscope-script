#!/bin/sh

echo $#
if [ $# -ne 3 ]; then
	echo usage: $0 src dest files
fi

echo $*

list=$(find $3 -type f)
echo handle files: ${list}
for file in ${list}
do
sed -i "s/$1/$2/g" ${file}
done

