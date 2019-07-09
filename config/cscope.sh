#!/bin/sh

SRC=`pwd`
OUT=${SRC}
update=1
change=0
while getopts "o:d:uc" opt;
do
    case $opt in
        d)
			SRC=$(cd "$(dirname "$OPTARG")" && pwd)/$(basename "$OPTARG")
			;;
        o)
            OUT=$OPTARG
			;;
		u)
			update=1
			;;
		c)
			change=1
			;;
		?)
			echo "invaild option!"
			exit 1
	esac
done

echo "project source:${SRC}"
echo "database output:${OUT}"

cd ${OUT}

if [ 1 -eq ${change} ]; then
	echo "change project cscope database!"
	res=$(find ${SRC} -maxdepth 1 -name cscope.out)
	if [ "x"${res} = "x" ]; then
		res=$(find ${SRC} -maxdepth 4 -name cscope.out)
		if [ "x"${res} != "x" ]; then
			echo "Found cscope database:${res}, just change CSCOPE_DB env!"
			#export CSCOPE_DB=${res}
		fi
		echo "Not found cscope database, generate cscope database!"
		find ${SRC} -name "*.h" -o -name "*.c" -o -name "*.cc" > cscope.files
		cscope -bkq -i cscope.files 
		#ctags -R *
		#export CSCOPE_DB=${OUT}/cscope.out
	else
		echo "Found cscope database:${res}, just change CSCOPE_DB env!"
		#export CSCOPE_DB=${res}
	fi
elif [ 1 -eq ${update} ]; then
	echo "udpate project cscope database!"
	find ${SRC} -name "*.h" -o -name "*.c" -o -name "*.cc" > cscope.files
	cscope -bkq -i cscope.files
	#ctags -R *
	#export CSCOPE_DB=${OUT}/cscope.out
fi

#echo CSCOPE_DB=${CSCOPE_DB}

