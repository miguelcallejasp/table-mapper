# Imports the Google Cloud client library
from google.cloud import datastore
from google.oauth2 import service_account

creds = service_account.Credentials.from_service_account_file('/Users/miguelcallejas/Documents/Engineering/Personal/table-mapper/src/main/gsa.json',)

# Instantiates a client
datastore_client = datastore.Client(credentials=creds, project='devops-db-resources')


# The kind for the new entity
kind = "hash"
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

lookup_key = datastore_client.key(kind, name)
result = datastore_client.get(key=lookup_key)
print(result)

query = datastore_client.query(kind='hash')

print(tu)