FROM python:3.12-slim

WORKDIR /app

# Package + metadata first, then assets the cogs load at runtime.
COPY pyproject.toml config.toml ./
COPY cbusbot ./cbusbot
COPY inspirePics ./inspirePics
COPY twerking ./twerking
COPY *.png *.jpeg *.jpg ./

# Editable install keeps the package rooted at /app so cbusbot.config.ROOT
# resolves asset paths correctly.
RUN pip install --no-cache-dir -e .

RUN useradd --create-home bot && mkdir -p /app/data && chown bot /app/data
USER bot

# Secrets (DISCORD_TOKEN, KLIPY_KEY) come from the environment at run time —
# never baked into the image. See docker-compose.yml's env_file.
CMD ["python", "-m", "cbusbot"]
