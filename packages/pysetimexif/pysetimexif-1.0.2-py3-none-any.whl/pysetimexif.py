import argparse
import logging
import os
from collections.abc import Iterator
from datetime import datetime, timedelta, timezone

import exifread

__version__ = "1.0.2"

logger = logging.getLogger("exifread").addHandler(logging.NullHandler())


class InvalidTimestampError(Exception):
    pass


class NoExifDataError(Exception):
    pass


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Set 'modified timestamp' on TIFF, JPEG, PNG, Webp and HEIC files according to the embedded exif information.",
        epilog="""THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
                INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
                AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
                DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
                OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.""",
    )
    parser.add_argument(
        "-r", "--recursive", help="process paths recursively", action="store_true"
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "paths", help="one or more files or directories to process", nargs="+"
    )
    args = parser.parse_args()

    for path in args.paths:
        if os.path.isfile(path):
            set_utime(path)
        elif os.path.isdir(path):
            for filename in get_filenames(path, recursive=args.recursive):
                set_utime(filename)
        else:
            print(f"{path}: No such file or directory.")


def set_utime(filename: str) -> None:
    """Set 'modified timestamp' on file."""
    if os.path.isfile(filename):
        try:
            timestamp, offset = read_exif_time_tags(filename)
            dt = datetime_from_exif_datetime(timestamp, offset)
            os.utime(filename, (dt.timestamp(), dt.timestamp()))
            print(f"{filename}: 'modified timestamp' set to {dt}")
        except PermissionError:
            print(f"{filename}: permission denied.")
        except NoExifDataError:
            print(f"{filename}: does not contain EXIF information.")
        except InvalidTimestampError:
            print(f"{filename}: skipped due to invalid EXIF time information.")


def get_filenames(path: str, recursive: bool = False) -> Iterator[str]:
    """Yield relative filenames found within the path specfication."""
    if os.path.isdir(path):
        if recursive:
            for dirname, _, filenames in os.walk(path):
                for filename in filenames:
                    yield os.path.join(dirname, filename)
        else:
            for filename in os.listdir(path):
                yield os.path.join(path, filename)


def read_exif_time_tags(filename: str) -> tuple[str, str]:
    """Read exif timestamp and offset string fields from file."""
    with open(filename, "rb") as f:
        tags = exifread.process_file(f, details=False)
        if not tags:
            raise NoExifDataError
        timestamp = str(tags.get("EXIF DateTimeOriginal"))
        offset = str(tags.get("EXIF OffsetTimeOriginal", "+00:00"))
    return (timestamp, offset)


def datetime_from_exif_datetime(exif_date_time: str, exif_time_offset: str) -> datetime:
    """Converted exif timestamp and offset strings as datetime object."""
    offset_hours, offset_minutes = exif_time_offset[1:].split(":")
    offset = timedelta(hours=int(offset_hours), minutes=int(offset_minutes))
    tz = timezone(offset)
    try:
        dt = datetime.strptime(exif_date_time, "%Y:%m:%d %H:%M:%S")
    except ValueError as error:
        raise InvalidTimestampError from error
    return dt.replace(tzinfo=tz)


if __name__ == "__main__":
    main()
