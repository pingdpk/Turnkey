import re
s = "abc##abcd##abcde##abcdef##abcdefg##abcdefgh##abcdefghi"

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_with_split(line, delimeter, cutAt, index ):
    try:
        return line.split(delimeter, cutAt)[index]
    except ValueError:
        return "find_between_with_split : Error finding ## in the line"


print(find_between_with_split(s, '##', -1, 5))
print(find_between( s, "123", "123" ))
print(find_between_r( s, "123", "123" ))