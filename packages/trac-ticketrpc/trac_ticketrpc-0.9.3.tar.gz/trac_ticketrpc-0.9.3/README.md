[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<br />
<div style="text-align: center;">
  <a href="https://github.com/FrankSommer-64/trac-ticketrpc">
  </a>

<h3 align="center">trac-ticketrpc</h3>
  <p style="text-align: center;">
    Trac plugin to handle JSON RPC requests for ticket creation, update and details.
    <br />
    <a href="https://github.com/FrankSommer-64/trac-ticketrpc"><strong>Documentation</strong></a>
    <br />
    <br />
    <a href="https://github.com/FrankSommer-64/trac-ticketrpc/issues">Report Bug</a>
    ·
    <a href="https://github.com/FrankSommer-64/trac-ticketrpc/issues">Request Feature</a>
  </p>
</div>


## About The Project

The plugin is intended as an interface for software development tools which want
to use Trac as an external bug tracker.<br/>
It allows to create a new Trac ticket, post comments for a ticket, read details
of a ticket and close an existing ticket.<br/>
Project was triggered, because I wanted to use Trac from Kiwi test case management system.


## Changelog

### v0.9.3 (15 Jul 2025)
- Return Trac ticket ID in response to ticket details request

### v0.9.2 (11 Jul 2025)
- Return full ticket details in response to ticket creation request

### v0.9.1 (5 Jul 2025)
- initial Release


## Getting Started

### Prerequisites

The plugin needs Python, version 3.7 or higher and Trac, version 1.6 or higher.


### Installation

1. Make sure you are working on the local Python installation used by your trac server,
   eventually activate appropriate virtual environment

1. pip install trac_ticketrpc

1. Enable plugin by adding the following in affected trac.ini files:

    [components]<br/>
    tracticketrpc.rpctickethandler.rpctickethandler = enabled
1. Restart Trac server


### JSON RPC API

All HTTP requests must be issued using method 'POST' and contain header attributes
'Content-type'='application/json' and 'Accept'='application/json'.<br/>
Make sure to supply a session cookie for methods changing Trac repository.
This can be achieved by sending an HTTP GET request with valid credentials to Trac-Server-URL/project-name/login before the RPC request, but in the same session.<br/>
The plugin supports the methods listed below.

* Create new ticket

    method: 'ticket.create'<br/>
    mandatory parameter: 'summary', 'description', 'project'<br/>
    optional parameter: 'priority', 'version', 'component'<br/>
    result: Trac ticket data as returned by ticket details
* Add ticket comment

    method: 'ticket.add_comment'<br/>
    mandatory parameter: 'id', 'text', 'project'<br/>
    result: 'id'=Trac ticket ID, 'cnum'=comment number
* Close ticket

    method: 'ticket.close'<br/>
    mandatory parameter: 'id', 'resolution', 'project'<br/>
    optional parameter: 'text'<br/>
    result: 'id'=Trac ticket ID
* Get ticket details

    method: 'ticket.details'<br/>
    mandatory parameter: 'id', 'project'<br/>
    result: 'id', 'summary', 'reporter', 'owner', 'description', 'type', 'status', 'priority',<br/>
    'milestone', 'component', 'version', 'keywords', 'cc', 'time', 'changetime'
* Get ticket comments

    method: 'ticket.comments'<br/>
    mandatory parameter: 'id', 'project'<br/>
    result: 'id', 'comments'


## Contributing

Any contributions are **greatly appreciated**.



## License

Distributed under the MIT License. See [LICENSE][license-url] for more information.



## Contact

Frank Sommer - Frank.Sommer@sherpa-software.de

Project Link: [https://github.com/FrankSommer-64/trac-ticketrpc](https://github.com/FrankSommer-64/trac-ticketrpc)

[contributors-shield]: https://img.shields.io/github/contributors/FrankSommer-64/trac-ticketrpc.svg?style=for-the-badge
[contributors-url]: https://github.com/FrankSommer-64/trac-ticketrpc/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues/FrankSommer-64/trac-ticketrpc.svg?style=for-the-badge
[issues-url]: https://github.com/FrankSommer-64/trac-ticketrpc/issues
[license-shield]: https://img.shields.io/github/license/FrankSommer-64/trac-ticketrpc.svg?style=for-the-badge
[license-url]: https://github.com/FrankSommer-64/trac-ticketrpc/blob/master/LICENSE
