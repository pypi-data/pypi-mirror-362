Changelog
=========

2.6.0
-----
 - added key-numbers paragraph type and portlet
 - updated paragraphs add menus order
 - updated PyAMS_scheduler interfaces imports

2.5.1
-----
 - updated CI for Python 3.12

2.5.0
-----
 - added file shared content
 - added indicator to display paragraphs added or modified in the last content version
 - added Dropzone support in associations container table view
 - added site manager property to handle robots indexation
 - updated search results portlet renderers settings and templates
 - updated associations item events handler to propagate modifications to parent paragraph
 - updated illustration sublocations adapter
 - use new PyAMS_workflow method to apply first publication date on published content

2.4.0
-----
 - added logos shared tool
 - added support for optional inner year and month folders inside shared tools
 - added shared content reverse links view
 - added content specificities paragraph type
 - added on/off pictograms support to thesaurus terms
 - updated renderers label
 - updated method call in configuration tools and tables checker
 - updated shared tools themes support
 - small improvements after Sonarqube analysis...
 - added warning messages in management interface
 - added argument to paragraphs container method to be able to exclude paragraphs types
 - allow exclusion of paragraphs types in paragraphs portlets settings
 - use illustration renderer settings in verbatim paragraph default renderer

2.3.0
-----
 - added site summary portlet
 - added resource shared content
 - updated QRCode action position and marker view
 - updated form title for unversioned contents
 - updated search folders interfaces, settings, filters and results portlets renderers
 - updated thesaurus filters types and parameters names
 - updated panels and cards renderers
 - updated scheduler tasks (require PyAMS_scheduler >= 2.6.0)

2.2.0
-----
 - added verbatim paragraph and portlet
 - added paragraphs group paragraph type
 - added redirections manager
 - added QRCodes generator
 - removed all attributes of invalid internal links in HTML renderer
 - updated glossary alert rendering
 - updated thesaurus-based filters sorting
 - updated paragraph title refresh handler
 - updated cards renderers
 - updated search results portlet renderers templates

2.1.0
-----
 - added location map paragraph and portlet
 - added contact card paragraph and portlet

2.0.2
-----
 - updated PIP version in Gitlab CI

2.0.1
-----
 - updated CI for GDAL support
 - added support for Python 3.12

2.0.0
-----
 - first production release!
 - added support for views alphabetical ordering
 - added PyAMS_gis package dependency

1.99.12
-------
 - updated associations paragraph default rendered

1.99.11
-------
 - added H3 and H3 title levels to frames HTML editors
 - added and updated HTML title and metas headers

1.99.10
-------
 - added external scripts feature

1.99.9
------
 - added view name and query to base view items URL getter arguments list

1.99.8
------
 - added framed text paragraph and portlet
 - added simple navigation portlet renderer
 - added rich text paragraph "alert" renderer
 - added "news" shared content
 - added site settings to check host-based external links restrictions
 - added display options to search filters options labels
 - updated illustration side renderers

1.99.7
------
 - updated paragraph add form renderer
 - updated header logo getter
 - updated content publication support views
 - added property to search filters to hide results count
 - extended sitemap, SEO settings and "robots.txt" view
 - added OpenGraph metas support
 - updated internal and external links pictograms to match TinyMCE editor
 - updated canonical URL support in navigation menus and internal sites links

1.99.6
------
 - added filter add and edit forms title adapters
 - updated viewlet manager interface in tables views
 - updated deprecated Python imports
 - updated filters add menus labels

1.99.5.1
--------
 - corrected error in I18n translation domain

1.99.5
------
 - added aggregated filters support
 - many internal updates

1.99.4
------
 - removed arguments override in thesaurus handlers components

1.99.3
------
 - updated shared content header viewlet to add button to go back to dashboard
 - added status to scheduler tasks execution result
 - added support for direct content retiring or archiving for managers
 - added support for custom modal content class

1.99.2
------
 - added permission and role to manage references tables
 - disable cache when using aggregated search results portlet renderer
 - always open switcher in associations paragraph
 - added method to paragraphs container to get iterator over paragraphs matching a given set of factories
 - removed required flag on gallery files author
 - updated menus order
 - formatting and other minor updates

1.99.1
------
 - added edit forms content getters
 - added alerts types
 - added vocabulary to handle shared contents which can be used by views and search folders
 - minor updates

1.99.0
------
 - first preliminary release
