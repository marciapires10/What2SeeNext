<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:template match="/">
        <div class = "pagination">
            <xsl:for-each select="//serie">
                <xsl:variable name="position" select="position()"/>
                <xsl:choose>
                    <xsl:when test="//serie[$position mod 5 != 0]">
                        <td>
                            <div class="col-md-2 clearfix d-none d-md-block">
                                <div class="card mb-2" id="full-card-all">
                                    <img>
                                        <xsl:attribute name="src">
                                            http://image.tmdb.org/t/p/w200<xsl:value-of select="poster_path"/>
                                        </xsl:attribute>
                                        <xsl:attribute name="alt">
                                            <xsl:value-of select="name"/>
                                        </xsl:attribute>
                                        <xsl:attribute name="title">
                                            <xsl:value-of select="name"/>
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
                    </xsl:when>
                    <xsl:otherwise>
                        <td>
                                <div class="col-md-2 clearfix d-none d-md-block">
                                    <div class="card mb-2" id="full-card-all">
                                        <img>
                                            <xsl:attribute name="src">
                                                http://image.tmdb.org/t/p/w200<xsl:value-of select="poster_path"/>
                                            </xsl:attribute>
                                            <xsl:attribute name="alt">
                                                <xsl:value-of select="name"/>
                                            </xsl:attribute>
                                            <xsl:attribute name="title">
                                                <xsl:value-of select="name"/>
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
                        <tr class="space">
                        </tr>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </div>
    </xsl:template>
</xsl:stylesheet>