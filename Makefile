# Idea from: 
#* http://stackoverflow.com/questions/637227/makefile-for-multi-file-latex-document
#* http://stackoverflow.com/questions/4058840/makefile-that-distincts-between-windows-and-unix-like-systems

.PHONY: all clean
CLASSES = 01 02 03 04 05 06 07 08 09 10 11 12 13 14
MAIN = 4M3-course

ifdef SystemRoot
	RM = -del /Q/F
	SUBDIR = classes\\
else
	RM = -rm -f
	SUBDIR = classes/
endif

.DEFAULT_GOAL := 01

default:
	pdflatex --shell-escape --jobname=$(SUBDIR)2014-4M3-class-$* $(MAIN).tex;
	open $(SUBDIR)2014-4M3-class-$*.pdf

all: clean
	$(foreach FILE, $(CLASSES), $(MAKE) $(FILE);)

$(CLASSES): %:
    # Runs PDF latex on the main file, sending in jobname that is used in 
    # $(MAIN).tex to \input{} the correct class file
	pdflatex --shell-escape --jobname=$(SUBDIR)2014-4M3-class-$* $(MAIN).tex;
    
	open $(SUBDIR)2014-4M3-class-$*.pdf

clean:  
    # Windows requires one wildcard entry per line, unfortunately
	$(RM) *.log
	$(RM) *.aux
	$(RM) *.out
	$(RM) *.idx
	$(RM) *.lof
	$(RM) *.lot
	$(RM) *.nav
	$(RM) *.toc
	$(RM) *.ilg
	$(RM) *.ind
	$(RM) *.glo
	$(RM) *.gls
	$(RM) *.snm
	$(RM) *.vrb
	$(RM) $(SUBDIR)*.log
	$(RM) $(SUBDIR)*.aux
	$(RM) $(SUBDIR)*.out
	$(RM) $(SUBDIR)*.idx
	$(RM) $(SUBDIR)*.lof
	$(RM) $(SUBDIR)*.lot
	$(RM) $(SUBDIR)*.nav
	$(RM) $(SUBDIR)*.toc
	$(RM) $(SUBDIR)*.ilg
	$(RM) $(SUBDIR)*.ind
	$(RM) $(SUBDIR)*.glo
	$(RM) $(SUBDIR)*.gls
	$(RM) $(SUBDIR)*.snm
	$(RM) $(SUBDIR)*.vrb
