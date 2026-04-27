# Coffee Accounting

To ensure that coffee costs are split fairly, we need a way to track consumption, 
as the Technische Hochschule Ingolstadt does not cover these expenses.

While we initially considered developing a web application, we feared that user 
adoption would be too low if people were required to use their phones every time 
they poured a coffee. Consequently, we decided to implement a simple, scannable, 
paper-based system.

## Architecture
To maximize portability and minimize technical debt, we opted against building a 
custom software suite. Instead, we use a plain XML file as our "database" and an 
XSLT stylesheet to convert this data into a printable SVG file.

### Future Improvements
- Automated OCR: The "schemata" for the optical recognition of the form fields could 
  be generated automatically from the empty SVG sheet. (e.g. using SURF features).
- Data Integrity: The XML schema could be evolved into a Merkle-Tree structure to
  create an append-only document. Currently, this is partially addressed by calculating 
  a SHA256 hash of the database, which is printed on the list to create a physical
  paper trail. However, this solution is not yet optimal.

## Installation
This project requires an XSLT 2.0 compatible processor, such as Saxon-HE[^1]. For
a straightforward installation, place a recent version of the processor in the same 
directory as the XML files and execute it as shown below.

## Generate a new list
```bash
java -jar SaxonHE11-4J/saxon-he-11.4.jar \
    revision=$(sha256sum coffee.xml | cut -d' ' -f1 | cut -c 1-16) \
    -s:coffee.xml \
    -xsl:coffee.xslt \
    -o:coffee.svg
```

[^1]: https://www.saxonica.com/download/download_page.xml
