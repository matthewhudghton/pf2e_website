tmp_dir=./tmp
journal_db_path=../FoundryVTT/Data/worlds/pf2eworld/data/
export assets_src=~/dnd/FoundryVTT/Data/
assets_dest=./assets

all:
	-mv /home/mhudghton/Downloads/fvtt-JournalEntry-campaign-journal-*.json journal.json
	source venv/bin/activate ; python3 encrypt_file.py journal.json encrypted.json $(PASS)
	sed -e '/JOURNAL_JSON_PLACEHOLDER/ r encrypted.json' -e '/JOURNAL_JSON_PLACEHOLDER/ d' journal.html > index.out.html
	mkdir -p $(assets_dest)
	python3 ./copy_journal_imgs.py journal.json $(assets_src) ./assets
