#!/bin/sh

if [ x$1 = x ]; then
	echo "Please pass an arg as source code path!!!\n"
	exit 1
fi

SRC=$(find $1 -name "*.c" -o -name "*.h" -o -name "*.sh")

echo "Handle Source Files:"
echo "${SRC}"

for file in ${SRC}
do
sed -i -e 's/\r$//' $file
sed -i -e 's/\s*$//' $file
done
