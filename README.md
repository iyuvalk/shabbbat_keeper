# shabbbat_keeper
Provides information about the upcoming Shabbat or Jewish holiday via REST based on the data from the API provided by https://www.hebcal.com

# Build
Build the Docker image using this command:
`docker buildx build --platform linux/amd64,linux/arm64/v8 -t artifexil/shabbat_keeper:latest --push .`