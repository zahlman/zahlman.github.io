# Filters to apply to the output (to transform files in-place).
# dict of (file extension or tuple of file extensions) to commands.
# Each command must be either:
# * a Python callable, called with the filename as argument
# * a shell command string, with a single %s placeholder for the filename
# By default, only .php files uses filters to inject PHP into
# Nikola’s templates. All other filters must be enabled through FILTERS.
# Many filters are shipped with Nikola. A list is available in the manual:
# <https://getnikola.com/handbook.html#post-processing-filters>
# from nikola import filters
# FILTERS = {
#    ".html": [filters.typogrify],
#    ".js": [filters.closure_compiler],
#    ".jpg": ["jpegoptim --strip-all -m75 -v %s"],
# }
# Executable for the "yui_compressor" filter (defaults to 'yui-compressor').
# YUI_COMPRESSOR_EXECUTABLE = 'yui-compressor'
# Executable for the "closure_compiler" filter (defaults to 'closure-compiler').
# CLOSURE_COMPILER_EXECUTABLE = 'closure-compiler'
# Executable for the "optipng" filter (defaults to 'optipng').
# OPTIPNG_EXECUTABLE = 'optipng'
# Executable for the "jpegoptim" filter (defaults to 'jpegoptim').
# JPEGOPTIM_EXECUTABLE = 'jpegoptim'
# Executable for the "html_tidy_withconfig", "html_tidy_nowrap",
# "html_tidy_wrap", "html_tidy_wrap_attr" and "html_tidy_mini" filters
# (defaults to 'tidy5').
# HTML_TIDY_EXECUTABLE = 'tidy5'

# List of XPath expressions which should be used for finding headers
# ({hx} is replaced by headers h1 through h6).
# You must change this if you use a custom theme that does not use
# "e-content entry-content" as a class for post and page contents.
# HEADER_PERMALINKS_XPATH_LIST = ['*//div[@class="e-content entry-content"]//{hx}']
# Include *every* header (not recommended):
# HEADER_PERMALINKS_XPATH_LIST = ['*//{hx}']
# File blacklist for header permalinks. Contains output path
# (eg. 'output/index.html')
# HEADER_PERMALINKS_FILE_BLACKLIST = []

# Set up gzip compression. Requires that the server uses appropriate headers:
# it must not return "Accept-Ranges: bytes" for compressed files, and
# range requests must not return partial content of another representation.
# TODO investigate whether GitHub supports this. Probably not.
# GZIP_FILES = False
# File extensions that will be compressed
# GZIP_EXTENSIONS = ('.txt', '.htm', '.html', '.css', '.js', '.json', '.atom', '.xml')
# Use an external gzip command? None means no.
# Example: GZIP_COMMAND = "pigz -k {filename}"
# GZIP_COMMAND = None
