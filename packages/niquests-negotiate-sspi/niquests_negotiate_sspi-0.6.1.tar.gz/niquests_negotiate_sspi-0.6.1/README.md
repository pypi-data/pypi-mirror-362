niquests-negotiate-sspi
=======================

This is a Python package that uses the Windows Security Support Provider Interface (SSPI) to authenticate with Kerberos/NTLM, using Negotiate and NTLM authentication schemes.

This module is a fork of requests-negotiate-sspi, which was originally written by [brandond](https://github.com/brandond/requests-negotiate-sspi).

It's built on top of the niquests library, which is a Python HTTP library for Python that functions as a drop-in replacement for the requests library, with various features and improvements over the requests library.

This module supports Extended Protection for Authentication (aka Channel Binding Hash), which makes it usable for services that require it, including Active Directory Federation Services.

Usage
-----

```python
import niquests
from niquests_negotiate_sspi import HttpNegotiateAuth

r = niquests.get('https://your.url.here', auth=HttpNegotiateAuth())
```

Options
-------

  - `username`: Username.
    Default: None

  - `password`: Password.
    Default: None

  - `domain`: NT Domain name.
    Default: None

  - `service`: Kerberos Service type for remote Service Principal
    Name.
    Default: 'HTTP'

  - `host`: Host name for Service Principal Name.
    Default: Extracted from request URI

  - `delegate`: Indicates that the user's credentials are to be delegated to the server.
    Default: False


If username and password are not specified, the user's default credentials are used. This allows for single-sign-on to domain resources if the user is currently logged on with a domain account.
