# I pledge my honor that I have abided by the Stevens Honor System - Corey Heckel, Trevor McKay
from typing import List
from datetime import datetime

tags: List[str] = ['0 INDI', '1 NAME', '1 SEX', '1 BIRT', '1 DEAT', '1 FAMC', '1 FAMS', '1 FAM', '1 MARR', '1 HUSB', '1 WIFE', '1 CHIL', '1 DIV', '2 DATE', '0 HEAD', '0 TRLR', '0 NOTE']

individuals = []
families = []
currIndividual = {}
currFamily = {}

path = 'GEDCOMTestFile'

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
        level = int(level)
        if level == 0 and count > 2:
            if tag == 'INDI':
                if currIndividual:
                    individuals.append(currIndividual)
                currIndividual = {}
                currIndividual['INDI'] = tag
            elif tag == 'FAM':
                if currFamily:
                    families.append(currFamily)
                currFamily = {}
                currFamily['FAM'] = tag
        elif level == 1:
            if tag == 'NAME':
                currIndividual['NAME'] = ' '.join(parts[2:])
            elif tag == 'SEX':
                currIndividual['SEX'] = parts[2]
            elif tag == 'BIRT':
                currIndividual['BIRTH'] = {}
            elif tag == 'FAMS':
                currIndividual['FAMS'] = parts[2]
            elif tag == 'FAMC':
                currIndividual['FAMC'] = parts[2]
            elif tag == 'DEAT':
                currIndividual['DEATH'] = {}
            if tag == 'MARR':
                currFamily['MARR'] = {}
            elif tag == 'DIV':
                currFamily['DIV'] = {}
            elif tag == 'HUSB':
                currFamily['HUSB'] = parts[2]
            elif tag == 'WIFE':
                currFamily['WIFE'] = parts[2]
            elif tag == 'CHIL':
                currFamily['CHIL'] = parts[2]
        elif level == 2:
            if 'DEATH' in currIndividual:
                if tag == 'DATE':
                    currIndividual['DEATH']['DDATE'] = ' '.join(parts[2:])
            elif 'BIRTH' in currIndividual:
                if tag == 'DATE':
                    currIndividual['BIRTH']['BDATE'] = ' '.join(parts[2:])
            if 'MARR' in currFamily:
                if tag == 'DATE':
                    currFamily['MARR']['MDATE'] = ' '.join(parts[2:])
            elif 'DIV' in currFamily:
                if tag == 'DATE':
                    currFamily['DIV']['DIVDATE'] = ' '.join(parts[2:])


def calcAge(birth, death):
    reference = datetime.today()
    birth = datetime.strptime(birth, "%d %b %Y")
    if death:
        death = datetime.strptime(death, "%d %b %Y")
        ageOfDeath = death.year - birth.year - ((death.month, death.day) < (birth.month, birth.day))
        return ageOfDeath
    else:
        currAge = reference.year - birth.year - ((reference.month, reference.day) < (birth.month, birth.day))
        return currAge


if currFamily not in families:
    families.append(currFamily)

if currIndividual not in individuals:
    individuals.append(currIndividual)
print("Individuals:")
print("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format("ID", "Name", "Sex", "Birth Date", "Age", "Alive Status", "Death Date", "Child", "Spouse"))

for individual in individuals:
    individualID = individual.get('INDI', '')
    individualString = ''.join(individualID)
    individualIDs = ''
    for char in individualString:
        if char.isdigit():
            individualIDs += char

    name = individual.get('NAME', '')
    sex = individual.get('SEX', '')

    spouse = individual.get('FAMS', '')
    spouseString = ''.join(spouse)
    spouseID = ''
    for char in spouseString:
        if char.isdigit():
            spouseID += char

    child = individual.get('FAMC', '')
    childString = ''.join(child)
    childID = ''
    for char in childString:
        if char.isdigit():
            childID += char

    birthDate = individual.get('BIRTH', {}).get('BDATE', '')
    deathDate = individual.get('DEATH', {}).get('DDATE', '')
    age = calcAge(birthDate, deathDate)
    status = "Alive" if not deathDate else "Deceased"

    print("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format(individualIDs, name, sex, birthDate, age, status, deathDate, childID, spouseID))

print("Families:")

print("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} ".format("ID", "Marraige Date", "Divorce Date", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children ID"))
for family in families:
    family1 = family.get('FAM', '')
    familyID = ''
    for char in family1:
        if char.isdigit():
            familyID += char
    marraigeDate = family.get('MARR', {}).get('MDATE', '')
    divorceDate = family.get('DIV', {}).get('DIVDATE', '')

    husband = family.get('HUSB', '')
    husbandID = ''
    for char in husband:
        if char.isdigit():
            husbandID += char
    husbandName = individuals[int(husbandID) - 1].get('NAME', '') if husbandID else ''

    wife = family.get('WIFE', '')
    wifeID = ''
    for char in wife:
        if char.isdigit():
            wifeID += char
    wifeName = individuals[int(wifeID) - 1].get('NAME', '') if wifeID else ''

    children = family.get('CHIL', '')
    childrenID = ''
    for char in children:
        if char.isdigit():
            childrenID += char
    print("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} ".format(family1, marraigeDate, divorceDate, husbandID, husbandName, wifeID, wifeName, childrenID))