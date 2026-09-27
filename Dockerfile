# Debt Empire Email Ops UI — stdlib Python only
FROM python:3.12-slim

WORKDIR /app
COPY . /app

ENV EMAIL_UI_HOST=0.0.0.0
ENV DRY_RUN=true
ENV PORT=8765

EXPOSE 8765

# Honor PORT from host (Render/Railway/Fly inject PORT)
CMD ["sh", "-c", "cd ui && DRY_RUN=${DRY_RUN:-true} EMAIL_UI_HOST=0.0.0.0 python3 server.py"]
