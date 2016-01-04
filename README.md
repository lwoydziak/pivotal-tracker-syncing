# pivotal-tracker-syncing
Automatically exported from code.google.com/p/pivotal-tracker-syncing

This Python and Shell Script code repo has the basic structure: Build, Test and Source.

I. Build section

This section contains several utility scripts to look for source dependencies and resolve them, ensure that the acceptance and unit tests are passing, find various Python packages and lastly define the build parameters for an ANT based make system.

II. Test section

This section contains acceptance test to prove connections to Pivotal Tracker and Jira (with potential other tracker additions). Additionally, this repo contains support functionality for those tests.

III Source section

This contains implementation for various task primitives: Ticket, Comments, Status, Users, and Time. Additionally, it contains logical representations for the various supported trackers basically wrapping the API’s of each. It also contains various utility implementations for things like filtering, interfacing with configuration files, user mapping, singletons and syncing.

License: GNU Lesser GPL

Supports syncing with:

-Jira

-Pivotal Tracker

If you wish to run the acceptance tests, please enter an issue and the config file will be delivered to your email address
