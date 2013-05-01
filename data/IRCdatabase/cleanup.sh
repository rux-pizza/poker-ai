#!/bin/bash
find . -type f -name "pdb*" | xargs cat > sumpdb.txt
cat sumpdb.txt | perl -p -i -e 's/^([^ ]*)[ ]+([^ ]*)[ ]+([^ ]*)[ ]+([^ ]*)[ ]+([^ ]*)[ ]+([^ ]*)[ ]+([^ ]*)[ ]+([^ ]*)[ ]+([^ ]*)[ ]+([^ ]*)[ ]+([^ ]*)[ ]+(.*)$/$1\t$2\t$3\t$4\t$5\t$6\t$7\t$8\t$9\t$10\t$11\t$12/' | sed 's/[\x00]//g' |awk ' (NF == 11 || NF ==13) && ($3 ~ "^[0-9]*$") {print $0;}' > sumpdb.cleanup.txt
find . -type f -name "hdb" | xargs cat > sumhdb.txt
cat sumhdb.txt | perl -p -e 's/^([^ ]*)[ ]+([^ ]*)[ ]+([^ ]*)[ ]+([^ ]*)[ ]+([^ ]*)[ ]+([^ ]*)[ ]+([^ ]*)[ ]+([^ ]*)[ ]+(.*)$/$1\t$2\t$3\t$4\t$5\t$6\t$7\t$8\t$9/' |sed 's/[\x00]//g' > sumhdb.cleanup.txt
