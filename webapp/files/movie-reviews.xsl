<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:template match="/">
        <xsl:for-each select="//review">
            <h3>
                <xsl:attribute name="style">white</xsl:attribute>
                <xsl:value-of select="results/item/author"/>
            </h3>
            <p>
                <xsl:attribute name="style">white</xsl:attribute>
                <xsl:value-of select="results/item/content"/>
            </p>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
