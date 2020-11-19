<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:template match="/">
        <xsl:for-each select="//item">
            <h3>
                <xsl:attribute name="style">color: white</xsl:attribute>
                <xsl:value-of select="author"/>
            </h3>
            <p>
                <xsl:attribute name="style">color: white</xsl:attribute>
                <xsl:attribute name="id"><xsl:value-of select="id"/></xsl:attribute>
                <xsl:value-of select="content"/>
            </p>
            <p></p>
                <button type="submit" name="delete" class="btn btn-primary" >
                    <xsl:attribute name="value">
                        <xsl:value-of select="id"/>
                    </xsl:attribute>
                    Delete
                </button>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
