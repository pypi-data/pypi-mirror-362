# Mock Event Generator

This package re-generates past gravitational wave pipeline events by time-translating them. It fetches already existing events from a GraceDB server into a cache, shifts the time references as if they were created now and sends a request to GraceDB server to create a new event. By specifiying a super-event, all the online events that are part of it are re-created, either all at the same time, in a specific time interval, or as they were originally uploaded in GraceDB.

Documentation is [here](https://emfollow.docs.ligo.org/mock-event-generator/).
