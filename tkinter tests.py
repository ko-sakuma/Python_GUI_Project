columns = ("hello", "there", "skywalker")
columns_to_update = ""
for x in columns:
    columns_to_update += ', ' + ('%s = ?' % x)
columns_to_update = columns_to_update[2:]

print(columns_to_update)