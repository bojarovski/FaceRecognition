# testFace

docker build -t app .
docker run -it app
docker run -it --rm   -p 5000:5000   --device=/dev/video0  app

