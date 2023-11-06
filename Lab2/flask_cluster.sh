#!/bin/bash

sudo yum update
sudo yum -y install python3-pip 
pip3 install flask
mkdir flask_app 
cd flask_app
instance_id=$(ec2metadata --instance-id) 
echo "from flask import Flask
app = Flask(__name__)
@app.route('/cluster')
def cluster1_app():
    return 'The cluster is running successfully !'

if __name__ == \"__main__\":
       app.run(host='0.0.0.0', port=80) " | tee app.py

python3 app.py