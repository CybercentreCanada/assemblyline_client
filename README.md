# Assemblyline Client Library

The assemblyline client library facilitates issuing requests to assemblyline.

## Pre-requisites

To install the client you'll need to make sure the you have the folowing installed:

    # APT/YUM
    libffi-dev
    libssl-dev

    # pypi
    pycryptodome
    requests
    requests[security]
    python-baseconv
    python-socketio[client]
    socketio-client==0.5.7.4

## Using the client

You can instantiate the client using the following snippet of code:

    # The new v4 client will test connection to detect if the server is v3 or v4. You should now use the get_client method.
    from assemblyline_client import get_client
    al_client = get_client("https://localhost:443", auth=('user', 'password'))

    # or with an apikey

    al_client = get_client("https://localhost:443", apikey=('user', 'key'))

    # or with a cert

    al_client = get_client("https://localhost:443", cert='/path/to/cert/file.pem')

    # and if your assemblyline server is using a self-signed cert

    al_client = get_client("https://localhost:443", auth=('user', 'password'), verify=False)
    al_client = get_client("https://localhost:443", auth=('user', 'password'), verify='/path/to/server.crt')

The assemblyline client is fully documented in the docstrings so if you use an interactive client like ipython you can use the help feature.

    al_client.search.alert?
    Signature: al_client.search.alert(query, *args, **kwargs)
    Docstring:
    Search alerts with a lucene query.

    Required:
    query   : Lucene query. (string)

    Search parameters can be passed as key/value tuples or keyword parameters.

    Returns all results.
    File:      /usr/local/lib/python2.7/dist-packages/assemblyline_client/__init__.py
    Type:      instancemethod

### Examples

#### Submit a file

Submitting a file to the system is just as simple as passing the file path

    al_client.submit('/path/to/my/file.txt')

#### Getting a key

To get a key of a given index, you simply need to pass it it's ID

    submission_details = al_client.submission("4nxrpBePQDLH427aA8m3TZ")

#### Using search

You can use the search engine in the client by simply passing a lucene query

    search_res = al_client.search.submission("submission.submitter:user")

#### Using search iterator

Instead of using a strait search and getting a page of result, you can use the search iterator to go through all results.

    for submission in al_client.search.stream.submission("submission.submitter:user"):
        # It only return the indexed fields if you want the full thing you need to go get it
        full_submission = al_client.submission(submission['submission.sid'])

        # Then do stuff with full submission (print for example)
        print(full_submission)

#### Using search parameters

##### Version 3

You can pass search parameters for any given query. The following examples a Lucene facet search to get the top users submitting to a server.

    kwargs = {'facet':'on', 'facet.field':'submission.submitter', 'facet.sort':'count', 'facet.limit':50, 'rows':0}  # rows=0 so that only facet results return
    c.search.submission('times.submitted:[NOW-7DAYS TO NOW]', **kwargs)

##### Version 4

Version 4 server will support facet query out of the box, no need to learn the Lucene facetting syntax.

    c.search.facet.submission('submission.submitter', query='times.submitted:[NOW-7DAYS TO NOW]')

#### Listen for message instead of querying for data

You can listen on the different message queues and execute a callback on each message.

    def callback(callback_data):
        print callback_data

    al_client.socketio.listen_on_dashboard_messages(callback)

**NOTE**: Depending on the volume of data, you might process a ton of messages!

---

# Bibliothèque cliente d’Assemblyline

La bibliothèque cliente d’Assemblyline facilite la soumission de demandes à Assemblyline.

## Exigences préalables

Avant de procéder à l’installation du client, vous devez vous assurer d’installer ce qui suit :

    # APT/YUM
    libffi-dev
    libssl-dev

    # pypi
    pycryptodome
    requests
    requests[security]
    python-baseconv
    python-socketio[client]
    socketio-client==0.5.7.4

## Utilisation du client

Vous pouvez instancier le client au moyen de l’extrait de code suivant :

    # Le nouveau client v4 détecte si le serveur est a la version 3 ou 4. Vous devez maintenant utilisé la fonction get_client.
    from assemblyline_client import get_client
    al_client = get_client("https://localhost:443", auth=('user', 'password'))

    # ou d’une clé API :

    al_client = get_client("https://localhost:443", apikey=('user', 'key'))

    # ou d’un certificat :

    al_client = get_client("https://localhost:443", cert='/path/to/cert/file.pem')

    # et si votre server assemblyline a un certificat auto-signé

    al_client = get_client("https://localhost:443", auth=('user', 'password'), verify=False)
    al_client = get_client("https://localhost:443", auth=('user', 'password'), verify='/path/to/server.crt')

Le client d’Assemblyline est pleinement documenté dans les docstrings. Si vous utilisez un client interactif comme ipython, vous serez en mesure d’utiliser la fonction d’aide.

    al_client.search.alert?
    Signature: al_client.search.alert(query, *args, **kwargs)
    Docstring:
    Search alerts with a Lucene query.

    Required:
    query   : Lucene query. (string)

    Search parameters can be passed as key/value tuples or keyword parameters.

    Returns all results.
    File:      /usr/local/lib/python2.7/dist-packages/assemblyline_client/__init__.py
    Type:      instancemethod

### Exemples

#### Soumission d’un fichier

Pour soumettre un fichier au système, il suffit d’envoyer le chemin d’accès du fichier.

    al_client.submit('/chemin/acces/de/mon/fichier.txt')

#### Obtention d’une clé

Pour obtenir une clé pour un compartiment donné, il suffit d’envoyer son ID.

    submission_details = al_client.submission("4nxrpBePQDLH427aA8m3TZ")

#### Utilisation de la recherche

Pour utiliser le moteur de recherche du client, il suffit de transmettre une demande Lucene.

    search_res = al_client.search.submission("submission.submitter:user")

#### Utilisation de l’itérateur de recherche

Plutôt que d’utiliser une recherche directe et d’obtenir une page de résultats, vous pouvez utiliser l’itérateur de recherche pour passer à travers tous les résultats.

    for submission in al_client.search.stream.submission("submission.submitter:user"):
        # Seuls les champs indexés sont renvoyés. Pour obtenir les résultats dans leur intégralité, vous devez y accéder manuellement,
        full_submission = al_client.submission(submission['submission.sid'])

        # puis faire quelque chose avec la soumission complète (imprimer, par exemple)
        print(full_submission)

#### Utilisation des paramètres de recherche

##### Version 3

Vous pouvez transmettre des paramètres de recherche pour une requête donnée. Les exemples suivants démontrent une recherche de facettes Lucene pour obtenir les utilisateurs les plus fréquants soumettant à un server.

    kwargs = {'facet':'on', 'facet.field':'submission.submitter', 'facet.sort':'count', 'facet.limit':50, 'rows':0}  # rows=0 pour que seuls les résultats de la facette soient retourné
    c.search.submission('times.submitted:[NOW-7DAYS TO NOW]', **kwargs)

##### Version 4

Le serveur version 4 supporte directement les recherches de facettes, vous navez donc pas besoin den apprendre la syntaxe.

    c.search.facet.submission('submission.submitter', query='times.submitted:[NOW-7DAYS TO NOW]')

#### L’écoute du message plutôt que la recherche de données

Vous pouvez écouter les différentes files d’attente de messages et effectuer un rappel pour chaque message.

    def callback(callback_data):
        print callback_data

    al_client.socketio.listen_on_dashboard_messages(callback)

**REMARQUE** : Selon le volume de données, vous pourriez traiter une grande quantité de messages!
