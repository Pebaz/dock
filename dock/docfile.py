

class MarkdeepStyles:
    __header = r'<link rel="stylesheet" href="https://casual-effects.com/markdeep/latest/{}.css?">'
    DEFAULT = ''
    JOURNAL = __header.format('journal')
    APIDOC = __header.format('apidoc')
    SLATE = __header.format('slate')
    NEWSMAG = __header.format('newsmag')
    WEBSITE = __header.format('website')
    LATEX = __header.format('latex')
    DARK = __header.format('dark')
    SLIDES = __header.format('slides')


MARKDEEP_STYLE = MarkdeepStyles.JOURNAL
MARKDEEP_FOOTER = r'<!-- Markdeep: --><style class="fallback">body{visibility:hidden;white-space:pre;font-family:monospace}</style><script src="markdeep.min.js" charset="utf-8"></script><script src="https://morgan3d.github.io/markdeep/latest/markdeep.min.js" charset="utf-8"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility="visible")</script>'
