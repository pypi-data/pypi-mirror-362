Introduction into URLs
**********************

URLs, or Uniform Resource Locators, are web addresses that specify where resources like web pages are located online.
The goal of this BalderHub project is the implementation according the defined standard in RFC 3986, which outlines
components like scheme, authority, and path.

.. note::
    URLs are a subset of URIs, focusing on resource location, with detailed rules in RFC documents.

What is a URL?
==============

A URL, or Uniform Resource Locator, is essentially a web address that f.e. tells your browser where to find a specific
resource, like a webpage, image, or video, on the internet. It includes details on how to access it, such as the
protocol (e.g., HTTP or HTTPS).

How is a URL Defined in RFC?
----------------------------

The syntax and rules for URLs are outlined in `RFC 3986 <https://www.rfc-editor.org/rfc/rfc3986.txt>`__, a standard
document by the Internet Engineering Task Force (IETF). This document defines URLs as a subset of URIs that provide a
location for resources, with components like:

**Scheme:** The protocol, like "http" or "https."
**Authority:** Includes the host (e.g., "www.example.com") and optionally a port.
**Path:** The specific location on the server, like "/path/to/resource."
**Query:** Optional parameters, like "?param=value."
**Fragment:** An optional part for a specific section, like "#section."

For example, in "https://www.example.com/path/to/resource?param=value#section," each part plays a role in locating the
resource. For more details, check `RFC 3986 <https://www.rfc-editor.org/rfc/rfc3986.txt>`__.

Detailed Analysis of URLs and RFC Definitions
=============================================

This section provides an in-depth exploration of Uniform Resource Locators (URLs) and their definition within RFC
documents, particularly focusing on the standards and historical context relevant to a project involving URL
manipulation. The analysis aims to ensure comprehensive understanding for developers working on URL-related
functionalities, ensuring alignment with internet standards.

Introduction to URLs
--------------------

URLs, or Uniform Resource Locators, are critical for identifying and locating resources on the internet, such as
web pages, images, and videos. They serve as a compact string that not only identifies a resource but also provides
a mechanism for accessing it, typically through protocols like HTTP, HTTPS, or FTP. This dual role of identification
and location distinguishes URLs as a subset of Uniform Resource Identifiers (URIs).

The importance of URLs lies in their widespread use in web browsing, API calls, and data exchange, making
standardized syntax and semantics essential for interoperability.

Historical and Current RFC Definitions
--------------------------------------

The concept of URLs was initially formalized in `RFC 1738 <https://www.rfc-editor.org/rfc/rfc1738.txt>`__, published
in December 1994 by T. Berners-Lee, L. Masinter, and M. McCahill. This document defined URLs as a compact string
representation for resources available via the internet, with a general syntax of <scheme>:<schemepart>. For
IP-based protocols, it included a common form like //<user>:<password>@<host>:<port>/<url-path>, though userinfo
components like passwords are now deprecated due to security concerns.

However, RFC 1738 has been superseded by more recent standards. The current authoritative document is
`RFC 3986 <https://www.rfc-editor.org/rfc/rfc3986.txt>`__, published in January 2005, which defines the generic syntax
for URIs and explicitly states that URLs are a subset of URIs that provide a means of locating resources by describing
their primary access mechanism, such as network location. This document updates RFC 1738 and obsoletes earlier
RFCs like `RFC 2732 <https://www.rfc-editor.org/rfc/rfc2732.txt>`__,
`RFC 2396 <https://www.rfc-editor.org/rfc/rfc2396.txt>`_, and `RFC 1808 <https://www.rfc-editor.org/rfc/rfc1808.txt>`__,
ensuring a unified approach to URI and URL syntax.

`RFC 3986 <https://www.rfc-editor.org/rfc/rfc3986.txt>`__ advises future specifications to use the general term
"URI" rather than the more restrictive "URL" or "URN," as per `RFC 3305 <https://www.rfc-editor.org/rfc/rfc3305.txt>`__,
to avoid confusion and promote flexibility. This shift reflects the evolution of internet standards toward a more
generalized framework, but for practical purposes, especially in web development, the term URL remains prevalent and
relevant.

Detailed Syntax and Components
------------------------------

The syntax for URLs, as defined in RFC 3986, follows the generic URI structure:

```
URI = scheme ":" hier-part [ "?" query ] [ "#" fragment ]
```

**hier-part** can take forms like "//" authority path-abempty, which is typical for web URLs, resulting in a common format
like ``scheme://authority/path?query#fragment``.

Breaking down the components:

* **scheme:** Starts with a letter, followed by letters, digits, "+", "-", or ".", and is case-insensitive (e.g., "http", "https"). It indicates the protocol, with registration processes detailed in BCP35.
* **authority:** Includes an optional userinfo (deprecated for security), host (e.g., domain name or IP address), and port. The host can be an IP-literal (e.g., IPv6 addresses in brackets), IPv4 address, or registered name, with case-insensitive handling and lowercase recommended for consistency.
* **path:** A sequence of segments separated by "/", can include dot-segments (".", "..") for relative references, and uses characters from unreserved, percent-encoded, sub-delims, ":", and "@".
* **query:** Indicated by "?", contains parameters, and is terminated by "#" or the end of the URI, using similar character sets as the path.
* **fragment:** Indicated by "#", identifies a specific part of the resource, with semantics depending on the media type, as per RFC2046.

For example, the URL "https://www.example.com/path/to/resource?param=value#section" illustrates:

* **scheme:** "https"
* **authority:** "www.example.com" (host, no port specified, defaults to 443 for HTTPS)
* **path:** "/path/to/resource"
* **query:** "param=value"
* **fragment:** "section"

This structure ensures URLs can be parsed and resolved consistently across systems.


Normalization and Security Considerations
-----------------------------------------

`RFC 3986 <https://www.rfc-editor.org/rfc/rfc3986>`__ also addresses normalization and equivalence, which are
important for URL manipulation. For instance, URLs like ``http://example.com`` and ``http://example.com/`` are
equivalent under HTTP rules, with an empty path normalizing to ``/``. Case-insensitive components like the host should
be normalized to lowercase, and explicit default ports (e.g., ":80" for HTTP) should be removed for brevity.

Security considerations include risks from malicious URLs, such as using non-standard port numbers
(e.g., port 25 for SMTP) to trigger unintended operations, or percent-encoded delimiters causing protocol issues.
Deprecated userinfo with passwords poses risks in logs and bookmarks, and developers should consider these when
implementing URL parsing or validation in the BalderHub project.

Comparative Analysis of RFCs
----------------------------

To illustrate the evolution, consider the following table comparing key aspects of RFC 1738 and RFC 3986:

+-----------------------+---------------------------------------+-----------------------------------------------------------+
| Aspect                | RFC 1738 (1994)                       | RFC 3986 (2005)                                           |
+=======================+=======================================+===========================================================+
| **Focus**             | Defines URLs specifically             | Defines URIs, with URLs as a subset                       |
+-----------------------+---------------------------------------+-----------------------------------------------------------+
| **Syntax**            | ``<scheme>:<schemepart>``, includes   | ``scheme ":" hier-part [ "?" query ] [ "#" fragment ]``,  |
|                       | userinfo                              | deprecates userinfo                                       |
+-----------------------+---------------------------------------+-----------------------------------------------------------+
| **Updates/Obsoletes** | Original URL standard                 | Updates                                                   |
|                       |                                       | `RFC 1738 <https://www.rfc-editor.org/rfc/rfc1738.txt>`_, |
|                       |                                       | obsoletes                                                 |
|                       |                                       | `RFC 2396 <https://www.rfc-editor.org/rfc/rfc2396.txt>`_, |
|                       |                                       | `RFC 2732 <https://www.rfc-editor.org/rfc/rfc2732.txt>`_, |
|                       |                                       | `RFC 1808 <https://www.rfc-editor.org/rfc/rfc1808.txt>`_  |
+-----------------------+---------------------------------------+-----------------------------------------------------------+
| **Security**          | Basic, no explicit deprecation of     | Explicitly deprecates userinfo for                        |
|                       | userinfo                              | security                                                  |
+-----------------------+---------------------------------------+-----------------------------------------------------------+
| **Current Relevance** | Historical, superseded                | Current standard for URI/URL syntax                       |
+-----------------------+---------------------------------------+-----------------------------------------------------------+

This table highlights the shift toward a more generalized and secure framework in
`RFC 3986 <https://www.rfc-editor.org/rfc/rfc3986.txt>`__, which is critical for modern URL handling.

Conclusion
----------

In summary, URLs are essential for locating internet resources, with their syntax and semantics defined primarily in
`RFC 3986 <https://www.rfc-editor.org/rfc/rfc3986.txt>`__, building on earlier standards like
`RFC 1738 <https://www.rfc-editor.org/rfc/rfc1738.txt>`__. This BalderHub project adheres to these standards for parsing,
normalization, and security, ensuring robust functionality in web-related operations. Developers are encouraged to
consult `RFC 3986 <https://www.rfc-editor.org/rfc/rfc3986.txt>`__ for detailed guidance and consider the historical
context from `RFC 1738 <https://www.rfc-editor.org/rfc/rfc1738.txt>`__ for legacy compatibility.