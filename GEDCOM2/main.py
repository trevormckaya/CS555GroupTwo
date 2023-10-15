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
        return dateObj < currDate
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

def compareDates(date1, date2):
    if date1 and date2:
        dateObj1 = datetime.strptime(date1, "%d %b %Y")
        dateObj2 = datetime.strptime(date2, "%d %b %Y")
        return dateObj1 < dateObj2
    return True

def birthBeforeMarriage(individuals, families):
    bd = individual.get('BIRTH', {}).get('BDATE', '')
    md = family.get('MARR', {}).get('MDATE', '')
    return compareDates(bd, md)

def divorceBeforeDeath(individuals, families):
    divd = family.get('DIV', {}).get('DIVDATE', '')
    dd = individual.get('DEATH', {}).get('DDATE', '')
    return compareDates(divd, dd)

class testDivBeforeDeath(unittest.TestCase):
    def setUp(self):
        self.individual1 = {
            'DEATH': {'DDATE': '01 JAN 2022'},
            'DIV': {'DIVDATE': '01 JAN 2020'}
        }
        self.individual2 = {
            'DEATH': {'DDATE': '01 JAN 2010'},
            'DIV': {'DIVDATE': '01 JAN 2000'}
        }
        self.individual3 = {
            'DEATH': {'DDATE': ''},
            'DIV': {'DIVDATE': ''}
        }
        self.individual4 = {
            'DEATH': {'DDATE': ''},
            'DIV': {'DIVDATE': '01 JAN 2020'}
        }
        self.individual5 = {
            'DEATH': {'DDATE': '01 JAN 1990'},
            'DIV': {'DIVDATE': ''}
        }
    def testDivBeforeDeath(self):
        self.assertTrue(divorceBeforeDeath(self.individual1, self.individual1))
        self.assertTrue(divorceBeforeDeath(self.individual2, self.individual2))

    def testDivBeforeDeathBothDatesMissing(self):
        # Test when both birth and death dates are missing
        self.assertTrue(divorceBeforeDeath(self.individual3, self.individual3))

    def testDivBeforeDeathDateMissing(self):
        # Test when either birth or death date is missing
        self.assertTrue(divorceBeforeDeath(self.individual4, self.individual4))
        self.assertTrue(divorceBeforeDeath(self.individual5, self.individual5))


def marriageBeforeDeath(individuals, families):
    md = family.get('MARR', {}).get('MDATE', '')
    dd = individual.get('DEATH', {}).get('DDATE', '')
    return compareDates(md, dd)

class testMarraigeBeforeDeath(unittest.TestCase):
    def setUp(self):
        self.individual1 = {
            'DEATH': {'DDATE': '01 JAN 2022'},
            'MARR': {'MDATE': '01 JAN 2020'}
        }
        self.individual2 = {
            'DEATH': {'DDATE': '01 JAN 2010'},
            'MARR': {'MDATE': '01 JAN 2000'}
        }
        self.individual3 = {
            'DEATH': {'DDATE': ''},
            'MARR': {'MDATE': ''}
        }
        self.individual4 = {
            'DEATH': {'DDATE': ''},
            'MARR': {'MDATE': '01 JAN 2020'}
        }
        self.individual5 = {
            'DEATH': {'DDATE': '01 JAN 1990'},
            'MARR': {'MDATE': ''}
        }
    def testMarriageBeforeDeath(self):
        self.assertTrue(marriageBeforeDeath(self.individual1, self.individual1))
        self.assertTrue(marriageBeforeDeath(self.individual2, self.individual2))

    def testMarriageBeforeDeathBothDatesMissing(self):
        # Test when both birth and death dates are missing
        self.assertTrue(marriageBeforeDeath(self.individual3, self.individual3))

    def testMarriageBeforeDeathDateMissing(self):
        # Test when either birth or death date is missing
        self.assertTrue(marriageBeforeDeath(self.individual4, self.individual4))
        self.assertTrue(marriageBeforeDeath(self.individual5, self.individual5))


class testBirthBeforeMarriage(unittest.TestCase):
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

    def testBirthBeforeMarriage(self):
        self.assertFalse(birthBeforeMarriage(self.individual1, self.individual1))
        self.assertFalse(birthBeforeMarriage(self.individual2, self.individual2))

    def testBirthAndMarriageDateMissing(self):
        # Test when both birth and death dates are missing
        self.assertFalse(birthBeforeMarriage(self.individual3, self.individual3))

    def testBirthOrMarriageDateMissing(self):
        # Test when either birth or death date is missing
        self.assertFalse(birthBeforeMarriage(self.individual4, self.individual4))
        self.assertFalse(birthBeforeMarriage(self.individual5, self.individual5))

    def testMarriageBeforeBirth(self):
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
    print("All birth dates are before death dates")
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
    print("All marriage dates are before divorce dates")
    return True

def US07_check_age(individuals):
    for individual in individuals:
        birth_date_str = individual.get('BIRTH', {}).get('BDATE', '')
        death_date_str = individual.get('DEATH', {}).get('DDATE', '')

        if birth_date_str:
            birth_date = datetime.strptime(birth_date_str, "%d %b %Y")
            if death_date_str:
                death_date = datetime.strptime(death_date_str, "%d %b %Y")
                age_at_death = death_date.year - birth_date.year - ((death_date.month, death_date.day) < (birth_date.month, birth_date.day))
                if age_at_death >= 150:
                    return False
            else:
                current_date = datetime.today()
                age_at_current = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
                if age_at_current >= 150:
                    return False
    return True


def US08_check_birth_before_marriage(families, individuals):
    for family in families:
        marriage_date_str = family.get('MARR', {}).get('MDATE', '')
        divorce_date_str = family.get('DIV', {}).get('DIVDATE', '')
        children_ids = family.get('CHIL', '')

        if marriage_date_str:
            marriage_date = datetime.strptime(marriage_date_str, "%d %b %Y")
            for child_id in children_ids:
                child = individuals[int(child_id) - 1]
                birth_date_str = child.get('BIRTH', {}).get('BDATE', '')
                if birth_date_str:
                    birth_date = datetime.strptime(birth_date_str, "%d %b %Y")
                    if birth_date < marriage_date:
                        return False
                    if divorce_date_str:
                        divorce_date = datetime.strptime(divorce_date_str, "%d %b %Y")
                        if (birth_date - marriage_date).days > 270:  # Check if birth is more than 9 months after divorce
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

print("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} ".format("ID", "Marriage Date", "Divorce Date", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children ID"))
for family in families:
    family1 = family.get('FAM', '')
    familyID = ''
    for char in family1:
        if char.isdigit():
            familyID += char
    marriageDate = family.get('MARR', {}).get('MDATE', '')
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
    print("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} ".format(family1, marriageDate, divorceDate, husbandID, husbandName, wifeID, wifeName, childrenID))
birthBeforeMarriage(individuals, families)
datesBeforeCurrent(individuals, families)
US04(families)
US03(individual)
divorceBeforeDeath(individuals, families)
marriageBeforeDeath(individuals,families)

'''
#US04 test
is_valid = US04(families)

if is_valid:
    print("US04: Marriage before divorce - All families have valid marriage and divorce dates.")
else:
    print("US04: Marriage before divorce - Some families have invalid marriage and divorce dates.")

#unittest functionality for US03
'''
class TestUS07CheckAge(unittest.TestCase):
    def setUp(self):
        # Initialize test data
        self.individual1 = {
            'BIRTH': {'BDATE': '01 JAN 1980'},
            'DEATH': {'DDATE': '01 JAN 2020'}
        }
        self.individual2 = {
            'BIRTH': {'BDATE': '01 JAN 1990'},
            'DEATH': {'DDATE': '01 JAN 2000'}
        }

    def test_age_valid(self):
        # Test cases with valid ages
        self.assertTrue(US07_check_age([self.individual1]))
        self.assertTrue(US07_check_age([self.individual2]))

    def test_age_missing_death(self):
        # Test cases with missing death date
        self.assertTrue(US07_check_age([self.individual1]))

    def test_age_missing_birth(self):
        # Test cases with missing birth date
        self.assertTrue(US07_check_age([self.individual2]))

    def test_age_invalid(self):
        # Test cases with invalid ages
        self.assertFalse(US07_check_age([self.individual1, self.individual2]))

class TestUS08CheckBirthBeforeMarriage(unittest.TestCase):
    def setUp(self):
        # Initialize test data
        self.family1 = {
            'MARR': {'MDATE': '01 JAN 2020'},
            'DIV': {'DIVDATE': '01 JAN 2021'},
            'CHIL': ['1', '2', '3']
        }
        self.family2 = {
            'MARR': {'MDATE': '01 JAN 2020'},
            'CHIL': ['4', '5']
        }

    def test_birth_before_marriage_valid(self):
        # Test cases with valid birth before marriage
        self.assertTrue(US08_check_birth_before_marriage([self.family1], individuals))

    def test_birth_before_marriage_invalid(self):
        # Test cases with birth after marriage
        self.assertFalse(US08_check_birth_before_marriage([self.family2], individuals))

if __name__ == '__main__':
    unittest.main()
