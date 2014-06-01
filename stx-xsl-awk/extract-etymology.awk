/^---MEDIAWIKI-WORD---/ {
	WORD=$2
}
/^===Etymology.*===$/,/^===[^E]/ {
	if (($1 ~ /^===/) || ($0 ~ /^\ *$/))
		next;
	printf("%s # %s\n", WORD, $0);
}
