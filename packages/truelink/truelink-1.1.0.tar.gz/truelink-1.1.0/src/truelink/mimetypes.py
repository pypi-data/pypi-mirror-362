"""Enhanced MIME type guessing module.

This module provides the same functionality as Python 3.14's mimetypes module
but works with Python 3.13 and earlier versions.

Main functions for type guessing:
- guess_type(url, strict=True) -- guess the MIME type and encoding of a URL
- guess_file_type(path, strict=True) -- guess the MIME type of a file path
- guess_extension(type, strict=True) -- guess the extension for a given MIME type
- guess_all_extensions(type, strict=True) -- guess all extensions for a MIME type
"""

from __future__ import annotations

import os
import posixpath
import urllib.parse

__all__ = [
    "MimeTypes",
    "add_type",
    "encodings_map",
    "guess_all_extensions",
    "guess_extension",
    "guess_file_type",
    "guess_type",
    "init",
    "inited",
    "knownfiles",
    "read_mime_types",
    "suffix_map",
    "types_map",
]

# Try to import Windows registry support
try:
    from _winapi import _mimetypes_read_windows_registry
except ImportError:
    _mimetypes_read_windows_registry = None

try:
    import winreg as _winreg
except ImportError:
    _winreg = None

knownfiles = [
    "/etc/mime.types",
    "/etc/httpd/mime.types",  # Mac OS X
    "/etc/httpd/conf/mime.types",  # Apache
    "/etc/apache/mime.types",  # Apache 1
    "/etc/apache2/mime.types",  # Apache 2
    "/usr/local/etc/httpd/conf/mime.types",
    "/usr/local/lib/netscape/mime.types",
    "/usr/local/etc/httpd/conf/mime.types",  # Apache 1.2
    "/usr/local/etc/mime.types",  # Apache 1.3
]

inited = False
_db = None


class MimeTypes:
    """MIME-types datastore with enhanced type detection."""

    def __init__(self, filenames=(), strict=True) -> None:
        if not inited:
            init()
        self.encodings_map = _encodings_map_default.copy()
        self.suffix_map = _suffix_map_default.copy()
        self.types_map = ({}, {})  # dict for (non-strict, strict)
        self.types_map_inv = ({}, {})
        for ext, type in _types_map_default.items():
            self.add_type(type, ext, True)
        for name in filenames:
            self.read(name, strict)

    def add_type(self, type, ext, strict=True) -> None:
        """Add a mapping between a type and an extension."""
        if ext and not ext.startswith("."):
            # Handle deprecated undotted extensions gracefully
            pass

        if not type:
            return
        self.types_map[strict][ext] = type
        exts = self.types_map_inv[strict].setdefault(type, [])
        if ext not in exts:
            exts.append(ext)

    def guess_type(self, url, strict=True):
        """Guess the type of a file which is either a URL or a path-like object."""
        url = os.fspath(url)
        p = urllib.parse.urlparse(url)
        if p.scheme and len(p.scheme) > 1:
            scheme = p.scheme
            url = p.path
        else:
            return self.guess_file_type(url, strict=strict)

        if scheme == "data":
            comma = url.find(",")
            if comma < 0:
                return None, None
            semi = url.find(";", 0, comma)
            type = url[:semi] if semi >= 0 else url[:comma]
            if "=" in type or "/" not in type:
                type = "text/plain"
            return type, None

        return self._guess_file_type(url, strict, posixpath.splitext)

    def guess_file_type(self, path, *, strict=True):
        """Guess the type of a file based on its path."""
        path = os.fsdecode(path)
        path = os.path.splitdrive(path)[1]
        return self._guess_file_type(path, strict, os.path.splitext)

    def _guess_file_type(self, path, strict, splitext):
        base, ext = splitext(path)
        ext_lower = ext.lower()
        while ext_lower in self.suffix_map:
            base, ext = splitext(base + self.suffix_map[ext_lower])
            ext_lower = ext.lower()

        if ext in self.encodings_map:
            encoding = self.encodings_map[ext]
            base, ext = splitext(base)
        else:
            encoding = None

        ext = ext.lower()
        types_map = self.types_map[True]
        if ext in types_map:
            return types_map[ext], encoding
        if strict:
            return None, encoding

        types_map = self.types_map[False]
        if ext in types_map:
            return types_map[ext], encoding
        return None, encoding

    def guess_all_extensions(self, type, strict=True):
        """Guess all extensions for a file based on its MIME type."""
        type = type.lower()
        extensions = list(self.types_map_inv[True].get(type, []))
        if not strict:
            for ext in self.types_map_inv[False].get(type, []):
                if ext not in extensions:
                    extensions.append(ext)
        return extensions

    def guess_extension(self, type, strict=True):
        """Guess the extension for a file based on its MIME type."""
        extensions = self.guess_all_extensions(type, strict)
        if not extensions:
            return None
        return extensions[0]

    def read(self, filename, strict=True) -> None:
        """Read a single mime.types-format file."""
        with open(filename, encoding="utf-8") as fp:
            self.readfp(fp, strict)

    def readfp(self, fp, strict=True) -> None:
        """Read a single mime.types-format file from file pointer."""
        for line in fp:
            words = line.split()
            for i in range(len(words)):
                if words[i][0] == "#":
                    del words[i:]
                    break
            if not words:
                continue
            type, suffixes = words[0], words[1:]
            for suff in suffixes:
                self.add_type(type, f".{suff}", strict)

    def read_windows_registry(self, strict=True) -> None:
        """Load the MIME types database from Windows registry."""
        if not _mimetypes_read_windows_registry and not _winreg:
            return

        add_type = self.add_type
        if strict:

            def add_type(type, ext):
                return self.add_type(type, ext, True)

        if _mimetypes_read_windows_registry:
            _mimetypes_read_windows_registry(add_type)
        elif _winreg:
            self._read_windows_registry(add_type)

    @classmethod
    def _read_windows_registry(cls, add_type) -> None:
        def enum_types(mimedb):
            i = 0
            while True:
                try:
                    ctype = _winreg.EnumKey(mimedb, i)
                except OSError:
                    break
                else:
                    if "\0" not in ctype:
                        yield ctype
                i += 1

        with _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, "") as hkcr:
            for subkeyname in enum_types(hkcr):
                try:
                    with _winreg.OpenKey(hkcr, subkeyname) as subkey:
                        if not subkeyname.startswith("."):
                            continue
                        mimetype, datatype = _winreg.QueryValueEx(
                            subkey, "Content Type"
                        )
                        if datatype != _winreg.REG_SZ:
                            continue
                        add_type(mimetype, subkeyname)
                except OSError:
                    continue


def guess_type(url, strict=True):
    """Guess the type of a file based on its URL."""
    if _db is None:
        init()
    return _db.guess_type(url, strict)


def guess_file_type(path, *, strict=True):
    """Guess the type of a file based on its path."""
    if _db is None:
        init()
    return _db.guess_file_type(path, strict=strict)


def guess_all_extensions(type, strict=True):
    """Guess all extensions for a file based on its MIME type."""
    if _db is None:
        init()
    return _db.guess_all_extensions(type, strict)


def guess_extension(type, strict=True):
    """Guess the extension for a file based on its MIME type."""
    if _db is None:
        init()
    return _db.guess_extension(type, strict)


def add_type(type, ext, strict=True):
    """Add a mapping between a type and an extension."""
    if _db is None:
        init()
    return _db.add_type(type, ext, strict)


def init(files=None) -> None:
    """Initialize the module."""
    global suffix_map, types_map, encodings_map
    global inited, _db
    inited = True

    if files is None or _db is None:
        db = MimeTypes()
        db.read_windows_registry()

        files = knownfiles if files is None else knownfiles + list(files)
    else:
        db = _db

    for file in files:
        if os.path.isfile(file):
            db.read(file)

    encodings_map = db.encodings_map
    suffix_map = db.suffix_map
    types_map = db.types_map[True]
    _db = db


def read_mime_types(file):
    """Read a single mime.types-format file and return types mapping."""
    try:
        f = open(file, encoding="utf-8")
    except OSError:
        return None
    with f:
        db = MimeTypes()
        db.readfp(f, True)
        return db.types_map[True]


def _default_mime_types() -> None:
    """Initialize default MIME type mappings."""
    global suffix_map, _suffix_map_default
    global encodings_map, _encodings_map_default
    global types_map, _types_map_default

    suffix_map = _suffix_map_default = {
        ".svgz": ".svg.gz",
        ".tgz": ".tar.gz",
        ".taz": ".tar.gz",
        ".tz": ".tar.gz",
        ".tbz2": ".tar.bz2",
        ".txz": ".tar.xz",
    }

    encodings_map = _encodings_map_default = {
        ".gz": "gzip",
        ".Z": "compress",
        ".bz2": "bzip2",
        ".xz": "xz",
        ".br": "br",
    }

    # Enhanced types from Python 3.14
    types_map = _types_map_default = {
        ".js": "text/javascript",
        ".mjs": "text/javascript",
        ".epub": "application/epub+zip",
        ".gz": "application/gzip",
        ".json": "application/json",
        ".webmanifest": "application/manifest+json",
        ".doc": "application/msword",
        ".dot": "application/msword",
        ".wiz": "application/msword",
        ".nq": "application/n-quads",
        ".nt": "application/n-triples",
        ".bin": "application/octet-stream",
        ".a": "application/octet-stream",
        ".dll": "application/octet-stream",
        ".exe": "application/octet-stream",
        ".o": "application/octet-stream",
        ".obj": "application/octet-stream",
        ".so": "application/octet-stream",
        ".oda": "application/oda",
        ".ogx": "application/ogg",
        ".pdf": "application/pdf",
        ".p7c": "application/pkcs7-mime",
        ".ps": "application/postscript",
        ".ai": "application/postscript",
        ".eps": "application/postscript",
        ".trig": "application/trig",
        ".m3u": "application/vnd.apple.mpegurl",
        ".m3u8": "application/vnd.apple.mpegurl",
        ".xls": "application/vnd.ms-excel",
        ".xlb": "application/vnd.ms-excel",
        ".eot": "application/vnd.ms-fontobject",
        ".ppt": "application/vnd.ms-powerpoint",
        ".pot": "application/vnd.ms-powerpoint",
        ".ppa": "application/vnd.ms-powerpoint",
        ".pps": "application/vnd.ms-powerpoint",
        ".pwz": "application/vnd.ms-powerpoint",
        ".odg": "application/vnd.oasis.opendocument.graphics",
        ".odp": "application/vnd.oasis.opendocument.presentation",
        ".ods": "application/vnd.oasis.opendocument.spreadsheet",
        ".odt": "application/vnd.oasis.opendocument.text",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".rar": "application/vnd.rar",
        ".wasm": "application/wasm",
        ".7z": "application/x-7z-compressed",
        ".bcpio": "application/x-bcpio",
        ".cpio": "application/x-cpio",
        ".csh": "application/x-csh",
        ".deb": "application/x-debian-package",
        ".dvi": "application/x-dvi",
        ".gtar": "application/x-gtar",
        ".hdf": "application/x-hdf",
        ".h5": "application/x-hdf5",
        ".latex": "application/x-latex",
        ".mif": "application/x-mif",
        ".cdf": "application/x-netcdf",
        ".nc": "application/x-netcdf",
        ".p12": "application/x-pkcs12",
        ".php": "application/x-httpd-php",
        ".pfx": "application/x-pkcs12",
        ".ram": "application/x-pn-realaudio",
        ".pyc": "application/x-python-code",
        ".pyo": "application/x-python-code",
        ".rpm": "application/x-rpm",
        ".sh": "application/x-sh",
        ".shar": "application/x-shar",
        ".swf": "application/x-shockwave-flash",
        ".sv4cpio": "application/x-sv4cpio",
        ".sv4crc": "application/x-sv4crc",
        ".tar": "application/x-tar",
        ".tcl": "application/x-tcl",
        ".tex": "application/x-tex",
        ".texi": "application/x-texinfo",
        ".texinfo": "application/x-texinfo",
        ".roff": "application/x-troff",
        ".t": "application/x-troff",
        ".tr": "application/x-troff",
        ".man": "application/x-troff-man",
        ".me": "application/x-troff-me",
        ".ms": "application/x-troff-ms",
        ".ustar": "application/x-ustar",
        ".src": "application/x-wais-source",
        ".xsl": "application/xml",
        ".rdf": "application/xml",
        ".wsdl": "application/xml",
        ".xpdl": "application/xml",
        ".yaml": "application/yaml",
        ".yml": "application/yaml",
        ".zip": "application/zip",
        ".3gp": "audio/3gpp",
        ".3gpp": "audio/3gpp",
        ".3g2": "audio/3gpp2",
        ".3gpp2": "audio/3gpp2",
        ".aac": "audio/aac",
        ".adts": "audio/aac",
        ".loas": "audio/aac",
        ".ass": "audio/aac",
        ".au": "audio/basic",
        ".snd": "audio/basic",
        ".flac": "audio/flac",
        ".mka": "audio/matroska",
        ".m4a": "audio/mp4",
        ".mp3": "audio/mpeg",
        ".mp2": "audio/mpeg",
        ".ogg": "audio/ogg",
        ".opus": "audio/opus",
        ".aif": "audio/x-aiff",
        ".aifc": "audio/x-aiff",
        ".aiff": "audio/x-aiff",
        ".ra": "audio/x-pn-realaudio",
        ".wav": "audio/vnd.wave",
        ".otf": "font/otf",
        ".ttf": "font/ttf",
        ".weba": "audio/webm",
        ".woff": "font/woff",
        ".woff2": "font/woff2",
        ".avif": "image/avif",
        ".bmp": "image/bmp",
        ".emf": "image/emf",
        ".fits": "image/fits",
        ".g3": "image/g3fax",
        ".gif": "image/gif",
        ".ief": "image/ief",
        ".jp2": "image/jp2",
        ".jpg": "image/jpeg",
        ".jpe": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".jpm": "image/jpm",
        ".jpx": "image/jpx",
        ".heic": "image/heic",
        ".heif": "image/heif",
        ".png": "image/png",
        ".svg": "image/svg+xml",
        ".t38": "image/t38",
        ".tiff": "image/tiff",
        ".tif": "image/tiff",
        ".tfx": "image/tiff-fx",
        ".ico": "image/vnd.microsoft.icon",
        ".webp": "image/webp",
        ".wmf": "image/wmf",
        ".ras": "image/x-cmu-raster",
        ".pnm": "image/x-portable-anymap",
        ".pbm": "image/x-portable-bitmap",
        ".pgm": "image/x-portable-graymap",
        ".ppm": "image/x-portable-pixmap",
        ".rgb": "image/x-rgb",
        ".xbm": "image/x-xbitmap",
        ".xpm": "image/x-xpixmap",
        ".xwd": "image/x-xwindowdump",
        ".eml": "message/rfc822",
        ".mht": "message/rfc822",
        ".mhtml": "message/rfc822",
        ".nws": "message/rfc822",
        ".gltf": "model/gltf+json",
        ".glb": "model/gltf-binary",
        ".stl": "model/stl",
        ".css": "text/css",
        ".csv": "text/csv",
        ".html": "text/html",
        ".htm": "text/html",
        ".md": "text/markdown",
        ".markdown": "text/markdown",
        ".n3": "text/n3",
        ".txt": "text/plain",
        ".bat": "text/plain",
        ".c": "text/plain",
        ".h": "text/plain",
        ".ksh": "text/plain",
        ".pl": "text/plain",
        ".srt": "text/plain",
        ".rtx": "text/richtext",
        ".rtf": "text/rtf",
        ".tsv": "text/tab-separated-values",
        ".vtt": "text/vtt",
        ".py": "text/x-python",
        ".rst": "text/x-rst",
        ".etx": "text/x-setext",
        ".sgm": "text/x-sgml",
        ".sgml": "text/x-sgml",
        ".vcf": "text/x-vcard",
        ".xml": "text/xml",
        ".mkv": "video/matroska",
        ".mk3d": "video/matroska-3d",
        ".mp4": "video/mp4",
        ".mpeg": "video/mpeg",
        ".m1v": "video/mpeg",
        ".mpa": "video/mpeg",
        ".mpe": "video/mpeg",
        ".mpg": "video/mpeg",
        ".ogv": "video/ogg",
        ".mov": "video/quicktime",
        ".qt": "video/quicktime",
        ".webm": "video/webm",
        ".avi": "video/vnd.avi",
        ".m4v": "video/x-m4v",
        ".wmv": "video/x-ms-wmv",
        ".movie": "video/x-sgi-movie",
        ".rtf": "application/rtf",
        ".apk": "application/vnd.android.package-archive",
        ".midi": "audio/midi",
        ".mid": "audio/midi",
        ".jpg": "image/jpg",
        ".pict": "image/pict",
        ".pct": "image/pict",
        ".pic": "image/pict",
        ".xul": "text/xul",
    }


# Initialize the module
_default_mime_types()
