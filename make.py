import sys, os, shutil, subprocess, logging
from getopt import getopt, GetoptError


OPTIONS = {
	"BUILDDIR"      : "build",
	"SOURCEDIR"     : "source",
	"PAPER"         : "",
	"SPHINXOPTS"    : "",
	"SPHINXBUILD"   : "sphinx-build",
	"DOCTREES"      : "%(BUILDDIR)s/doctrees",
	"TARGETDIR"     : "%(BUILDDIR)s/%(TARGET)s",
	"ALLSPHINXOPTS" : "%(DOCTREES)s %(PAPER)s %(SPHINXOPTS)s %(SOURCEDIR)s",
	"CMD"           : "%(SPHINXBUILD)s -b %(TARGET)s %(ALLSPHINXOPTS)s %(TARGETDIR)s",
}


def getTarget(targetName=None):
	# Targets supported by this make.
	# Remove or comment out function to remove it from supported build targets.
	# Add custom function to extend set of supported build targets.

	### {{{ Targets
	def html(argv):
		"""to make standalone HTML files"""
		callBuilder()
		show.info("Build finished. The HTML pages are in %(TARGETDIR)s.", OPTIONS)

	def dirhtml(argv):
		"""to make HTML files named index.html in directories"""
		callBuilder()
		show.info("Build finished. The HTML pages are in %(TARGETDIR)s.", OPTIONS)

	def singlehtml(argv):
		"""to make a single large HTML file"""
		callBuilder()
		show.info("Build finished. The HTML page are in %(TARGETDIR)s.", OPTIONS)

	def pickle(argv):
		"""to make pickle files"""
		callBuilder()
		show.info("Build finished; now you can process the pickle files.")

	def json(argv):
		"""to make JSON files"""
		callBuilder()
		show.info("Build finished; now you can process the JSON files.")

	def htmlhelp(argv):
		"""to make HTML files and a HTML help project"""
		callBuilder()
		show.info("Build finished; now you can run HTML Help Workshop with the .hhp project file in %(TARGETDIR)s.", OPTIONS)

	def qthelp(argv):
		"""to make HTML files and a qthelp project"""
		callBuilder()
		show.info("Build finished; now you can run 'qcollectiongenerator' with the .qhcp project file in %(TARGETDIR)s, like this:", OPTIONS)
		show.info("# qcollectiongenerator %s", os.path.join(OPTIONS["TARGETDIR"], "qweasd.qhcp"))
		show.info("To view the help file:")
		show.info("# assistant -collectionFile %s", os.path.join(OPTIONS["TARGETDIR"], "qweasd.qhc"))

	def devhelp(argv):
		"""to make HTML files and a Devhelp project"""
		callBuilder()
		show.info("Build finished.")

	def epub(argv):
		"""to make an epub"""
		callBuilder()
		show.info("Build finished. The epub file is in %(TARGETDIR)s.", OPTIONS)

	def latex(argv):
		"""\
to make LaTeX files

options:
  -p <paper>    Sets PAPER to <paper> value (defaults to "").
                Only the first occurrence is taken into account.
                Example: make.py latex -p a4"""
		try:
			opts, args = getopt(argv, "p:")
		except GetoptError as e:
			log.error(e)
			args = []
		else:
			if len(opts):
				OPTIONS["PAPER"] = opts[0][1]
		callBuilder()
		show.info("Build finished; the LaTeX files are in %(TARGETDIR)s.", OPTIONS)
		show.info("Run 'make' in that directory to run these through (pdf)latex (use 'make.py latexpdf' here to do that automatically).")

	def latexpdf(argv):
		"""\
to make LaTeX files and run them through pdflatex

options:
  See help for target 'latex'"""
		OPTIONS["TARGET"] = "latex"
		latex(argv)
		show.info("Running LaTeX files through pdflatex...")
		subprocess.check_call(("make -C %(TARGETDIR)s all-pdf" % OPTIONS).split())
		show.info("pdflatex finished; the PDF files are in %(TARGETDIR)s.", OPTIONS)

	def text(argv):
		"""to make text files"""
		callBuilder()
		show.info("Build finished. The text files are in %(TARGETDIR)s.", OPTIONS)

	def man(argv):
		"""to make manual pages"""
		callBuilder()
		show.info("Build finished. The manual pages are in %(TARGETDIR)s.", OPTIONS)

	def texinfo(argv):
		"""to make Texinfo files"""
		callBuilder()
		show.info("Build finished. The Texinfo files are in %(TARGETDIR)s.", OPTIONS)
		show.info("Run 'make' in that directory to run these through makeinfo (use 'make.py info' here to do that automatically).")

	def info(argv):
		"""to make Texinfo files and run them through makeinfo"""
		OPTIONS["TARGET"] = "texinfo"
		texinfo(argv)
		show.info("Running Texinfo files through makeinfo...")
		subprocess.check_call(("make -C %(TARGETDIR)s info" % OPTIONS).split())
		show.info("makeinfo finished; the Info files are in %(TARGETDIR)s.", OPTIONS)

	def gettext(argv):
		"""to make PO message catalogs"""
		OPTIONS["DOCTREESDIR"] = ""
		callBuilder()
		show.info("Build finished. The message catalogs are in %(TARGETDIR)s.", OPTIONS)

	def changes(argv):
		"""to make an overview of all changed/added/deprecated items"""
		callBuilder()
		show.info("The overview file is in %(TARGETDIR)s.", OPTIONS)

	def linkcheck(argv):
		"""to check all external links for integrity"""
		callBuilder()
		show.info("Link check complete; look for any errors in the above output or in %s.",
			os.path.join(OPTIONS["TARGETDIR"], output.txt))

	def doctest(argv):
		"""to run all doctests embedded in the documentation (if enabled)"""
		callBuilder()
		show.info("Testing of doctests in the sources finished, look at the results in %s.",
			os.path.join(OPTIONS["TARGETDIR"], output.txt))

	def clean(argv):
		"""to remove BUIDLDIR and its contents"""
		parseOptions()
		buildDir = OPTIONS["BUILDDIR"]
		if os.path.exists(buildDir):
			try:
				shutil.rmtree(buildDir)
				show.info("Build folder '%s' cleaned", buildDir)
			except Exception as e:
				log.error("Cannot remove folder '%s'!\n\t%s", buildDir, e)
		else:
			log.warning("Folder '%s' not found, nothing to clean", buildDir)
	### Targets }}}

	TARGETS = dict([(name, item) for name, item in locals().iteritems() if hasattr(item, "__call__")])
	if targetName:
		return TARGETS.get(targetName, None)
	else:
		return TARGETS


def parseOptions():
	o = OPTIONS
	o["BUILDDIR"] = os.path.normpath(o["BUILDDIR"])
	o["SOURCEDIR"] = os.path.normpath(o["SOURCEDIR"])
	o["TARGETDIR"] = os.path.normpath(o["TARGETDIR"] % o)
	if o["DOCTREES"]:
		o["DOCTREES"] = "-d %s" % os.path.normpath(o["DOCTREES"] % o)
	if o["PAPER"]:
		o["PAPER"] = "-D latex_paper_size=%(PAPER)s" % o
	o["ALLSPHINXOPTS"] = o["ALLSPHINXOPTS"] % o
	o["CMD"] = o["CMD"] % o
	return o["CMD"]


def callBuilder():
	cmd = parseOptions()
	show.info("Running Sphinx builder with the following command:\n\n  %s\n", cmd)
	subprocess.check_call(cmd.split())
	show.info("")


def showFnHelp(targetName, target):
	HELP = """\
Use 'make.py %(name)s [options]' %(begin)s
%(more)s%(rest)s"""

	doc = (target.__doc__ or "*** help is not available ***").split("\n")
	o = {
		"name": targetName,
		"begin": doc[0],
		"rest": "\n".join(doc[1:])
	}
	o["more"] = o["rest"] and " " or "\nThis target has no options defined"
	show.info(HELP, o)


def showHelp(targets):
	HELP = """\
Use 'make.py <target> [options]' where <target> is one of
%s

Use 'make.py -h <target>' to see help for <target> and it's options
(not every <target> has options defined)

Use 'make.py [-h]' to show this help and exit"""

	doc = []
	if targets:
		maxNameLen = max([len(i) for i in targets.keys()])
		tpl = "  %%-%ds%%s" % (maxNameLen + 1)
		for name, fn in sorted(targets.items()):
			doc.append(tpl % (name, (fn.__doc__ or "*** help is not available ***").split("\n")[0]))
	else:
		doc.append("*** No targets defined ***")
	show.info(HELP, "\n".join(doc))


show = logging.getLogger("make")
log = logging.getLogger("make.log")

def configureLoggers():
	show.setLevel(logging.INFO)
	showHandler = logging.StreamHandler()
	showHandler.setFormatter(logging.Formatter("%(message)s"))
	show.addHandler(showHandler)
	log.setLevel(logging.WARNING)
	logHandler = logging.StreamHandler()
	logHandler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
	log.addHandler(logHandler)
	log.propagate = 0


def main(argv):
	try:
		opts, args = getopt(argv, "h")
	except GetoptError as e:
		log.error(e)
		show.info("Use 'make.py [-h]' for help")
	else:
		targetName = args and args[0] or None
		target = getTarget(targetName)
		helpMode = bool(opts)
		if not targetName:
			showHelp(target)
		elif not target:
			log.error("Target '%s' not found", targetName)
		elif helpMode:
			showFnHelp(targetName, target)
		else:
			OPTIONS["TARGET"] = targetName
			target(args[1:])


if __name__ == "__main__":
	configureLoggers()
	main(sys.argv[1:])
	show.info("")
