REST API
========

Get the application settings
----------------------------

**Request**
::

    GET /:site_id/@@rapido/:app_id
    Accept: application/json


**Response**
::

    {"no_settings": {}}
    
**HTTP Response Headers**
::

    x-csrf-token: token
    
Returns the Rapido application settings and sets a token in the
``X-CSRF-TOKEN`` HTTP header value.

This HTTP header will have to be reused in all the requests made to the API (but
for GET requests).

Authentication
------------------
Some of the operations below require authentication before they will run successfully.
You will need to generate an Authorization String (A Base64 encoded version of your username and password separated by a dot).

Basic Authorization String
`````````````````````````````````
If your username is "john" and your password is "password", you can quickly generate the basic authorization string on the python prompt as follows::

    >>> "john.password".encode('base64','strict').strip()
    'am9obi5wYXNzd29yZA=='

Now you can use this header in all your requests::

    Authorization: Basic am9obi5wYXNzd29yZA==

.. note:: The expected X-CSRF-TOKEN will be change when you use a Basic Authorization header.

Compute an element
------------------

**Request**
::

    GET /:site_id/@@rapido/:app_id/block/:block_id/:element_id
    Accept: application/json
    X-CSRF-TOKEN: :token

or
::

    POST /:site_id/@@rapido/:app_id/block/:block_id/:element_id
    Accept: application/json
    X-CSRF-TOKEN: :token

**Response**
::

    {"something": "bla"}

Returns the value returned by the element computation. The X-CSRF-TOKEN is not
needed for a GET if the computation does not produce any change.

Get a record
------------

**Request**
::

    GET /:site_id/@@rapido/:app_id/record/:record_id
    Accept: application/json
    X-CSRF-TOKEN: :token

**Response**
::

    {"item1": "value1", "id": "boom"}

Returns the record items.

Get all the records
-------------------

**Request**
::

    GET /:site_id/@@rapido/:app_id/records
    Accept: application/json
    X-CSRF-TOKEN: :token

**Response**
::

    [{"path": "http://localhost:8080/demo/@@rapido/test2/record/boom", "id": "boom", "items": {"bla": "bla", "id": "boom"}}, {"path": "http://localhost:8080/demo/@@rapido/test2/record/10025657", "id": "10025657", "items": {"id": "10025657"}}, {"path": "http://localhost:8080/demo/@@rapido/test2/record/9755269", "id": "9755269", "items": {"bla": "bli", "id": "9755269"}}, {"path": "http://localhost:8080/demo/@@rapido/test2/record/8742197835653", "id": "8742197835653", "items": {"bla": "bli", "id": "8742197835653"}}, {"path": "http://localhost:8080/demo/@@rapido/test2/record/9755345", "id": "9755345", "items": {"id": "9755345"}}]

Returns all the records.

Create a new record
-------------------

**Request**
::

    POST /:site_id/@@rapido/:app_id
    Accept: application/json
    X-CSRF-TOKEN: :token
    {"item1": "value1"}

**Response**
::

    {"path": "http://localhost:8080/demo/@@rapido/test2/record/9755269", "id": "9755269", "success": "created"}

Creates a new record with the provided items.

Create many records
-------------------

**Request**
::

    POST /:site_id/@@rapido/:app_id/records
    Accept: application/json
    X-CSRF-TOKEN: :token
    [{"item1": "a"}, {"item1": "b", "item2": "c"}]

**Response**
::

    {"total": 2, "success": "created"}

Bulk creation of records.

Create a new record by id
-------------------------

**Request**
::

    PUT /:site_id/@@rapido/:app_id/record/:record_id
    Accept: application/json
    X-CSRF-TOKEN: :token
    {"item1": "value1"}

**Response**
::

    {"path": "http://localhost:8080/demo/@@rapido/test2/record/boom", "id": "boom", "success": "created"}

Creates a new record with the provided items and having the specified id.

Delete a record
---------------

**Request**
::

    DELETE /:site_id/@@rapido/:app_id/record/:record_id
    Accept: application/json
    X-CSRF-TOKEN: :token

**Response**
::

    {"success": "deleted"}

Deletes the record.

Remove all records
------------------

**Request**
::

    DELETE /:site_id/@@rapido/:app_id/records
    Accept: application/json
    X-CSRF-TOKEN: :token

**Response**
::

    {"success": "deleted"}

Remove all the records and delete the indexes.

Update a record
---------------

**Request**
::

    POST /:site_id/@@rapido/:app_id/record/:record_id
    Accept: application/json
    X-CSRF-TOKEN: :token
    {"item1": "newvalue1"}

or
::

    PATCH /:site_id/@@rapido/:app_id/record/:record_id
    Accept: application/json
    X-CSRF-TOKEN: :token
    {"item1": "newvalue1"}

**Response**
::

    {"success": "updated"}

Updates the record with provided items.

Search for records
------------------

**Request**
::

    POST /:site_id/@@rapido/:app_id/search
    Accept: application/json
    X-CSRF-TOKEN: :token
    {"query": "total>0", "sort_index": "total"}

**Response**
::

    [{"path": "http://localhost:8080/tutorial/@@rapido/rating/record//tutorial/news", "id": "/tutorial/news", "items": {"total": 5, "id": "/tutorial/news"}}, {"path": "http://localhost:8080/tutorial/@@rapido/rating/record//tutorial", "id": "/tutorial", "items": {"total": 8, "id": "/tutorial"}}]

Search for records.

Re-index
--------

**Request**
::

    POST /:site_id/@@rapido/:app_id/refresh
    Accept: application/json
    X-CSRF-TOKEN: :token

**Response**
::

    {"success": "refresh", "indexes": ["id", "total"]}

Re-declare the indexes and re-index all the records.
