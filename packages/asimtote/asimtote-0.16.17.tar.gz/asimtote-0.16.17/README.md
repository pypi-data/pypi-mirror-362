ASIMTOTE
========

This package contains two main elements used to compare text-based
configuration files (or other files in simple text in a similar format) where
they are structured using indented blocks of directives/commands, typically for
network devices:

* a parser to read in configuration files and stored them in a dictionary --
  the parser utilises the hierarchical nature of the configuration to
  understand that the same command name might mean different things in
  different contexts

* a comparator that takes two configuration dictionaries (typically produced by
  the parser, above) - a source and a target configuration - and writes out
  a configuration file (or update command set) to transform the source
  configuration into the destination - this uses a series of 'converters' to
  handle the difference for each configuration element (e.g. changing the
  description assigned to an interface)

Each of these are written as abstract base classes that can be inherited from
to crete concrete classes for each platform, but the base processing of the
parsing and comparing should be consistent, requiring only the specific
commands to be handled.

Currently, Cisco IOS is the only concrete platform and only a subset so far
(the comparator is still being tweaked to handle this all relatively
straightforwardly, before all the commands are implemented).  There are
currently some odd commands and edge cases which are awkward to handle without
some improvements to the core process.

The scripts also support a system whereby 'excludes' can be specified, to
exclude those elements of the configuration dictionary which should not be
compared, if a known difference exists that cannot be resolved, either as an
interim divergence, or a permanent exception.


THE NAME
--------

This package was formerly known as net-contextdiff but has been renamed as it
is expected to drop the indented configuration difference mechansim (still
using context, but not via indenting).

The new name 'asimtote' is a backronym for something like 'Autonomous System
Internetwork Management ...' but the rest has not yet been completed.  It's
similarity to 'asymptote' is deliberate as it aims to get a configuration into
a desired state but will probably never ever get there.


FUTURE DEVELOPMENTS
-------------------

Longer term, this script may be made unnecessary by other tools but, if it
remains, will probably be parsing configurations via something like REST and
JSON, rather than by reading legacy text configuration files.  It would also be
making changes using similar calls rather than generating legacy text
conversions.  The problem of making changes in the correct order and committing
them may still remain, though.

It would also be desirable to separate the parser as this could be useful
elsewhere.  At the moment, however, it's so intertwined with the converter this
would be tedious to maintain and keep in sync.  It should probably be made
easily usable as a separate component, however.
