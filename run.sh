#!/bin/bash

### Print total arguments and their values
 
### Command arguments can be accessed as
if [ -z "$1" ]
then echo 'Need workerid in integer (0,1,2,...)'
else
    WORKERID='worker'$1
    
    # Run worker
    docker run -v $(pwd):/tmp/test --name ${WORKERID} --network sk_tfdistnetwork -it sk_tfimage /bin/bash -c "cd /tmp/test && python3 run.py --workerid $1"
    
    # Remove reserved name 
    docker rm ${WORKERID}

fi
