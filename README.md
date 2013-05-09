riak-tableau
============

Sample code for exporting data from [Riak](http://basho.com/riak/) into [Tableau](http://www.tableausoftware.com/) 
via TDE (Tableau Data Extract API)

Instructions
------------

1. Install the [Riak Python client](https://github.com/basho/riak-python-client). For Windows, this means:
    * Install Python first: Download the [Python 2.7 installer](http://www.python.org/download/) for your processor architecture, install Python, 
        make sure the PATH and PYTHON_HOME system variables are set. (See [sample instructions here](http://www.varunpant.com/posts/how-to-setup-easy_install-on-windows)).
    * Install [setuptools](http://pypi.python.org/pypi/setuptools)/Easy_install. 
    * Install Protocol Buffers: ```easy_install protobuf``` (a requirement for the Riak client)
    * Install the python Riak client, either from source, or via ```easy_install riak```
2. Download the [Tableau Data Extract API](http://www.tableausoftware.com/data-extract-api) (this requires a 
    quick registration first) for your appropriate language and architecture (Windows-only, unfortunately). 
    Watch the [TDE tutorial videos](http://www.tableausoftware.com/learn/tutorials/on-demand/extract-api-introduction)
    for some walkthroughs, installation instructions and examples.
3. (Optional) Generate a fresh sample data file from Twitter (or you can use the [sample .json file provided](https://github.com/dmitrizagidulin/riak-tableau/blob/master/sf_tweets.json)):
    ```curl --user username:yourpassword -X POST -d 'locations=-123.044,36.846,-121.591,38.352' https://stream.twitter.com/1.1/statuses/filter.json > sf_tweets.json```
    (you can omit the ```locations=``` parameter filtering for the SF area, for just a general data dump from the Twitter stream).
4. If you're going to be filtering the Twitter dataset by various fields (as the ```export_search.py``` example does),
    make sure to enable Search in the Riak ```app.config``` and on the data set bucket before running the import script:
    ```search-cmd install twitter_sample``` (on the Riak cluster side)
5. Run the ```import_riak.py``` script to load the sample Twitter data from the ```.json``` file into the Riak cluster.
    (Make sure to update the hostname, port and data file path appropriately).
6. You can now run the Export scripts to produce .TDE files for use with Tableau (again, make sure to update the hostname and port 
    to point to your Riak cluster).
