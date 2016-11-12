#!/usr/bin/env bash

DIR=$(dirname "$0")

cd "$DIR"

git clone https://github.com/xzoert/dedalus-tagger.git
git clone https://github.com/xzoert/dedalus-browser.git
git clone https://github.com/xzoert/dedalus-server.git
cd dedalus-server
npm install
cd "$DIR"






