# StatusContainer

A simple docker container to query server status.  

## Usage

The server will listen on port `9527` inside the container.

```bash
docker pull somebottle/mcstatusapi:1.0.1

docker run -d --name mcstatus --restart unless-stopped -e MC_SERVER_ADDR=mc.hypixel.net -p 5100:9527 somebottle/mcstatusapi:1.0.1
```  

Run the command above, and then the service will be available at port `5100`, try:   

```bash
curl http://localhost:5100/mcstatus
```

## Configuration

Through environment variables.  

| ENV Variable | Description |
| --- | --- |
| `MC_SERVER_ADDR` | The address of the Minecraft server to query. |
| `MC_QUERY_TIMEOUT` | The timeout for the query in seconds. Defaults to `10.0`. |
| `MC_CACHE_MAX_AGE` | The maximum age of the server status cache in seconds. Defaults to `60.0`. |
| `APP_LOG_DIR` | (**Inside the container**) The directory where the application logs will be stored. Defaults to `/app/logs`. |

## License

MIT Licensed.  