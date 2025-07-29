Once the package is installed, the executable `meg` is available. To interact with the
`gracedb` the command realy that the user as necessary privileg to access the data base.
This is usualy achived providing the necessary autorization using teh command
`"ligo-proxy-init albert.einstein"`. Detailed information on the CLI usage can be
displayed with the `--help` option:
```bash
meg --help
```

## Command `fetch`

To download all the events belonging to a super-event from the production GranceDB server.
```bash
meg fetch S200225q
```

The option `--source` can be used to download events from another GraceDB server:
```bash
meg fetch G587369 E505784 --source playground
```

More information by typing `meg fetch --help`:
```
 Usage: meg fetch [OPTIONS] EVENTS...

 Fetch G-events and store them in the cache.

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    events      EVENTS...  G-events or S-events to be generated. [default: None] [required]                      │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --source                                 TEXT  GraceDB instance (production, playground, test, cnaf, mocked or    │
│                                                <URL>) from which the original events are downloaded.              │
│                                                [default: production]                                              │
│ --cache-path                             PATH  Directory where the event' data files are downloaded.              │
│                                                [default: /home/chanial/.cache/mock-event-generator]               │
│ --refresh-cache    --no-refresh-cache          If set, ignore the event's potential cache entry.                  │
│                                                [default: no-refresh-cache]                                        │
│ --help                                         Show this message and exit.                                        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Command `cache list`

To list the content of the cache:
```bash
meg cache list --include-files
```

More information by typing `meg cache list --help`:
```
Usage: meg cache list [OPTIONS]

 List the content of the cache.

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --include-files    --no-include-files          If set, also display the data files. [default: no-include-files]   │
│ --cache-path                             PATH  Directory where the event' data files are downloaded.              │
│                                                [default: /home/chanial/.cache/mock-event-generator]               │
│ --help                                         Show this message and exit.                                        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```


## Command `cache clean`

To empty the Mock Event Generator cache:
```bash
meg cache clean
```

More information by typing `meg cache clean --help`:
```
 Usage: meg cache clean [OPTIONS]

 Remove the content of the cache.

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --cache-path        PATH  Directory where the event' data files are downloaded.                                   │
│                           [default: /home/chanial/.cache/mock-event-generator]                                    │
│ --help                    Show this message and exit.                                                             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Command `create`

To re-create all the events belonging to a super-event in the playground GraceDB, with the search type set to 'MDC', in the cnaf GraceDB server:
```bash
$ meg create S200225q --target cnaf
```

To re-create a single event as a Test event in playground:
```bash
$ meg create G355462 --group Test --target playground
```

More information by typing `meg create --help`:
```
 Usage: meg create [OPTIONS] EVENTS...

 Create G-events and send them to GraceDB.

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    events      EVENTS...  G-events or S-events to be generated. [default: None] [required]                      │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --target                                     TEXT   GraceDB instance (production, playground, test, cnaf,      │
│                                                        mocked or <URL>) to which the time-translated events are   │
│                                                        sent.                                                      │
│                                                        [default: None]                                            │
│                                                        [required]                                                 │
│    --source                                     TEXT   GraceDB instance (production, playground, test, cnaf,      │
│                                                        mocked or <URL>) from which the original events are        │
│                                                        downloaded.                                                │
│                                                        [default: production]                                      │
│    --group                                      TEXT   Change the analysis group which identified the candidate.  │
│                                                        [default: None]                                            │
│    --search                                     TEXT   Change the type of search of the analysis pipeline. By     │
│                                                        default, the event search is changed to 'MDC'.             │
│                                                        [default: None]                                            │
│    --original-search    --no-original-search           Use the original event search type, instead of MDC.        │
│                                                        [default: no-original-search]                              │
│    --cache-path                                 PATH   Directory where the event' data files are downloaded.      │
│                                                        [default: /home/chanial/.cache/mock-event-generator]       │
│    --refresh-cache      --no-refresh-cache             If set, ignore the event's potential cache entry.          │
│                                                        [default: no-refresh-cache]                                │
│    --max-delay                                  FLOAT  Shrink the interval between the first event creation and   │
│                                                        the last upload (in seconds). By setting zero, all uploads │
│                                                        are sent at once.                                          │
│                                                        [default: None]                                            │
│    --help                                              Show this message and exit.                                │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Command `replay`:

To replay all the events in the O3 Replay MDC belonging to a superevent, with
the search type set to 'MDC' and the group type set to 'Test', in the test
GraceDB server:
```bash
$ meg replay 1262304000 1265760000 --source playground --target test --group Test
```

More information by typing `meg replay --help`:

```
meg replay --help

 Usage: meg replay [OPTIONS] START END

 Replay a set of S-events continuously and upload all G-events to GraceDB.

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    start      INTEGER  Start time (GPS) of events to replay. [default: None] [required]                         │
│ *    end        INTEGER  End time (GPS) of events to replay. [default: None] [required]                           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --target                                     TEXT   GraceDB instance (production, playground, test, DEV, cnaf, │
│                                                        local, mocked or <URL>) to which the time-translated       │
│                                                        events are sent.                                           │
│                                                        [default: None]                                            │
│                                                        [required]                                                 │
│    --source                                     TEXT   GraceDB instance (production, playground, test, DEV, cnaf, │
│                                                        local, mocked or <URL>) from which the original events are │
│                                                        downloaded.                                                │
│                                                        [default: playground]                                      │
│    --group                                      TEXT   Change the analysis group which identified the candidate.  │
│                                                        [default: None]                                            │
│    --search                                     TEXT   Change the type of search of the analysis pipeline. By     │
│                                                        default, the event search is changed to 'MDC'.             │
│                                                        [default: None]                                            │
│    --original-search    --no-original-search           Use the original event search type, instead of MDC.        │
│                                                        [default: no-original-search]                              │
│    --cache-path                                 PATH   Directory where the event' data files are downloaded.      │
│                                                        [default: /home/patrick/.cache/mock-event-generator]       │
│    --refresh-cache      --no-refresh-cache             If set, ignore the event's potential cache entry.          │
│                                                        [default: no-refresh-cache]                                │
│    --max-delay                                  FLOAT  Shrink the interval between the first event creation and   │
│                                                        the last upload (in seconds). By setting zero, all uploads │
│                                                        are sent at once.                                          │
│                                                        [default: None]                                            │
│    --help                                              Show this message and exit.                                │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Command `replay-events`:

To replay all the events in the O3 Replay MDC, with the search type set to 'MDC' and the group type set to 'Test',
in the test GraceDB server:

```bash
$ meg replay-events 1262304000 1265760000 --source playground --target test --group Test
```
```
meg replay --help

 Usage: meg replay-events [OPTIONS] START END

 Mock a search pipeline that continuously uploads G-events to GraceDB.

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    start      INTEGER  Start time (GPS) of events to replay. [default: None] [required]                         │
│ *    end        INTEGER  End time (GPS) of events to replay. [default: None] [required]                           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --target                                          TEXT   GraceDB instance (production, playground, test, DEV,  │
│                                                             cnaf, local, mocked or <URL>) to which the            │
│                                                             time-translated events are sent.                      │
│                                                             [default: None]                                       │
│                                                             [required]                                            │
│    --source                                          TEXT   GraceDB instance (production, playground, test, DEV,  │
│                                                             cnaf, local, mocked or <URL>) from which the original │
│                                                             events are downloaded.                                │
│                                                             [default: playground]                                 │
│    --replay-only-pipeline                            TEXT   Replay only events associated with the specified      │
│                                                             pipeline.                                             │
│                                                             [default: None]                                       │
│    --replay-only-search                              TEXT   Replay only events associated with the specified      │
│                                                             search.                                               │
│                                                             [default: None]                                       │
│    --group                                           TEXT   Change the analysis group which identified the        │
│                                                             candidate.                                            │
│                                                             [default: None]                                       │
│    --search                                          TEXT   Change the type of search of the analysis pipeline.   │
│                                                             By default, the event search is changed to 'MDC'.     │
│                                                             [default: None]                                       │
│    --original-search         --no-original-search           Use the original event search type, instead of MDC.   │
│                                                             [default: no-original-search]                         │
│    --cache-path                                      PATH   Directory where the event' data files are downloaded. │
│                                                             [default:                                             │
│                                                             /Users/roberto.depietri/.cache/mock-event-generator]  │
│    --refresh-cache           --no-refresh-cache             If set, ignore the event's potential cache entry.     │
│                                                             [default: no-refresh-cache]                           │
│    --max-delay                                       FLOAT  Shrink the interval between the first event creation  │
│                                                             and the last upload (in seconds). By setting zero,    │
│                                                             all uploads are sent at once.                         │
│                                                             [default: None]                                       │
│    --help                                                   Show this message and exit.                           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Command `replay-fetch`:

To fetch all the super-events present in playground in the specified gpstime intervall:
```bash
$ meg replay-fetch 1391712000 1395168000
```

More information by typing `meg replay-fetch --help`:
```
 Usage: meg replay-fetch [OPTIONS] START END

 Fetch all the S-event create on the specified gpstime intervall.


╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    start      INTEGER  Start time (GPS) of events to replay. [default: None] [required]                         │
│ *    end        INTEGER  End time (GPS) of events to replay. [default: None] [required]                           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --source                                 TEXT  GraceDB instance (production, playground, test, DEV, cnaf, local,  │
│                                                mocked or <URL>) from which the original events are downloaded.    │
│                                                [default: playground]                                              │
│ --cache-path                             PATH  Directory where the event' data files are downloaded.              │
│                                                [default: /home/depietri/.cache/mock-event-generator]              │
│ --refresh-cache    --no-refresh-cache          If set, ignore the event's potential cache entry.                  │
│                                                [default: no-refresh-cache]                                        │
│ --help                                         Show this message and exit.                                        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Command `ca-certificate`:
Certificates from a Certification Authority can be added to the list of known CA certificates:
```bash
meg ca-certificate patth/to/ca.crt
```
