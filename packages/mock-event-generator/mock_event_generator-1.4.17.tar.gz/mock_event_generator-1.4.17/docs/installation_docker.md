Containers for the Mock Event Generator are stored in the Gitlab Container Registry. To access it, a [Personal Access Token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) (with at least the read_registry scope) is required. To login:

```bash
echo <access-token> | docker login containers.ligo.org -u <token-name> --password-stdin
```

Upon successful login, the latest Docker image can be run. It contains a pre-loaded mock super-event from GraceDB playground. By creating a docker volume for the Mock Event Generator cache, downloaded events can be persisted. It is possible to use the host x509 certificate:
```
docker volume create meg-cache
docker run --pull always -it --rm \
    -v meg-cache:/home/meguser/.cache/mock-event-generator \
    -v /tmp/x509up_u$(id -u):/tmp/x509up_u1000 \
    containers.ligo.org/emfollow/mock-event-generator:latest bash
```

It is also possible not to bind the host x509 certificate to the container, but rather executing `ligo-proxy-init` inside the container:
```
docker volume create meg-cache
docker run --pull always -it --rm \
    -v meg-cache:/home/meguser/.cache/mock-event-generator \
    containers.ligo.org/emfollow/mock-event-generator:latest bash
meguser@f8e5602cb5d7:~$ ligo-proxy-init albert.einstein
Enter password for 'albert.einstein' on login.ligo.org:
```

Commands in the docker image can then be issued:
```
meguser@f8e5602cb5d7:~$ meg cache list
Cache: /home/meguser/.cache/mock-event-generator
└── S220609hl
    ├── G587364     gstlal         CBC            AllSky         1338848303.813655
    ├── G587365     gstlal         CBC            AllSky         1338848303.808759
    ├── G587366     MBTAOnline     CBC            AllSky         1338848303.869315
    ├── G587367     CWB            Burst          BBH            1338848303.7873
    ├── G587368     CWB            Burst          AllSky         1338848303.7855
    └── G587369     CWB            Burst          BBH            1338848303.7875
```
or
```
meguser@f8e5602cb5d7:~$ meg fetch E394410
2022-06-22 13:29:32 INFO     Downloading E394410 from the production GraceDB server...
```
