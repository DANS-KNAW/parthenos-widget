# parthenos-widget
Parthenos widget to disseminate policies content 

# CENTOS installation
```
yum install python python-pip
yum install gcc
yum install python-devel
yum install openssl-devel
yum install httpd

# Install python dependencies
pip install -r requirements.txt
# Build Docker image
docker build -t parthenos:latest .
# Run Docker container
docker run -p 8081:8081 parthenos
```
