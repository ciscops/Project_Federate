# GVE_DevNet_DevOps_ITSM_PoV

## Contacts
* Alexander Hoecht

## Solution Components
* 

## Installation/Configuration
```
# Create and Enter a Virtual Environment (MacOS)
python3 -m venv <NAME>
source <NAME>/bin/activate

# Set Environmental settings
export FLASK_APP=src
export FLASK_ENV=development
```

## Validate Setup
```
# If configured correctly, this command should display the available paths of the application
flask routes
```


## Usage
```
# Initialize application database (only needed on first use)
flask init-db

# Start the application
flask run
```


# Screenshots

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
