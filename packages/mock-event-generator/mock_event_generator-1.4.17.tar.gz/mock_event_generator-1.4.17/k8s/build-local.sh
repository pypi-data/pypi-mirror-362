set -ex

IMAGE=emfollow/mock-event-generator:local
LIGO_CERTIFICATE_PATH=/tmp/x509up_u$(id -u)

DOCKER_BUILDKIT=1 docker build \
    --file k8s/Dockerfile \
    --pull \
    --build-arg BUILD_ENV=local \
    --secret id=x509,src=${LIGO_CERTIFICATE_PATH} \
    --progress=plain \
    -t ${IMAGE} .
