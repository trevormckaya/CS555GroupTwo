# I pledge my honor that I have abided by the Stevens Honor System - Corey Heckel, Trevor McKay
from typing import List
from datetime import datetime
import unittest

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

def isDateBeforeCurr(date):
    if date:
        dateObj = datetime.strptime(date, "%d %b %Y")
        currDate = datetime.today()
        return dateObj< currDate
    return True

def datesBeforeCurrent(individuals, families):
    for individual in individuals:
        bd = individual.get('BIRTH', {}).get('BDATE', '')
        dd = individual.get('DEATH', {}).get('DDATE', '')
        if not (isDateBeforeCurr(bd) and isDateBeforeCurr(dd)):
            print("Date after current")
            return False

    for family in families:
        md = family.get('MARR', {}).get('MDATE', '')
        divD = family.get('DIV', {}).get('DIVDATE', '')
        if not (isDateBeforeCurr(md) and isDateBeforeCurr(divD)):
            print("Date after current")
            return False
    print("All dates before current")
    return True

def birthBeforeMarriage(individuals, families):
    md = family.get('MARR', {}).get('MDATE', '')
    bd = individual.get('BIRTH', {}).get('BDATE', '')
    if md and bd:

        if md > bd:
            return True
    return False

class testBirthBeforeMarraige(unittest.TestCase):
    def setUp(self):
        self.individual1 = {
            'BIRTH': {'BDATE': '01 JAN 1980'},
            'MARR': {'MDATE': '01 JAN 2020'}
        }
        self.individual2 = {
            'BIRTH': {'BDATE': '01 JAN 1990'},
            'MARR': {'MDATE': '01 JAN 2000'}
        }
        self.individual3 = {
            'BIRTH': {'BDATE': ''},
            'MARR': {'MDATE': ''}
        }
        self.individual4 = {
            'BIRTH': {'BDATE': ''},
            'MARR': {'MDATE': '01 JAN 2020'}
        }
        self.individual5 = {
            'BIRTH': {'BDATE': '01 JAN 1990'},
            'MARR': {'MDATE': ''}
        }

    def testBirthBeforeMarraige(self):
        self.assertFalse(birthBeforeMarriage(self.individual1, self.individual1))
        self.assertFalse(birthBeforeMarriage(self.individual2, self.individual2))

    def testBirthAndMarraigeDateMissing(self):
        # Test when both birth and death dates are missing
        self.assertFalse(birthBeforeMarriage(self.individual3, self.individual3))

    def testBirthOrMarraigeDateMissing(self):
        # Test when either birth or death date is missing
        self.assertFalse(birthBeforeMarriage(self.individual4, self.individual4))
        self.assertFalse(birthBeforeMarriage(self.individual5, self.individual5))

    def testMarraigeBeforeBirth(self):
        # Test when death occurs before birth
        individual = {
            'BIRTH': {'BDATE': '01 JAN 2020'},
            'MARR': {'MDATE': '01 JAN 1990'}
        }
        self.assertFalse(birthBeforeMarriage(individual, individual))

    def testSameBirthAndDeathDate(self):
        # Test when an individual's birth and death dates are the same
        individual = {
            'BIRTH': {'BDATE': '01 JAN 2000'},
            'MARR': {'MDATE': '01 JAN 2000'}
        }
        self.assertFalse(birthBeforeMarriage(individual, individual))



datesBeforeCurrent(individuals,families)
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

def US03(individual):
    bd = individual.get('BIRTH', {}).get('BDATE', '')
    dd = individual.get('DEATH', {}).get('DDATE', '')

    if bd and dd:
        bd = datetime.strptime(bd, "%d %b %Y")
        dd = datetime.strptime(dd, "%d %b %Y")
        return bd < dd
    return True
class US03Test(unittest.TestCase):
    def setUp(self):
        self.individual1 = {
            'BIRTH': {'BDATE': '01 JAN 1980'},
            'DEATH': {'DDATE': '01 JAN 2020'}
        }
        self.individual2 = {
            'BIRTH': {'BDATE': '01 JAN 1990'},
            'DEATH': {'DDATE': '01 JAN 2000'}
        }
        self.individual3 = {
            'BIRTH': {'BDATE': '01 JAN 2000'},
            'DEATH': {'DDATE': ''}
        }
        self.individual4 = {
            'BIRTH': {'BDATE': ''},
            'DEATH': {'DDATE': '01 JAN 2020'}
        }
        self.individual5 = {
            'BIRTH': {'BDATE': '01 JAN 1990'},
            'DEATH': {'DDATE': ''}
        }

    def test_birth_before_death(self):
        self.assertTrue(US03(self.individual1))
        self.assertTrue(US03(self.individual2))

    def test_birth_and_death_dates_missing(self):
        # Test when both birth and death dates are missing
        self.assertTrue(US03(self.individual3))

    def test_birth_or_death_date_missing(self):
        # Test when either birth or death date is missing
        self.assertTrue(US03(self.individual4))
        self.assertTrue(US03(self.individual5))

    def test_death_before_birth(self):
        # Test when death occurs before birth
        individual = {
            'BIRTH': {'BDATE': '01 JAN 2020'},
            'DEATH': {'DDATE': '01 JAN 1990'}
        }
        self.assertFalse(US03(individual))

    def test_same_birth_and_death_date(self):
        # Test when an individual's birth and death dates are the same
        individual = {
            'BIRTH': {'BDATE': '01 JAN 2000'},
            'DEATH': {'DDATE': '01 JAN 2000'}
        }
        self.assertFalse(US03(individual))

def US04(families):
    for family in families:
        marriage_date = family.get('MARR', {}).get('MDATE', '')
        divorce_date = family.get('DIV', {}).get('DIVDATE', '')

        if marriage_date and divorce_date:
            marriage_date_obj = datetime.strptime(marriage_date, "%d %b %Y")
            divorce_date_obj = datetime.strptime(divorce_date, "%d %b %Y")

            if marriage_date_obj > divorce_date_obj:
                return False

    return True

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

'''
#US04 test
is_valid = US04(families)

if is_valid:
    print("US04: Marriage before divorce - All families have valid marriage and divorce dates.")
else:
    print("US04: Marriage before divorce - Some families have invalid marriage and divorce dates.")

#unittest functionality for US03
'''
if __name__ == '__main__':
    unittest.main()
