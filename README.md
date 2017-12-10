# Pretty-Printing-Parser

This is a sample program to convert a log file into a system readable JSON format file as given in the example.

et machineStatus(cassette) {
{
  -name {P430_BLK}
  -mfgDate {Sun Aug 7 17:27:16 2016}
  -mfgLot {101275}
  -initialMatl 56.3
  -1stUsageDate {Fri Dec 16 09:50:45 2016}

  -serialNumber {337213871.000000}
  -remainingMatl 12.7353
  -status Loaded
}

Pretty-printing parser output:

[{'action': 'set',
'data': {'1stUsageDate': 'Fri Dec 16 09:50:45 2016',
         'initialMatl': 56.3,
         'mfgDate': 'Sun Aug 7 17:27:16 2016',
         'name': 'P430_BLK',
         'remainingMatl': 12.7353,
         'serialNumber': '337213871.000000',
         'status': 'Loaded'},
 'subtype': 'cassette',
 'type': 'machineStatus’}]
