#!/usr/bin/env bash

FILE=`readlink -f $1`

chmod a+x ${FILE}
cp ${FILE} ~/bin/


