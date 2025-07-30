import click
from azure.cosmos import CosmosClient


@click.group()
def cli():
    """Commands for managing Azure CosmosDB."""
    pass

def get_cosmos_client(endpoint, key):
    return CosmosClient(endpoint, credential=key)

@cli.command("list-databases")
@click.option("--endpoint", required=True, help="Cosmos DB endpoint URL.")
@click.option("--key", required=True, help="Cosmos DB primary key.")
def list_databases(endpoint, key):
    """Lists all databases in the CosmosDB account."""
    click.echo("Listing CosmosDB databases...")
    client = get_cosmos_client(endpoint, key)
    try:
        databases = client.list_databases()
        for db in databases:
            click.echo(f"- {db['id']}")
    except Exception as e:
        click.echo(f"Error listing databases: {e}")

@cli.command("list-containers")
@click.option("--endpoint", required=True, help="Cosmos DB endpoint URL.")
@click.option("--key", required=True, help="Cosmos DB primary key.")
@click.option("--database-name", required=True, help="Name of the database.")
def list_containers(endpoint, key, database_name):
    """Lists all containers in a specific database."""
    click.echo(f"Listing containers in database: {database_name}...")
    client = get_cosmos_client(endpoint, key)
    try:
        database = client.get_database_client(database_name)
        containers = database.list_containers()
        for container in containers:
            click.echo(f"- {container['id']}")
    except Exception as e:
        click.echo(f"Error listing containers in database {database_name}: {e}")

@cli.command("set-container-ru")
@click.option("--endpoint", required=True, help="Cosmos DB endpoint URL.")
@click.option("--key", required=True, help="Cosmos DB primary key.")
@click.option("--database-name", required=True, help="Name of the database.")
@click.option("--container-name", required=True, help="Name of the container.")
@click.option("--throughput", type=int, required=True, help="New throughput (RUs) for the container.")
def set_container_ru(endpoint, key, database_name, container_name, throughput):
    """Sets the request units (RU/s) for an existing container."""
    click.echo(f"Setting throughput for container {container_name} in database {database_name} to {throughput} RUs...")
    client = get_cosmos_client(endpoint, key)
    try:
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)
        container.replace_throughput(throughput)
        click.echo(f"Successfully updated throughput for container {container_name}.")
    except Exception as e:
        click.echo(f"Error setting throughput for container {container_name}: {e}")

@cli.command("create-container")
@click.option("--endpoint", required=True, help="Cosmos DB endpoint URL.")
@click.option("--key", required=True, help="Cosmos DB primary key.")
@click.option("--database-name", required=True, help="Name of the database where the container will be created.")
@click.option("--container-name", required=True, help="Name of the new container.")
@click.option("--partition-key-path", required=True, help="Path for the partition key (e.g., '/id').")
@click.option("--throughput", type=int, help="Optional throughput (RUs) for the container.")
def create_container(endpoint, key, database_name, container_name, partition_key_path, throughput):
    """Creates a new container in a specified database."""
    click.echo(f"Creating container {container_name} in database {database_name}...")
    client = get_cosmos_client(endpoint, key)
    try:
        database = client.get_database_client(database_name)
        container_properties = {
            'id': container_name,
            'partitionKey': {'paths': [partition_key_path]}
        }
        if throughput:
            container_properties['throughput'] = throughput
        
        database.create_container(id=container_name, partition_key=partition_key_path, offer_throughput=throughput)
        click.echo(f"Successfully created container {container_name}.")
    except Exception as e:
        click.echo(f"Error creating container {container_name}: {e}")

@cli.command("create-database")
@click.option("--endpoint", required=True, help="Cosmos DB endpoint URL.")
@click.option("--key", required=True, help="Cosmos DB primary key.")
@click.option("--database-name", required=True, help="Name of the new database.")
@click.option("--throughput", type=int, help="Optional throughput (RUs) for the database.")
def create_database(endpoint, key, database_name, throughput):
    """Creates a new database in the CosmosDB account."""
    click.echo(f"Creating database {database_name}...")
    client = get_cosmos_client(endpoint, key)
    try:
        if throughput:
            client.create_database(id=database_name, offer_throughput=throughput)
        else:
            client.create_database(id=database_name)
        click.echo(f"Successfully created database {database_name}.")
    except Exception as e:
        click.echo(f"Error creating database {database_name}: {e}")