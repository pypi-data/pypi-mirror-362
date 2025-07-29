Changelog
=========

3.0.4 (2025-07-15)
------------------

- Fix controlpanel label.
  [cekk]


3.0.3 (2024-07-31)
------------------

- Add default value.
  [cekk]


3.0.2 (2024-06-18)
------------------

- Add default value in publicationAuthor field (#28553).
  [cekk]


3.0.1 (2024-03-25)
------------------

- Release on pypi.
  [cekk]


3.0.0 (2024-03-25)
------------------

- Python3 and Plone6 compatibility.
  [cekk]


2.2.3 (2019-11-14)
------------------

- Fix author index encoding for authors (#20207).
  [cekk]


2.2.2 (2019-10-15)
------------------

- Fix typo [nzambello]


2.2.1 (2019-10-15)
------------------

- Fix ARIA roles and a11y for pubblicazione view
  [nzambello]


2.2.0 (2019-10-14)
------------------

- Fix DOM semantic structure for pubblicazione view
  [nzambello]


2.1.3 (2019-09-18)
------------------

- Added title and css fields to the tile interface.
  [daniele]
- Added style collapsible for tile search pubblicazioni
  [giuliaghisini]


2.1.2 (2019-05-23)
------------------

- Fix unicode decode error
  [cekk]


2.1.1 (2019-02-07)
------------------

- The tile "Ricerca Pubblicazioni" now behaves differently: the authors list
  in the drop drown menu depends on the user (if it's logged in), on the path
  set in the tile and if the publication is published or not #16555.
  [arsenico13]
- Fix the url-encoding for the search-pubblications tile in the javascript
  bundle (#16555)
  [arsenico13]
- authors indexer now store values as strings and not unicode.
  [cekk]

2.1.0 (2018-12-28)
------------------

- Fix: The field publicationURL of a pubblication is now rendered as an 'a' tag
  in the template (#16555)
  [arsenico13]
- Fix: Now the vocabulary for the authors of a pubblication is correct and
  filters the names while typing in the edit view (2.a of #16555)
  [arsenico13]
- New: upgrade step that fixes authors field wrongly filled (with comma
  separated names all in one piece) #16555
  [arsenico13]


2.0.3 (2018-07-05)
------------------

- Added the path to search the publications in for the Search Tile. There is an
  upgrade step for this.
  [arsenico13]


2.0.2 (2018-02-07)
------------------

- Fix headings in templates [nzambello]


2.0.1 (2018-02-02)
------------------

- Templating and translations [nzambello]


2.0.0 (2018-01-29)
------------------
- Prepared for production.
  [arsenico13, lucabel, daniele]

1.0a1 (unreleased)
------------------

- Initial release.
  [arsenico13, lucabel]
