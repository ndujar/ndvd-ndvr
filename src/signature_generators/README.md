# Go dev environment

Build it with:

```
docker build -t ubuntu-go -f Dockerfile 
```

Run it with:
```
docker run -it -v ${PWD}:/test ubuntu-go /bin/bash
```

 
## License

[Apache-2.0 License](LICENSE)
