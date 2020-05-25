
This is a new version of tuition_admin
it is based on the latest tuition_admin version that was deployed in Qt4
and connected to private_tuition_v2

It has been completely morphed to Qt5 with PyQt5
It uses a new database with foreign table support
and extra costs instead of travel cost, website cost etc.

*** 29/08/2019 idea
+ reimplemet QSqlRecord, data is filled with model.data ---> done
    --not necessary. I have reimplemented the functions that take
    or produce records like  deleteRows
+ reimplement the seek functions without record ---> done

+ update check_invoice()
+ implement check tuition, so that not 2 tuition_id's can be added and no two
    entries for one day

+ fix time recording so that it can easily switched on or off
+ fix invoice table, triggers  --> done
+ fix saving. When I save, it still asks me to save on quit. --> done
