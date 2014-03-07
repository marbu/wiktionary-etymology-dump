<?xml version="1.0"?>
<xsl:stylesheet version = '1.0'
  xmlns:xsl='http://www.w3.org/1999/XSL/Transform'
  xmlns:mw="http://www.mediawiki.org/xml/export-0.8/" >

<!-- this xslt style generates plain text file -->
<xsl:output method="text" indent="no" />

<!-- don't output any string values without asking
     (redefinition of one of the implicit templates) -->
<xsl:template match="text()|@*"/>

<xsl:template match="mw:page">
  <xsl:text>---MEDIAWIKI-WORD--- </xsl:text>
  <xsl:value-of select="mw:title/text()"/>
  <xsl:text>&#10;</xsl:text>
  <xsl:value-of select="mw:revision/mw:text/text()"/>
  <xsl:text>&#10;</xsl:text>
</xsl:template>

</xsl:stylesheet>
