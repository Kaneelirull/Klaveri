FROM nginx:alpine

# Python 3 (stdlib only) for the scores API
RUN apk add --no-cache python3

# Run nginx worker processes as root so they can read
# the TrueNAS volume mount at /data regardless of ownership
RUN sed -i 's/^user\s.*/user root;/' /etc/nginx/nginx.conf || true

# Scores API backend
COPY api.py /app/api.py
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Web files
COPY index.html /usr/share/nginx/html/index.html
COPY games     /usr/share/nginx/html/games

# nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# /data is the persistent volume mount point (TrueNAS host path mapped here).
# Structure:
#   /data/dosbox/    ← .zip / .jsdos files
#   /data/scores/    ← highscore JSON files (created automatically)
#   /data/config/    ← site config JSON (future)
VOLUME ["/data"]

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
