# -*- coding: utf-8 -*-

import os


class Payment:
    def __init__(self, name, S, ID, ref, message, date):
        self.name = name
        self.S = S
        self.ID = ID
        self.ref = ref
        self.message = message
        self.date = date

    def __str__(self):
        return self.ID + ", " + self.date + ", " + self.name + ",  " + str(self.S) + ", " + self.ref + ", " + self.message

    def CSVString(self):
        return self.ID + ", " + self.date + ", " + self.name + ",  " + str(self.S) + ", " + self.ref + ", " + self.message + '\n'


class NordeaParser:

    def __init__(self):
        self.PaymentData = []
        self.lines = []

    def readAllPRN(self):
        """Read all PRN files in current directory"""
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            if f.split('.')[1] == 'PRN':
                self.readPRN(f)
                print("Reading " + f)

    def readPRN(self, filename):
        """Read a PRN file to parser data array"""
        lines = []
        with open(filename, 'r', encoding='latin-1', errors='ignore') as f:
            try:
                for i in f:
                    i = str(i)
                    lines.append(i.rstrip('\n'))
            except UnicodeDecodeError:
                pass

            self.lines += lines
            self.parse()

    def detectYear(self):
        for i in range(len(self.lines)):
            line = self.lines[i]
            #detect payments by delimiter
            if "Kausi" in line:
                return (self.lines[i + 1].split()[4].split('.')[2])

    def parse(self):
        #parse year, will work in the 21st century
        year = "20" + self.detectYear()
        for i in range(len(self.lines)):
            line = self.lines[i]
            #parse payments by delimiter
            msg = ""
            ref = ""
            if "  __________ " in line:
                try:
                    arr = (self.lines[i].strip().split())
                    #replace decimal separator and spacer and convert to float
                    Sum = (arr[-1]).replace('.', '').replace(',', '.')
                    Sum = float(Sum[-1] + Sum[:-1])
                    ID = (arr[-3])
                    date = (arr[-4]) + year
                    name = (self.lines[i + 2].strip())[:-2].rstrip()
                    if "Viite" in self.lines[i + 4]:
                        ref = self.lines[i + 4].split()[1].lstrip('0').rstrip()
                    else:
                        ref = self.lines[i + 4].lstrip().lstrip('0').rstrip()
                        try:
                            #dumb verification, replace this asap
                            int(ref)
                            msg = ""
                        except:
                            if not "." or not "-" in ref:
                                msg = ref
                            ref = ""

                    # self, name, S, ID, ref, message, date
                    payment = Payment(name, Sum, ID, ref, msg, date)
                    self.PaymentData.append(payment)
                except:
                    pass

    def dumpArray(self):
        data = []
        for i in self.PaymentData:
            data.append([i.ID, i.S, i.date, i.name, i.ref, i.message])
        return data

    def dumpCSV(self, filename):
        f = open(filename, 'w+')
        for i in self.PaymentData:
            f.write(i.CSVString())
        f.close()
        print("Dumped parser data to " + filename)

    def output(self):
        for i in self.PaymentData:
            print(i)

    def __str__(self):
        print("Printing parser contents (Payment objects): ")
        self.output()
        return ""


parser = NordeaParser()
parser.readAllPRN()
a = parser.dumpArray()
parser.dumpCSV("output.CSV")
