# Coffee Accounting

We have to keep track who drinks how much coffee to be able to split the
costs, as unfortunately the Technische Hochschule Ingolstadt does not pay
for our coffee.
The initial idea was to create a web app for tracking usage, but we feared
acceptance would be too low when requiring users to use their phone when
consuming coffee. Instead we decided for going with an easily scannable paper
based list.

## Architecture
For maximum portability (and to keep the technical debt fairly low), we decided 
against developing a custom software tool. Instead, we use a plain XML-file as 
the "database", and a XSLT-stylesheet to convert it into a SVG-file that can be 
printed.

### Future ideas
- The "schemata" for the optical recognition of the form fields could be 
generated automatically from the empty SVG-sheet. Keywords: SURF-features
- The XML-scheme could be improved to follow a Merkle-Tree scheme, i.e. build 
an append-only document. This is already slightly addressed by calculating a 
SHA256-hash over the database that ends up on the paper list and therefore 
leaves a papertrail. This solution is still not optimal, though.


## Installation
This project requires a XSLT 2.0 compatible processor, f.e. Saxon-HE[^1].
For easy installation, put a somewhat recent version next to the XML files
and use it as demonstrated below.

## Create new list
`$ java -jar SaxonHE11-4J/saxon-he-11.5.jar revision=$(sha256sum coffee.xml | cut -d' ' -f1 | cut -c 1-16) -s:coffee.xml -xsl:coffee.xslt -o:coffee.svg`

[1] https://www.saxonica.com/download/download_page.xml