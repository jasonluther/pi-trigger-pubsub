import os
from time import sleep

"""Methods for managing a queue using a spool directory."""


def create_spool_dir(spool_dir, user_id=None, group_id=None):
    """Create a spool directory if it does not exist."""
    if not os.path.exists(spool_dir):
        os.makedirs(spool_dir)
    if user_id is not None and group_id is not None:
        os.chown(spool_dir, user_id, group_id)


def write_spool_file(spool_dir, filename, data):
    """Write data to a file in the spool directory."""
    with open(f"{spool_dir}/{filename}.tmp", "w") as f:
        f.write(data)
    """Renaming should be an atomic operation."""
    os.rename(f"{spool_dir}/{filename}.tmp", f"{spool_dir}/{filename}")


def read_spool_file(spool_dir, filename):
    """Read data from a file in the spool directory."""
    with open(f"{spool_dir}/{filename}", "r") as f:
        return f.read()


def delete_spool_file(spool_dir, filename, archive_extension=None):
    """Delete a file in the spool directory."""
    if archive_extension is not None:
        os.rename(
            f"{spool_dir}/{filename}", f"{spool_dir}/{filename}{archive_extension}"
        )
    else:
        os.remove(f"{spool_dir}/{filename}")


def list_spool_files(spool_dir, extension=None):
    """List files in the spool directory."""
    if extension is not None:
        return [
            filename
            for filename in os.listdir(spool_dir)
            if filename.endswith(extension)
        ]
    else:
        return os.listdir(spool_dir)


def spool_loop_forever(spool_dir, process_request_func, extension=None, sleep_dur=1):
    """Process files in the spool directory."""
    while True:
        for filename in list_spool_files(spool_dir, extension):
            print("Processing spool file:", filename)
            try:
                if process_request_func(read_spool_file(spool_dir, filename)):
                    print("Completed processing spool file:", filename)
                    delete_spool_file(spool_dir, filename)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
        sleep(sleep_dur)
