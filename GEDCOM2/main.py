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
def is_marriage_after_14(individuals, families):
    for family in families:
        marriage_date_str = family.get('MARR', {}).get('MDATE', '')
        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')

        if marriage_date_str and husband_id and wife_id:
            marriage_date = datetime.strptime(marriage_date_str, "%d %b %Y")

            # Check husband's age at marriage
            husband = individuals[int(husband_id) - 1]
            birth_date_husband_str = husband.get('BIRTH', {}).get('BDATE', '')
            if birth_date_husband_str:
                birth_date_husband = datetime.strptime(birth_date_husband_str, "%d %b %Y")
                age_at_marriage_husband = marriage_date.year - birth_date_husband.year - ((marriage_date.month, marriage_date.day) < (birth_date_husband.month, birth_date_husband.day))
                if age_at_marriage_husband < 14:
                    return False

            # Check wife's age at marriage
            wife = individuals[int(wife_id) - 1]
            birth_date_wife_str = wife.get('BIRTH', {}).get('BDATE', '')
            if birth_date_wife_str:
                birth_date_wife = datetime.strptime(birth_date_wife_str, "%d %b %Y")
                age_at_marriage_wife = marriage_date.year - birth_date_wife.year - ((marriage_date.month, marriage_date.day) < (birth_date_wife.month, birth_date_wife.day))
                if age_at_marriage_wife < 14:
                    return False

    return True

def list_deceased_individuals(individuals):
    deceased_individuals = []
    for individual in individuals:
        death_date = individual.get('DEATH', {}).get('DDATE', '')
        if death_date:
            deceased_individuals.append(individual)
    return deceased_individuals

def list_living_married_individuals(individuals, families):
    living_married_list = []
    for family in families:
        husband_id = family.get('HUSB', None)
        wife_id = family.get('WIFE', None)
        marriage_date = family.get('MARR', None)

        if husband_id and wife_id and marriage_date:
            husband_index = int(husband_id[2:-1]) - 1
            wife_index = int(wife_id[2:-1]) - 1

            husband = individuals[husband_index] if 0 <= husband_index < len(individuals) else None
            wife = individuals[wife_index] if 0 <= wife_index < len(individuals) else None

            if husband and wife and 'DEAT' not in husband and 'DEAT' not in wife:
                living_married_list.append(husband)
                living_married_list.append(wife)

    return living_married_list

# Print the list of deceased individuals
deceased_list = list_deceased_individuals(individuals)
print("\nDeceased Individuals:")
for individual in deceased_list:
    print(individual)

# Print the list of living married individuals
living_married_list = list_living_married_individuals(individuals, families)
print("\nLiving Married Individuals:")
for individual in living_married_list:
    print(individual)


def test_list_deceased_individuals():
    individuals = [
        {'ID': '1', 'NAME': 'John Doe', 'DEATH': {'DDATE': '2022-01-01'}},
        {'ID': '2', 'NAME': 'Jane Doe'},
        # Add more individuals as needed
    ]

    deceased_list = list_deceased_individuals(individuals)
    assert len(deceased_list) == 1
    assert deceased_list[0]['NAME'] == 'John Doe'
    # Run the test cases
    test_list_deceased_individuals()

# Test case for listing living married individuals
def test_list_living_married_individuals():
    individuals = [
        {'ID': '@I1@', 'DEAT': '2000-01-01'},
        {'ID': '@I2@'},
        {'ID': '@I3@'},
    ]
    families = [
        {'HUSB': '@I2@', 'WIFE': '@I3@', 'MARR': '1990-01-01'},
    ]

    living_married_list = list_living_married_individuals(individuals, families)
    assert len(living_married_list) == 2

test_list_living_married_individuals()



class TestIsMarriageAfter14(unittest.TestCase):
    def setUp(self):
        # Test data for individuals and families
        self.individuals = [
            {
                'BIRTH': {'BDATE': '01 JAN 1990'},
                'DEATH': {},
            },
            {
                'BIRTH': {'BDATE': '01 JAN 1976'},
                'DEATH': {},
            },
            {
                'BIRTH': {'BDATE': '01 JAN 1960'},
                'DEATH': {},
            },
        ]
        self.families = [
            {
                'MARR': {'MDATE': '01 JAN 2010'},
                'HUSB': '1',
                'WIFE': '2',
            },
            {
                'MARR': {'MDATE': '01 JAN 2022'},
                'HUSB': '1',
                'WIFE': '3',
            },
            {
                'MARR': {'MDATE': '01 JAN 2025'},
                'HUSB': '3',
                'WIFE': '2',
            }]

    def test_marriage_after_14(self):
        # Test marriages where both husband and wife are older than 14
        self.assertTrue(is_marriage_after_14(self.individuals, self.families))

    def test_marriage_with_underage_husband(self):
        # Test marriage with an underage husband
        self.individuals[0]['BIRTH']['BDATE'] = '01 JAN 2008'
        self.assertFalse(is_marriage_after_14(self.individuals, self.families))

    def test_marriage_with_underage_wife(self):
        # Test marriage with an underage wife
        self.individuals[1]['BIRTH']['BDATE'] = '01 JAN 2012'
        self.assertFalse(is_marriage_after_14(self.individuals, self.families))

    def test_marriage_with_both_underage(self):
        # Test marriage with both husband and wife underage
        self.individuals[0]['BIRTH']['BDATE'] = '01 JAN 2008'
        self.individuals[1]['BIRTH']['BDATE'] = '01 JAN 2012'
        self.assertFalse(is_marriage_after_14(self.individuals, self.families))


def isBirthBeforeDeath(individuals):
    for individual in individuals:
        bd = individual.get('BIRTH', {}).get('BDATE', '')
        dd = individual.get('DEATH', {}).get('DDATE', '')
        dateBirthObj = datetime.strptime(bd, "%d %b %Y")
        dateDeathObj = datetime.strptime(dd, "%d %b %Y")
        return dateBirthObj < dateDeathObj
class testDivBeforeDeath(unittest.TestCase):
    def setUp(self):
        self.individual1 = {
            'DEATH': {'DDATE': '01 JAN 2022'},
            'BIRTH': {'BDATE': '01 JAN 2020'}
        }
        self.individual2 = {
            'DEATH': {'DDATE': '01 JAN 2010'},
            'BIRTH': {'BDATE': '01 JAN 2000'}
        }
        self.individual3 = {
            'DEATH': {'DDATE': ''},
            'BIRTH': {'BDATE': ''}
        }
        self.individual4 = {
            'DEATH': {'DDATE': ''},
            'BIRTH': {'BDATE': '01 JAN 2020'}
        }
        self.individual5 = {
            'DEATH': {'DDATE': '01 JAN 1990'},
            'BIRTH': {'BDATE': ''}
        }
    def testBirthBeforeDeath(self):
        self.assertTrue(isBirthBeforeDeath(self.individual1, self.individual1))
        self.assertTrue(isBirthBeforeDeath(self.individual2, self.individual2))

    def testBirthBeforeDeathBothDatesMissing(self):
        # Test when both birth and death dates are missing
        self.assertTrue(isBirthBeforeDeath(self.individual3, self.individual3))

    def testBirthBeforeDeathDateMissing(self):
        # Test when either birth or death date is missing
        self.assertTrue(isBirthBeforeDeath(self.individual4, self.individual4))
        self.assertTrue(isBirthBeforeDeath(self.individual5, self.individual5))





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
    def calculate_age(birth_date, death_date=None):
        today = datetime.today()
        birth_date = datetime.strptime(birth_date, "%d %b %Y")
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if death_date:
            death_date = datetime.strptime(death_date, "%d %b %Y")
            age_at_death = death_date.year - birth_date.year - ((death_date.month, death_date.day) < (birth_date.month, birth_date.day))
            return age_at_death
        return age

    for individual in individuals:
        birth_date = individual.get('BIRTH', {}).get('BDATE', '')
        death_date = individual.get('DEATH', {}).get('DDATE', '')

        if birth_date:
            if death_date and calculate_age(birth_date, death_date) >= 150:
                return False
            elif not death_date and calculate_age(birth_date) >= 150:
                return False
    return True


def US08_check_birth_before_marriage(families, individuals):
    for family in families:
        marriage_date_str = family.get('MARR', {}).get('MDATE', '')
        divorce_date_str = family.get('DIV', {}).get('DIVDATE', '')
        children_ids = family.get('CHIL', [])
        
        if marriage_date_str:
            marriage_date = datetime.strptime(marriage_date_str, "%d %b %Y")
            
            for child_id in children_ids:
                child = individuals[int(child_id) - 1]
                birth_date_str = child.get('BIRTH', {}).get('BDATE', '')
                
                if birth_date_str:
                    birth_date = datetime.strptime(birth_date_str, "%d %b %Y")
                    
                    if birth_date < marriage_date:
                        if divorce_date_str:
                            divorce_date = datetime.strptime(divorce_date_str, "%d %b %Y")
                            if (birth_date - marriage_date).days > 270:
                                return False
                        else:
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

def US11(families):
    marriages = {}
    for family in families:
        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')
        marriage_date = family.get('MARR', {}).get('MDATE', '')

        if husband_id and wife_id and marriage_date:
            if husband_id in marriages:
                if marriages[husband_id] == marriage_date:
                    return False
            if wife_id in marriages:
                if marriages[wife_id] == marriage_date:
                    return False
            marriages[husband_id] = marriage_date
            marriages[wife_id] = marriage_date

    return True


class TestUS11(unittest.TestCase):
    def test_no_bigamy(self):
        # Test with no bigamy, all marriages are in order
        families = [
            {
                'HUSB': '1',
                'WIFE': '2',
                'MARR': {'MDATE': '01 JAN 2000'},
            },
            {
                'HUSB': '3',
                'WIFE': '4',
                'MARR': {'MDATE': '01 JAN 2010'},
            },
        ]
        self.assertTrue(US11(families))

    def test_bigamy_husband(self):
        # Test with bigamy, husband has two marriages on the same date
        families = [
            {
                'HUSB': '1',
                'WIFE': '2',
                'MARR': {'MDATE': '01 JAN 2000'},
            },
            {
                'HUSB': '1',
                'WIFE': '3',
                'MARR': {'MDATE': '01 JAN 2000'},
            },
        ]
        self.assertFalse(US11(families))

    def test_bigamy_wife(self):
        # Test with bigamy, wife has two marriages on the same date
        families = [
            {
                'HUSB': '1',
                'WIFE': '2',
                'MARR': {'MDATE': '01 JAN 2000'},
            },
            {
                'HUSB': '3',
                'WIFE': '2',
                'MARR': {'MDATE': '01 JAN 2000'},
            },
        ]
        self.assertFalse(US11(families))

def US12(individuals, families):
    for family in families:
        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')
        children_ids = family.get('CHIL', [])

        for child_id in children_ids:
            child_birth_date_str = individuals[int(child_id) - 1].get('BIRTH', {}).get('BDATE', '')
            if child_birth_date_str:
                child_birth_date = datetime.strptime(child_birth_date_str, "%d %b %Y")
                if husband_id:
                    father_birth_date_str = individuals[int(husband_id) - 1].get('BIRTH', {}).get('BDATE', '')
                    if father_birth_date_str:
                        father_birth_date = datetime.strptime(father_birth_date_str, "%d %b %Y")
                        if (father_birth_date.year - child_birth_date.year) >= 80:
                            return False
                if wife_id:
                    mother_birth_date_str = individuals[int(wife_id) - 1].get('BIRTH', {}).get('BDATE', '')
                    if mother_birth_date_str:
                        mother_birth_date = datetime.strptime(mother_birth_date_str, "%d %b %Y")
                        if (mother_birth_date.year - child_birth_date.year) >= 60:
                            return False

    return True

class TestUS12(unittest.TestCase):
    def test_parents_not_too_old(self):
        # Test with parents not too old, mother is less than 60 years older and father is less than 80 years older than their children
        individuals = [
            {
                'BIRTH': {'BDATE': '01 JAN 1980'},
            },
            {
                'BIRTH': {'BDATE': '01 JAN 1985'},
            },
            {
                'BIRTH': {'BDATE': '01 JAN 1970'},
            },
        ]
        families = [
            {
                'HUSB': '1',
                'WIFE': '2',
                'CHIL': ['3'],
            },
        ]
        self.assertTrue(US12(individuals, families))


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

    def test_age_missing_death(self):
        # Test cases with missing death date
        self.assertTrue(US07_check_age([self.individual1]))

    def test_age_missing_birth(self):
        # Test cases with missing birth date
        self.assertTrue(US07_check_age([self.individual2]))


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

    def test_birth_before_marriage_invalid(self):
        # Test cases with birth after marriage
        self.assertFalse(US08_check_birth_before_marriage([self.family2], individuals))

def is_correct_gender_roles(individuals, families):
    for family in families:
        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')

        if husband_id:
            husband = individuals[int(husband_id) - 1]
            if 'SEX' in husband and husband['SEX'] != 'M':
                return False

        if wife_id:
            wife = individuals[int(wife_id) - 1]
            if 'SEX' in wife and wife['SEX'] != 'F':
                return False

    return True

class TestCorrectGenderRoles(unittest.TestCase):
    def setUp(self):
        self.individuals = [
            {'ID': '1', 'SEX': 'M'},
            {'ID': '2', 'SEX': 'F'},
            {'ID': '3', 'SEX': 'M'},
        ]
        self.families = [
            {'HUSB': '1', 'WIFE': '2'},
            {'HUSB': '3', 'WIFE': '2'},
        ]

    def test_correct_gender_roles(self):
        self.assertTrue(is_correct_gender_roles(self.individuals, self.families))

    def test_incorrect_gender_roles(self):
        # Intentionally set incorrect gender roles
        self.individuals[0]['SEX'] = 'F'
        self.assertFalse(is_correct_gender_roles(self.individuals, self.families))

        # Reset gender for the next test case
        self.individuals[0]['SEX'] = 'M'

        # Intentionally set incorrect gender roles
        self.individuals[1]['SEX'] = 'M'
        self.assertFalse(is_correct_gender_roles(self.individuals, self.families))

def are_all_ids_unique(individuals, families):
    all_ids = set()
    

    for individual in individuals:
        individual_id = individual.get('ID', '')
        if individual_id in all_ids:
            return False
        all_ids.add(individual_id)

    # Check family IDs
    for family in families:
        family_id = family.get('FAM', '')
        if family_id in all_ids:
            return False
        all_ids.add(family_id)

    return True

class TestUniqueIDs(unittest.TestCase):
    def setUp(self):
        self.individuals = [
            {'ID': 'I1'},
            {'ID': 'I2'},
            {'ID': 'I3'},
        ]
        self.families = [
            {'FAM': 'F1'},
            {'FAM': 'F2'},
            {'FAM': 'F3'},
        ]

    def test_unique_ids(self):
        self.assertTrue(are_all_ids_unique(self.individuals, self.families))

    def test_non_unique_individual_ids(self):
        # Intentionally set non-unique individual IDs
        self.individuals[1]['ID'] = 'I1'
        self.assertFalse(are_all_ids_unique(self.individuals, self.families))

        # Reset IDs for the next test case
        self.individuals[1]['ID'] = 'I2'

    def test_non_unique_family_ids(self):
        # Intentionally set non-unique family IDs
        self.families[2]['FAM'] = 'F1'
        self.assertFalse(are_all_ids_unique(self.individuals, self.families))

        # Reset IDs for the next test case
        self.families[2]['FAM'] = 'F3'

if __name__ == '__main__':
    unittest.main()
