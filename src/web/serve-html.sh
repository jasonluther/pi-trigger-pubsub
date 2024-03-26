#!/bin/sh
# Serve HTML pages locally to display the form and response
python3 -m http.server 8000 &
open "http://localhost:8000"