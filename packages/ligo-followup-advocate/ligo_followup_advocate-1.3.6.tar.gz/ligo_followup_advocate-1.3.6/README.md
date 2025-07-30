LIGO Follow-up Advocate Tools
=============================

This package provides tools for LIGO/Virgo/KAGRA follow-up advocates to assist
in tasks such as drafting astronomical bulletins for gravitational-wave
detections.

To install
----------

The easiest way to install `ligo-followup-advocate`, is with `pip`:

    pip install --user ligo-followup-advocate

To upgrade
----------

Once you have installed the package, to check for and install updates, run the
following command:

    pip install --user --upgrade ligo-followup-advocate

Current templates
-----------------

If you wish to just see examples of the current templates or submit these to be
reviewed in P&P, you can find them [here](https://git.ligo.org/emfollow/ligo-followup-advocate/builds/artifacts/master/file/templates.pdf?job=publish).

Example
-------

`ligo-followup-advocate` provides a single command to draft a GCN Circular
skeleton. Pass it the authors and the GraceDB ID as follows:

    ligo-followup-advocate compose \
        'A. Einstein (IAS)' 'S. Hawking (Cambridge)' \
        'I. Newton (Cambridge)' 'Data (Starfleet)' \
        'S190407w'

Optionally, you can have the program open the draft in your default mail client
by passing it the `--mailto` option.

For a list of other supported commands, run:

    ligo-followup-advocate --help

For further options for composing circulars, run:

    ligo-followup-advocate compose --help

You can also invoke most functions directly from a Python interpreter, like
this:

    >>> from ligo import followup_advocate
    >>> text = followup_advocate.compose('S190407w')

To develop
----------

To participate in development, clone the git repository:

    git clone git@git.ligo.org:emfollow/ligo-followup-advocate.git

To release
----------

The project is set up so that releases are automatically uploaded to PyPI
whenever a tag is created. Use the following steps to issue a release. In the
example below, we are assuming that the current version is 0.0.5, and that we
are releasing version 0.0.6.

1.  Check the latest [pipeline status](https://git.ligo.org/emfollow/ligo-followup-advocate/pipelines)
    to make sure that the `master` branch builds without any errors.

2.  Before making any changes, switch to the `master` branch and incorporate
    the changes going into this release:

        git fetch upstream
        git checkout master
        git rebase upstream/master

3.  Make sure that all significant changes since the last release are
    documented in `CHANGES.md`. If missing, make additional entries.

4.  Update the heading for the current release in `CHANGES.md` from
    `0.0.6 (unreleased)` to `0.0.6 (YYYY-MM-DD)` where `YYYY-MM-DD` is today's
    date. Also update the version in `pyproject.toml` similarly. Save both
    files once done.

5.  [Update the PDF templates](https://git.ligo.org/emfollow/ligo-followup-advocate/-/tree/master/ligo/followup_advocate/test/templates/templates.tex)
    with this new version.
    
6.  Check these files were changed and saved properly
    
        git status

7.  Commit those changes:

        git commit -a -m "Update changelog for version 0.0.6"

8.  Tag the release:

        git tag v0.0.6 -m "Version 0.0.6"

9.  Add a new section to `CHANGES.md` like this:

        ## 0.0.7 (unreleased)

        -   No changes yet.

    You can also consider updating the version in `pyproject.toml` and
    `template.tex` as was done above in preparation for the next release.

10. Commit the changes:

        git commit -a -m "Back to development"

11. Check that the changes worked correctly:

        git log
    
    You should see the top three commits look like the following:

        commit fc5b54cfb926f3e0265fd10e0501e3b403e7d88c (HEAD -> master)
        Author: Brandon Piotrzkowski <brandon.piotrzkowski@ligo.org>
        Date:   Mon Jun 23 11:18:49 2025 -0400

            Back to development

        commit 14c43f49022f51d5c72309dc7306171953011516 (tag: v0.0.6)
        Author: Brandon Piotrzkowski <brandon.piotrzkowski@ligo.org>
        Date:   Mon Jun 23 11:17:24 2025 -0400

            Update changelog for version 0.0.6
        
        commit d0e9075484992e75b4d1aa4dba02a962b990b84c (upstream/master)
        Author: Deep Chatterjee <deep.chatterjee@ligo.org>
        Date:   Wed Jun 18 20:02:00 2025 +0000

            add cgmi information, update skymap filename for aframe events; fix #158

    You should see `upstream/master` for the third commit, the the correct tag
    name in the second commit, and the top commit coming after both.

12. If these two new commits look good, push everything to GitLab:

        git push upstream && git push upstream --tags

    Within a few minutes, the new package will be built and uploaded to [PyPI](https://pypi.org/project/ligo-followup-advocate/).

13. If the changes of this release significantly impact the text of the example
   templates, upload the PDF of templates created from the `publish` CI job to
   DCC. Initiate P&P review and address comments in a new release. Note that it
   may take multiple releases to get P&P approval.

14. Once P&P approval has been given, [create an SCCB ticket](https://git.ligo.org/computing/sccb/-/issues/new).
   Note that there is an option to do this via the a button in the CI/CD
   pipeline, but this template could be outdated. The recommendation is to
   create the ticket by hand via the above link.

15. Once the SCCB ticket has been created, created a merge request to update
   this version in [`gwcelery`](https://git.ligo.org/emfollow/gwcelery) if this
   has not already been done. You can check the current version used via the
   [`poetry.lock`](https://git.ligo.org/emfollow/gwcelery/-/blob/main/poetry.lock)
   file. This will involve using [`poetry`](https://python-poetry.org/), so
   having this installed and being familiar with the commands will be needed.
