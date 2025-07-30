# asimtote.diff
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



"""Configuration differences converter module.

This module contains abstract classes and functions to convert
configurations (as a whole and individual elements) given the
differences between two configurations.
"""



# --- imports ---



from itertools import chain
import sys

from deepops import (
    deepdiff, deepfilter, deepget, deepremoveitems, deepsetdefault)

import yaml

from .misc import deepselect



# --- constants ---



# different debugging levels and what they mean (they're used in lots of
# places so it seems sensible to avoid hard coding the values, in case
# anything changes)

DEBUG_CONVERT_MATCH = 1         # matching class and action type only
DEBUG_CONVERT_STEPS = 2         # include working steps
DEBUG_CONVERT_PARAMS = 3        # include old/new/remove/update arguments
DEBUG_CONVERT_NODIFF = 4        # include skipped converters or no action
DEBUG_CONVERT_NOMATCH = 5       # include non-matching converters

# maximum debug level
DEBUG_CONVERT_MAX = DEBUG_CONVERT_NOMATCH



# --- functions ---



def pathstr(path, wildcard_indices=set()):
    """This function converts a path, which is a list of items of
    various types (typically strings and integers), into a string,
    useful for debugging messages.

    The items are separated by commas and elements which are None are
    converted to a '*' since they're wildcards.

    If the index of the item in the path is in the wildcard_indices
    list, that item is prefixed with "*=" to show it matched a wildcard.
    The default for this parameter is an empty list, which causes no
    index to match.

    If we just printed the list, it would by in the more verbose Python
    format, with surrounding square brackets, quotes around strings and
    None for a wildcard, which is a little less readable.
    """

    return ':'.join([ ("*=" if i in wildcard_indices else "") + str(v)
                            for i, v in enumerate(path) ])



# --- classes ---



class Convert:
    """This abstract class handles converting the difference between an
    old ('from') configuration item to the corresponding new ('to')
    configuration item.

    The main difference process will use deepops.deepdiff() to work out
    what has been removed and what updated (added/changed) between the
    two configurations.

    Individual differences are checked using child classes, which
    specify the part of the configuration directionaries where they
    occur and the remove() and update() methods called.  For example, if
    the hostname is changed, a 'hostname' converter would specify the
    part of the configuration dictionary where the hostname is stored
    and the update() method would return the commands required to change
    it to the new value.

    The methods called to do the conversions (documented in the methods
    themselves) are:

    * add(new, *args) -- appears in the new configuration but was not
      present in the old configuration; calls update(None, new, new,
      *args) by default.

    * delete(old, rem, new, *args) -- appears in the old configuration
      but is not present in the new configuration; calls remove(old,
      *args) by default)

    * remove(old, *args) -- appears in the old configuration but is not
      present in the new configuration; calls truncate(old, old, None,
      *args) by default.

    * truncate(old, rem, new, *args) -- appears in the remove
      differences but still exists in the new configuration - i.e. is
      being partially removed.

    * update(old, upd, new, *args) -- appers in the update differences
      and existed in the old configuration - i.e. is being changed or
      added to.

    * trigger(new, *args) -- called when a trigger causes a converter to
      fire, and would not otherwise, e.g. with a remove() or update(),
      as a remove() or update() has not been called, nothing has been
      changed in the configuration, so only a 'new' argument is
      supplied; calls update(new, None, new, *args) by default.

    In addition, there are some filter methods which are called with the
    same wildcard arguments as the conversion action methods, above.  If
    this returns a false value, this particular conversion will be
    skipped:

    * filter_delete() - called before a delete(), remove() or
      truncate().

    * filter_update() - called before an add() or update().

    * filter_trigger() - called before a trigger().

    * filter() - by default, the above method calls the same filter()
      method allowing all conversion actions to be filtered in one
      place.

    In most cases, only the remove() and update() methods need defining
    as the add() and trigger() methods call update(), and truncate() is
    rarely required, but there some odd cases where they are, hence
    their inclusion.

    The 'context', 'cmd' and 'ext' parameters, below, are all tuples
    giving parts of the path through the keys of the configuration
    dictionary to match for the specific converter.  These can be
    literal keys, the value None, or a set.  The value None or a set
    specify a wildcard match to any value or limited to the specified
    set of values.  For example, '("interface", None)' to match all
    interfaces; ("redistribute", { "connected", "static" }) will match
    only connected or static redistributions.

    The part of the configuration dictionary that matches the 'context +
    cmd' parts of the path will be passed as the 'old/new' and 'rem/upd'
    parameters to the action methods.

    The child classes can override the following values:

    context -- the path to the context containing the commands used in
    this conversion: if this context is removed in its entirety, the
    remove() action for this converter will not be called as the
    removal of the context will remove it; this variable defaults to
    the empty tuple, for a command at the top level

    cmd -- the path for this command in the configuration, following
    the context; this part of the dictionary will be passed in the
    'old/new' and 'rem/upd' parameters to the action methods; this
    variable defaults to None and must be defined by a child class

    ext -- an extension to path which must be matched, but this part is
    not used to further specify the part of the dictionaries passed to
    the action functions for the 'old/new' and 'rem/upd' parameters:
    this is useful when a higher level in the configuration dictionary
    is required in the action function

    block -- the block of configuration in which this converter is to be
    applied (see DiffConfig)

    trigger_blocks -- a set of block names to be triggered when a match
    is made against this converter and the conversion methods return
    some output (i.e. commands to do the conversion)

    empty_trigger -- if this is set to True, the converter will always
    fire the named triggers, even if the converter generated no output

    context_offset -- this is used by the get_args() method to adjust
    the boundary between the context and cmd+ext parts when fetching
    wildcard argument values to be passed to converter methods: it
    defaults to 0, causing it to use the natural boundary between the
    context and cmd/ext) but can be adjusted to (typically) negative
    values and include part of the context as the local arguments
    """


    context = tuple()
    cmd = None    # leave as None to cause an error if not defined in child
    ext = tuple()
    block = None
    sort_key = None
    trigger_blocks = set()
    empty_trigger = False
    context_offset = 0


    def __init__(self):
        """The constructor just precalculates some details to optimise
        the repeated processing of the converter matches.
        """

        # to avoid confusing error messages, just check all the
        # definitions for this converter class are all tuples and not
        # something like simple strings
        if not (isinstance(self.context, tuple)):
            raise TypeError("%s: definition not tuple: context"
                                % type(self).__name__)
        if not (isinstance(self.cmd, tuple)):
            raise TypeError("%s: definition not tuple: cmd"
                                % type(self).__name__)
        if not (isinstance(self.ext, tuple)):
            raise TypeError("%s: definition not tuple: ext"
                                % type(self).__name__)

        # calculate and store a few things, for efficiency
        self._path_full = self.context + self.cmd + self.ext
        self._context_len = len(self.context)
        self._path_len = len(self.context + self.cmd)

        # store the set of indices of wildcard elements of the path (we
        # need these to get the argument list to pass to the converter
        # action methods)
        self.wildcard_indices = [
            i for i, v in enumerate(self._path_full)
                if (v is None) or isinstance(v, set) ]

        # set _context_args value for this converter, specifies the
        # number of wildcard arguments in the context (vs the cmd+ext),
        # and used by get_args() method
        #
        # by default, this counts the number of wildcard arguments in
        # the context but can be adjusted with context_offset
        #
        # this is useful when writing converters which can work in
        # several different contexts (such as those for commands in BGP
        # configuration)
        #
        # if set to negative values, additional wildcard arguments from
        # the context will be included in the cmd/ext side; positive
        # values will shift the other way
        self._context_args = (
            len([ i for i, v in enumerate(self.context)
                     if (v is None) or isinstance(v, set) ])
            + self.context_offset)


    def _path_matches(self, d, path):
        """This method is used to recursively step along the paths.  It
        is initially called by full_matches() from the top of the path -
        see that for more information.
        """

        # if the path is finished, return a single result with an
        # empty list, as there are no more path elements
        #
        # note that this is different from an empty list (which
        # would mean no matches
        if not path:
            return [ [] ]

        # get the path head and tail to make things easier to read
        path_head, path_tail = path[0], path[1:]

        # if this element is not a type we can iterate or search
        # through (we've perhaps reached a value or a None), or the
        # dictionary is empty, there are no matches, so just return
        # an empty list (which will cause all higher levels in the
        # path that matched to be discarded, giving no resulsts)
        if not isinstance(d, (dict, list, set)) or (not d):
            return []

        # if the path element is None, we're doing a wildcard match
        if (path_head is None) or (isinstance(path_head, set)):
            # initialise an empty list for all returned matching
            # results
            results = []

            # go through all the keys at this level in the dictonary
            for d_key in d:
                if (path_head is None) or (d_key in path_head):
                    # are there levels below this one?
                    if path_tail:
                        # yes - recursively get the matches from under
                        # this key
                        for matches in self._path_matches(d[d_key], path_tail):
                            # add this match to the list of matches,
                            # prepending this key onto the start of the
                            # path
                            results.append([d_key] + matches)
                    else:
                        # no - just add this result (this is a minor
                        # optimisation, as well as avoiding an error by
                        # trying to index into a non-dict type), above
                        results.append([d_key])

            return results

        # we have a literal key to match - if it's found,
        # recursively get the matches under this level
        if path_head in d:
            return [ ([path_head] + matches)
                            for matches
                            in self._path_matches(d[path_head], path_tail) ]

        # we have no matches, return the empty list
        return []


    def full_matches(self, d):
        """This method takes a dictionary and returns any matches for
        the full path in it, as a list of paths; each path is, itself, a
        list of keys.

        If any of the elements of the path are None, this is treated as
        a wildcard and will match all keys at that level.

        If there are no matching entries, the returned list will be
        empty.

        The returned list of matches is not guaranteed to be in any
        particular order.
        """

        return self._path_matches(d, self._path_full)


    def explicit_context_matches(self, d, trigger_context):
        """This method is used when checking for trigger matches.

        It is similar to full_matches() except the explicit context
        (without wildcards) is supplied and the command and extended
        paths appended; the matches are returned as a list.

        The context will have been taken from the converter which set up
        the trigger (with the wildcarded fields completed) so we only
        want to match parts of the configuration which have that
        explicit context.
        """

        # check the supplied context to confirm that it matches that of
        # this converter (allowing for wildcards) - if it does not,
        # return an empty list of matches
        #
        # this is because it may have been triggered in a completely
        # different context and we need to make sure that this converter
        # applies to the same context as the trigger

        # if the length of the trigger context differs from ours, this
        # is definitely not the same context
        if len(trigger_context) != len(self.context):
            return []

        # check the items in our context and the trigger context
        for s, t in zip(self.context, trigger_context):
            # if our item is a set, and the trigger is not in it, no match
            if isinstance(s, set) and (t not in s):
                return []

            # if our item is a literal, and the trigger is not the same,
            # no match
            if (s is not None) and (s != t):
                return []

        # we know the contexts are the same, so find all the matches in
        # the supplied dictionary
        return self._path_matches(d, tuple(trigger_context) + self.cmd + self.ext)


    def context_removed(self, d, match):
        """This method takes a remove dictionary, as returned by
        deepdiff(), and a specific match into it (which must be from
        the same Convert object as the method is called on) and returns
        True iff the context for this converter is either:

        1.  In the remove dictionary entirely and exactly (i.e. it is
        empty at the end of the match path), or

        2.  The dictionary does not contain the match path but the match
        path runs out at a point in the dictionary where it is empty
        (indicating everything below this is removed).
        """

        # if this converter has no containing context, we definitely
        # can't be removing it, so will need to remove the item
        if not self.context:
            return False

        # get the part of the match for this item which covers the
        # context of this converter
        match_context = match[0 : self._context_len]

        # loop whilst there is more match remaining and the remove
        # dictionary still has items in it
        while match_context and d:
            # get the head of the match path and remove it from the path
            # if we iterate after matching
            match_head = match_context.pop(0)

            # if the the head of the match path is not in the
            # dictionary, we're not its context so return no match
            if match_head not in d:
                return False

            # move down to the next level in the remove dictionary
            d = d[match_head]


        # if the remove dictionary is not empty, we've either reached
        # the end of the match path and something remains, so we won't
        # be removing the entire context, or the match path was not
        # completely traversed but something remains
        #
        # either way, this converter will not be removing the context of
        # this item so return no match
        if d:
            return False

        # the remove dictionary is empty, so we've either reached the
        # end of the match path and are removing everything, or we ran
        # out of remove dictionary, traversing the path, but everything
        # at this point is going
        #
        # regardless, this converter will already be removing the
        # context of this match so this item doesn't need to be
        # explicitly removed, itself
        return True


    def get_path(self):
        """Get the non-extended path for this converter (i.e. the
        'context' and 'cmd' paths joined, excluding the 'ext').
        """

        return self.context + self.cmd


    def _get_sort_key(self):
        """Get the key used to order converters within a block.

        This consists of the context with the sort_key appended (which
        is a tuple of elements).  If sort_key is None, cmd+ext will be
        assumed as a default.
        """

        key = self.context + (self.sort_key or (self.cmd + self.ext))
        return [ "" if i is None else i for i in key ]


    def get_match_context(self, match):
        """Return the context portion of a particular match for this
        converter.

        This is used when a trigger is set, to extract the context of a
        converter.
        """

        return match[0 : self._context_len]


    def get_cfg(self, cfg, match):
        """This method returns the configuration to be passed to the
        converter's action methods [remove() and update()].

        By default, it indexes through the configuration using the path
        in the converter.  Converters may wish to override this, in some
        cases, for performance (perhaps if the entire configuration is
        to be returned).

        If the specified match path is not found, or there was a problem
        indexing along the path, None is returned, rather than an
        exception raised.
        """

        # try to get the specified matching path
        try:
            return deepget(cfg, *match[0 : self._path_len])

        except TypeError:
            # we got a TypeError so make the assumption that we've hit
            # a non-indexable element (such as a set) as the final
            # element of the path, so just return None
            return None


    def get_ext(self, cfg, *args):
        """This method gets the extension part of the path, given a
        configuration dictionary starting at the path (i.e. what is
        passed as 'old/new' and 'rem/upd' in the action methods).

        An action method [remove() or update()] can use this to get the
        extension portion without needing to explicitly index through
        it.

        If the extension contains any wildcard elements (= None), these
        will be filled from the supplied 'args'.  The number of args
        must be the same (or larger) than the number of wildcard fields,
        else an error will occur.
        """

        # get the extension path, filling in the wildcards (= None) with
        # the supplied matched arguments
        ext_match = []
        for i in self.ext:
            if i is None:
                i = args[0]
                args = args[1:]
            ext_match.append(i)

        return deepget(cfg, *ext_match)


    def get_args(self, match):
        """This method returns a the wildcarded parts of the specified
        match as a 2-tuple with each element a list.  The first element
        is the list of wildcard arguments from the context and the
        second is from the cmd+ext part.

        The boundary between the context and the cmd+ext parts is
        normally determined automatically but can be adjusted by setting
        context_offset in the converter (typically to a negative value,
        to include part of the context in the local arguments to the
        converter).
        """

        wildcard_args = [ match[i] for i in self.wildcard_indices ]
        return (wildcard_args[:self._context_args],
                wildcard_args[self._context_args:])


    def filter(self, context_args, *local_args):
        """Specifies if a particular conversion is to be filtered out
        (return = False) or executed (True), given the wildcard match
        arguments.

        This filtering could be done by the action methods delete(),
        remove(), truncate(), add(), update() and trigger() but
        sometimes it is useful to separate this out to operate
        independently, if a filter method is to be shared across a set
        of subclasses.

        A side benefit is it's also a bit quicker as the filtering
        happens before all the differences are calculated.

        This method is not called directly by convert() but provides a
        single method that the individual action filtering methods
        (filter_delete(), filter_update() and filter_trigger()) will
        call by default, if all types of action are to be equally
        filtered.

        This method (and its associated action-specific methods) differs
        from the trigger_set_filter() method (and its methods) as this
        is called on the converter which has been triggered, rather than
        on the converter which sets up the trigger.

        Keyword arguments:

        context_args -- [only] the wildcard arguments from the context
        part of path, supplied as an iterable (typically a list).  For
        example, if the context matches ["interface", None], this will
        be the the value of None (as the list [a]).

        *local_args -- [only] the wildcard arguments in the command and
        extensions parts of the path, supplied as a number of discrete
        arguments.  For example, if the command and extension matches
        ["standby", "group", None, "ip-secondary", None], this will be
        the value of the two None fields (as the list [a, b]).
        """

        return True


    def filter_delete(self, context_args, *local_args):
        """See filter() - this method is called by convert() before a
        delete()/remove()/truncate() action is called.
        """

        return self.filter(context_args, *local_args)


    def filter_update(self, context_args, *local_args):
        """See filter() - this method is called by convert() before an
        add()/update() action is called.
        """

        return self.filter(context_args, *local_args)


    def filter_trigger(self, context_args, *local_args):
        """See filter() - this method is called by convert() before a
        trigger() action is called.
        """

        return self.filter(context_args, *local_args)


    def trigger_set_filter(self, trigger, old, new, context_args, *local_args):
        """If a converter action has fired and trigger_blocks is
        specified, this method will be called for each trigger, along
        with the same parameters supplied to the action method.  If
        True is returned, the trigger will be set up; if False is
        returned, the trigger will NOT be set up.

        This method can be used to prevent a trigger being set up in
        certain situations.

        By default, the method returns True, which performs no
        filtering (so triggers are always set up).

        Note that this differs from the filter() method (and its
        associated methods for each type of action) as this is called on
        the converter that sets up the trigger, rather than on the
        converter which is triggered later.

        Keyword arguments:

        old, new, context_args, *local_args -- see the update() method
        """

        return True


    def trigger_set_filter_delete(
            self, trigger, old, rem, new, context_args, *local_args):

        """See trigger_set_filter() - this method is called before a
        trigger is set up following a delete()/remove()/truncate()
        action method.
        """

        return self.trigger_set_filter(
                   trigger, old, new, context_args, *local_args)


    def trigger_set_filter_update(
            self, trigger, old, upd, new, context_args, *local_args):

        """See trigger_set_filter() - this method is called before a
        trigger is set up following a add()/update() action method.
        """

        return self.trigger_set_filter(
                   trigger, old, new, context_args, *local_args)


    def delete(self, old, rem, new, context_args, *local_args):
        """The delete() method is called when the specified path is in
        the remove differences (i.e. it's in the old configuration but
        but not in the new configuration), unless the containing context
        is being removed in its entirety.

        The default behaviour of this method is to call remove() with
        the old value for 'old'.

        This method may be required in odd situations where there is a
        full removal of a configuration element matched by the 'cmd' and
        'ext' attributes but there still something in the context (at a
        higher level) and this is required to do the removal.  Normally
        the remove() method should be sufficient, however.

        The difference between delete() and truncate() is that the
        latter is called when something remains in the configuration
        value identified by the complete match (i.e. context + cmd +
        ext), so only some items are being removed.  delete(), on the
        other hand, is called when the configuration item identified by
        the match is empty; 'rem' and 'new' are identify the
        configuration identified by just the context and not the
        complete match and may be required when deleting items.

        Keyword arguments:

        old -- the value of the dictionary item at the matching path in
        the old configuration dictionary (sometimes, the full details of
        the old configuration may be required to remove it)

        rem -- the value of the dictionary item at the matching path in
        the remove differences dictionary (sometimes, it's necessary to
        know only what is removed from the new configuration)

        new -- the value of the dictionary item at the matching path in
        the new configuration dictionary (sometimes, parts of the old
        configuration cannot be removed and the entire new configuration
        is required to replace it)

        context_args -- [only] the wildcard arguments from the context
        part of path, supplied as an iterable (typically a list).  For
        example, if the context matches ["interface", None], this will
        be the the value of None (as the list [a]).

        *local_args -- [only] the wildcard arguments in the command and
        extensions parts of the path, supplied as a number of discrete
        arguments.  For example, if the command and extension matches
        ["standby", "group", None, "ip-secondary", None], this will be
        the value of the two None fields (as the list [a, b]).
        """

        return self.remove(old, context_args, *local_args)


    def remove(self, old, context_args, *local_args):
        """The remove() method is called when the specified path is in
        the remove differences (i.e. it's in the old configuration but
        but not in the new configuration), unless the containing context
        is being removed in its entirety.

        The default behaviour of this method is to call truncate() with
        the old value for 'old' and 'remove' as, if there is no specific
        behaviour for removing an entire object, we should remove the
        individual elements.

        The 'new' value passed to truncate() is None as nothing exists
        in the new configuration - if the truncate() needs this, a
        separate remove() method will normally be needed.

        Keyword arguments:

        old -- the value of the dictionary item at the matching path in
        the old configuration dictionary (sometimes, the full details of
        the old configuration may be required to remove it)

        context_args -- [only] the wildcard arguments from the context
        part of path, supplied as an iterable (typically a list).  For
        example, if the context matches ["interface", None], this will
        be the the value of None (as the list [a]).

        *local_args -- [only] the wildcard arguments in the command and
        extensions parts of the path, supplied as a number of discrete
        arguments.  For example, if the command and extension matches
        ["standby", "group", None, "ip-secondary", None], this will be
        the value of the two None fields (as the list [a, b]).

        The return value is the commands to insert into the
        configuration to convert it.  This can either be a simple
        string, in the case of only one line being required, or an
        iterable containing one string per line.  If the return value is
        None, it is an indication nothing needed to be done.  An empty
        string or iterable indicates the update did something, which did
        not change the configuration (this may have semantic
        differences).
        """

        return self.truncate(old, old, None, context_args, *local_args)


    def truncate(self, old, rem, new, context_args, *local_args):
        """The truncate() method is identical to remove() except that it
        is called when an item is partially removed (i.e. something
        remains in the new configuration - it is 'truncated').

        It is useful when amending lists or sets and matching at the
        containing object level.

        Keyword arguments:

        old -- the value of the dictionary item at the matching path in
        the old configuration dictionary (sometimes, the full details of
        the old configuration may be required to remove it)

        rem -- the value of the dictionary item at the matching path in
        the remove differences dictionary (sometimes, it's necessary to
        know only what is removed from the new configuration)

        new -- the value of the dictionary item at the matching path in
        the new configuration dictionary (sometimes, parts of the old
        configuration cannot be removed and the entire new configuration
        is required to replace it)

        context_args -- [only] the wildcard arguments from the context
        part of path, supplied as an iterable (typically a list).  For
        example, if the context matches ["interface", None], this will
        be the the value of None (as the list [a]).

        *local_args -- [only] the wildcard arguments in the command and
        extensions parts of the path, supplied as a number of discrete
        arguments.  For example, if the command and extension matches
        ["standby", "group", None, "ip-secondary", None], this will be
        the value of the two None fields (as the list [a, b]).

        The return value is the commands to insert into the
        configuration to convert it.  This can either be a simple
        string, in the case of only one line being required, or an
        iterable containing one string per line.  If the return value is
        None, it is an indication nothing needed to be done.  An empty
        string or iterable indicates the update did something, which did
        not change the configuration (this may have semantic
        differences).
        """

        pass


    def add(self, new, context_args, *local_args):
        """The add() method is called when the specified path is in the
        update differences but did not exist in the old configuration
        (i.e. it's something new that is being added to the
        configuration).

        By default, this calls update() with the new configuration as
        the updated and new configuration arguments (and 'args') as, in
        many cases, the process for adding something is the same as
        updating it (e.g. updating an interface description).  It can,
        however, be overridden to do something different or, more
        commonly, implement add() but not update() for a particular
        change (as the updates will be picked up by more specific
        paths in other objects).

        Keyword arguments:

        new -- the value of the dictionary item at the matching path in
        the new configuration dictionary

        context_args -- [only] the wildcard arguments from the context
        part of path, supplied as an iterable (typically a list).  For
        example, if the context matches ["interface", None], this will
        be the the value of None (as the list [a]).

        *local_args -- [only] the wildcard arguments in the command and
        extensions parts of the path, supplied as a number of discrete
        arguments.  For example, if the command and extension matches
        ["standby", "group", None, "ip-secondary", None], this will be
        the value of the two None fields (as the list [a, b]).

        The return value is the commands to insert into the
        configuration to convert it.  This can either be a simple
        string, in the case of only one line being required, or an
        iterable containing one string per line.  If the return value is
        None, it is an indication nothing needed to be done.  An empty
        string or iterable indicates the update did something, which did
        not change the configuration (this may have semantic
        differences).
        """

        return self.update(None, new, new, context_args, *local_args)


    def update(self, old, upd, new, context_args, *local_args):
        """The update() method is called when the specified path is in
        the update differences and also in the old configuration (i.e.
        something is being updated in the configuration).

        Keyword arguments:

        old -- the value of the dictionary item at the matching path in
        the old configuration dictionary (sometimes, the old
        configuration must be removed first, before the new
        configuration can be updated, so the details are required)

        upd -- the value of the dictionary item at the matching path in
        the update differences dictionary

        new -- the value of the dictionary item at the matching path in
        the new configuration dictionary (sometimes, the full details of
        the new configuration may be required to update it)

        context_args -- [only] the wildcard arguments from the context
        part of path, supplied as an iterable (typically a list).  For
        example, if the context matches ["interface", None], this will
        be the the value of None (as the list [a]).

        *local_args -- [only] the wildcard arguments in the command and
        extensions parts of the path, supplied as a number of discrete
        arguments.  For example, if the command and extension matches
        ["standby", "group", None, "ip-secondary", None], this will be
        the value of the two None fields (as the list [a, b]).

        The return value is the commands to insert into the
        configuration to convert it.  This can either be a simple
        string, in the case of only one line being required, or an
        iterable containing one string per line.  If the return value is
        None, it is an indication nothing needed to be done.  An empty
        string or iterable indicates the update did something, which did
        not change the configuration (this may have semantic
        differences).
        """

        pass


    def trigger(self, new, context_args, *local_args):
        """The trigger() method is the same as the update() method
        except it is called when a trigger match occurs.

        By default, this method just calls update(new, None, old,
        context_args, *local_args) but can be overridden by subclasses
        if a special action needs to be taken in this situation (i.e.
        where this is no change but an item of configuration is already
        present).

        Note that as the upd argument passed to update() is None, which
        may need to be carefully handled to avoid checking things like
        dictionary key membership.

        Note that a trigger() method will not be called if a remove or
        update match has already been called on a particular match.
        """

        return self.update(new, None, new, context_args, *local_args)



class DiffConfig:
    """This abstract class is used to represent a configuration
    difference processor that can convert a configuration from one to
    another, using a method (which can be called once for each pair of
    configuration files).

    It encapsulates the rules for exluding items from the comparison.

    The list of converters is organised into 'blocks', each with a list
    of converters.  The sequence of blocks is set in _init_blocks() and
    each converter has an optional 'block' attribute which specifies
    which block it is to be added to.  The converters are added with
    _add_converters().  Both of these methods will likely need to be
    overridden in concrete classes.
    """


    def __init__(self, init_explain=False, init_dump_config=False,
                 init_dump_diff=False, init_debug_convert=0,
                 init_subtree_dump_filter=[]):

        """The constructor initialises the exclude list to empty and
        adds the converter block sequence with _add_blocks() and
        individual converters using _add_converters().  It also stores
        some settings controlling the level of information describing
        the conversion process, based on the command line arguments:

        init_explain=False -- include comments in the output
        configuration changes that explain the differences being matched
        by the Convert objects (if available).

        init_dump_config=False -- dump the old and new configurations
        (after excludes).

        init_dump_diff=False -- dump the differences (remove and update
        configurations).

        init_debug_convert=0 -- level of debugging information for the
        conversion process (see DEBUG_CONVERT_xxx constants).
        """

        # store the [initial] settings for the conversion process
        self._explain = init_explain
        self._dump_config = init_dump_config
        self._dump_diff = init_dump_diff
        self._debug_convert = init_debug_convert
        self._subtree_dump_filter = init_subtree_dump_filter

        # initialise the dictionary of excludes, which will be passed
        # to deepremoveitems()
        self.init_rules()

        # initialise the converter block sequence
        self._init_blocks()

        # the converters are stored in a dictionary, keyed on the block
        # name, with each value a list of converters in that block, to
        # be applied in the specified order
        self._cvts = {}
        for block in self._blocks:
            self._cvts[block] = []

        # add and sort the converters
        self._add_converters()
        self._sort_converters()


    def _add_blocks(self):
        """This method adds the sequence of converter blocks.  Blocks
        group together converters which must be run before others (in
        other blocks).

        The base class assumes a single block with no name ('None'),
        which is the default under a converter specifies a different
        one.
        """

        self._blocks = [None]


    def _add_converters(self):
        """This method adds the converters for a particular object to
        the list used by the convert() method, usually by calling
        _add_converter() for each (see that method).

        The base class does nothing but child classes will implement it
        as they require.
        """

        pass


    def _add_converter(self, cvt):
        """Add an individual converter object, a child of the Convert
        class, to the list of converters for its block.

        If the block used in the converter does not exist, a KeyError
        will be raised.
        """

        block = cvt.block

        if block not in self._cvts:
            raise KeyError("converter: %s block: %s not found"
                                % (type(cvt).__name__, block))

        self._cvts[block].append(cvt)


    def _sort_converters(self):
        """This method sorts the converters within each block.  The
        default ordering is the the complete path (context + cmd + ext)
        but can be overridden, if required.

        This method is called by the constructor, after the converters
        have been added to ensure a consist order.
        """

        for block in self._cvts:
            self._cvts[block].sort(key=lambda c: c._get_sort_key())


    def _explain_comment(self, path):
        """This method returns a comment or other configuration item
        explaining the path supplied (which will typically be a match
        against a converter).  The path is supplied a list of levels and
        converted to a string using pathstr().

        Child classes can override this to provide a comment appropriate
        for their platform.

        If the function returns None, no comment is inserted.
        """

        return None


    def _diffs_begin(self):
        """This method returns a head (beginning) for a generated
        changes configuration file as an iterable of strings.

        In the abstract class, it returns None (which does not add
        anything) but, in child classes it may return a beginning line
        or similar.

        Note that if there are no changes, this will not be included in
        an otherwise empty file.
        """

        return []


    def _diffs_end(self):
        """This method returns a tail (ending) for a generated changes
        configuration file as an iterable of strings.

        In the abstract class, it returns None (which does not add
        anything) but, in child classes it may return an 'end' line or
        similar.

        Note that if there are no changes, this will not be included in
        an otherwise empty file.
        """

        return []


    def init_rules(self):
        """This method initialises the rules s.  In the base
        class, it the resets it to an empty dictionary, but child
        classes can extend this to add some default exclusions for
        standard system configuration entries which should not be
        changed.

        It is normally only called by the constructor but can be called
        later, to clear the excludes list before adding more (if
        required).
        """

        self.init_rules_tree()
        self.init_rules_active()


    def init_rules_tree(self):
        """This method initialises the rules tree (the dictionary of
        rules typically read from a file.

        In the base class, it just sets it to an empty dictionary but
        some platform-specific classes may wish to extend this to set up
        a default tree (along with init_rules_active()).
        """

        self._rules_tree = {}


    def init_rules_active(self):
        """This method initialises the active rules list (the list of
        rules specifying what should be used from the rules tree).

        In the base class, it just sets it to an empty list but some
        platform-specific classes may wish to extend this to set up a
        default list.
        """

        self._rules_active = []


    def add_rules_tree_file(self, filename):
        """Read a tree of rules items from a YAML file.  This is
        typically done once but then different portions of the rules
        dictionary selected with set_rules_active().

        The contents of the file are added to the current tree.  To
        clear the current tree first, use init_rules_tree().
        """

        try:
            file_rules_tree = yaml.safe_load(open(filename))

        except yaml.parser.ParserError as exception:
            raise ValueError("failed parsing rules file: %s: %s"
                                 % (filename, exception))

        self._rules_tree.update(file_rules_tree)


    def add_rules_active(self, rule_specs, devicename):
        """Add a list of rules to the current rule list, which specifies
        what parts of the rules tree should be used and how (include or
        exclude these items), to control the comparison done by the
        convert() method.

        The rules are specified as a list of strings in the format
        '[!]<path>' where '!' means 'exclude' (if omitted, it means
        'include') and 'path' is a colon-separated list of keys giving
        the path into the rules tree.  A particular element can be
        given as '%', in which case the 'devicename' parameter will be
        used but, if the devicename argument is None/empty (False),
        then a warning is printed and the rule skipped.

        For example, if '!device-excludes:%' is given, and the
        devicename is 'router1', the part of the rules tree indexed by
        ["device-excludes"]["router1"] will be excluded from the
        comparison.

        The rules given will be added to the current rules list; if the
        list is to be cleared first, use init_rules_list().
        """

        for rule_spec in rule_specs:
            # find if this is an include or exclude rule and get the
            # path part

            include = not rule_spec.startswith("!")

            if include:
                rule_spec_path = rule_spec
            else:
                rule_spec_path = rule_spec[1:]


            path_elements = rule_spec_path.split(":")

            if ("%" in path_elements) and (not devicename):
                print("warning: rule specification: %s contains '%%' but no "
                      "device name - ignoring" % rule_spec_path,
                      file=sys.stderr)

                continue


            path = [ devicename if i == '%' else i for i in path_elements ]

            self._rules_active.append( (include, path) )


    def get_rules_tree(self):
        """The method returns the current rules tree (as initialised by
        init_rules_tree() and extended with read_rules_tree()).  This
        should not be modified.
        """

        return self._rules_tree


    def get_rules(self):
        """This method just returns the active rules list and the
        portion of the rules tree it applies to.

        The return value is a list, one entry per rule, containing
        2-tuples: the first entry is the rule specification (a string,
        in the format described by add_rules_active()), and the second
        the portion of the rules tree that the path references (or None,
        if that part of the tree does not exist).

        This method is mainly used for debugging messages.
        """

        r = []
        for include, path in self._rules_active:
            r.append(
                (("" if include else '!') + ':'.join(path),
                 deepget(self._rules_tree, *path) ) )

        return r


    def apply_rules(self, d):
        """This method applies the current rules (tree and active list)
        to the supplied configuration dictionary, either only including
        what's specified (using deepfilter()) or excluding (using
        deepremoveitems()) the specified portions.

        The configuration dictionary is modified in place.

        The method can be used on a configuration dictionary, or the
        remove/update dictionaries returned by deepdiff().
        """

        for include, path in self._rules_active:
            # get the porttion of the rules tree specified by the path
            # in this rule
            path_dict = deepget(self._rules_tree, *path)

            # skip to the next entry, if this part was not found
            if path_dict is None:
                continue

            # do either the include or exclude on the configuration
            # dictionary, in place)
            if include:
                d = deepfilter(d, path_dict)
            else:
                deepremoveitems(d, path_dict)


    def update_dump_config(self, new_dump_config):
        "Updates the dump configuration setting."
        self._dump_config = new_dump_config


    def update_dump_diff(self, new_dump_diff):
        "Updates the dump differences setting."
        self._dump_diff = new_dump_diff


    def update_debug_convert(self, new_debug_convert):
        "Updates the debug conversion level."
        self._debug_convert = new_debug_convert


    def _print_debug(self, msg, blank_if_single=True):
        """Print the supplied debugging message followed by a blank
        line, if it's not empty (in which case, do nothing), unless
        blank_if_single is True and the message is only one line long.

        Prior to printing the message, _print_debug_block() and
        _print_debug_converter() will be called, to print those
        messages, if they haven't already been printed.
        """

        if msg:
            self._print_debug_block()
            self._print_debug_converter()

            for line in msg:
                print(line, file=sys.stderr)

            if blank_if_single or (len(msg) > 1):
                print(file=sys.stderr)


    def _print_debug_block(self):
            """Print the block debug message explicitly, if the debug
            level is above DEBUG_CONVERT_MATCH (the bottom level).

            Normally this is called by _print_debug() when the first
            debug message is displayed but, if more detailed debugging
            is requireed, it can be called explicitly.

            After printing, the message is cleared to not be printed
            again.
            """

            if self._debug_block_msg:
                for line in self._debug_block_msg + [""]:
                    print(line, file=sys.stderr)

                self._debug_block_msg = []


    def _print_debug_converter(self):
            """Print the converter debug message explicitly, if the debug
            level is above DEBUG_CONVERT_MATCH (the bottom level).

            Normally this is called by _print_debug() when the first
            debug message is displayed but, if more detailed debugging
            is requireed, it can be called explicitly.

            After printing, the message is cleared to not be printed
            again.
            """

            if self._debug_converter_msg:
                for line in self._debug_converter_msg + [""]:
                    print(line, file=sys.stderr)

                self._debug_converter_msg = []


    def convert(self, old_cfg, new_cfg):
        """This method processes the conversion from the old
        configuration to the new configuration, removing excluded parts
        of each and calling the applicable converters' action methods.

        Note that, if excludes are used, the configurations will be
        modified in place by a deepremoveitems().  They will need to be
        copy.deepcopy()ed before passing them in, if this is
        undesirable.

        The returned value is a 2-tuple:

        - the first element is a big string of all the configuration
          changes that need to be made, sandwiched between
          _diffs_begin() and _diffs_end(), or None, if there were no
          differences

        - the second element is a dictionary giving the tree of
          differences (i.e. the elements where a difference was
          encountered - either a remove or an update)
        """


        self.apply_rules(old_cfg)

        if self._dump_config:
            print(">>"
                  + (" old" if new_cfg else "")
                  + " configuration (after rules, if specified):",
                  yaml.dump(deepselect(dict(old_cfg),
                                       *self._subtree_dump_filter),
                            default_flow_style=False),
                  sep="\n")


        # initialise the list of diffs (the returned configuration
        # conversions) and the tree of differences to empty

        diffs = []
        diffs_tree = {}


        # initialise the dictionary of activated triggers and their
        # configuration points

        active_triggers = {}


        # if no new config was specified, stop here (we assume we're
        # just testing, parsing and excluding items from the old
        # configuration and stopping
        #
        # we check for None explicitly for the difference between no
        # configuration and an empty configuration

        if new_cfg is None:
            return None, diffs_tree


        self.apply_rules(new_cfg)

        if self._dump_config:
            print(">> new configuration (after rules, if specified):",
                  yaml.dump(deepselect(dict(new_cfg),
                                       *self._subtree_dump_filter),
                            default_flow_style=False),
                  sep="\n")


        # use deepdiff() to work out the differences between the two
        # configuration dictionaries - what must be removed and what
        # needs to be added or updated
        #
        # then use deepfilter() to get the full details of each item
        # being removed, rather than just the top of a subtree being
        # removed

        remove_cfg, update_cfg = deepdiff(old_cfg, new_cfg)
        remove_cfg_full = deepfilter(old_cfg, remove_cfg)


        if self._dump_diff:
            print("=> differences - remove:",
                  yaml.dump(deepselect(dict(remove_cfg),
                                       *self._subtree_dump_filter),
                            default_flow_style=False),

                  "=> differences - remove full:",
                  yaml.dump(deepselect(dict(remove_cfg_full),
                                       *self._subtree_dump_filter),
                            default_flow_style=False),

                  "=> differences - update (add/change):",
                  yaml.dump(deepselect(dict(update_cfg),
                                       *self._subtree_dump_filter),
                            default_flow_style=False),

                  sep="\n")


        # set the current block name (used to print when a new block is
        # entered) - we use an empty string as something that won't be
        # used as a block name (we can't use 'None' as that's the
        # default block)

        current_block = ""

        self._debug_block_msg = []


        # go through the list of blocks and then the converter objects
        # within them, in order

        for cvt in chain.from_iterable(
            [ self._cvts[block] for block in self._blocks ]):

            # if we're entering a new block, set a 'new block' debug
            # message and print it immediately, if we are debugging to
            # that level

            if cvt.block != current_block:
                current_block = cvt.block

                if self._debug_convert > DEBUG_CONVERT_MATCH:
                    self._debug_block_msg = [">> [block: %s]" % current_block]

                    if self._debug_convert >= DEBUG_CONVERT_NOMATCH:
                        self._print_debug_block()


            # get all the remove and update matches for this converter
            # and combine them into one list, discarding any duplicates
            #
            # we do this rather than processing each list one after the
            # other so we combine removes and updates on the same part
            # of the configuration together

            remove_matches = cvt.full_matches(remove_cfg_full)
            update_matches = cvt.full_matches(update_cfg)


            # if this converter is in a block which has been triggered,
            # find all the matches in the new configuration which match
            # the context in which the trigger was set

            triggered_matches = []
            if cvt.block in active_triggers:
                for t in active_triggers[cvt.block]:
                    triggered_matches.extend(
                        cvt.explicit_context_matches(new_cfg, t))


            # combine all the matches for this converter into a single
            # list
            #
            # we sort this list so changes are processed in a consistent
            # and predictable order - there can, however, be elements
            # where the corresponding element in another path is of a
            # different type (e.g. one is a string and the other None),
            # so they can't be sorted directly
            #
            # to resolve this, the sorting key for a match is trans-
            # formed by converting all the path elements to strings,
            # with the value None being transformed to an empty string
            # ('')

            sorted_matches = (
                sorted(remove_matches + update_matches + triggered_matches,
                       key=lambda k: [ ('' if i is None else str(i))
                                          for i in k ]))

            all_matches = []
            for match in sorted_matches:
                if match not in all_matches:
                    all_matches.append(match)


            # print the name of the converter if either: 1. we have the
            # debugging messages always enabled for this, or 2. we are
            # only debugging converters with matches and there are some
            #
            # the matching converters might be skipped or not generate
            # any differences, but we can't avoid doing that unless we
            # store this message to be printed later, if so - it doesn't
            # currently seem worth doing that for debugging messages

            self._debug_converter_msg = []

            if self._debug_convert > DEBUG_CONVERT_MATCH:
                self._debug_converter_msg = [
                    ">> " + pathstr([ '*' if i is None else i
                                        for i in cvt.get_path() ]),
                    "-> " + type(cvt).__name__]

                if self._debug_convert >= DEBUG_CONVERT_NOMATCH:
                    self._print_debug_converter()


            for match in all_matches:
                # handle REMOVE conversions, if matching

                if match in remove_matches:
                    debug_msg = []


                    # check if anything remains at this level or below
                    # in the new configuration - if it does, we're doing
                    # a partial removal

                    remove_is_truncate = False

                    try:
                        # we don't want the result here, just to find
                        # out if the path exists (if not, KeyError will
                        # be raised)
                        deepget(new_cfg, *match, default_error=True)

                    except KeyError:
                        # nothing remains so we're doing a full remove
                        pass

                    else:
                        # something remains so this is partial
                        if self._debug_convert >= DEBUG_CONVERT_STEPS:
                            debug_msg.append(
                                "-> subconfiguration not empty - truncate")
                        remove_is_truncate = True


                    if self._debug_convert >= DEBUG_CONVERT_MATCH:
                        debug_msg.append(
                            "=> "
                            + ("truncate" if remove_is_truncate else "remove")
                            + ": "
                            + pathstr(match, cvt.wildcard_indices))


                    # get elements in the path matching wildcards

                    context_args, local_args = cvt.get_args(match)


                    # skip this conversion if it is filtered out

                    try:
                        filtered = cvt.filter_delete(context_args, *local_args)

                    except:
                        print("Exception in %s.filter_delete() with:"
                                  % type(cvt),
                              "  context_args=" + repr(context_args),
                              "  *local_args=" + repr(local_args),
                              "",
                              sep="\n", file=sys.stderr)

                        raise

                    if not filtered:
                        if self._debug_convert >= DEBUG_CONVERT_NODIFF:
                            debug_msg.append("-> filtered - skip")
                            self._print_debug(debug_msg)
                        continue


                    # if we're removing the entire context for this
                    # match, we don't need to do it, as that will
                    # remove this, while it's at it

                    if cvt.context_removed(remove_cfg, match):
                        if self._debug_convert >= DEBUG_CONVERT_NODIFF:
                            debug_msg.append(
                                "-> containing context being removed - skip")

                            self._print_debug(
                                debug_msg,
                                blank_if_single=
                                    self._debug_convert > DEBUG_CONVERT_MATCH)

                        continue


                    # get the old, remove and new parts of the
                    # configuration and remove difference dictionaries,
                    # for the path specified in the converter (ignoring
                    # the extension 'ext')

                    cvt_old = cvt.get_cfg(old_cfg, match)
                    cvt_rem = cvt.get_cfg(remove_cfg_full, match)
                    cvt_new = cvt.get_cfg(new_cfg, match)

                    if self._debug_convert >= DEBUG_CONVERT_PARAMS:
                        debug_msg.extend([
                            "-> old configuration:",
                            yaml.dump(cvt_old, default_flow_style=False)])

                        if remove_is_truncate:
                            debug_msg.extend([
                                "-> remove configuration:",
                                yaml.dump(cvt_rem, default_flow_style=False)])

                        debug_msg.extend([
                            "-> new configuration:",
                            yaml.dump(cvt_new, default_flow_style=False)])


                    # call the truncate or delete converter action method

                    try:
                        if remove_is_truncate:
                            diff = cvt.truncate(cvt_old, cvt_rem, cvt_new,
                                                context_args, *local_args)
                        else:
                            diff = cvt.delete(cvt_old, cvt_rem, cvt_new,
                                              context_args, *local_args)

                    except:
                        # builld a list of arguments for passing to the
                        # converter action method for the exception
                        # message
                        action_args_str = ["  old=" + repr(cvt_old)]
                        if remove_is_truncate:
                            action_args_str.append("  rem=" + repr(cvt_rem))
                        action_args_str.append("  new=" + repr(cvt_new))

                        print("Exception in %s.%s() with:"
                                  % (type(cvt).__name__,
                                     "truncate" if remove_is_truncate
                                         else "delete"),
                              *action_args_str,
                              "  context_args=" + repr(context_args),
                              "  *local_args=" + repr(local_args),
                              "",
                              sep="\n", file=sys.stderr)

                        raise


                    # if some diffs were returned by the action, add
                    # them

                    if diff is not None:
                        # the return can be either a simple string or a
                        # list of strings - if it's a string, make it a
                        # list of one so we can do the rest the same way

                        if isinstance(diff, str):
                            diff = [diff]

                        if self._debug_convert >= DEBUG_CONVERT_STEPS:
                            debug_msg += diff


                        # add a comment, explaining the match, if
                        # enabled

                        if self._explain:
                            comment = self._explain_comment(match)
                            if comment:
                                diffs.append(comment)


                        # store this diff on the end of the list of
                        # diffs so far

                        diffs += diff
                        diffs.append("")


                        # add this match to the differences tree

                        deepsetdefault(diffs_tree, *match)

                    else:
                        if self._debug_convert >= DEBUG_CONVERT_NODIFF:
                            debug_msg.append("-> no action")
                        else:
                            # no differences were returned by the
                            # conversion method and we're not debugging
                            # 'no diff's so blank any debugging message
                            # we've built up so we don't print anything
                            # for this match

                            debug_msg = []


                    # if this converter sets off some triggers, add
                    # those to the active trigger dictionary, along with
                    # the matching patch
                    #
                    # we only set triggers if the converter actually
                    # generated some conversion commands, or if the
                    # empty_trigger option is set, and they're not
                    # filtered out with trigger_set_filter_delete()

                    if (diff is not None) or cvt.empty_trigger:
                        for t in cvt.trigger_blocks:
                            match_context = cvt.get_match_context(match)

                            if t not in self._blocks:
                                raise KeyError(
                                    "converter: %s triggers non-existent"
                                    " block: %s" % (type(cvt).__name__, t))

                            if not cvt.trigger_set_filter_delete(
                                       t, cvt_old, cvt_rem, cvt_new,
                                       context_args, *local_args):

                                if self._debug_convert >= DEBUG_CONVERT_STEPS:
                                    debug_msg.append(
                                        "-> trigger filtered out: %s @ %s"
                                            % (t,
                                               pathstr(match_context, set())))

                                # skip this trigger without setting it up
                                continue

                            if self._debug_convert >= DEBUG_CONVERT_STEPS:
                                debug_msg.append(
                                    "-> trigger set: %s @ %s"
                                        % (t, pathstr(match_context, set())))

                            active_triggers.setdefault(t, []).append(
                                match_context)


                    self._print_debug(
                        debug_msg,
                        blank_if_single=
                            self._debug_convert > DEBUG_CONVERT_MATCH)


                # handle UPDATE conversions, if matching

                if match in update_matches:
                    debug_msg = []


                    # check if there is anything for this level in the
                    # old configuration - if not, we're actually adding
                    # this, rather than updating it, so record that

                    update_is_add = False

                    try:
                        deepget(old_cfg, *match, default_error=True)

                    except KeyError:
                        if self._debug_convert >= DEBUG_CONVERT_STEPS:
                            debug_msg.append("-> no old configuration - add")
                        update_is_add = True


                    if self._debug_convert >= DEBUG_CONVERT_MATCH:
                        debug_msg.append(
                            "=> "
                            + ("add" if update_is_add else "update")
                            + ": "
                            + pathstr(match, cvt.wildcard_indices))


                    # (same as in remove, above)

                    context_args, local_args = cvt.get_args(match)

                    try:
                        filtered = cvt.filter_update(context_args, *local_args)

                    except:
                        print("Exception in %s.filter_update() with:"
                                  % type(cvt),
                              "  context_args=" + repr(context_args),
                              "  *local_args=" + repr(local_args),
                              "",
                              sep="\n", file=sys.stderr)

                        raise

                    if not filtered:
                        if self._debug_convert >= DEBUG_CONVERT_NODIFF:
                            debug_msg.append("-> filtered - skip")
                            self._print_debug(debug_msg)
                        continue


                    # get the old, update and new parts of the
                    # configuration difference dictionaries, for the
                    # path specified in the converter (ignoring the
                    # extension 'ext')

                    cvt_old = cvt.get_cfg(old_cfg, match)
                    cvt_upd = cvt.get_cfg(update_cfg, match)
                    cvt_new = cvt.get_cfg(new_cfg, match)

                    if self._debug_convert >= DEBUG_CONVERT_PARAMS:
                        if not update_is_add:
                            debug_msg.extend([
                                "-> old configuration:",
                                yaml.dump(cvt_old, default_flow_style=False),
                                "-> update configuration:",
                                yaml.dump(cvt_upd, default_flow_style=False)])

                        debug_msg.extend([
                            "-> new configuration:",
                            yaml.dump(cvt_new, default_flow_style=False)])


                    # call the update or add converter action method

                    try:
                        # if we're adding this, call the add() method,
                        # else update()
                        if update_is_add:
                            diff = cvt.add(cvt_new, context_args, *local_args)
                        else:
                            diff = cvt.update(cvt_old, cvt_upd, cvt_new,
                                              context_args, *local_args)

                    except:
                        # builld a list of arguments for passing to the
                        # converter action method for the exception
                        # message
                        action_args_str = []
                        if not update_is_add:
                            action_args_str.extend([
                                "  old=" + repr(cvt_old),
                                "  upd=" + repr(cvt_upd)])
                        action_args_str.append("  new=" + repr(cvt_new))

                        print("Exception in %s.%s() with:"
                                  % (type(cvt).__name__,
                                     "add" if update_is_add else "update"),
                              *action_args_str,
                              "  context_args=" + repr(context_args),
                              "  *local_args=" + repr(local_args),
                              "",
                              sep="\n", file=sys.stderr)

                        raise


                    # (same as in remove, above)

                    if diff is not None:
                        if isinstance(diff, str):
                            diff = [diff]

                        if self._debug_convert >= DEBUG_CONVERT_STEPS:
                            debug_msg += diff


                        if self._explain:
                            comment = self._explain_comment(match)
                            if comment:
                                diffs.append(comment)


                        diffs.extend(diff)
                        diffs.append("")

                        deepsetdefault(diffs_tree, *match)

                    else:
                        if self._debug_convert >= DEBUG_CONVERT_NODIFF:
                            debug_msg.append("-> no action")
                        else:
                            debug_msg = []


                    if (diff is not None) or cvt.empty_trigger:
                        for t in cvt.trigger_blocks:
                            match_context = cvt.get_match_context(match)

                            if t not in self._blocks:
                                raise KeyError(
                                    "converter: %s triggers non-existent"
                                    " block: %s" % (type(cvt).__name__, t))

                            if not cvt.trigger_set_filter_update(
                                       t, cvt_old, cvt_upd, cvt_new,
                                       context_args, *local_args):

                                if self._debug_convert >= DEBUG_CONVERT_STEPS:
                                    debug_msg.append(
                                        "-> trigger filtered out: %s @ %s"
                                            % (t,
                                               pathstr(match_context, set())))

                                # skip this trigger without setting it up
                                continue

                            if self._debug_convert >= DEBUG_CONVERT_STEPS:
                                debug_msg.append(
                                    "-> trigger set: %s @ %s"
                                        % (t, pathstr(match_context, set())))

                            active_triggers.setdefault(t, []).append(
                                match_context)


                    self._print_debug(
                        debug_msg,
                        blank_if_single=
                            self._debug_convert > DEBUG_CONVERT_MATCH)


                # handle TRIGGERED conversions, if matching, and this
                # wasn't already a remove or update conversion

                if ((match in triggered_matches)
                    and (match not in remove_matches)
                    and (match not in update_matches)):

                    debug_msg = []

                    if self._debug_convert >= DEBUG_CONVERT_MATCH:
                        debug_msg.append(
                            "=> trigger: %s @ %s"
                                % (cvt.block,
                                   pathstr(match, cvt.wildcard_indices)))


                    # (same as in remove, above)

                    context_args, local_args = cvt.get_args(match)

                    try:
                        filtered = cvt.filter_trigger(context_args, *local_args)

                    except:
                        print("Exception in %s.filter_trigger() with:"
                                  % type(cvt),
                              "  context_args=" + repr(context_args),
                              "  *local_args=" + repr(local_args),
                              "",
                              sep="\n", file=sys.stderr)

                        raise

                    if not filtered:
                        if self._debug_convert >= DEBUG_CONVERT_NODIFF:
                            debug_msg.append("-> filtered - skip")
                            self._print_debug(debug_msg)
                        continue


                    # get the old, update and new parts of the
                    # configuration difference dictionaries for the path
                    # specified in the converter (ignoring the extension
                    # 'ext')

                    cvt_new = cvt.get_cfg(new_cfg, match)

                    if self._debug_convert >= DEBUG_CONVERT_PARAMS:
                        debug_msg.extend([
                            "-> new configuration:",
                            yaml.dump(cvt_new, default_flow_style=False)])


                    # call the trigger converter action method

                    try:
                        diff = cvt.trigger(cvt_new, context_args, *local_args)

                    except:
                        print("%s.trigger() with:" % type(cvt).__name__,
                              "  new=" + repr(cvt_new),
                              "  context_args=" + repr(context_args),
                              "  *local_args=" + repr(local_args),
                              sep="\n", file=sys.stderr)

                        raise


                    # (same as in remove, above)

                    if diff is not None:
                        if isinstance(diff, str):
                            diff = [diff]

                        if self._debug_convert >= DEBUG_CONVERT_STEPS:
                            debug_msg += diff


                        if self._explain:
                            comment = self._explain_comment(match)
                            if comment:
                                diffs.append(comment)


                        diffs.extend(diff)
                        diffs.append("")

                        deepsetdefault(diffs_tree, *match)

                        # except one trigger cannot fire another

                    else:
                        if self._debug_convert >= DEBUG_CONVERT_STEPS:
                            debug_msg.append("-> no action")
                        else:
                            debug_msg = []


                    self._print_debug(
                        debug_msg,
                        blank_if_single=
                            self._debug_convert > DEBUG_CONVERT_MATCH)


        # if nothing was generated, just return nothing

        if not diffs:
            return None, diffs_tree


        # return the diffs concatenated into a big, multiline string,
        # along with the begin and end blocks

        return ("\n".join(self._diffs_begin() + diffs + self._diffs_end()),
                diffs_tree)
