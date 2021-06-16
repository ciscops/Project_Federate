# GVE_DevNet_DevOps_ITSM_PoV
This is the source code for the DNA Center and Prime Infrastructure events 
dashboard. Using the APIs of DNA Center and Prime Infrastructure, we have 
developed a method to pull the events of DNA Center and Prime Infrastructure. 
The events are then displayed onto a dashboard, BMC incident tickets are 
generated for events of a specified severity, and Teams messages about the 
events are sent to a specified channel.



## Contacts
* Alexander Hoecht
* Danielle Stacy



## Solution Components
* DNA Center API
* Prime Infrastructure API
* Microsoft Teams
* BMC API
* Python 3.9
* Javascript



## Installation


#### Clone the repo
```
$ git clone https://wwwin-github.cisco.com/gve/GVE_DevNet_DevOps_ITSM_PoV
```



## Run on local machine


#### Set up virtual environment
Create and Enter a Virtual Environment (MacOS)
```
$ python3 -m venv <NAME>
$ source <NAME>/bin/activate
```


#### Set environmental settings
```
$ export FLASK_APP=src
$ export FLASK_ENV=development
```


#### Validate setup
```
# If configured correctly, this command should display the available paths of the 
application
$ flask routes
```


## Run app
```
# Initialize application database (only needed on first use)
$ flask init-db

# Start the application
$ flask run
```



## Run on Docker container


#### Build container
```
$ docker build -t [give docker container name] .
```

#### Run container
```
# -d is an optional tag to run the container in detached mode
$ docker run -d -p 5000:5000 [name given to docker container]
```



### Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)


### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)


### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)


### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)


#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
