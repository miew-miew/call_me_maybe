export UV_CACHE_DIR=$(HOME)/goinfre/uv-cache
export HF_HOME=$(HOME)/goinfre/huggingface-cache

install:
# 	@echo ${UV_CACHE_DIR}
# 	@echo ${HF_HOME}
	uv sync

run:
	uv run python -m src

debug:
	uv run python -m pdb -m src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	flake8 .
	mypy . --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
