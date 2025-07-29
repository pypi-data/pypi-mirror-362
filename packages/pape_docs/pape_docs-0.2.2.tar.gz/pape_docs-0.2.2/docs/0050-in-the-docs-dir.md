# What happens if this script is run inside a `docs/` dir?

A **potential task** about **making sure docs are placed correctly if the CWD is a `docs/` directory or subdirectory**

## Status

In draft

## Description

If the CWD contains `docs/`, we should place the new doc at the base of the deepest `docs/` dir in the current path. So, for example, if our CWD is `/Users/user/Developer/project/docs/sub-project/docs/hey-there/`, we should make the new docs file at `/Users/user/Developer/project/docs/sub-project/docs/new-doc.md`

Note this should only apply if we get to the step of looking for `docs/` in the CWD.

## Make a test

I believe this is already the default functionality, but regardless, there should be a test for this behavior in the test suite if there isn't already.
