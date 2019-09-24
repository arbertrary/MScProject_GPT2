# Masterpraktikum

## Overview

- `allenai/bilm-tf` is the elmo implementation found on [https://github.com/allenai/bilm-tf](https://github.com/allenai/bilm-tf)
- `nshepperd/gpt-2` is a gpt2 implementation found on [https://github.com/nshepperd/gpt-2](https://github.com/nshepperd/gpt-2)
- `crawl` contains the scripts for the crawler used on [http://www.team-andro.com/](http://www.team-andro.com/)
- `training` and `predict` are an unusable amalgamation of scripts and kubernetes yaml configs
- `report` contains the TeX files for the report
- `notes` contains ... notes


## Stuff on vingilot (the relevant parts)

```
/home/stud/bernstetter
├── datasets
│   ├── minimal_corpus          // a minimal corpus used for test runs
│   ├── super_corpus            // Team Andro text combined with existing text
│   ├── ta-mongodb              // everything from the crawler in a mongodb
│   ├── TeamAndroStructured     // Team Andro text in forum hierarchy
│   └── TeamAndroUnstructured   // Team Andro text as simple plain text files
├── elmo                        
│   ├── elmo_model_final
│   └── elmo_output
├── gpt2                        // text samples and checkpoints generated during gpt2 training
│   ├── gpt2minimal
│   └── gpt2output
├── models                      // final models together with options and parameter files etc
│   ├── minimal117M
│   ├── super345M
│   └── superElmo
```
