from .bio import SITE_URL

# DDG search form from suggestions in the original config.
# (translatable)
SEARCH_FORM = f"""
<!-- DuckDuckGo custom search -->
<form method="get" id="search" action="https://duckduckgo.com/"
 class="navbar-form pull-left">
<img src="https://duckduckgo.com/assets/logo_header.v109.svg" width="28" height="28">
<input type="hidden" name="sites" value="{SITE_URL}">
<input type="hidden" name="k8" value="#444444">
<input type="hidden" name="k9" value="#D51920">
<input type="hidden" name="kt" value="h">
<input type="text" name="q" maxlength="255"
 placeholder="Search&hellip;" class="span2" style="margin-top:4px;margin-left:4px;">
<input type="submit" value="DuckDuckGo Search" style="visibility: hidden;">
</form>
<!-- End of custom search -->
"""
