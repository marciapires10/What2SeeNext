<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:template match="/">
        <xsl:for-each select="//movie">
        <td>
            <div class="col-md-2 clearfix d-none d-md-block">
                <div class="card mb-2" id="full-card-all">
                    <img>
                        <xsl:attribute name="src">
                            http://image.tmdb.org/t/p/w200<xsl:value-of select="poster_path"/>
                        </xsl:attribute>
                        <xsl:attribute name="alt">
                            <xsl:value-of select="original_title"/>
                        </xsl:attribute>
                        <xsl:attribute name="id">
                            "card-img-all"
                        </xsl:attribute>
                    </img>
                    <div class="overlay"/>
                    <a class="btn btn-primary" id="more-movie-all">See more</a>
                </div>
            </div>
        </td>
    </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>