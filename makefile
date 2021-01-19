.PHONY: install down

SHELL=/usr/bin/fish

.ONESHELL:

install:
	conda create -n wload python=3.9
	conda activate wload
	pip install requests click multiprocess tqdm
	conda deactivate
	mkdir ~/Pictures/Wallpapers

down:
	conda activate wload
	python main.py
	conda deactivate

