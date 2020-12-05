<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:template match="/">
    <table class="table">
        <thead>
            <tr>
                <th scope="col">Position</th>
                <th scope="col">Title</th>
                <th scope="col">Button</th>
            </tr>
        </thead>
        <tbody>
        <xsl:for-each select="tools/tool">
            <tr>
                <th scope="row"><xsl:value-of select="title"/></th>
                <th><xsl:value-of select="position"/></th>
                <th><a href="<xsl:value-of select='href'/>"><xsl:value-of select="href"/></a></th>
            </tr>
        </xsl:for-each>
        </tbody>
    </table>   
    </xsl:template>
</xsl:stylesheet>