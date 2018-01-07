# Create site in ${OUT}
OUT=/home/mattias/sandbox/stage.niklewski.com
DEPLOY=/home/mattias/sandbox/mattias.niklewski.com

STATIC_SRC=$(shell find static/ -type f -name "*")
STATIC=$(patsubst static/%,${OUT}/%,${STATIC_SRC})

SCSS_SRC=$(wildcard style/*.scss)
SCSS=$(patsubst %.scss,${OUT}/%.css,${SCSS_SRC})

SITE_SCRIPT=site.py
SCRIPTS=$(filter-out ${IDX_SCRIPT},$(wildcard *.py))

# delete incomplete output files
.DELETE_ON_ERROR:

default: stage

# run sass on scss files
${SCSS}: ${OUT}/%.css: %.scss
	@echo $@
	@mkdir -p $(@D)
	@sass $< > $@

# copy any files under static/
${STATIC}: ${OUT}/%: static/%
	@echo $@
	@mkdir -p $(@D)
	@cp $< $@

# generate templated content: posts, index, feed, etc
site:
	OUT=${OUT} python ${SITE_SCRIPT}

# generate site to staging directory
stage: ${STATIC} ${SCSS} site

# move site from staging -> deploy dir, excluding drafts
deploy: stage
	rsync -r --delete --exclude "/drafts/" ${OUT}/ ${DEPLOY}/
