================
CODE SNIPPETS
================
TITLE: Install Supabase Realtime Client
DESCRIPTION: Installs the Supabase Realtime client package using pip.

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/realtime/README.md#_snippet_0

LANGUAGE: bash
CODE:
```
pip3 install realtime
```

--------------------------------

TITLE: Invoke Supabase Function Asynchronously
DESCRIPTION: Demonstrates how to use the `AsyncFunctionsClient` to invoke a Supabase function named 'payment-sheet' with a JSON payload. It includes setting up the client and running the asynchronous function.

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/functions/README.md#_snippet_1

LANGUAGE: python
CODE:
```
import asyncio
from supabase_functions import AsyncFunctionsClient

async def run_func():
    fc = AsyncFunctionsClient("https://<project_ref>.functions.supabase.co", {})
    res = await fc.invoke("payment-sheet", {"responseType": "json"})

if __name__ == "__main__":
    asyncio.run(run_func())
```

--------------------------------

TITLE: Create and Subscribe to a Supabase Realtime Channel
DESCRIPTION: Establishes a connection to the Supabase Realtime server and subscribes to a specified channel. It includes callback functions to handle subscription status updates, such as connection success, errors, timeouts, and unexpected closures.

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/realtime/README.md#_snippet_1

LANGUAGE: python
CODE:
```
import asyncio
from typing import Optional

from realtime import AsyncRealtimeClient, RealtimeSubscribeStates


async def main():
    REALTIME_URL = "ws://localhost:4000/websocket"
    API_KEY = "1234567890"

    socket = AsyncRealtimeClient(REALTIME_URL, API_KEY)
    channel = socket.channel("test-channel")

    def _on_subscribe(status: RealtimeSubscribeStates, err: Optional[Exception]):
        if status == RealtimeSubscribeStates.SUBSCRIBED:
            print("Connected!")
        elif status == RealtimeSubscribeStates.CHANNEL_ERROR:
            print(f"There was an error subscribing to channel: {err.args}")
        elif status == RealtimeSubscribeStates.TIMED_OUT:
            print("Realtime server did not respond in time.")
        elif status == RealtimeSubscribeStates.CLOSED:
            print("Realtime channel was unexpectedly closed.")

    await channel.subscribe(_on_subscribe)
```

--------------------------------

TITLE: Supabase Realtime Presence: Track and Sync State
DESCRIPTION: Illustrates how to use the Presence feature to track and synchronize shared state across clients in Supabase Realtime. It includes event listeners for when users join, leave, or when the presence state is synced, and demonstrates tracking a user's presence.

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/realtime/README.md#_snippet_3

LANGUAGE: python
CODE:
```
# Setup...

channel = client.channel(
    "presence-test",
    {
        "config": {
            "presence": {
                "key": ""
            }
        }
    }
)

channel.on_presence_sync(lambda: print("Online users: ", channel.presence_state()))
channel.on_presence_join(lambda new_presences: print("New users have joined: ", new_presences))
channel.on_presence_leave(lambda left_presences: print("Users have left: ", left_presences))

await channel.track({ 'user_id': 1 })
```

--------------------------------

TITLE: Install Supabase Functions Python Client
DESCRIPTION: Installs the Supabase Functions Python client using pip.

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/functions/README.md#_snippet_0

LANGUAGE: bash
CODE:
```
pip3 install supabase_functions
```

--------------------------------

TITLE: Supabase Python Library Overview
DESCRIPTION: This section provides a high-level overview of the supabase-py library, detailing its core functionalities and how to get started. It highlights key features such as authentication, real-time data synchronization, and file storage.

SOURCE: https://github.com/supabase/supabase-py/blob/main/docs/index.rst#_snippet_0

LANGUAGE: python
CODE:
```
import supabase

# Initialize Supabase client
client = supabase.create_client("YOUR_SUPABASE_URL", "YOUR_SUPABASE_ANON_KEY")

# Example: Fetching data
response = client.from_('your_table').select('*').execute()
print(response.data)

# Example: Realtime subscription

def my_realtime_callback(payload):
    print("Payload received:", payload)

client.from_('your_table').on('INSERT', my_realtime_callback).subscribe()

```

--------------------------------

TITLE: Remove All Channels
DESCRIPTION: This code example illustrates how to remove all active real-time channels managed by the Supabase Python client. It's a convenient way to clean up all real-time connections at once.

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/realtime/README.md#_snippet_7

LANGUAGE: python
CODE:
```
# Setup...

channel1 = client.channel('a-channel-to-remove')
channel2 = client.channel('another-channel-to-remove')

await channel1.subscribe()
await channel2.subscribe()

await client.remove_all_channels()
```

--------------------------------

TITLE: Remove a Single Channel
DESCRIPTION: Demonstrates the process of removing a specific real-time channel managed by the Supabase Python client. This involves creating a channel, subscribing to it, and then explicitly removing it.

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/realtime/README.md#_snippet_6

LANGUAGE: python
CODE:
```
# Setup...

channel = client.channel('some-channel-to-remove')

channel.subscribe()

await client.remove_channel(channel)
```

--------------------------------

TITLE: Proper Supabase Client Shutdown
DESCRIPTION: Ensure the Supabase client terminates correctly and prevent resource leaks by explicitly calling client.auth.sign_out().

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/supabase/README.md#_snippet_6

LANGUAGE: Python
CODE:
```
client.auth.sign_out()
```

--------------------------------

TITLE: Activate Development Environment with nix
DESCRIPTION: Enables the development environment using 'nix' with flakes enabled.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_4

LANGUAGE: nix
CODE:
```
nix develop
```

--------------------------------

TITLE: Initialize Supabase Client in Python
DESCRIPTION: Initialize the Supabase client with your Supabase URL and API key.  These should be set as environment variables. The client is then used to interact with your Supabase project.

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/supabase/README.md#_snippet_1

LANGUAGE: Python
CODE:
```
import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
```

--------------------------------

TITLE: Subscribe to PostgreSQL Changes
DESCRIPTION: This snippet demonstrates how to subscribe to various PostgreSQL database changes using the Supabase Python client. It covers subscribing to all changes in a schema, specific insert operations on a table, and updates with a filter condition. A callback function is used to process the received payloads.

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/realtime/README.md#_snippet_4

LANGUAGE: python
CODE:
```
channel = client.channel("db-changes")

channel.on_postgres_changes(
    "*",
    schema="public",
    callback=lambda payload: print("All changes in public schema: ", payload),
)

channel.on_postgres_changes(
    "INSERT",
    schema="public",
    table="messages",
    callback=lambda payload: print("All inserts in messages table: ", payload),
)

channel.on_postgres_changes(
    "UPDATE",
    schema="public",
    table="users",
    filter="username=eq.Realtime",
    callback=lambda payload: print(
        "All updates on users table when username is Realtime: ", payload
    ),
)

channel.subscribe(
    lambda status, err: status == RealtimeSubscribeStates.SUBSCRIBED
    and print("Ready to receive database changes!")
)
```

--------------------------------

TITLE: Initialize Supabase Python Client
DESCRIPTION: This Python snippet demonstrates how to initialize the Supabase client using the `create_client` function. It retrieves the Supabase URL and API key from environment variables, which is a recommended practice for security.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_7

LANGUAGE: python
CODE:
```
import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
```

--------------------------------

TITLE: Call Supabase Edge Functions
DESCRIPTION: Invoke an Edge Function with the Supabase client.  Handles potential errors during the function call and prints the error message.

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/supabase/README.md#_snippet_4

LANGUAGE: Python
CODE:
```
def test_func():
  try:
    resp = supabase.functions.invoke("hello-world", invoke_options={'body':{}})
    return resp
  except (FunctionsRelayError, FunctionsHttpError) as exception:
    err = exception.to_dict()
    print(err.get("message"))
```

--------------------------------

TITLE: Invoke Supabase Edge Function
DESCRIPTION: This Python snippet shows how to call a Supabase Edge Function by its name using the `invoke` method. It includes error handling for `FunctionsRelayError` and `FunctionsHttpError`, demonstrating how to catch and print function-related exceptions.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_15

LANGUAGE: python
CODE:
```
def test_func():
  try:
    resp = supabase.functions.invoke("hello-world", invoke_options={'body':{}})
    return resp
  except (FunctionsRelayError, FunctionsHttpError) as exception:
    err = exception.to_dict()
    print(err.get("message"))
```

--------------------------------

TITLE: Supabase Query Builder
DESCRIPTION: Detailed documentation on using the query builder for interacting with your Supabase database. This includes methods for selecting, filtering, inserting, updating, and deleting data, along with advanced query capabilities.

SOURCE: https://github.com/supabase/supabase-py/blob/main/docs/index.rst#_snippet_1

LANGUAGE: python
CODE:
```
# Example: Building a complex query
query = client.from_('users').select('id, name, email').filter('is_active', 'eq', 'true').order('name', ascending=True)
result = query.execute()

```

--------------------------------

TITLE: Supabase Realtime Broadcast: Send and Receive Messages
DESCRIPTION: Demonstrates how to send and receive ephemeral messages on a Supabase Realtime channel using the Broadcast feature. It configures broadcast options like acknowledgments and self-delivery, and sets up a listener for incoming messages.

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/realtime/README.md#_snippet_2

LANGUAGE: python
CODE:
```
# Setup...

channel = client.channel(
    "broadcast-test", {"config": {"broadcast": {"ack": False, "self": False}}}
)

await channel.on_broadcast("some-event", lambda payload: print(payload)).subscribe()
await channel.send_broadcast("some-event", {"hello": "world"})
```

--------------------------------

TITLE: Install supabase-py
DESCRIPTION: Install the supabase-py package using pip, uv, or conda. This package requires Python 3.9 or higher.

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/supabase/README.md#_snippet_0

LANGUAGE: Bash
CODE:
```
# with pip
pip install supabase

# with uv
uv add supabase

# with conda
conda install -c conda-forge supabase
```

--------------------------------

TITLE: Clone Supabase-py Repository
DESCRIPTION: Clones the supabase-py GitHub repository and navigates into the project directory.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_0

LANGUAGE: bash
CODE:
```
git clone https://github.com/supabase/supabase-py.git
cd supabase-py
```

--------------------------------

TITLE: Supabase Storage Bucket API Methods
DESCRIPTION: This section details the methods available for interacting with Supabase Storage Buckets via the supabase-py library. It covers operations such as creating, retrieving, updating, and deleting buckets, as well as managing bucket permissions and files within buckets.

SOURCE: https://github.com/supabase/supabase-py/blob/main/docs/storage_bucket.rst#_snippet_0

LANGUAGE: APIDOC
CODE:
```
StorageBucketAPI:
  __init__(client: SupabaseClient)
    Initializes the StorageBucketAPI with a SupabaseClient instance.
    client: An authenticated SupabaseClient object.

  create_bucket(name: str, options: dict = None)
    Creates a new storage bucket.
    Parameters:
      name: The name for the new bucket.
      options: Optional configuration for the bucket (e.g., public access).
    Returns: A dictionary representing the created bucket.

  list_buckets()
    Retrieves a list of all storage buckets.
    Returns: A list of dictionaries, each representing a bucket.

  get_bucket(id_or_name: str)
    Retrieves a specific storage bucket by its ID or name.
    Parameters:
      id_or_name: The unique identifier or name of the bucket.
    Returns: A dictionary representing the specified bucket.

  update_bucket(id_or_name: str, options: dict)
    Updates an existing storage bucket.
    Parameters:
      id_or_name: The unique identifier or name of the bucket to update.
      options: A dictionary containing the updated bucket settings.
    Returns: A dictionary representing the updated bucket.

  delete_bucket(id_or_name: str)
    Deletes a storage bucket.
    Parameters:
      id_or_name: The unique identifier or name of the bucket to delete.
    Returns: A dictionary indicating the result of the deletion.

  get_bucket_public_url(bucket_name: str, file_path: str)
    Generates the public URL for a file within a bucket.
    Parameters:
      bucket_name: The name of the bucket.
      file_path: The path to the file within the bucket.
    Returns: The public URL of the file.
```

--------------------------------

TITLE: Local Installation
DESCRIPTION: Installs the supabase-py package in editable mode using pip, allowing for direct code modifications.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_5

LANGUAGE: bash
CODE:
```
pip install -e .
```

--------------------------------

TITLE: Conventional Commits Example
DESCRIPTION: An example of how to format commit messages using the Conventional Commits specification for documentation updates.

SOURCE: https://github.com/supabase/supabase-py/blob/main/CONTRIBUTING.md#_snippet_0

LANGUAGE: git
CODE:
```
docs(extension-name) updated installation documentation
```

--------------------------------

TITLE: Execute Supabase-py Test Suite
DESCRIPTION: This command runs the test scripts for the Supabase Python client library. It connects to a pre-populated test database instance, which includes a `countries` table.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_22

LANGUAGE: bash
CODE:
```
./test.sh
```

--------------------------------

TITLE: Get All Instantiated Channels
DESCRIPTION: This section shows how to retrieve a list of all channels that have been instantiated by the Supabase Python client. This is useful for monitoring or managing active real-time connections.

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/realtime/README.md#_snippet_5

LANGUAGE: python
CODE:
```
# Setup...

client.get_channels()
```

--------------------------------

TITLE: Supabase Authentication: Sign-up and Sign-in
DESCRIPTION: Sign-up a new user or sign-in an existing user using email and password with Supabase authentication.  The email and password are required inputs.

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/supabase/README.md#_snippet_2

LANGUAGE: Python
CODE:
```
# Sign-up
user = supabase.auth.sign_up({ "email": users_email, "password": users_password })

# Sign-in
user = supabase.auth.sign_in_with_password({ "email": users_email, "password": users_password })
```

--------------------------------

TITLE: Activate Virtual Environment with venv
DESCRIPTION: Creates a virtual environment using Python's built-in 'venv' module and activates it.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_2

LANGUAGE: bash
CODE:
```
python3 -m venv env
source env/bin/activate  # On Windows, use .\env\Scripts\activate
```

--------------------------------

TITLE: Activate Virtual Environment with uv
DESCRIPTION: Creates a virtual environment using 'uv' and activates it, followed by synchronizing dependencies.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_1

LANGUAGE: bash
CODE:
```
uv venv supabase-py
source supabase-py/bin/activate
uv sync
```

--------------------------------

TITLE: Supabase Storage Operations: Download, Upload, Remove, List, Move
DESCRIPTION: Perform storage operations such as downloading, uploading, removing, listing, and moving files in a Supabase storage bucket.  Each operation requires specifying the bucket name and file paths.

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/supabase/README.md#_snippet_5

LANGUAGE: Python
CODE:
```
# Download a file from Storage
bucket_name: str = "photos"

data = supabase.storage.from_(bucket_name).download("photo1.png")

# Upload a file
bucket_name: str = "photos"
new_file = getUserFile()

data = supabase.storage.from_(bucket_name).upload("/user1/profile.png", new_file)

# Remove a file
bucket_name: str = "photos"

data = supabase.storage.from_(bucket_name).remove(["old_photo.png", "image5.jpg"])

# List all files
bucket_name: str = "charts"

data = supabase.storage.from_(bucket_name).list()

# Move and rename files
bucket_name: str = "charts"
old_file_path: str = "generic/graph1.png"
new_file_path: str = "important/revenue.png"

data = supabase.storage.from_(bucket_name).move(old_file_path, new_file_path)
```

--------------------------------

TITLE: Proper Supabase Client Shutdown in Python
DESCRIPTION: To ensure the Supabase client terminates correctly and to prevent resource leaks, you must explicitly call the `sign_out()` method on the `auth` object of your client instance.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_21

LANGUAGE: python
CODE:
```
client.auth.sign_out()
```

--------------------------------

TITLE: Sign Up a New User with Supabase Auth
DESCRIPTION: This Python snippet shows how to register a new user with an email and password using the Supabase authentication service. The `sign_up` method returns the user object upon successful creation.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_8

LANGUAGE: python
CODE:
```
user = supabase.auth.sign_up({ "email": users_email, "password": users_password })
```

--------------------------------

TITLE: Supabase Storage Buckets
DESCRIPTION: Documentation for managing files and interacting with Supabase Storage. This covers uploading, downloading, and deleting files, as well as managing bucket permissions and configurations.

SOURCE: https://github.com/supabase/supabase-py/blob/main/docs/index.rst#_snippet_2

LANGUAGE: python
CODE:
```
# Example: Uploading a file
with open("path/to/your/file.txt", "rb") as f:
    upload_response = client.storage.from_('your_bucket').upload('folder/file.txt', f)

# Example: Downloading a file
with open("downloaded_file.txt", "wb") as f:
    download_response = client.storage.from_('your_bucket').download_public('folder/file.txt')
    f.write(download_response.data)

```

--------------------------------

TITLE: Activate Virtual Environment with conda
DESCRIPTION: Creates and activates a virtual environment named 'supabase-py' using the 'conda' package manager.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_3

LANGUAGE: conda
CODE:
```
conda create --name supabase-py
conda activate supabase-py
```

--------------------------------

TITLE: Supabase Database Operations: Insert, Select, Update, Delete
DESCRIPTION: Perform basic database operations such as inserting, selecting, updating, and deleting data from a Supabase table.  Each operation requires specifying the table name and any necessary conditions.

SOURCE: https://github.com/supabase/supabase-py/blob/main/src/supabase/README.md#_snippet_3

LANGUAGE: Python
CODE:
```
# Insert Data
data = supabase.table("countries").insert({"name":"Germany"}).execute()

# Assert we pulled real data.
assert len(data.data) > 0

# Select Data
data = supabase.table("countries").select("*").eq("country", "IL").execute()

# Assert we pulled real data.
assert len(data.data) > 0

# Update Data
data = supabase.table("countries").update({"country": "Indonesia", "capital_city": "Jakarta"}).eq("id", 1).execute()

# Update data with duplicate keys
country = {
  "country": "United Kingdom",
  "capital_city": "London" # This was missing when it was added
}

data = supabase.table("countries").upsert(country).execute()
assert len(data.data) > 0

# Delete Data
data = supabase.table("countries").delete().eq("id", 1).execute()
```

--------------------------------

TITLE: Select Data from Supabase Table
DESCRIPTION: This Python snippet demonstrates how to query and retrieve data from a Supabase table. It uses the `select` method to specify columns (or all with `*`) and `eq` to filter results based on a condition, followed by `execute()`.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_11

LANGUAGE: python
CODE:
```
data = supabase.table("countries").select("*").eq("country", "IL").execute()

# Assert we pulled real data.
assert len(data.data) > 0
```

--------------------------------

TITLE: Upsert Data into Supabase Table
DESCRIPTION: This Python snippet demonstrates how to perform an 'upsert' operation, which inserts a new row if it doesn't exist or updates it if it does. It's useful for handling data with potential duplicate keys gracefully.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_13

LANGUAGE: python
CODE:
```
country = {
  "country": "United Kingdom",
  "capital_city": "London" # This was missing when it was added
}

data = supabase.table("countries").upsert(country).execute()
assert len(data.data) > 0
```

--------------------------------

TITLE: Set Supabase Environment Variables
DESCRIPTION: This snippet shows how to set the `SUPABASE_URL` and `SUPABASE_KEY` environment variables in your shell. These variables are crucial for the Supabase client to connect to your specific Supabase instance securely.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_6

LANGUAGE: bash
CODE:
```
export SUPABASE_URL="my-url-to-my-awesome-supabase-instance"
export SUPABASE_KEY="my-supa-dupa-secret-supabase-api-key"
```

--------------------------------

TITLE: Upload File to Supabase Storage
DESCRIPTION: This Python snippet shows how to upload a new file to a Supabase Storage bucket. It specifies the destination path within the bucket and the file content to be uploaded.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_17

LANGUAGE: python
CODE:
```
bucket_name: str = "photos"
new_file = getUserFile()

data = supabase.storage.from_(bucket_name).upload("/user1/profile.png", new_file)
```

--------------------------------

TITLE: Download File from Supabase Storage
DESCRIPTION: This Python snippet demonstrates how to download a file from a specified Supabase Storage bucket. It uses the `download` method, providing the file path within the bucket.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_16

LANGUAGE: python
CODE:
```
bucket_name: str = "photos"

data = supabase.storage.from_(bucket_name).download("photo1.png")
```

--------------------------------

TITLE: Insert Data into Supabase Table
DESCRIPTION: This Python snippet illustrates how to insert a new row into a specified Supabase table. It uses the `insert` method, chaining it with `execute()` to perform the operation and retrieve the result.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_10

LANGUAGE: python
CODE:
```
data = supabase.table("countries").insert({"name":"Germany"}).execute()

# Assert we pulled real data.
assert len(data.data) > 0
```

--------------------------------

TITLE: Remove Files from Supabase Storage
DESCRIPTION: This Python snippet illustrates how to delete one or more files from a Supabase Storage bucket. It accepts a list of file paths to be removed.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_18

LANGUAGE: python
CODE:
```
bucket_name: str = "photos"

data = supabase.storage.from_(bucket_name).remove(["old_photo.png", "image5.jpg"])
```

--------------------------------

TITLE: Delete Data from Supabase Table
DESCRIPTION: This Python snippet illustrates how to delete rows from a Supabase table. It uses the `delete` method combined with `eq` to specify the criteria for deletion.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_14

LANGUAGE: python
CODE:
```
data = supabase.table("countries").delete().eq("id", 1).execute()
```

--------------------------------

TITLE: Move and Rename Files in Supabase Storage
DESCRIPTION: This Python snippet shows how to move a file from one path to another within a Supabase Storage bucket, effectively allowing for renaming or reorganizing files. It requires both the old and new file paths.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_20

LANGUAGE: python
CODE:
```
bucket_name: str = "charts"
old_file_path: str = "generic/graph1.png"
new_file_path: str = "important/revenue.png"

data = supabase.storage.from_(bucket_name).move(old_file_path, new_file_path)
```

--------------------------------

TITLE: List Files in Supabase Storage Bucket
DESCRIPTION: This Python snippet demonstrates how to list all files within a specified Supabase Storage bucket. It provides an overview of the bucket's contents.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_19

LANGUAGE: python
CODE:
```
bucket_name: str = "charts"

data = supabase.storage.from_(bucket_name).list()
```

--------------------------------

TITLE: Update Data in Supabase Table
DESCRIPTION: This Python snippet shows how to update existing rows in a Supabase table. It uses the `update` method with a dictionary of new values and `eq` to specify which rows to update based on a condition.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_12

LANGUAGE: python
CODE:
```
data = supabase.table("countries").update({"country": "Indonesia", "capital_city": "Jakarta"}).eq("id", 1).execute()
```

--------------------------------

TITLE: Sign In an Existing User with Supabase Auth
DESCRIPTION: This Python snippet demonstrates how to authenticate an existing user using their email and password via the Supabase authentication service. The `sign_in_with_password` method returns the authenticated user object.

SOURCE: https://github.com/supabase/supabase-py/blob/main/README.md#_snippet_9

LANGUAGE: python
CODE:
```
user = supabase.auth.sign_in_with_password({ "email": users_email, "password": users_password })
```