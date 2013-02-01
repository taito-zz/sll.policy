==========
sll.policy
==========

This package contains policies for SLL site.

Change log
----------

1.6 (2013-02-01)
================

- Added upgrade step to exclude some objects from navigation. [taito]
- Tested with Plone-4.2.4. [taito]

1.5.1 (2013-01-06)
==================

- Tested with Plone-4.2.3. [taito]

1.5 (2012-12-10)
================

- Unregister browserlayer. [taito]

1.4 (2012-12-10)
================

- Updated dependencies and refactored. [taito]

1.3 (2012-11-30)
================

- Added testing integration to Travis CI. [taito]

1.2.2 (2012-11-14)
==================

- Tested with Plone-4.2.2. [taito]

1.2.1 (2012-10-30)
==================

- Added dependency to plone.app.dexterity to avoid the next error [taito]::

    AttributeError: type object 'IDexterityFTI' has no attribute '__iro__'

1.2 (2012-10-29)
================

- Added upgrade step to enable visible_ids to all the registered members and also
  default to property value True for new members. [taito]

1.1.1 (2012-10-16)
==================

- Added logger to the upgrade step function: remove_portlet. [taito]

1.1 (2012-10-16)
================

- Added upgrade step to remove fblike portlet removing dependency to collective.portlet.fblikebox. [taito]
- Removed dependency to sll.shopping. [taito]

1.0.4 (2012-09-24)
==================

- Added Collection and Topic to types_not_searched. [taito]

1.0.3 (2012-09-21)
==================

- Moved content lead image related property to sll.templates package. [taito]
- Enabled upgrade step to migrate only to use TinyMCE. [taito]

1.0.2 (2012-09-20)
==================

- Removed kysely from registry. [taito]

1.0.1 (2012-09-19)
==================

- Disabled upgrade step to migrate only to use TinyMCE. [taito]

1.0 (2012-09-16)
================

- Initial release. [taito]
