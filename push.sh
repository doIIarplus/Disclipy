#!/usr/bin/env bash

autopep8 --in-place --exclude=./venv --recursive --max-line-length 90 --aggressive --aggressive --ignore=E711,E713,E714 -v .

if [ $# -gt 0 ]; then
	git add "$@" 
else
	git add .
fi

files_added=$(git status -s | grep -E "^(M|A|D|R|C|U)")

echo "M = modified"
echo "A = added"
echo "D = deleted"
echo "R = renamed"
echo "C = copied"
echo "U = updated but unmerged"
echo ""

echo "$files_added" | awk '{print "    " $0}'
echo ""

echo "These are the files you are about to push."
echo "Are you sure you want to push these files? [y/n]"
read yn

if [ "$yn" != "${yn#[Yy]}" ]; then
	git commit --allow-empty-message -m ''
	git push origin master
else
	echo "Aborting push."
	git reset HEAD .
	exit 1
fi


