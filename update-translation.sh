#!/bin/bash
set -e
xgettext -o mauna-power-manager.pot --from-code="utf-8" src/data/MainWindow.ui `find src -type f -iname "*.py"`
for file in `ls po/*.po`; do
    msgmerge $file mauna-power-manager.pot -o $file.new
    echo POT: $file
    rm -f $file
    mv $file.new $file
done


