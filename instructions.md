# testFace

docker build -t app .
docker run -it app
docker run -it --device=/dev/video0 app
