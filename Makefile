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

# delete incomplete output files
.DELETE_ON_ERROR:

# run markdown on txt files under posts/
${OUTDIR}/%.html: posts/%.txt ${TEMPLATES}
	@mkdir -p $(@D)
	python mm.py $< > $@

# same for drafts (but see deploy rule)
${OUTDIR}/drafts/%.html: drafts/%.txt ${TEMPLATES}
	@mkdir -p $(@D)
	python mm.py $< > $@

# run sass on scss files
${OUTDIR}/%.css: %.scss
	@mkdir -p $(@D)
	sass $< > $@

# copy literally any files under static/
${OUTDIR}/%: static/%
	@mkdir -p $(@D)
	cp $< $@

# generate site to staging directory
stage: ${POSTS} ${DRAFTS} ${STATIC} ${SCSS}

clean:
	rm -rf ${OUTDIR}

# move site from staging -> deploy dir, excluding drafts
deploy: stage
	rsync -r --delete --exclude "/drafts/" ${OUTDIR}/ ${DEPLOYDIR}/
