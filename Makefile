# AI-Augmented Productivity for Finance — convenience targets
PY ?= python3

setup:            ## Create a local venv and install dependencies
	$(PY) -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	@echo "Done. Activate with:  source .venv/bin/activate"

check:            ## Verify the environment is ready for class
	$(PY) setup/check_setup.py

test:             ## Run the Session 3 sanity tests (against the broken DCF: they should FAIL until fixed)
	$(PY) -m pytest session-03-debugging/demo/ -q

verify:           ## Acceptance-test the whole kit (instructor/tester repo only)
	@test -f devtools/verify_course.py \
		&& $(PY) devtools/verify_course.py \
		|| echo "verify tooling ships in the instructor repo, not the student copy"

dataset:          ## Rebuild the Session 2 dataset from live SEC EDGAR data
	$(PY) session-02-coding-copilot/data/make_dataset.py

student-repo:     ## Build the student copy (strips instructor/ and solutions/) into ./student-repo
	@test -f devtools/build_student_repo.sh \
		&& bash devtools/build_student_repo.sh \
		|| echo "student-repo tooling ships in the instructor repo, not the student copy"

publish-student:  ## THE sync command: rebuild student repo, commit, push, refresh zip (rehearsal mode)
	@test -f devtools/publish_student_repo.sh \
		&& bash devtools/publish_student_repo.sh \
		|| echo "publish tooling ships in the instructor repo, not the student copy"

publish-student-class: ## Same, for CLASS: drops the rehearsal TEST-GUIDE.md
	@test -f devtools/publish_student_repo.sh \
		&& bash devtools/publish_student_repo.sh --class \
		|| echo "publish tooling ships in the instructor repo, not the student copy"

clean:            ## Remove generated outputs and caches
	rm -rf outputs .cache .pytest_cache
	find . -name __pycache__ -type d -exec rm -rf {} +


solutions-key:    ## Regenerate instructor/SOLUTIONS-KEY.md from the notebooks
	$(PY) devtools/make_solutions_key.py

.PHONY: setup check test verify dataset student-repo publish-student publish-student-class solutions-key clean
