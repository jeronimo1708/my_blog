import markdown # Import the markdown library
from django import template # Django's template library
from django.utils.safestring import mark_safe # To mark output as safe HTML

register = template.Library() # Register custom template tags and filters

@register.filter(name='markdown') # Decorator to register this function as a filter
def markdown_format(text):
    # Render Markdown with extensions for fenced code blocks and code highlighting
    html = markdown.markdown(text, extensions=['fenced_code', 'codehilite'])
    return mark_safe(html) # Mark the generated HTML as safe so Django doesn't escape it