#!/bin/bash
sudo `which gunicorn` -w 4 -b 0.0.0.0:80 app:app
