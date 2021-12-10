

link_string = 'govinfo.gov/bulkdata/BILLSTATUS/{congress}/{chamber}/BILLSTATUS-{congress}-{chamber}.zip'
for chamber in ['hr', 's']:
    for congress in range(108,118):
        print(link_string.format(congress = congress, chamber = chamber))
