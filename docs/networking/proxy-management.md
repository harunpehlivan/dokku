# Proxy Management

> New as of 0.5.0, Enhanced in 0.6.0

```
proxy:build-config [--parallel count] [--all|<app>] # (Re)builds config for given app
proxy:clear-config [--all|<app>] # Clears config for given app
proxy:disable [--parallel count] [--all|<app>]      # Disable proxy for app
proxy:enable [--parallel count] [--all|<app>]       # Enable proxy for app
proxy:report [<app>] [<flag>]                       # Displays a proxy report for one or more apps
proxy:set <app> <proxy-type>                        # Set proxy type for app
```

In Dokku 0.5.0, port proxying was decoupled from the `nginx-vhosts` plugin into the proxy plugin. Dokku 0.6.0 introduced the ability to map host ports to specific container ports. In the future this will allow other proxy software - such as HAProxy or Caddy - to be used in place of nginx.

## Usage

### Regenerating proxy config

In certain cases, your app proxy configs may drift from the correct config for your app. You may regenerate the config at any point via the `proxy:build-config` command. This command will trigger a rebuild for the configured proxy implementation (default: nginx) for a given app. The command may fail if there are no current web listeners for your app.

```shell
dokku proxy:build-config node-js-app
```

All apps may have their proxy config rebuilt by using the `--all` flag.

```shell
dokku proxy:build-config --all
```

By default, rebuilding proxy configs for all apps happens serially. The parallelism may be controlled by the `--parallel` flag.

```shell
dokku proxy:build-config --all --parallel 2
```

Finally, the number of parallel workers may be automatically set to the number of CPUs available by setting the `--parallel` flag to `-1`

```shell
dokku proxy:build-config --all --parallel -1
```

### Clearing the generated proxy config

> New as of 0.27.0

Generated proxy configurations can also be cleared using the `proxy:clear-config` command.

```shell
dokku proxy:clear-config node-js-app
```

All apps may have their proxy config cleared by using the `--all` flag.

```shell
dokku proxy:clear-config --all
```

Clearing a proxy configuration has different effects depending on the proxy plugin in use. Consul the documentation for your proxy implementation for further details.

### Displaying proxy reports for an app

> New as of 0.8.1

You can get a report about the app's proxy status using the `proxy:report` command:

```shell
dokku proxy:report
```

```
=====> node-js-app proxy information
       Proxy enabled:       true
       Proxy type:          nginx
       Proxy port map:      http:80:5000 https:443:5000
=====> python-sample proxy information
       Proxy enabled:       true
       Proxy type:          nginx
       Proxy port map:      http:80:5000
=====> ruby-sample proxy information
       Proxy enabled:       true
       Proxy type:          nginx
       Proxy port map:      http:80:5000
```

You can run the command for a specific app also.

```shell
dokku proxy:report node-js-app
```

```
=====> node-js-app proxy information
       Proxy enabled:       true
       Proxy type:          nginx
       Proxy port map:      http:80:5000 https:443:5000
```

You can pass flags which will output only the value of the specific information you want. For example:

```shell
dokku proxy:report node-js-app --proxy-type
```

#### Proxy Port Scheme

The proxy port scheme is as follows:

- `SCHEME:HOST_PORT:CONTAINER_PORT`

The scheme metadata can be used by proxy implementations in order to properly handle proxying of requests. For example, the built-in `nginx-vhosts` proxy implementation supports the `http`, `https`, `grpc` and `grpcs` schemes. 
For the `grpc` and `grpcs` see [nginx blog post on grpc](https://www.nginx.com/blog/nginx-1-13-10-grpc/).

Developers of proxy implementations are encouraged to use whatever schemes make the most sense, and ignore configurations which they do not support. For instance, a `udp` proxy implementation can safely ignore `http` and `https` port mappings.

To change the proxy implementation in use for an application, use the `proxy:set` command:

```shell
# no validation will be performed against
# the specified proxy implementation
dokku proxy:set node-js-app nginx
```

### Proxy port mapping

See the [port management documentation](/docs/networking/port-management.md) for more information on how port mappings are managed for an application.

### Container network interface binding

> Changed as of 0.11.0

From Dokku versions `0.5.0` until `0.11.0`, enabling or disabling an application's proxy would **also** control whether or not the application was bound to all interfaces - e.g. `0.0.0.0`. As of `0.11.0`, this is now controlled by the network plugin. Please see the [network documentation](/docs/networking/network.md#container-network-interface-binding) for more information.
