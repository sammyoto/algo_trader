docker build -t algo-trader .
docker run -p 8080:8080 \
    -e APP_KEY="APP KEY HERE" \
    -e SECRET_KEY="SECRET KEY HERE" \
    -e TOKENS='TOKENS HERE' \
    algo-trader