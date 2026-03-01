# Klaveri 🎹

An Estonian keyboard typing game for kids, built as a single self-contained HTML file.

## Levels

| Level | Description | Keys | Time Limit |
|-------|-------------|------|------------|
| 1 | Home row basics | F, J | 90s |
| 2 | More fingers | F, J, D, K, S, L | 120s |
| 3 | Story mode | All keys | No limit |

## Features

- 🎮 3 progressive levels unlocked in sequence
- ⌨️ On-screen keyboard with colour-coded hands (red = left, blue = right)
- 💡 Per-keystroke hint showing which hand to use
- ⏱ Live timer + WPM counter
- 🎉 Confetti on level completion
- 📱 Responsive — works on desktop and tablet

## Deployment on TrueNAS SCALE

### Option A – Static file via nginx

Place `index.html` in your nginx web root (e.g. `/var/www/klaveri/`) and point a Custom App or existing nginx instance at it.

### Option B – Docker (recommended)

```bash
docker run -d \
  --name klaveri \
  -p 8080:80 \
  --restart unless-stopped \
  kaneelir0ll/klaveri:latest
```

Then open `http://<truenas-ip>:8080` in the browser.

## Docker Hub

[https://hub.docker.com/r/kaneelir0ll/klaveri](https://hub.docker.com/r/kaneelir0ll/klaveri)

## Development

```bash
# Just open in browser — no build step needed
start index.html
```
