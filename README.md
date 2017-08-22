# Assemblyline Client Library

The assemblyline client library facilitates issuing requests to assemblyline.

## Pre-requisites

To install the client you'll need to make sure the you have the folowing installed:

    # APT/YUM
    libffi-dev
    libssl-dev

    # pypi
    socketio-client==0.5.6
    requests
    requests[security]
    pycrypto

## Using the client

You can instantiate the client using the following snippet of code:

    from assemblyline_client import Client
    al_client = Client("https://localhost:443", auth=('user', 'password'))
    
    # or with an apikey
    
    al_client = Client("https://localhost:443", apikey=('user', 'key'))
    
    # or with a cert 
    
    al_client = Client("https://localhost:443", cert='/path/to/cert/file.pem')

The assemblyline client is fully documented in the docstrings so if you use an interactive client like ipython you can use the help feature.

    al_client.search.alert?
    Signature: al_client.search.alert(query, *args, **kwargs)
    Docstring:
    Search alerts with a SOLR query.

    Required:
    query   : SOLR query. (string)

    SOLR parameters can be passed as key/value tuples or keyword parameters.

    Returns all results.
    File:      /usr/local/lib/python2.7/dist-packages/assemblyline_client/__init__.py
    Type:      instancemethod

### Examples

#### Submit a file

Submitting a file to the system is just as simple as passing the file path

    al_client.submit('/path/to/my/file.txt')

#### Getting a key

To get a key of a given bucket, you simply need to pass it it's ID

    submission_details = al_client.submission("8c24b49d-d907-4cd3-8d74-abb24df72402")

#### Using search

You can use the search engine in the client by simply passing a SOLR query

    search_res = al_client.search.submission("submission.submitter:user")

**NOTE**: By using search like this, you'll get the exact same output that you would using strait SOLR

#### Using search iterator

Instead of using a strait search and getting a page of result, you can use the search iterator to go through all results.

    for submission in al_client.search.stream.submission("submission.submitter:user"):
        # It only return the indexed fields if you want the full thing you need to go get it
        full_submission = al_client.submission(submission['submission.sid'])

        # Then do stuff with full submission (print for example)
        print full_submission

#### Listen for message instead of querying for data

You can listen on the different message queues and execute a callback on each message.

    def callback(callback_data):
        print callback_data

    al_client.socketio.listen_on_dashboard_messages(callback)

**NOTE**: Depending on the volume of data, you might process a ton of messages!