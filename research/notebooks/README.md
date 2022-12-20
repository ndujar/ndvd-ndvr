This folder contains the material used for the experimentation and also the presented results in the [livepeer forum](https://forum.livepeer.org/c/research/15) under the different milestones.

The jupyter notebooks are fairly self-contained, installing their own libraries when needed and can be tested from [google colab](https://colab.research.google.com/).

For local deployment, though, it is recommended, to use a docker environment:

```
$ git clone https://github.com/ndujar/ndvd-ndvr.git && cd ndvd-ndvr 
$ docker run -p 8888:8888 -v $(pwd):/home/jovyan/work jupyter/datascience-notebook
```