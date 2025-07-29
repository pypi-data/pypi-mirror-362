import argparse
import configparser
import datetime
import http.client
import io
import os
import random
import struct
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from . import paper

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "cupless.ini"

PARSER = argparse.ArgumentParser(description='Print to a printer which supports IPP from from the command-line')
PARSER.add_argument('--ipp', help='Path of server. Read from printer.uri in ~/.config/cupless.ini')
PARSER.add_argument('file', nargs='?', type=Path, help='Input file (defaults to stdin)')
PARSER.add_argument('--extension', help='File extension (e.g. pdf, ps, txt). Used to infer type.')
PARSER.add_argument("--paper", help="Paper size (e.g., A4, Letter)")

def main():
    args = PARSER.parse_args()

    if args.ipp is None:
        config = configparser.ConfigParser()
        if not DEFAULT_CONFIG_PATH.exists():
            PARSER.error(f"--ipp not specified and default config {DEFAULT_CONFIG_PATH} does not exist")
        config.read(DEFAULT_CONFIG_PATH)

        # Example: suppose the ipp URI is under section 'printer', key 'ipp_uri'
        try:
            args.ipp = config.get("printer", "uri")
        except (configparser.NoSectionError, configparser.NoOptionError):
            PARSER.error(f"'printer' section or 'uri' key not found in {DEFAULT_CONFIG_PATH}")


    # Check printer is compatible
    response_bytes = get_ipp_attributes(args.ipp)
    try:
        response = parse_ipp_response(response_bytes)
    except Exception as e:
        raise ValueError(response_bytes) from e

    if response['status_code'] != 0:
        raise Exception(f'info request failed with status code: {response["status_code"]}')

    if 'image/pwg-raster' not in response['attributes']['document-format-supported']:
        raise Exception('image/pwg-raster not supported by printer supported formats: ({response["attributes"]["document-format-supported"]})')


    print(response)

    default_res = response['attributes'].get('printer-resolution-default')
    if not default_res:
        raise Exception('printer-resolution-default attribute missing in printer attributes')


    if not (default_res['x'] == 300 and default_res['y'] == 300 and default_res['units'] == 'dpi'):
        raise Exception(f'Default printer resolution is not 300dpi: {default_res}')

    # Read file contents
    if args.file:
        file_bytes = args.file.read_bytes()
        ext = args.extension or args.file.suffix.lstrip('.').lower()
    else:
        file_bytes = sys.stdin.buffer.read()
        ext = args.extension.lower()  # must be provided when reading from stdin

    if not ext:
        PARSER.error("You must specify --extension when reading from stdin.")

    paper_size = args.paper or paper.get_paper_size()

    # Convert to PDF if not already PDF
    if ext != 'pdf':
        paper_size = paper.get_paper_size()
        file_bytes = convert_to_pdf(paper_size, ext, file_bytes)

    # Convert PDF to PWG raster (final format for sending)
    pwg_bytes = convert_to_pwg(paper_size, file_bytes)
    print_with_ipptool(args.ipp, pwg_bytes)

def print_with_ipptool(printer_uri, pwg_bytes):
    # Write the PWG raster bytes to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".pwg", delete=True) as pwg_file:
        pwg_file.write(pwg_bytes)
        pwg_file.flush()

        # Write the test file that will use variables
        ipp_test_content = """
{
  NAME "Print file using Print-Job"
  OPERATION Print-Job

  GROUP operation-attributes-tag
  ATTR charset attributes-charset utf-8
  ATTR language attributes-natural-language en
  ATTR uri printer-uri $uri
  ATTR name requesting-user-name $user
  ATTR mimeMediaType document-format $filetype

  FILE $filename

  STATUS successful-ok
  STATUS successful-ok-ignored-or-substituted-attributes
}
"""
        with tempfile.NamedTemporaryFile('w', suffix=".test", delete=True) as test_file:
            test_file.write(ipp_test_content)
            test_file.flush()

            # Now call ipptool with the correct order and variable bindings
            result = subprocess.run([
                'ipptool',
                '-t',                              # Enable test output
                '-f', pwg_file.name,               # Default file to use
                '-d', f'user=cupless',             # Set $user (arbitrary)
                '-d', f'filetype=image/pwg-raster',# Set $filetype
                '-d', f'filename={pwg_file.name}', # Set $filename
                printer_uri,                       # This must come before test file
                test_file.name
            ], capture_output=True, text=True)

            if result.returncode != 0:
                print("ipptool error output:", result.stderr)
                raise Exception("Printing via ipptool failed")
            else:
                print("Print job submitted successfully.")
                print(result.stdout)

def build_ipp_get_printer_attributes(printer_uri):
    requested_attributes = ['document-format-supported', 'printer-resolution-default']

    version_major = 0x02
    version_minor = 0x00
    operation_id = 0x000B  # Get-Printer-Attributes
    rid = 1

    buf = io.BytesIO()

    def write_struct(fmt, *values):
        buf.write(struct.pack(fmt, *values))

    def write_attr(tag_byte: bytes, name: str, value: str):
        name_bytes = name.encode('utf-8')
        value_bytes = value.encode('utf-8')
        buf.write(tag_byte)
        write_struct('>H', len(name_bytes))
        buf.write(name_bytes)
        write_struct('>H', len(value_bytes))
        buf.write(value_bytes)

    # Version, Minor Version, Operation ID
    write_struct('!BBH', version_major, version_minor, operation_id)
    # Request ID
    write_struct('!I', rid)
    # Operation-attributes tag (1 byte)
    buf.write(b'\x01')

    # Required attributes
    write_attr(b'\x47', 'attributes-charset', 'utf-8')
    write_attr(b'\x48', 'attributes-natural-language', 'en')
    write_attr(b'\x45', 'printer-uri', printer_uri)

    # requested-attributes (multi-value)
    for i, attr in enumerate(requested_attributes):
        name = 'requested-attributes' if i == 0 else ''
        buf.write(b'\x44')  # tag for keyword
        write_struct('>H', len(name.encode('utf-8')))
        buf.write(name.encode('utf-8'))
        write_struct('>H', len(attr.encode('utf-8')))
        buf.write(attr.encode('utf-8'))

    # End of attributes tag
    buf.write(b'\x03')

    return buf.getvalue()

def get_ipp_attributes(printer_uri):
    ipp_data = build_ipp_get_printer_attributes(printer_uri)

    parsed = urlparse(printer_uri)
    if parsed.scheme != 'ipp':
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    host = parsed.hostname
    port = parsed.port or 631
    path = parsed.path

    conn = http.client.HTTPConnection(host, port)
    conn.request("POST", path, body=ipp_data, headers={
        "Content-Type": "application/ipp"
    })

    response = conn.getresponse()
    return response.read()


class BufferReader:
    def __init__(self, data: bytes):
        self.stream = io.BytesIO(data)

    def read(self, size: int) -> bytes:
        b = self.stream.read(size)
        if len(b) != size:
            raise EOFError("Unexpected end of data")
        return b

    def read_struct(self, fmt: str):
        size = struct.calcsize(fmt)
        return struct.unpack(fmt, self.read(size))

    def read_byte(self):
        return self.read(1)[0]

    def read_utf8(self, size: int) -> str:
        return self.read(size).decode('utf-8')

# Documentation for this
# https://www.rfc-editor.org/rfc/rfc8010.html#section-3.2
# https://www.rfc-editor.org/rfc/rfc8011.html#section-4.2.5.2
def parse_ipp_response(data: bytes):
    buf = BufferReader(data)

    version_major, version_minor = buf.read_struct('>BB')
    version = f'{version_major}.{version_minor}'

    status_code, request_id = buf.read_struct('>HI')

    attributes = {}
    current_name = None
    current_group = None

    while True:
        try:
            tag = buf.read_byte()
        except EOFError:
            break

        if tag == 0x03:  # end-of-attributes
            break

        # Group tags per IPP spec:
        # 0x01 = operation-attributes-tag
        # 0x02 = job-attributes-tag
        # 0x04 = printer-attributes-tag
        # 0x05 = unsupported-attributes-tag
        if tag in (0x01, 0x02, 0x04, 0x05):
            current_group = tag
            current_name = None  # reset current name for new group
            continue

        # Otherwise, this tag is a value tag for an attribute in current group
        value_tag = tag
        name_len = buf.read_struct('>H')[0]

        if name_len > 0:
            current_name = buf.read_utf8(name_len)
        elif current_name is None:
            break  # invalid response

        value_len = buf.read_struct('>H')[0]
        value_bytes = buf.read(value_len)

        # Decode value based on tag
        if value_tag == 0x21:  # boolean
            value = bool(value_bytes[0])
        elif value_tag == 0x22:  # enum
            value = struct.unpack('>I', value_bytes)[0]
        elif value_tag == 0x23:  # integer
            value = struct.unpack('>i', value_bytes)[0]
        elif value_tag == 0x32:  # resolution
            print(current_name, value_tag, 'resolution', value_len)

            # apparently
            if value_len == 6:
                x_res, y_res, units = struct.unpack('>HHB', value_bytes)
            else:
                x_res, y_res, units = struct.unpack('>IIB', value_bytes)
            units_str = {3: 'dpi', 4: 'dpcm'}[units]
            value = {'x': x_res, 'y': y_res, 'units': units_str}
        else:
            print(current_name, value_tag)
            value = value_bytes.decode('utf-8')

        if current_name not in attributes:
            attributes[current_name] = []

        attributes[current_name].append(value)

    # Flatten single-item lists
    for k, v in attributes.items():
        if len(v) == 1:
            attributes[k] = v[0]

    return {
        'version': version,
        'status_code': status_code,
        'request_id': request_id,
        'attributes': attributes
    }




def build_ipp_print_job(printer_uri, document_format, document_bytes):
    # could not get this working - decided to give up
    version_major = 0x02
    version_minor = 0x00
    operation_id = 0x0002  # Print-Job
    rid = random.randint(1, 1000000)

    buf = io.BytesIO()

    def write_struct(fmt, *values):
        buf.write(struct.pack(fmt, *values))

    def write_attr(tag_byte: bytes, name: str, value: str):
        name_bytes = name.encode('utf-8')
        value_bytes = value.encode('utf-8')
        buf.write(tag_byte)
        write_struct('>H', len(name_bytes))
        buf.write(name_bytes)
        write_struct('>H', len(value_bytes))
        buf.write(value_bytes)

    # Version, Operation ID
    write_struct('!BBH', version_major, version_minor, operation_id)
    write_struct('!I', rid)

    # Operation attributes tag
    buf.write(b'\x01')

    # Required attributes
    write_attr(b'\x47', 'attributes-charset', 'utf-8')
    write_attr(b'\x48', 'attributes-natural-language', 'en')
    write_attr(b'\x45', 'printer-uri', printer_uri)
    write_attr(b'\x44', 'document-format', document_format)
    write_attr(b'\x42', 'job-name', f'Cupless job: {datetime.datetime.now().isoformat()}')


    # End of attributes
    buf.write(b'\x03')

    # Append document data (the print job payload)
    buf.write(document_bytes)

    return buf.getvalue()


def get_paper_dimensions_pixels(paper_size, dpi=300):
    """
    Return pixel width and height for a given paper size and DPI.

    Supported paper sizes: "a4", "letter"

    Args:
        paper_size (str): "a4" or "letter" (case insensitive)
        dpi (int): dots per inch (default 300)

    Returns:
        (int, int): (width_px, height_px)
    """
    # Paper sizes in points (1 point = 1/72 inch)
    sizes_pts = {
        "letter": (612, 792),  # 8.5" x 11"
        "a4": (595, 842),      # 210mm x 297mm approx
    }

    paper_size = paper_size.lower()
    if paper_size not in sizes_pts:
        raise ValueError(f"Unsupported paper size: {paper_size}")

    width_pts, height_pts = sizes_pts[paper_size]
    width_px = int(width_pts * dpi / 72)
    height_px = int(height_pts * dpi / 72)
    return width_px, height_px


def convert_to_pwg(paper_size, pdf_bytes, dpi=300):
    width_px, height_px = get_paper_dimensions_pixels(paper_size, dpi)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as pdf_file:
        pdf_file.write(pdf_bytes)
        pdf_path = pdf_file.name

    with tempfile.NamedTemporaryFile(suffix=".pwg", delete=False) as img_file:
        img_path = img_file.name

    try:
        subprocess.run([
            "mutool", "draw",
            "-r", str(dpi),
            "-W", str(width_px),
            "-H", str(height_px),
            "-o", img_path,
            pdf_path,
        ], check=True)

        with open(img_path, "rb") as f:
            image_bytes = f.read()

    finally:
        os.remove(pdf_path)
        os.remove(img_path)

    return image_bytes

def convert_to_pdf(paper, ext, file_bytes):
    ext = ext.lower()
    if ext == 'pdf':
        # Already PDF, just return as-is
        return file_bytes

    # Otherwise, write input to a temp file and convert via pdfjam
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{ext}') as tmp_in:
        tmp_in.write(file_bytes)
        input_path = tmp_in.name

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_out:
        output_path = tmp_out.name

    try:
        cmd = [
            'pdfjam',
            '--paper', paper,
            '--fitpaper', 'true',
            '--outfile', output_path,
            input_path,
        ]
        subprocess.run(cmd, check=True)

        with open(output_path, 'rb') as f:
            pdf_data = f.read()

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

    return pdf_data
