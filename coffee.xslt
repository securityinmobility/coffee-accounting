<xsl:stylesheet version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fn="http://www.w3.org/2003/05/xpath-functions"
    xmlns:xs="http://www.w3.org/2001/XMLSchema-datatypes"
    xmlns="http://www.w3.org/2000/svg"
    exclude-result-prefixes="#all"
>
<xsl:param name="revision" select="'(none)'"/>
<xsl:param name="date" select="current-dateTime()"/>

<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
<xsl:strip-space elements="*"/>

<xsl:template match="/">
    <svg baseProfile="tiny" version="1.2" width="297mm" height="210mm" viewBox="0 0 297 210">
        <rect x="0" y="0" width="100%" height="100%" fill="none" stroke="black" stroke-width="1" />
        <svg x="10" y="10" width="277" height="190">
            <text dominant-baseline="hanging" text-anchor="middle" font-size="10">
            <tspan x="50%">Cyber Kaffeemaschine der Forschungsgruppe</tspan>
            <tspan x="50%" dy="1.2em">Security in Mobility</tspan>
            </text>
            <svg class="table" y="30" width="100%" height="151">
                <g>
                    <xsl:for-each select="0 to 14">
                        <rect class="row" y="{ 10 * . }" width="100%" height="10" />
                    </xsl:for-each>
                </g>
                <g>
                    <xsl:for-each select="1 to 29">
                        <line class="halfsep horizontal" x1="20%" y1="{ 5.5 +  5 * . }" x2="100%" y2="{ 5.5 +  5 * . }" />
                    </xsl:for-each>
                </g>
                <g>
                    <xsl:for-each select="0 to 40">
                        <line class="halfsep vertical" x1="{ 20 + 2 * . }%" y1="10" x2="{ 20 + 2 * . }%" y2="100%" />
                    </xsl:for-each>
                </g>

                <xsl:apply-templates select="//account" />

                <text y="5" dominant-baseline="middle" text-anchor="middle" font-size="8">
                    <tspan x="10%">Name</tspan>
                    <xsl:for-each select ="//product">
                        <xsl:variable name="xpos" select="20 + (80 div count(//product)) * (position() - 1 div 2)"/>
                        <tspan x="{ $xpos }%"><xsl:value-of select = "./name" /> (<xsl:value-of select = "./price" />)</tspan>
                    </xsl:for-each>
                </text>

                <xsl:for-each select ="//product">
                    <xsl:variable name="xpos" select="20 + (position() - 1) * (80 div count(//product))"/>
                    <line x1="{ $xpos }%" y1="0" x2="{ $xpos }%" y2="100%" stroke="red" />
                </xsl:for-each>
            </svg>
            <text x="50%" y="188" dominant-baseline="auto" text-anchor="middle" font-size="5">
                <tspan>Bezahlung an</tspan>
                <tspan class="monospace">paypal@example.org</tspan>
                <tspan>oder</tspan>
                <tspan class="monospace">DE000000000000000000000</tspan>
            </text>
        </svg>
        <text x="8" y="105" dominant-baseline="middle" text-anchor="middle" font-size="3" class="monospace" transform="rotate(-90 8 105)">
            date: <tspan><xsl:value-of select="format-dateTime($date, '[Y]-[M,2]-[D,2]')"/></tspan>
            |
            state: <tspan><xsl:value-of select="$revision"/></tspan>
        </text>

        <style>
            <![CDATA[
            text {
                font-weight: bold;
                font-family: Verdana, Helvetica, Arial, sans-serif;
            }

            rect.row {
                fill: none;
            }
            rect.row:nth-child(even) {
                fill: #eee;
            }

            .monospace {
                font-family: Courier New;
            }

            .halfsep {
                stroke: #aaa;
            }
            ]]>
        </style>
    </svg>
</xsl:template>

<xsl:template match="//account">
    <text class="monospace" x="10%" y="{ 2 + 10 * position() }" dominant-baseline="hanging" text-anchor="middle" font-size="5">
        <xsl:value-of select="substring(./@name, 1, 17)" />
    </text>
    <text class="monospace" x="10%" y="{ 9 + 10 * position() }" dominant-baseline="auto" text-anchor="middle" font-size="3">
        <xsl:value-of select="format-number(sum(./transaction/@balance, 0),'#0.00 €')" />
    </text>
</xsl:template>

</xsl:stylesheet>
