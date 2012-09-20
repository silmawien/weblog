# Create site in ${OUTDIR}
OUTDIR=/home/mattias/sandbox/stage.niklewski.com
DEPLOYDIR=/home/mattias/sandbox/blog.niklewski.com

POSTS_SRC=$(wildcard posts/*/*/*.txt)
POSTS=$(patsubst posts/%.txt,${OUTDIR}/%.html,${POSTS_SRC})

DRAFTS_SRC=$(wildcard drafts/*.txt)
DRAFTS=$(patsubst drafts/%.txt,${OUTDIR}/drafts/%.html,${DRAFTS_SRC})

STATIC_SRC=$(shell find static/ -type f -name "*")
STATIC=$(patsubst static/%,${OUTDIR}/%,${STATIC_SRC})

SCSS_SRC=$(wildcard style/*.scss)
SCSS=$(patsubst %.scss,${OUTDIR}/%.css,${SCSS_SRC})

TEMPLATES=$(wildcard templates/*)

SCRIPTS=$(wildcard *.py)

INDEX=${OUTDIR}/index.html

# src paths and webroot-relative dst paths to all posts
POSTS_ENV=SRC="${POSTS_SRC}" DST="$(subst ${OUTDIR},,${POSTS})"

# delete incomplete output files
.DELETE_ON_ERROR:

#tmp:
#	${POSTS_ENV} python

default: stage

# run markdown on txt files under posts/
${POSTS}: ${OUTDIR}/%.html: posts/%.txt ${TEMPLATES} ${SCRIPTS}
	@echo $<
	@mkdir -p $(@D)
	@DST=$(subst ${OUTDIR},,$@) python render_post.py $< > $@

# same for drafts (but see deploy rule)
${DRAFTS}: ${OUTDIR}/drafts/%.html: drafts/%.txt ${TEMPLATES} ${SCRIPTS}
	@echo $<
	@mkdir -p $(@D)
	@DST=$(subst ${OUTDIR},,$@) python render_post.py $< > $@

# run sass on scss files
${SCSS}: ${OUTDIR}/%.css: %.scss
	@echo $<
	@mkdir -p $(@D)
	@sass $< > $@

# copy literally any files under static/
${STATIC}: ${OUTDIR}/%: static/%
	@echo $<
	@mkdir -p $(@D)
	@cp $< $@

# render front page
${INDEX}: ${POSTS} ${TEMPLATES} ${SCRIPTS}
	@echo index
	@${POSTS_ENV} python render_index.py > $@

# generate site to staging directory
stage: ${POSTS} ${DRAFTS} ${STATIC} ${SCSS} ${INDEX}

clean:
	rm -rf ${OUTDIR}

# move site from staging -> deploy dir, excluding drafts
deploy: stage
	rsync -r --delete --exclude "/drafts/" ${OUTDIR}/ ${DEPLOYDIR}/
