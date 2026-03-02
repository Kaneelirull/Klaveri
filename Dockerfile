FROM nginx:alpine

# Copy site files
COPY . /usr/share/nginx/html/

# Use our custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# /data is the persistent volume mount point.
# On TrueNAS, map a host path to /data.
# Structure expected:
#   /data/dosbox/    ← drop .zip / .jsdos files here
#   /data/scores/    ← highscore JSON (future)
#   /data/config/    ← site config JSON (future)
VOLUME ["/data"]

EXPOSE 80
