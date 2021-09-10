cd site
. siteenv/bin/activate
python3 manage.py runscript test_cron -v2 > test_cron.out
