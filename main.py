from pathlib import Path
import csv
from pprint import pprint
import re

file = Path("phonebook_raw.csv")
if file.exists():
    with file.open('r',encoding='utf-8',newline='') as f:
        reader = csv.reader(f)
        users = list(reader)[1:]
result_user = []
for i in users:
    fio = ' '.join(i[:3]).split()
    del i[:3]
    if len(fio) == 3:
        i.insert(0,fio[0])
        i.insert(1, fio[1])
        i.insert(2, fio[2])
    else:
        i.insert(0, fio[0])
        i.insert(1, fio[1])
all_word_pattern = r"(\+7|8)?\s*\(?(\d{3})\)?[\s*-]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})\s*\(?(\w*\.?)(\s?\w*)\)?"
replacement_pattern = r"+7(\2)\3-\4-\5 \6\7"
replacement_pattern2 = r"+7(\2)\3-\4-\5\6"
for i in users:
    users_clear = ''
    cleaned_phones = []

    for j in i:
        j = re.sub(r"доб\.\s+", "доб.", j)
        if 'доб' in j:
            cleaned_phones.append(re.sub(all_word_pattern, replacement_pattern, j.strip()))
        else:
            cleaned_phones.append(re.sub(all_word_pattern, replacement_pattern2, j.strip()))
    result_user.append(cleaned_phones)
pprint(result_user)
group = {}
for i in result_user:
    while len(i) < 7:
        i.append('')
    email_idx = -1
    for idx, value in enumerate(i):
        if '@' in str(value):
            email_idx = idx
            break
    if email_idx != -1 and email_idx != 6:
        email_value = i[email_idx]
        i[email_idx] = ''
        if len(i) > 6:
            if not i[6]:
                i[6] = email_value
        else:
            i.append(email_value)
    username = f'{i[0].strip()} {i[1].strip()}'
    if username not in group:
        group[username] = i.copy()
    else:
        for j in range(2, 7):
            if j < len(i) and j < len(group[username]):
                existing_value = group[username][j]
                new_value = i[j]
                if (not existing_value or str(existing_value).strip() == '') and new_value:
                    group[username][j] = new_value
result = list(group.values())
pprint(result)

output_file = Path('phonebook.csv')
with output_file.open('w',encoding='utf-8', newline='') as f:
    writer = csv.writer(f,delimiter=',')
    writer.writerows(result)

