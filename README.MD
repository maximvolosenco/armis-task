## Setup

### Clone repository
`git clone https://github.com/maximvolosenco/armis-task.git`

### Create virtual environment
`python -m venv venv`

### Activate on Windows
`venv\Scripts\activate`

### Activate on macOS/Linux
`source venv/bin/activate`

### Install dependencies
`pip install -r requirements.txt`

### Config file

Populate **api-key**, **crowdstrike-url** and **qualys-url**. Update mongo-connection-string, collection-name and database-name if you like.

## Run

### Locate project

`cd armis-task`

### Run project
`python main.py`


## Not Implemented Features

- Host Merging: The functionality to merge multiple hosts is not currently implemented.
- Time-based Host Definition: The ability to define hosts based on time parameters is not implemented.
- Tests not implemented.