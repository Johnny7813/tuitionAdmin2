
the program
===========

This is tuitionAdmin2 a tuition administration program.
It is written in python3 and uses PyQt5 and mySQL.
The mySQL connection is made through Qt5.
I use it for my small tuition business. It is perfectly
tailored to my needs and reduces the time I spend on
administration a really great deal.

The original version "tuitionAdmin1" was based on Qt4.
This program has been slowly developed over 5 years.
Many changes have been made over time, whenever I encountered
something that I thought I could improve. Or I encountered
and error.

In mySQL I don't use enumerates anymore. I have switched to
uing foreign tables. The reason is, foreign tables are 
more portable. And I want to switch from mySQL to SQlite.

development goals
=================

* I want to switch from the mySQL backend to SQlite. Since SQlite 
does not support enumerates, I have changed enumerates to foreign
tables in mySQL.

* currently pdf files like invoices and receipts are created using
LaTeX. But I want to reduce the dependence of my program on other
programs. Therefore I want to try producing pdf files using the python
library reportlab.



