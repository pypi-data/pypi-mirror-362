# TODO: There is probably a better place or way to do this. Maybe static files that are built into the release? -W. Werner, 2025-07-15

page_template = """<!DOCTYPE html>
<html>
 <head>
  <title>{title}</title>
 </head>
 <body>
  <h1>{title}</h1>
  {body}
 </body>
</html>
"""


message_list = """
<fieldset class={lower_title}>
<legend>{title}</legend>
<table>
 <tr>{li_items}</tr>
</table>
</fieldset>
"""

issue_page = """
<a href="index.html">Home</a>
<fieldset class="issue">
<legend>{issue[Message-ID]} - {issue[Subject]}</legend>
Hi 
<pre>{issue}</pre>
</fieldset>
"""
