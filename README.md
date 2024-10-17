# MSc Programming Project 2019

This was a programming project done during my M.Sc. program at University of Würzburg.

The goal was to fine-tune the - at that time in 2019 - rather small publically available GPT-2 models.
Since these models then only knew English, I fine-tuned them on german Wikipedia texts and posts from a german phpBB3 internet forum focussing on the rather specific topic of fitness and strength training.
I successfully managed to train the models to respond in german to german prompts and provide e.g. strength training advice.

A write-up of this project can be found here: [/report/report.pdf](https://github.com/arbertrary/MScProject_GPT2/blob/master/report/report.pdf)


## Overview

- `allenai/bilm-tf` is the elmo implementation found on [https://github.com/allenai/bilm-tf](https://github.com/allenai/bilm-tf)
- `nshepperd/gpt-2` is a gpt2 implementation found on [https://github.com/nshepperd/gpt-2](https://github.com/nshepperd/gpt-2)
- `crawl` contains the scripts for the crawler used on [http://www.team-andro.com/](http://www.team-andro.com/)
- `training` and `predict` are an unusable amalgamation of scripts and kubernetes yaml configs
- `report` contains the TeX files for the report
- `notes` contains ... notes


## Container Registry

The container registry in this repository currently contains the two docker containers which were used to train the ELMo model (bilmtfcuda10) and the gpt2 model.

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

## Generate Samples from the gpt2 models

The gpt2 models in `models/` can directly be used for sample generation using e.g. the script in `nshepperd/gpt-2/src/interactive_conditional_samples.py`.

- Move the model into `nshepperd/gpt-2/models`
- Obviously make sure all Python requirements are installed
- Call e.g. `python src/interactive_conditional_samples.py --top_k 40 --temperature 0.9 --seed 2000 --model_name super345M`
(for the different options see their documentation/code)
- Wait
- Enter your model prompt text
- Wait
- Enjoy your generated text sample



