
# Initial setup
The database is contained in a docker instance. Start by building the container. 
The API code can be run locally without a container.

```bash
docker build -t ratestask .
```

Then use docker run to start the database. Port `5433` is used instead of `5432`
to avoid conflicts with an existing database.
```bash
docker run -p 0.0.0.0:5433:5432 --name ratestask ratestask
```

The database can be accessed either with `psql` locally, or by running `psql` 
from the container.

```bash
PGPASSWORD=ratestask psql -h 127.0.0.1 -U postgres
```

```bash
docker exec -e PGPASSWORD=ratestask -it ratestask psql -U postgres
```

# API endpoints
There are two endpoints:
* rates
* status

## The _rates_ endpoint
This takes four parameters, and finds the average cost each day between ports.
The parameters are:
* date_from (start date for rates search)
* date_to (ending date for rate search)
* origin (starting location, either region or port)
* destination (ending location, either region or port)

> Note: The origin and destination can be either ports or regions, so the caller
> must make sure to use only uppercase for ports and lowercase for regions in order
> to make the name unambiguous.

The database has not been modified. The design could be improved by including
surrogate keys in the `regions` table so that the full slug name is not required in the `ports` table.