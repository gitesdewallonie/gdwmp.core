#!/usr/bin/make
#
# Makefile for gdwmp.core

translations: extract-translations update-translations compile-translations

.PHONY: extract-translations
extract-translations:
	../../../../i18n/bin/i18ndude rebuild-pot --pot locales/gdwmp.pot --create gdwmp . ../../../gdwmp.skin/gdwmp/skin/

.PHONY: update-translations
update-translations:
	msgmerge -U --backup=off locales/fr/LC_MESSAGES/gdwmp.po locales/gdwmp.pot
	msgmerge -U --backup=off locales/nl/LC_MESSAGES/gdwmp.po locales/gdwmp.pot

.PHONY: compile-translations
compile-translations:
	set -e; \
	for f in locales/*/LC_MESSAGES/gdwmp.po; do \
		msgfmt -o $${f%.po}.mo $$f;\
	done;\
