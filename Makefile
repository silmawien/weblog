# Create site in ${OUT}
OUT=/home/mattias/sandbox/stage.niklewski.com
DEPLOY=/home/mattias/sandbox/mattias.niklewski.com

STATIC_SRC=$(shell find static/ -type f -name "*")
STATIC=$(patsubst static/%,${OUT}/%,${STATIC_SRC})

STYLE_SRC=$(shell find style/ -type f -name "*")
STYLE=$(patsubst %,${OUT}/%,${STYLE_SRC})

SITE_SCRIPT=site.py
SCRIPTS=$(filter-out ${IDX_SCRIPT},$(wildcard *.py))

# delete incomplete output files
.DELETE_ON_ERROR:

default: stage

# copy styles
${STYLE}: ${OUT}/%: %
	@echo $@
	@mkdir -p $(@D)
	@cp $< $@

# copy any files under static/
${STATIC}: ${OUT}/%: static/%
	@echo $@
	@mkdir -p $(@D)
	@cp $< $@

# generate templated content: posts, index, feed, etc
site:
	OUT=${OUT} python ${SITE_SCRIPT}

# generate site to staging directory
stage: ${STATIC} ${STYLE} site

# move site from staging -> deploy dir, excluding drafts
deploy: stage
	rsync -r --delete --exclude "/drafts/" ${OUT}/ ${DEPLOY}/
