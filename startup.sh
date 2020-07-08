#!/bin/sh

cd "$(dirname "$(find / -type f -name HomeControl.py | head -1)")" && python3 HomeControl.py