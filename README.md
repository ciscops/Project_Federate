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



## Run on local machine (Not Recommended)


#### Install Dependencies with Package Manager
<b>Mac OS</b>
Install Homebrew
Find documentation and instructions for installing Homebrew on https://brew.sh/

Then install nmap 
```
$ brew install nmap
```


<b>Windows</b>
Install Chocolatey
Find documentation and instructions for install Chocolatey on https://chocolatey.org/

Then install nmap
```
$ choco install nmap
```


<b>Linux</b>
Install nmap with apt-get
```
$ apt-get install nmap
```


#### Set up virtual environment
Create and Enter a Virtual Environment (MacOS and Linux)
```
$ python3 -m venv <NAME>
$ source <NAME>/bin/activate
```


Create and Enter a Virtual Environment (Windows)
```
$ py -m venv <NAME>
$ .\env\Scripts\activate
```


#### Install Python modules
Use pip to install the requirements listed in the requirements.txt file
```
$ pip install -r requirements.txt
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


#### Run app
```
# Initialize application database (only needed on first use)
$ flask init-db

# Start the application
$ flask run
```



## Run on Docker container (Recommended)


#### Build container
```
$ docker build -t [give docker container name] .
```

#### Run container
```
# -d is an optional tag to run the container in detached mode
$ docker run -d -p 5000:5000 [name given to docker container]
```



## Usage


#### Access dashboard
You may access the dashboard by opening the browser of your choice and 
entering the address 127.0.0.1:5000 


#### Log In/Register User
From here, you may sign in. If you have not registered a user yet, click the 
Register button on the sidebar and register a username and password Then 
sign in with those credentials. 


#### Using the dashboard
Once you have signed in, you will be taken to a page to enter your 
credentials for DNA Center, Prime Infrastructure, BMC Remedy ITSM, and 
Microsoft Teams channel. When entering the credentials for these systems do 
not include http or https at the start of the ip address or url. Then click 
the Apply Settings button.

After the settings are applied, the dashboard opens to the home page. At the 
top of the home page, the connection status to your DNA Center, Prime 
Infrastructure, BMC Remedy ITSM, and Microsoft Teams channel is displayed. 
Below the connection statuses, the dashboard displays the number of DNAC and 
Prime Infrastructure events at the time of logging into the dashboard. 

Clicking on the number of events will open a new page, displaying all the 
events associated with the system you clicked on.

The home page updates periodically, pulling in the new events from DNAC and 
Prime Infrastructure. The number updates to show the number of new events 
that have occurred since the last time the dashboard updated. If no new 
events have occurred, it will show 0 new events. Clicking on the number will
still take you to the page displaying all the events associated with the 
system you clicked on. Every event that has occurred since logging on will 
still be visible on these pages.



### Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

Login page

![/IMAGES/login.png](/IMAGES/login.png)

Settings page

![/IMAGES/settings.png](/IMAGES/settings.png)

Home page

![/IMAGES/home-page.png](/IMAGES/home-page.png)

Events logs pages

![/IMAGES/dnac-logs.png](/IMAGES/dnac-logs.png)

![/IMAGES/prime-logs.png](/IMAGES/prime-logs.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)


### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)


### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)


#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
