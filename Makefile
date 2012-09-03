# Create site in ${OUTDIR}
OUTDIR=/home/mattias/sandbox/blog.niklewski.com

POSTS_SRC=$(wildcard posts/*/*/*.txt)
POSTS=$(patsubst posts/%.txt,${OUTDIR}/%.html,${POSTS_SRC})

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

# run sass on scss files
${OUTDIR}/%.css: %.scss
	@mkdir -p $(@D)
	bundle exec sass $< > $@

# copy literally any files under static/
${OUTDIR}/%: static/%
	@mkdir -p $(@D)
	cp $< $@

all: ${POSTS} ${STATIC} ${SCSS}

clean:
	rm -rf ${OUTDIR}

