#!/bin/bash

die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || [ "$#" -eq 2 ] || die "1 or 2 arguments required, $# provided"
[ -d "$1" ] || die "path: $1 does not exist"

OUTPUT_DIR=$1

update() {
    # Nodejs packages
    npm install
    # Bower
    bower update
}

if [ "$#" -eq 1 ]; then 
    while true; do
        read -p "This will overwrite $OUTPUT_DIR.  Continue? " yn
        case $yn in
            [Yy]* ) break;;
            [Nn]* ) echo 'Did not deploy.'; exit;;
            * ) echo "Please answer y or n.";;
        esac
    done
elif [ "$2" != "f" ]; then
    die "Second parameter must be 'f' (for forced overwrite)";
fi

rm -rf $OUTPUT_DIR
mkdir $OUTPUT_DIR
update
cp index.html $OUTPUT_DIR
cp -rf elements $OUTPUT_DIR
cp -rf bower_components $OUTPUT_DIR
cp -rf data $OUTPUT_DIR
cp -rf u $OUTPUT_DIR
echo "Successfully deployed to $OUTPUT_DIR"