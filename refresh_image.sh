docker image rm us-central1-docker.pkg.dev/schwab-algo-trading/algo-trading/algo-trader
docker buildx build --platform linux/amd64 -t algo-trader .
docker tag algo-trader:latest \us-central1-docker.pkg.dev/schwab-algo-trading/algo-trading/algo-trader
gcloud container images delete us-central1-docker.pkg.dev/schwab-algo-trading/algo-trading/algo-trader
docker push us-central1-docker.pkg.dev/schwab-algo-trading/algo-trading/algo-trader