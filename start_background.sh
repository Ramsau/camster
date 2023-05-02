#!/usr/bin/env bash
cd /home/christoph/Dokumente/Camster
source venv/bin/activate
python base.py --background &
echo $! > /home/christoph/Dokumente/Camster/pid.pid