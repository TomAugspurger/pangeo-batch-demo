IMAGE=pangeo/pangeo-notebook

notebook:
	docker run -p 8888:8888 --mount type=bind,src=$(PWD),target=/home/jovyan --env PANGEO_TOKEN -it --rm $(IMAGE) -- jupyter lab --ip=0.0.0.0 --no-browser --LabApp.token=''

ipython:
	docker run --mount type=bind,src=$(PWD),target=/home/jovyan --env PANGEO_TOKEN -it --rm $(IMAGE) -- ipython


example:
	docker run --mount type=bind,src=$(PWD),target=/home/jovyan --env PANGEO_TOKEN -it --rm $(IMAGE) -- python example.py
