# Create site in ${OUT}
OUT=/home/mattias/sandbox/stage
DEPLOY=/home/mattias/sandbox/blog

ROOT=/mattias

POSTS_SRC=$(wildcard posts/*/*/*.txt)
POSTS=$(patsubst posts/%.txt,${OUT}/%.html,${POSTS_SRC})

DRAFTS_SRC=$(wildcard drafts/*.txt)
DRAFTS=$(patsubst drafts/%.txt,${OUT}/drafts/%.html,${DRAFTS_SRC})

STATIC_SRC=$(shell find static/ -type f -name "*")
STATIC=$(patsubst static/%,${OUT}/%,${STATIC_SRC})

SCSS_SRC=$(wildcard style/*.scss)
SCSS=$(patsubst %.scss,${OUT}/%.css,${SCSS_SRC})

TEMPLATES=$(wildcard templates/*)

GEN_TEMPLATES=gen/footer.html gen/nav.html

IDX_SCRIPT=render_index.py
SCRIPTS=$(filter-out ${IDX_SCRIPT},$(wildcard *.py))

INDEX=${OUT}/index.html

# parameters for single-post scripts
POST_ENV=TMP="${GEN_TEMPLATES}"

# parameters for multi-post scripts
FULL_ENV=SRC="${POSTS_SRC}" URL="$(subst ${OUT},${ROOT},${POSTS})" TMP="${GEN_TEMPLATES}" OUT=${OUT}

# delete incomplete output files
.DELETE_ON_ERROR:

#debugenv:
#	${FULL_ENV} python

default: stage

# Generated templates. This extra step allows us to generate common pieces
# once, and include the result from many pages. A generated template can itself
# use templates. E.g. "gen/footer.html" is rendered with "gen_footer.py" and
# included from render_post.py.
${GEN_TEMPLATES}: ${SCRIPTS} ${POSTS_SRC} ${TEMPLATES}
	@echo $@
	@mkdir -p ${@D}
	@${FULL_ENV} python $(patsubst gen/%.html,gen_%.py,$@) > $@

# run markdown on txt files under posts/
${POSTS}: ${OUT}/%.html: posts/%.txt ${TEMPLATES} ${SCRIPTS} ${GEN_TEMPLATES}
	@echo $@
	@mkdir -p $(@D)
	@${POST_ENV} URL=$(subst ${OUT},${ROOT},$@) python render_post.py $< > $@

# same for drafts (but see deploy rule)
${DRAFTS}: ${OUT}/drafts/%.html: drafts/%.txt ${TEMPLATES} ${SCRIPTS} | ${GEN_TEMPLATES}
	@echo $@
	@mkdir -p $(@D)
	@${POST_ENV} URL=$(subst ${OUT},${ROOT},$@) python render_post.py $< > $@

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
${INDEX}: ${POSTS} ${TEMPLATES} ${SCRIPTS} ${IDX_SCRIPT} ${GEN_TEMPLATES}
	@echo $@
	@${FULL_ENV} python render_index.py > $@

# generate site to staging directory
stage: ${POSTS} ${DRAFTS} ${STATIC} ${SCSS} ${INDEX}

clean:
	rm -rf ${OUT}
	rm -rf gen/

# move site from staging -> deploy dir, excluding drafts
deploy: stage
	rsync -r --delete --exclude "/drafts/" ${OUT}/ ${DEPLOY}/
