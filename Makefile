# Create site in ${OUT}
OUT=/home/mattias/sandbox/stage.niklewski.com
DEPLOY=/home/mattias/sandbox/mattias.niklewski.com

# import config variables from python
ROOT=`python -c "import config; print config.BLOG['root']"`

POSTS_SRC=$(wildcard posts/*/*/*.txt)
POSTS=$(patsubst posts/%.txt,${OUT}/%.html,${POSTS_SRC})

DRAFTS_SRC=$(wildcard drafts/*.txt)
DRAFTS=$(patsubst drafts/%.txt,${OUT}/drafts/%.html,${DRAFTS_SRC})

STATIC_SRC=$(shell find static/ -type f -name "*")
STATIC=$(patsubst static/%,${OUT}/%,${STATIC_SRC})

SCSS_SRC=$(wildcard style/*.scss)
SCSS=$(patsubst %.scss,${OUT}/%.css,${SCSS_SRC})

TEMPLATES=$(wildcard templates/*)

SSI_SRC=footer.html
SSI=$(addprefix ${OUT}/ssi/,${SSI_SRC})

IDX_SCRIPT=render_index.py
SCRIPTS=$(filter-out ${IDX_SCRIPT},$(wildcard *.py))

INDEX=${OUT}/index.html

# parameters for multi-post scripts
FULL_ENV=SRC="${POSTS_SRC}" URL="$(subst ${OUT},${ROOT},${POSTS})" OUT=${OUT}

# delete incomplete output files
.DELETE_ON_ERROR:

default: stage

# Generated chunks. These are included via SSI to avoid rebuilding all pages
# when e.g. the footer changes.
${SSI}: ${OUT}/%.html: ${SCRIPTS} ${POSTS_SRC} ${TEMPLATES}
	@echo $@
	@mkdir -p ${@D}
	@${FULL_ENV} python gen_$(notdir $*).py > $@

# run markdown on txt files under posts/
${POSTS}: ${OUT}/%.html: posts/%.txt ${TEMPLATES} ${SCRIPTS}
	@echo $@
	@mkdir -p $(@D)
	@URL=$(subst ${OUT},${ROOT},$@) python render_post.py $< > $@

# same for drafts (but see deploy rule)
${DRAFTS}: ${OUT}/drafts/%.html: drafts/%.txt ${TEMPLATES} ${SCRIPTS}
	@echo $@
	@mkdir -p $(@D)
	@URL=$(subst ${OUT},${ROOT},$@) python render_post.py $< > $@

# run sass on scss files
${SCSS}: ${OUT}/%.css: %.scss
	@echo $@
	@mkdir -p $(@D)
	@sass $< > $@

# copy literally any files under static/
${STATIC}: ${OUT}/%: static/%
	@echo $@
	@mkdir -p $(@D)
	@cp $< $@

# Render front page. This script reads every single post, so other index pages
# (tags, by-date index) are generated here too, to keep things fast.
${INDEX}: ${POSTS} ${TEMPLATES} ${SCRIPTS} ${IDX_SCRIPT}
	@echo $@
	@${FULL_ENV} python render_index.py > $@

# generate site to staging directory
stage: ${POSTS} ${DRAFTS} ${STATIC} ${SCSS} ${INDEX} ${SSI}

clean:
	rm -rf ${OUT}
	rm -rf gen/

# move site from staging -> deploy dir, excluding drafts
deploy: stage
	rsync -r --delete --exclude "/drafts/" ${OUT}/ ${DEPLOY}/
