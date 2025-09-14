# mcp-tutorial

## Keys

To generate R256 keys, run:

```bash
sh generate_key.pem
mv mcp-tutorial.pem jwt-server/
mv mcp-tutorial.pub.pem mcp-server/
```

It will generate the public (`mcp-tutorial.pub.pem`) and private (`mcp-tutorial.pem`) keys.

## Env Variables

Create `.env` files from `dev.env` and set the values on the folders:

- jwt-server
- mcp-server
- google-adk-agent

## Run

Run the project by doing:

```bash
docker compose up
```

To stop it, you may do:

```bash
docker compose down --rmi all
```

#

### JWT Server

Go to folder:

```bash
cd jwt-server
```

Create `.env` based on `dev.env` and set values. Then build the docker image:

```bash
docker build -t jwt-server .
```

Run it:

```bash
docker run -p 8000:8000 jwt-server
```

## Docker

To run the servers separately, you may follow the subsequent sections below.

### MCP Server

Go to folder:

```bash
cd mcp-server
```

Create `.env` based on `dev.env` and set values. Then build the docker image:

```bash
docker build -t mcp-server .
```

Run it:

```bash
docker run -p 8080:8080 mcp-server
```

### Agent Server

Go to folder:

```bash
cd google-adk-server
```

Create `fundamental_analyst/.env` based on `dev.env` and set values. Then build the docker image:

```bash
docker build -t agent-server .
```

Run it:

```bash
docker run -p 7685:7685 agent-server
```