It is preferable to install the Mock Event Generator in a virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install mock-event-generator
```

The executable `meg` has been installed and can be used to fetch existing G-events or S-events.
```
meg fetch S220609hl --source playground
```

And also to create new events:
```bash
meg create S220609hl --target cnaf
```
