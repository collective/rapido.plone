REST API
========

**Request**
::

    GET /:site_id/@@rapido/:app_id
    Accept: application/json

**Response**
::

    {"no_settings": {}}

Returns the Rapido application settings and set a token in the
``X-CSRF-TOKEN`` HTTP header value.

This HTTP header will have to be reused in all the requests made to the API (but
for GET requests).

**Request**
::

    GET /:site_id/@@rapido/:app_id/record/:record_id
    Accept: application/json
    X-CSRF-TOKEN: :token

**Response**
::

    {"bla": "bla", "id": "boom"}

Returns the record items.

**Request**
::

    GET /:site_id/@@rapido/:app_id/records
    Accept: application/json
    X-CSRF-TOKEN: :token

**Response**
::

    [{"path": "http://localhost:8080/demo/@@rapido/test2/record/boom", "id": "boom", "items": {"bla": "bla", "id": "boom"}}, {"path": "http://localhost:8080/demo/@@rapido/test2/record/10025657", "id": "10025657", "items": {"id": "10025657"}}, {"path": "http://localhost:8080/demo/@@rapido/test2/record/9755269", "id": "9755269", "items": {"bla": "bli", "id": "9755269"}}, {"path": "http://localhost:8080/demo/@@rapido/test2/record/8742197835653", "id": "8742197835653", "items": {"bla": "bli", "id": "8742197835653"}}, {"path": "http://localhost:8080/demo/@@rapido/test2/record/9755345", "id": "9755345", "items": {"id": "9755345"}}]

Returns all the records.

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

**Request**
::

    DELETE /:site_id/@@rapido/:app_id/record/:record_id
    Accept: application/json
    X-CSRF-TOKEN: :token

**Response**
::

    {"success": "deleted"}

Deletes the record.

**Request**
::

    POST /:site_id/@@rapido/:app_id/record/:record_id
    Accept: application/json
    X-CSRF-TOKEN: :token
    {"item1": "newvalue1"}

**Response**
::

    {"success": "updated"}

Updates the record with provided items.

**Request**
::

    PATCH /:site_id/@@rapido/:app_id/record/:record_id
    Accept: application/json
    X-CSRF-TOKEN: :token
    {"item1": "newvalue1"}

**Response**
::

    {"success": "updated"}

Updates the record with provided items.

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

**Request**
::

    POST /:site_id/@@rapido/:app_id/clear
    Accept: application/json
    X-CSRF-TOKEN: :token

**Response**
::

    {"success": "clear_storage"}

Remove all the records and delete the indexes.

**Request**
::

    POST /:site_id/@@rapido/:app_id/refresh
    Accept: application/json
    X-CSRF-TOKEN: :token

**Response**
::

    {"success": "refresh", "indexes": ["id", "total"]}

Re-declare the indexes and re-index all the records.
