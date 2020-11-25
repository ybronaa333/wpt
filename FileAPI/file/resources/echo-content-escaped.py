from wptserve.utils import isomorphic_encode

# Outputs the request body, with controls and non-ASCII bytes escaped
# (b"\n" becomes b"\\x0a"), and with backslashes doubled.
# As a convenience, CRLF newlines are left as is.

def escape_byte(byte):
    # Iterating over a binary string gives different types in Py2 & Py3.
    # Py3: bytes -> int
    # Py2: str -> str (of length 1), so we convert it to int
    if type(byte) is not int:
        byte = ord(byte)
    if 0 <= byte <= 0x1F or byte >= 0x7F:
        return rb"\x%02x" % byte
    if byte == ord(rb"\"):
        return rb"\\"
    return byte

def main(request, response):

    headers = [(b"X-Request-Method", isomorphic_encode(request.method)),
               (b"X-Request-Content-Length", request.headers.get(b"Content-Length", b"NO")),
               (b"X-Request-Content-Type", request.headers.get(b"Content-Type", b"NO")),
               # Avoid any kind of content sniffing on the response.
               (b"Content-Type", b"text/plain; charset=UTF-8")]

    content = b"".join(map(escape_byte, request.body)).replace(b"\\x0d\\x0a", b"\r\n")

    return headers, content
