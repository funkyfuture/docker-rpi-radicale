# Radicale calendar server Docker image for the Raspberry Pi

> The Radicale Project is a complete CalDAV (calendar) and CardDAV (contact)
> server solution.

> Calendars and address books are available for both local and remote access,
> possibly limited through authentication policies. They can be viewed and
> edited by calendar and contact clients on mobile phones or computers.

## Features enabled by this image

- configurable with config file and environment variables
- collections that are stored in the filesystem are versioned with `git`
- local passwords are hashed with `bcrypt`
- `htpasswd` for credentials management is on board

## Invokation

Here's an example configuration that is suited to manage an instance with
[`docker-compose`](https://docs.docker.com/compose/):

```yaml
version: '2'

services:
  server:
    image: funkyfuture/rpi-radicale
    restart: unless-stopped
    ports:
      - "5232:5232"
    volumes:
      - ./config:/config
      - ./collections:/collections
```

## Configuration

Refer to the Radicale documentation for a full overview of configuration
options. The following only elaborates specifics for this image.

### Interpolation

Radicale is invoked with a configuration that will be interpolated from
`/config/radicale.ini` and environment variables where the latter have
precedence.

An environment variable name must start with `R_` followed by the upper-cased
section and parameter name concentated by a `_`. E.g. this variable defintion

    R_AUTH_TYPE=ldap

is equivalent with this config file definition

    [auth]
    type = ldap


### Defaults

The following values will be added to the config if they are not defined otherwise.

- `auth`
  - `type`: `passwd`
  - `htpasswd_encryption`: `bcrypt`
  - `htpasswd_filename`: `/config/users`
- `logging`
  - `config`: `/config/logging`
- `rights`
  - `type`: `from_file`
  - `file`: `/config/rights`
- `storage`
  - `type`: `filesystem`
  - `filesystem_folder`: `/collections`


## Add users for `passwd/bcrypt` authentication method

To manage users for the default authentication setting, you can enter the
container context:

    docker exec -ti radicale_server_1 /bin/sh

If there's yet no credentials file, create one:

    su radicale
    touch /config/users

Add a user `anna`:

    htpasswd -B -C 12 /config/users anna

You'll be prompted for the new password. Invoking `htpasswd` with no arguments
will print its help.

Using `-C 12` for computing time seems to be a reasonable trade-off concerning
response time on a Raspberry Pi B+.

## Resources

###### Docker Hub repository

https://hub.docker.com/r/funkyfuture/rpi-radicale

###### Source repository

https://github.com/funkyfuture/docker-rpi-radicale

###### Radicale documentation

http://radicale.org/user_documentation
