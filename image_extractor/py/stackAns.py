s = "|SUN|400\r\n|MON|6700\r\n|TUE|9999\r\n|MON|500SPHA\r\n|SUN|4388\r\n|THU|6788,00\r\n|FRI|/78KLY|ZOO TIMBER DOG\r\n|MON|/FORMATTED|PILLER"

last_sun_data = ''
res_lines = []
for line in s.splitlines():
    _, day, data = line.split('|', 2)
    if day == 'SUN':
        last_sun_data = data
    res_lines.append(last_sun_data + line)
transformed = '\r\n'.join(res_lines)


print(transformed)