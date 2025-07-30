PROJECT_SOURCE_DIR ?= $(abspath ./)
PROJECT_NAME ?= $(shell basename $(PROJECT_SOURCE_DIR))

all:
	@echo nothing special

lint:
	pre-commit run -a
	prettier --write index.html
	cd frontend/viewer && npm run lint
lint_install:
	python3 -m pip install pre-commit
	pre-commit install

install:
	python3 -m pip install 'numpy<2'
	python3 -m pip install rosbag --extra-index-url https://rospypi.github.io/simple/
	python3 -m pip install 'roscpp<1.15' --extra-index-url https://rospypi.github.io/simple/
	python3 -m pip install -e .
package:
	python3 -m pip install build
	python3 -m build --sdist
	# tar -tvf dist/frames-pack*.tar.gz
pypi_remote ?= pypi
upload:
	python3 -m pip install twine
	python3 -m twine upload --skip-existing -r $(pypi_remote) --verbose dist/*.tar.gz

clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf __pycache__
	rm -f *.pyc

test: pytest clitest
pytest:
	python3 -m pip install pytest pytest-xdist
	# pytest --capture=tee-sys tests
	# pytest tests -vv
	PYTHONPATH=src:$$PYTHONPATH pytest tests -vv -n 10
clitest:
	python3 -m frames_pack
	python3 -m frames_pack.compile --help
	python3 -m frames_pack.compile rosbag2framespack data/65ce63c95fbf245fbffd97419d48af2e.bag dump build/frames_pack.bin
	python3 -m frames_pack.compile framespack2json build/frames_pack.bin
	python3 -m frames_pack.compile geojson2framespack data/cloverleaf.pbf.json dump build/frames_pack2.bin
	python3 -m frames_pack.compile framespack2json build/frames_pack2.bin
.PHONY: test pytest clitest

# python:3.12-bookworm
DOCKER_RELEASE ?= ghcr.io/cubao/build-env-manylinux2014-x64:v0.0.5
DEV_CONTAINER_NAME ?= $(USER)_$(subst /,_,$(PROJECT_NAME)____$(PROJECT_SOURCE_DIR))
DEV_CONTAINER_IMAG ?= $(DOCKER_RELEASE)
test_in_dev_container:
	docker ps | grep $(DEV_CONTAINER_NAME) \
		&& docker exec -it $(DEV_CONTAINER_NAME) bash \
		|| docker run --rm --name $(DEV_CONTAINER_NAME) \
			--network host --security-opt seccomp=unconfined \
			-v `pwd`:`pwd` -w `pwd` -it $(DEV_CONTAINER_IMAG) bash
