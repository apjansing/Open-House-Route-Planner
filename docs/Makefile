TARGET = Open-House-Route-Planner
MAIN = ${TARGET}.tex
BIB = ${TARGET}.bib

DVI = ${TARGET}.dvi
PS = ${TARGET}.ps
PDF = ${TARGET}.pdf
OUT = ${TARGET}.out

TEXFILES = ${MAIN} vita.tex abstract.tex acknowledgments.tex appendix.tex
BIBFILES = ${BIB}

all:	${PDF}

clean:	clean_tex clean_code

cleaner: clean_tex clean_code
	rm -f ${PDF}

clean_tex:
	rm -f ${PS} ${DVI} ${OUT} ${TARGET}.aux ${TARGET}.lof ${TARGET}.log ${TARGET}.lot ${TARGET}.toc ${TARGET}.bbl ${TARGET}.blg ${TARGET}.fls ${TARGET}.synctex.gz ${TARGET}.fdb_latexmk *~

# If you use this makefile to build code that affects your thesis,
# edit the "Makefile.code" file for this.
clean_code:
	make -f Makefile.code clean

code:
	make -f Makefile.code

${DVI}:	clean_tex code ${TEXFILES} ${BIBFILES}
	latex -shell-escape ${MAIN}
	bibtex ${TARGET}
	latex -shell-escape ${MAIN}
	latex -shell-escape ${MAIN}

${PDF}:	${DVI}
	dvipdf ${DVI}
	pdflatex -shell-escape ${MAIN}

# Just in case you want a PostScript file for some reason
${PS}:	${DVI}
	dvips ${DVI}

# Just in case you prefer Troff
troff: 
	clear ; echo "\n\n\n\n\nBurn in the fire of a thousand demon armpit hairs!\n\n\n\n\n"
