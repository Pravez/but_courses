#!/usr/bin/env nu

scw container container list -o json | from json | where memory_limit > 256 and cpu_limit > 250 | each {|c| echo "Removing $c.name"; scw container container delete $c.id region=fr-par}
