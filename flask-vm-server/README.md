# Flask Backend Server

[Flask](https://en.wikipedia.org/wiki/Flask_(web_framework)) is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. We use Flask as the backend in the cloud because its simplicity.

Our Flask application is in *app.py* and has 2 endpoints, namely */predict* & */image*.

- Endpoint */predict* will provide prediction results from images sent by the user
- Endpoint */image* will give an annotated image result

## Project Structure

    .
    ├── yolo-models                     # Pre-trained model files
        └── food.names                  # Object labels (rice, omelette, tempeh, tofu)
        └── yolov3-custom.cfg           # Model configuration
        └── yolov3-custom.weights       # Model weights              
    ├── app.py                          # Flask app serving predictions
    ├── yolo.py                         # Functions to generate predictions
    ├── requirements.txt                # Dependencies
    └── README.md


## Installation Instructions

### Create Google Compute Engine Instance

Head over to `Compute Engine > VM instances` to create a new GCE instance
- Name: ml-server (*you can customize your VM name*)
- Region: us-central1
- Machine type: g1-small
- Boot disk: Ubuntu 18.04 LTS
- Firewall: Allow HTTP & HTTPS traffic

![Google Compute Engine Instance](https://user-images.githubusercontent.com/34884046/120169256-f41e3480-c229-11eb-8066-97c13f0eec91.png)
![Google Compute Engine Instance](https://user-images.githubusercontent.com/34884046/120169403-1b750180-c22a-11eb-8d87-3d440def4cfa.png)

### Create Firewall Rule for Flask

Our Flask app will be running on port 5000 and Google Cloud, by default, doesn’t listen to port 5000. The default network in the project comes with default firewall rules "default-allow-http" and "default-allow-https" to allow traffic on port 80 and 443. We need to head over to `VPC network > Firewall` rules and create a new firewall rule to accept incoming connections and requests on the port our app will be running on.
- Name: flask-rule (*you can customize your firewall name*)
- Target tags: http-server
- Source IP ranges: 0.0.0.0/0
- TCP port: 5000

![Flask Firewall Rule](https://user-images.githubusercontent.com/34884046/120172644-75c39180-c22d-11eb-8dfe-da3f49082a5d.png)
![Flask Firewall Rule](https://user-images.githubusercontent.com/34884046/120172774-92f86000-c22d-11eb-953d-532d59743e3c.png)

### Configuring the Compute Engine Instance

1. Click the SSH button to login to the instance from your browser
![image](https://user-images.githubusercontent.com/34884046/120173833-a657fb00-c22e-11eb-9ef9-10b78e4a41e7.png)
2. Clone this repository
```
git clone https://github.com/abuwildanm/food-recognition.git
```
3. Install Miniconda to manage the dependencies and the environment
```
# update system packages and install the required packages
sudo apt-get update
sudo apt-get install bzip2 libxml2-dev libsm6 libxrender1 libfontconfig1

# download and install miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```
4. Confirm the installation. You might need to close and re-open the SSH terminal for changes to take effect after running conda init.
```
# export the full path of Miniconda to make it executable
export PATH=/home/<your name here>/miniconda3/bin:$PATH
rm Miniconda3-latest-Linux-x86_64.sh

# confirm installation
which conda
```
5. Create environtment
```
cd food-recognition/flask-vm-server
conda create -p ./env python=3.7
conda activate ./env
```

### Deploying and Testing the Flask App

1. Install the requirements/dependencies
```
pip install -r requirements.txt
```
2. Run the app
```
python app.py
```
![Flask App](https://user-images.githubusercontent.com/34884046/120177610-d0132100-c232-11eb-873c-cd8ae91c1fc0.png)
3. You can use the sample code *request_predict.py* or *request_image.py* to make a request
![prediction](https://user-images.githubusercontent.com/34884046/120178436-b4f4e100-c233-11eb-884c-eae04c8267e0.png)

### Setting up a Production Server with Gunicorn and NGINX
1. Install and start NGINX
```
cd ~
sudo apt-get install nginx-full
sudo /etc/init.d/nginx start
```
2. Create a new site configuration file
```
# remove default configuration file
sudo rm /etc/nginx/sites-enabled/default

# create a new site configuration file
sudo touch /etc/nginx/sites-available/flask_project
sudo ln -s /etc/nginx/sites-available/flask_project /etc/nginx/sites-enabled/flask_project
```
3. Edit the configuration file
```
sudo nano /etc/nginx/sites-enabled/flask_project
```
Copy and paste the code below and save the configuration file
```
server {
    location / {
        proxy_pass http://0.0.0.0:5000;
    }
}
```
4. Restart the NGINX server
```
sudo /etc/init.d/nginx restart
```
5. Bind the Flask app to the Gunicorn server 

    One important thing to keep in mind is we want the server and the Flask app keep running after we close the terminal window. Adding the daemon flag keeps the process running in background
```
cd food-recognition/flask-vm-server
gunicorn --bind 0.0.0.0:5000 app:app --daemon
```
