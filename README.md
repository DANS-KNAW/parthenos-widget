# parthenos-widget
Parthenos widget to disseminate policies content 

# CENTOS installation
```
yum install python python-pip
yum install gcc
yum install python-devel
yum install openssl-devel
yum install httpd
```

# Install python dependencies
pip install -r requirements.txt
# Build Docker image
docker build -t parthenos:latest .
# Run Docker container
docker run -p 8082:8082 parthenos
# Run curl to get contents
curl http://localhost:8081/contents
# Run curl to get topics list
curl http://localhost:8081/topics
