#!/bin/sh
# Start the scores API in the background, then run nginx in the foreground.
python3 /app/api.py &
exec nginx -g 'daemon off;'
