# brain2_oc
[![pypi version](https://img.shields.io/pypi/v/brain2-oc.svg)](https://pypi.org/project/brain2-oc) ![Custom License](https://img.shields.io/pypi/l/brain2-oc.svg)

[body_oc](https://pypi.org/project/body-oc/) 2.0 service that handles users
and permissions.

Please see [LICENSE](https://github.com/ouroboroscoding/brain2/blob/main/LICENSE)
for further information.

See [Releases](https://github.com/ouroboroscoding/brain2/blob/main/releases.md)
for changes from release to release.

## RESTlike Documentation
If you're only connecting to brain through the RESTlike API, check out the
[full documentation](https://github.com/ouroboroscoding/brain2/blob/main/rest.md)
on the individual requests.

## JavaScript/TypeScript
Also check out [@ouroboros/brain](https://www.npmjs.com/package/@ouroboros/brain)
on npm if you want to easily connect to brain in your choice of javascript /
typescript framework.

## Contents
- [Module Install](#module-install)
- [Module Configuration](#module-configuration)
  - [Example Configuration](#example-configuration)
  - [Configuration Sections](#configuration-sections)
  - [Install Tables and Records](#install-tables-and-records)
  - [Update Tables and/or Records](#upgrade-tables-andor-records)
- [Access Helper](#access-helper)
  - [Generate Key](#accessgenerate_key)
  - [Internal](#accessinternal)
  - [Internal or Verify](#accessinternal_or_verify)
  - [Verify](#accessverify)
- [Users Helper](#users-helper)
  - [Details](#usersdetails)
  - [Exists](#usersdetails)
  - [Permissions](#userspermissions)

## Module Install

### Requires
brain2_oc requires python 3.10 or higher

### Install via pip
```console
foo@bar:~$ pip install brain2_oc
```

[ [brain2_oc](#brain2_oc) / [contents](#contents) ]

## Module Configuration
Brain and all [body_oc](https://pypi.org/project/body-oc/) services use
[JSON](https://www.json.org/) to store their server side settings. For more
information on how to setup and store these configuration files, visit
[config_oc](https://pypi.org/project/config-oc/).

### Example Configuration
Below is a sample configuration file, we'll break it down section by section
immediately after.

```json
{
  "body": {
    "rest": {
      "allowed": [ "mydomain.com" ],
      "default": {
        "domain": "localhost",
        "host": "0.0.0.0",
        "protocol": "http"
      },
      "services": {
        "brain": { "port": 8000, "workers": 10 },
        "mouth": { "port": 8001, "workers": 2 }
      }
    }
  },

  "brain": {
    "data": "../.data",
    "google": false,
    "internal": {
      "redis": "session",
      "salt": "K_B.c6iUMTeESC@Z",
      "ttl": 5
    },
    "mysql": "records",
    "notify": {
      "setup": [ {
        "action": "create",
        "service": "myservice",
        "path": "user/setup"
      } ]
    },
    "portals": {
      "my_app": {
        "rights": {
          "my_service_permission": 15,
          "my_other_permission": 2
        },
        "ttl": 7884000
      }
    },
    "recaptcha": false,
    "redis": "records",
    "send_error_emails": true,
    "user_default_locale": "en-US",
    "verbose": false
  },

  "email": {
    "error_to": "me+errors@mydomain.com",
    "from": "MyApp! <contact@mydomain.com>",
    "smtp": {
      "host": "smtp.mydomain.com",
      "port": 587,
      "tls": true,
      "user": "contact@mydomain.com",
      "passwd": "********"
    }
  },

  "memory": {
    "redis": "session"
  },

  "mysql": {
    "hosts": {
      "records": {
        "host": "sql.mydomain.com",
        "charset": "utf8mb4",
        "passwd": "********"
      }
    },
    "db": "my_app"
  },

  "redis": {
    "records": {
      "host": "redis.mydomain.com",
      "db": 0
    },
    "session": {
      "host": "redis.mydomain.com",
      "db": 1
    }
  }
}
```

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) ]

### Configuration Sections
First, we'll start with the lowest level things we control, the email/smtp,
database, and caching software connection settings. Later we'll talk about other
Ouroboros Coding software, the memory, body, and brain settings.

#### email section
```json
  "email": {
    "error_to": "me+errors@mydomain.com",
    "from": "MyApp! <contact@mydomain.com>",
    "smtp": {
      "host": "smtp.mydomain.com",
      "port": 587,
      "tls": true,
      "user": "contact@mydomain.com",
      "passwd": "********"
    }
  }
```
This section will most likely exist in your project, but really only matters to
brain if the [send_error_emails](#brainsend_error_emails) config is set to
`true`.

`error_to` represents the person or person's who will receive emails whenever
brain has some sort of exception that wasn't handled.

`from` is the default email address the error email will come from.

`smtp` represents the SMTP server connection values.

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) ]

#### mysql section
```json
  "mysql": {
    "hosts": {
      "records": {
        "host": "sql.mydomain.com",
        "charset": "utf8mb4",
        "passwd": "********"
      }
    },
    "db": "my_app"
  }
```
Each object under `hosts` represents a named [MySQL](https://www.mysql.com/) or
[MariaDB](https://mariadb.org/) connection. The important part is the name, we
only have one, **records**.

For more information on what can be entered under each name, see
[rest_mysql](https://pypi.org/project/rest_mysql/).

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) ]

#### redis section
```json
  "redis": {
    "records": {
      "host": "redis.mydomain.com",
      "db": 0
    },
    "session": {
      "host": "redis.mydomain.com",
      "db": 1
    }
  }
```
Each object under the "redis" section represents a named [Redis](https://redis.io/)
connection. The important part is the name, we have two here, **records** and
**session**.

For more info on what can be put under each name, see the extensive
list on [Connecting to Redis](https://redis.readthedocs.io/en/stable/connections.html).

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) ]

#### memory section
```json
  "memory": {
    "redis": "session"
  }
```
[memory_oc](https://pypi.org/project/memory_oc/) is an Ouroboros Coding module
that handles the sessions for all services that run on the
[body_oc](https://pypi.org/project/body_oc/) framework.

It needs to know which [Redis](https://redis.io/) connection it should use to
store the session information. We have two from the redis section, **records**
and **session**, and we are telling [memory_oc](https://pypi.org/project/memory_oc/)
to use the **session** one.

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) ]

#### body section
```json
  "body": {
    "rest": {
      "allowed": [ "mydomain.com" ],
      "default": {
        "domain": "localhost",
        "host": "0.0.0.0",
        "protocol": "http"
      },
      "services": {
        "brain": { "port": 8000, "workers": 10 },
        "mouth": { "port": 8001, "workers": 2 }
      }
    }
  }
```

[body_oc](https://pypi.org/project/body_oc/) is the rest / service framework
that brain runs on top of. There's a lot of data here, but it's really only
setting up two things.

##### body.rest.allowed
Represents the domains that can make cross origin requests to the RESTlike
interface. This is mandatory if requests are being made from browsers, but in no
way affects direct requests via curl / requests / postman / etc. In this case,
we are allowing any pages across `https://mydomain.com`, this includes
`https://mydomain.com/some/page/`, `https://mydomain.com/other`, and
even `https://admin.mydomain.com/`.

To limit to a specific subdomain, change "allowed" to be more specific
```json
      "allowed": [ "admin.mydomain.com" ]
```
this way `https://admin.mydomain.com/` and `https://bob.admin.mydomain.com/`
work, but not `https://mydomain.com/`.

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) /
[body section](#body-section) ]

##### body.rest.services
Second, in order to know how to both run and connect to
[body_oc](https://pypi.org/project/body_oc/) services, we need to indicate,
what protocol, domain, and port to use to connect, what interface they will
respond to, and how many instances of each we can spin up.

In this instance we have two services, brain and [mouth](https://pypi.org/project/mouth2-oc/).
Brain is available at `http://localhost:8000` and will be running 10 threads
that will be listening on ip `0.0.0.0`, or internal only traffic. Mouth is
available at `http://localhost:8001` and will be running 2 threads that will
also be listening on ip `0.0.0.0`.

We are relying on the defaults to generate some of the data, and this is a very
simplistic initial launch setup. As we launch more servers and spread the load,
you might have the config on the brain server be something more like this where
[mouth](https://pypi.org/project/mouth2-oc/) is running on another server inside
the network.
```json
      "services": {
        "brain": {
          "domain": "localhost",
          "host": "192.168.0.1",
          "port": 80,
          "protocol": "http",
          "workers": 10
        },
        "mouth": {
          "domain": "mouth.mydomain",
          "port": 80,
          "protocol": "http"
        }
      }
```
...or like this, where it's running outside the network
```json
        "mouth": {
          "domain": "mouth.mydomain.com",
          "port": 443,
          "protocol": "https"
        }
```

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) /
[body section](#body-section) ]

#### brain section
```json
  "brain": {
    "data": "../.data",
    "google": false,
    "internal": {
      "redis": "session",
      "salt": "K_B.c6iUMTeESC@Z",
      "ttl": 5
    },
    "mysql": "records",
    "notify": {
      "setup": [ {
        "action": "create",
        "service": "myservice",
        "path": "user/setup"
      } ]
    },
    "portals": {
      "my_app": {
        "rights": {
          "my_service_permission": 15,
          "my_other_permission": 2
        },
        "ttl": 7884000
      }
    },
    "recaptcha": false,
    "redis": "records",
    "send_error_emails": true,
    "user_default_locale": "en-US",
    "verbose": false
  }
```
With the rest of the sections cleared up, hopefully the brain section is easier
to digest.

##### brain.data
A directory where brain will store any files it needs. Things like the version file
"brain.ver" which keeps track of what is [installed](#install-tables-and-records)
and [upgraded](#upgrade-tables-andor-records). We want this directory outside of
the root of brain or the project it's in, in case that folder ever gets deleted.

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) /
[brain section](#brain-section) ]

##### brain.google
Google is used with the `google/auth` POST request, see
[Google Auth create](https://github.com/ouroboroscoding/brain2/blob/main/rest.md#google-auth-create).

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) /
[brain section](#brain-section) ]

##### brain.internal
```json
    "internal": {
      "redis": "session",
      "salt": "K_B.c6iUMTeESC@Z",
      "ttl": 5
    }
```

The values are used to generate ([access.generate_key](#accessgenerate_key)) and
verify ([access.internal](#accessinternal) / [access.internal_or_verify](#accessinternal_or_verify))
internal requests between two services.

"**redis**" references one of the named connections from the
[redis configuration](#redis-configuration).

"**salt**" is a string used to encode a value.

"**ttl**" is the time to live in seconds before a message can no longer be trusted
from the source.

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) /
[brain section](#brain-section) ]

##### brain.mysql
References the only named connection from the
[mysql configuration](#mysql-configuration), **records**. This is the connection
brain will use to store its tables.

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) /
[brain section](#brain-section) ]

##### brain.notify
Notify is used to send service requests to specific endpoints based on one of
three types of things happening.

| type | description | additional |
| ---- | ----------- | ----- |
| setup | Called when the user has finished setting up their account. | `portal` and `user` set up on |
| signin | Called when the user has signed into the system. | `portal` the portal signed into. |
| signup | Called when someone has created a new account. | `portal` and `user` signed up on |

Each type can be set in the config, and expects an array of request objects with
the following keys:

| name | type | description |
| ---- | ---- | ----------- |
| action | create \| delete \| read \| update | The action to take |
| service | string | The name of the service we are calling |
| path | string | The path / noun of the endpoint to call |

Each request dict in the list will be called in the same order it is in the
array. The response will not be checked or validated in any way, nor will anyone
be notified if it fails, so make sure your endpoints work before adding them to
the config.

Requests will be passed a `user_id` string, as well as `additional` an object of
optional data, see the table above for what additional data is sent with each
type.

For the sake of security, requests are made with the
[access.generate_key](#accessgenerate_key) wrapper, so endpoints should call
[access.internal](#accessinternal) to verify the request really is from inside
the system, but it is not mandatory.

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) /
[brain section](#brain-section) ]

##### brain.portals
Here each key of the object represents a possible portal in the system. For each
portal listed, you can set

"rights" which are the default when a user is
created or signed up, see [rights](https://github.com/ouroboroscoding/brain2/blob/main/rest.md#rights)

"ttl" the time to live in seconds for any session created by a user signing in.

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) /
[brain section](#brain-section) ]

##### brain.recaptcha
Recaptcha is used with the `signup` POST request, see
[Signup create](https://github.com/ouroboroscoding/brain2/blob/main/rest.md#signup-create).

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) /
[brain section](#brain-section) ]

##### brain.redis
References one of the two named connections from the
[redis configuration](#redis-configuration), **records**. This is where brain
will stored cached versions of record data.

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) /
[brain section](#brain-section) ]

##### brain.send_error_emails
If true, error emails will be sent to the address in `config.email.error_to`
whenever a request to brain causes an uncaught exception.

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) /
[brain section](#brain-section) ]

##### brain.user_default_locale
This is the default locale to set for created and signed up users if no locale
was passed with the request.

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) /
[brain section](#brain-section) ]

##### brain.verbose
If `true` all requests to brain and the corresponding response will be printed
to stdout.

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) /
[configuration sections](#configuration-sections) /
[brain section](#brain-section) ]

### Install Tables and Records
After installing the module into the project via pip, you will need to install
the tables to your database.

```console
foo@bar:~$ source myenv/bin/activate
(myenv) foo@bar:~$ pip install brain2_oc
(myenv) foo@bar:~$ brain install
Installing tables
Setting lastest version
Please enter details to give administrator access
E-mail address: me@mydomain.com
Password:
First name: Bob
Last name: Smith
User created
Permissions added
(myenv) foo@bar:~$ deactivate
foo@bar:~$ 
```
You can also run it directly without switching environments
```console
foo@bar:~$ myenv/bin/pip install brain2_oc
foo@bar:~$ myenv/bin/brain install
```
Part of this process will be to store a file "brain.ver" in the
[brain.data](#braindata) directory with the current version of brain. This will
be used by the [upgrade](#upgrade-tables-andor-records) process to know what, if
any, scripts need to be run to update your data.

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) ]

### Upgrade Tables and/or Records
If you upgrade to a new version of brain2_oc be sure to run the upgrade script.
This will ensure any data and tables are up to date with the new version.

```console
foo@bar:~$ source myenv/bin/activate
(myenv) foo@bar:~$ brain upgrade
Already up to date
(myenv) foo@bar:~$ deactivate
foo@bar:~$ 
```
Alternatively
```console
foo@bar:~$ myenv/bin/brain upgrade
Already up to date
foo@bar:~$ 
```
This process works by checking the "brain.ver" in the [brain.data](#braindata)
directory to see what, if any, scripts need to be run to upgrade tables and/or
data. This is one reason why it's very important not to keep the [brain.data](#braindata)
directory inside your repository or some directory that might get wiped out.

Have no fear though, if the file does get wiped out, the next time the upgrade
process is run you will be prompted to pick the current version you are on and
the file will be re-created.

Take note though, the options you will be given will not correspond directly to
every version of brain2_oc, only to the versions where data or tables changed in
a way that the software couldn't support alone. When prompted, ALWAYS pick the
version which is closest to, but under, the version of brain2_oc you have
installed in your project. If you're on `8.1.0` and the choices are between
`1.0.0` and `8.1.1`, you pick `1.0.0`.

[ [brain2_oc](#brain2_oc) / [contents](#contents) /
[module configuration](#module-configuration) ]

## Access Helper
The `brain.helpers.access` module contains requests to verify both internal and
external connections requests.

### access.generate_key
When sending a request to an endpoint as an internal request, assuming it allows
it, we need the `generate_key()` method to wrap the request object and generate
the key the other end will use to validate the request.

```python
import body
from brain import access
response = body.create('brain', 'user', access.generate_key({
  'data': {
    'email': 'me@mydomain.com',
    'locale': 'en-CA',
    'first_name': 'Bob',
    'last_name': 'Smith',
    'portal': 'my_app',
    'url': 'https://mydomain.com/setup/{key}'
  }
}))
```

[ [brain2_oc](#brain2_oc) / [contents](#contents) / [access helper](#access-helper) ]

### access.internal
When writing a request that allows internal connections, we can use the
`internal()` method to verify the correct meta data was sent.

```python
from body import Service
from brain import access

class MyService(Service):
  def my_request_read(self, req: jobject) -> Response:

    # Check request is valid
    access.internal(req)

    # All good, return stuff
    return Response([ """ stuff to return """ ])
```
No return checking is required when calling `internal()` If the request is not
valid, a `ResponseException` will be raised which `body` will handle and return
to the requester as an internal key, `1203` `INTERNAL_KEY`, error.

[ [brain2_oc](#brain2_oc) / [contents](#contents) / [access helper](#access-helper) ]

### access.internal_or_verify
Sometimes we might want to allow requests on both internal connections and based
on session user permissions. In this case we can use the `internal_or_verify()`
method. If successful, the method returns either the ID of the user in the
session, or the `SYSTEM_USER_ID`, also available from `access`

`internal_or_verify()` has two arguments, `req`, like in
[access.internal](#accessinternal) above, and `permission` like in
[access.verify](#accessverify) below.

```python
from body import Service
from brain import access

class MyService(Service):
  def my_request_read(self, req: jobject) -> Response:

    # Check request is valid
    sUserID = access.internal_or_verify(req, {
      'name': 'my_other_permission',
      'right' access.READ
    })

    # If this is an internal request
    if sUserID == access.SYSTEM_USER_ID:
      # do internal stuff
      pass

    # All good, return stuff
    return Response([ """ stuff to return """ ])
```

[ [brain2_oc](#brain2_oc) / [contents](#contents) / [access helper](#access-helper) ]

### access.verify
Verify is used to make sure the session user, aka, the currently signed in user,
has the proper permissions to make a request. It's a shorthand for calling
[Verify read](https://github.com/ouroboroscoding/brain2/blob/main/rest.md#verify-read).

It has three arguments.

`session` is the current session making the request, in `body` requests this is
always `req.session`.

`permission` is the "name", "right", and optional "id" to check against.

`_return` is an optional argument which defaults to `False`. If set to `True`,
calling `access.verify` returns `False` on an error instead of raising a
`ResponseException`.

```python
from body import Service
from brain import access

class MyService(Service):
  def my_request_read(self, req: jobject) -> Response:

    # Check request is valid
    access.verify(req.session, {
      'name': 'my_other_permission',
      'right': access.READ
    })

    # All good, return stuff
    return Response([ """ stuff to return """ ])
```

`permission` can also be an array of multiple permissions to check against. If
ANY are valid, verify returns `True`.

```python
from body import Service
from brain import access

class MyService(Service):
  def my_request_read(self, req: jobject) -> Response:

    # Check request is valid
    access.verify(req.session, [{
      'name': 'my_other_permission',
      'right' access.DELETE # Fails
    }, {
      'name': 'my_service_permission',
      'right': access.READ # Succeeds, verify returns True
    }])

    # All good, return stuff
    return Response([ """ stuff to return """ ])
```

Unless the `_return` param is set to `True`, no checking of `access.verify`'s
return is required as `ResponseException` will be raised which `body` will
handle and return to the requester as an insufficient rights, `1000` `RIGHTS`,
error.

[ [brain2_oc](#brain2_oc) / [contents](#contents) / [access helper](#access-helper) ]

## Users Helper
The `brain.helpers.users` module contains methods to find out informatiom about
users in the system.

### users.details
Fetches details about one
```python
from brain import users
users.details(
  _id = '18f85e33036d11f08878ea3e7aa7d94a',
  fields = [ 'email', 'first_name', 'last_name' ]
)
```
```json
{
  "email": "me@mydomain.com",
  "first_name": "Bob",
  "last_name": "Smith"
}
```
...or many users
```python
from brain import users
users.details(
  _id = [ '18f85e33036d11f08878ea3e7aa7d94a',
          '0905dba5042e11f0b65524a3c6f47776' ],
  fields = [ 'email', 'first_name', 'last_name' ],
  order = [ 'last_name', 'first_name' ]
)
```
```json
{
  "0905dba5042e11f0b65524a3c6f47776": {
    "email": "johnnieb@gmail.com",
    "first_name": "John",
    "last_night": "Baker"
  },
  "18f85e33036d11f08878ea3e7aa7d94a": {
    "email": "me@mydomain.com",
    "first_name": "Bob",
    "last_name": "Smith"
  }
}
```
...or many users as an array
```python
from brain import users
users.details(
  _id = [ '18f85e33036d11f08878ea3e7aa7d94a',
          '0905dba5042e11f0b65524a3c6f47776' ],
  fields = [ 'email', 'first_name', 'last_name' ],
  order = [ 'last_name', 'first_name' ],
  as_dict = False
)
```
```json
[ {
  "email": "johnnieb@gmail.com",
  "first_name": "John",
  "last_night": "Baker"
}, {
  "email": "me@mydomain.com",
  "first_name": "Bob",
  "last_name": "Smith"
} ]
```

[ [brain2_oc](#brain2_oc) / [contents](#contents) / [users helper](#users-helper) ]

### users.exists
Validates if ID(s) point to valid user(s).
```python
from brain import users

# Checking a single user
# returns True
users.exists('18f85e33036d11f08878ea3e7aa7d94a')
# returns False
users.exists('blahblah')

# Checking multiple users
# returns True
users.exists([
  '18f85e33036d11f08878ea3e7aa7d94a',
  '0905dba5042e11f0b65524a3c6f47776'
])
# returns False
users.exists([
  '0905dba5042e11f0b65524a3c6f47776',
  'blahblah'
])
```

[ [brain2_oc](#brain2_oc) / [contents](#contents) / [users helper](#users-helper) ]

### users.permissions
Fetches all, or by portal, the permissions for a specific user.

```python
from brain import users
users.permissions('18f85e33036d11f08878ea3e7aa7d94a')
```
```json
{
  "my_app": {
    "my_service_permission": {
      "012345679abc4defa0123456789abcde": 15
    },
    "my_other_permission": {
      "012345679abc4defa0123456789abcde": 2
    }
  },
  "my_other_portal": {
    "my_other_other": {
      "28069c9705ac11f0ba880c6af381aee5": 6
    }
  }
}
```
by portal
```python
from brain import users
users.permissions('18f85e33036d11f08878ea3e7aa7d94a', 'my_app')
```
```json
{
  "my_service_permission": {
    "012345679abc4defa0123456789abcde": 15
  },
  "my_other_permission": {
    "012345679abc4defa0123456789abcde": 2
  }
}
```

[ [brain2_oc](#brain2_oc) / [contents](#contents) / [users helper](#users-helper) ]