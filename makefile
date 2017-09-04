filename=these

open:
	evince $(filename).pdf &

simple:
	pdflatex $(filename)

complete:
	pdflatex $(filename)
	bibtex $(filename)
	pdflatex $(filename)
	pdflatex $(filename)
