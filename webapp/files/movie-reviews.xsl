<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:template match="/">
        <xsl:for-each select="//review">
            <h3>
                <xsl:attribute name="style">color: white</xsl:attribute>
                <xsl:value-of select="results/item/author"/>
            </h3>
            <p>
                <xsl:attribute name="style">color: white</xsl:attribute>
                <xsl:value-of select="results/item/content"/>
            </p>
            <p></p>
            <form method="post">
                <button type="submit" name="delete-review" class="btn btn-primary">
                    <xsl:attribute name="value">
                        <xsl:value-of select="id"/>
                    </xsl:attribute>
                    Delete review
                </button>
                <button type="submit" name="update-review" class="btn btn-primary">
                    <xsl:attribute name="value">
                        <xsl:value-of select="id"/>
                    </xsl:attribute>
                    Update review
                </button>
            </form>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
