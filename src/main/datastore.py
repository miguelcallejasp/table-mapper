# Imports the Google Cloud client library
from google.cloud import datastore

# Instantiates a client
datastore_client = datastore.Client.from_service_account_json('gsa.json')

# The kind for the new entity
kind = "Hashed"
# The name/ID for the new entity
name = "209k0d923j0dj092j90j3d"
# The Cloud Datastore key for the new entity
task_key = datastore_client.key(kind, name)

# Prepares the new entity
task = datastore.Entity(key=task_key)
task["tenant"] = "MIGUEL"
task["thingType"] = "ITEMUPDATED"
task["other"] = "additional info"

# Saves the entity
datastore_client.put(task)

print(f"Saved {task.key.name}: {task['tenant']}")