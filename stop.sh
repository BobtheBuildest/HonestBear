#!/bin/bash
kill $(ps -ef | grep -v grep | grep bot.py | awk '{print $2}')
