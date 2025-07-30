# flickr-photos-api

This is a library for using the Flickr API at the [Flickr Foundation].

It's *not* a general-purpose Flickr API library.
It provides a subset of Flickr API methods with the following goals:

*   Provide reusable code that can be called across all our projects.
*   Keep all the details of dealing with the Flickr API in one place.
*   Apply types to all results, so the Flickr API can be used safely in a typed context.

[Flickr Foundation]: https://www.flickr.org/

## Design

Using the Flickr API is fairly simple: you make an HTTP GET to `https://api.flickr.com/services/rest/?api_key={api_key}` and pass one or more URL query parameters.
One of those query parameters must be `method`, then you add other parameters depending on the API method.

There's an abstract class that represents this interface:

```python
import abc
from xml.etree import ElementTree as ET


class FlickrApi(abc.ABC):
    @abc.abstractmethod
    def call(self, method: str, params: dict[str, str] | None = None) -> ET.Element:
        return NotImplemented
```

The idea is that you can extend this class with "method" classes that wrap specific API methods, and make HTTP GET calls through this `call()` method:

```python
class GetSinglePhotoMethods(FlickrApi):
    def get_single_photo(self, photo_id: str) -> ET.Element:
        return self.call(method="flickr.photos.getInfo", params={"photo_id": photo_id})
```

This separates the code for making HTTP requests and separating the responses.

The library includes a single implementation of `FlickrApi` for making HTTP requests, using `httpx`, but you could swap it out if you wanted to use e.g. `requests` or `urllib3`.
This httpx implementation is the default implementation.

## Examples

```console
>>> from flickr_api import FlickrApi
>>> api = FlickrApi.with_api_key(api_key="…", user_agent="…")

>>> photo = api.get_single_photo(photo_id="14898030836")

>>> photo
{'id': '14898030836', 'title': 'NASA Scientists Says', …}

>>> photo["license"]
{'id': 'cc-by-2.0', 'label': 'CC BY 2.0', 'url': 'https://creativecommons.org/licenses/by/2.0/'}

>>> photo["url"]
'https://www.flickr.com/photos/lassennps/14898030836/'
```

## Usage

1.  Install flickr-photos-api from PyPI:

    ```console
    $ pip install flickr-photos-api
    ```

2.  Construct an instance of `FlickrApi`.

    There are two approaches you can use:

    *   You can make unauthenticated requests by passing a [Flickr API key][key] in the headers:

        ```python
        import httpx

        client = httpx.Client(params={"api_key": api_key})

        api = FlickrApi(cleint)
        ```

    *   You can make authenticated requests by using OAuth 1.0a:

        ```python
        from authlib.integrations.httpx_client import OAuth1Client

        client=OAuth1Client(
            client_id=client_id,
            client_secret=client_secret,
            token=token,
            token_secret=token_secret,
        )

        api = FlickrApi(client)
        ```

3.  Call methods on FlickrApi.
    There's no complete list of methods right now; look at the files `X_methods.py` in the `api` directory.

    Methods that return collections of photos also support `page` and `per_page` parameters to control pagination.

[key]: https://www.flickr.com/services/api/misc.api_keys.html

## Development

If you want to make changes to the library, there are instructions in [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

This project is dual-licensed as Apache-2.0 and MIT.
