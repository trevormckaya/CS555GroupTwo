#I pledge my honor that I have abided by the Stevens Honor System -Corey Heckel
from typing import List

tags: List[str] = ['0 INDI', '1 NAME', '1 SEX', '1 BIRT', '1 DEAT', '1 FAMC',
                  '1 FAMS', '1 FAM', '1 MARR', '1 HUSB', '1 WIFE', '1 CHIL',
                  '1 DIV', '2 DATE', '0 HEAD', '0 TRLR', '0 NOTE']
path = 'GEDCOM.ged'

with open(path, "r") as file:
    for line in file:
        print('-->', line.rstrip("\n"))
        parts: List[str] = line.rstrip("\n").split(' ', 2)
        count: int = len(parts)

        level: str = parts[0]
        tag: str = parts[1]
        valid: str = 'Y' if f"{level} {tag}" in tags else 'N'

        if count == 2:
            print(f"<-- {'|'.join([level, tag, valid])}")
        elif parts[2] in ['INDI', 'FAM']:
            _id: str = parts[1]
            tag: str = parts[2]
            valid: str = 'Y' if f"{level} {tag}" in tags else 'N'
            print(f"<-- {'|'.join([level, tag, valid, _id])}")
        else:
            args: str = parts[2]
            print(f"<-- {'|'.join([level, tag, valid, args])}")



