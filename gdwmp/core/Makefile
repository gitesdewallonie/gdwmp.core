#!/usr/bin/make
#
# Makefile for gdwmp.core

translations: extract-translations update-translations compile-translations

.PHONY: extract-translations
extract-translations:
	../../../../i18n/bin/i18ndude rebuild-pot --pot locales/gdwmp.core.pot --create gdwmp.core .

.PHONY: update-translations
update-translations:
	msgmerge -U --backup=off locales/fr/LC_MESSAGES/gdwmp.core.po locales/gdwmp.core.pot
	msgmerge -U --backup=off locales/nl/LC_MESSAGES/gdwmp.core.po locales/gdwmp.core.pot

.PHONY: compile-translations
compile-translations:
	set -e; \
	for f in locales/*/LC_MESSAGES/gdwmp.core.po; do \
		msgfmt -o $${f%.po}.mo $$f;\
	done;\
