# YT_API

This is a project that gets video data from given youtube channels (through the add_channel.py file), stores said data in a JSON file, and then plots that data (via visual.ipynb).

## Requirements

- Python 3
- Jupyter Notebook
- Pandas library
- ipywidgets library
- dotenv library

## Usage

First download code from this repo.

To add a channel to the data.json file, run command:

`python [PATH OF CODE FOLDER]/add_channel.py [YOUTUBE ID OF CHANNEL TO ADD] [NO. OF VIDEOS]`

For example, if 10 is provided as the [NO. OF VIDEOS], then data will be collected on the 10 most recent videos from the specified channel.
50 is the maximum value that can be provided as [NO. OF VIDEOS].
The default value of [NO. OF VIDEOS] is 25 (i.e if no number is provided, data will be collected on the 25 most recent videos).

To visualize collected channel data, access & run visual.ipynb in jupyter notebooks.
