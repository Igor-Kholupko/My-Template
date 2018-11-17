#!/bin/bash

# Getting basedirectory of script
BASEDIR=$(dirname "$0")

# Setting up virtual environment
python3 -m venv $BASEDIR/../venv
source $BASEDIR/../venv/bin/activate
python3 -m pip install -qU pip
python3 -m pip install -qU setuptools
python3 -m pip install -qr $BASEDIR/../src/requirements.txt
deactivate

# Creating environment variables template
echo \
"SECRET_KEY=[SECRET_KEY]
ALLOWED_HOSTS=[ALLOWED_HOSTS]
DEBUG=False
WK_EXECUTABLE_PATH=[WK_EXECUTABLE_PATH]
WK_OPTION_XVFB=True
DB_NAME=[DB_NAME]
DB_USER=[DB_USER]
DB_PASS=[DB_PASS]
DB_HOST=127.0.0.1
DB_PORT=5432
EMAIL_USER=[EMAIL_USER]
EMAIL_PASS=[EMAIL_PASS]" \
> $BASEDIR/../venv/bin/.env

# Updating environment activation file

sed -i \
"/deactivate () {/a\
\    if ! [ -z \"\${VIRTUAL_ENV}\" ] ; then\n\
\        unset \$(cut -d= -f1 \$VIRTUAL_ENV/bin/.env)\n\
\    fi" \
$BASEDIR/../venv/bin/activate

echo \
"
# User defined variables
source \$VIRTUAL_ENV/bin/.env
export \$(cut -d= -f1 \$VIRTUAL_ENV/bin/.env)" \
>> $BASEDIR/../venv/bin/activate
