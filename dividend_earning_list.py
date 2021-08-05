#!/usr/bin/python
#list details of stocks reporting earnings/dividends
#data are extracted from Fidelity.com
#three parameters to run: filename earnings/dividends date(m/d/yyyy)
#example: "dividend_earning_list.py earnings (or dividends) 5/29/2020"
#works with Python3.6.6

import sys
import requests
from tabulate import tabulate
from bs4 import BeautifulSoup

def eORd_list(eORd, dt): #eORd=earnings or dividends dt= date in "m/d/yyyy" format
    nameOf=[]
    divORearn=[]
    url = "https://eresearch.fidelity.com/eresearch/conferenceCalls.jhtml?tab="+eORd+"&begindate="+dt
    dv_table=requests.get(url)
    sp = BeautifulSoup(dv_table.text, 'lxml')
    if eORd =="earnings":
        for tr in sp.table(id="messageTableCurrentTimeOfDay")[0].tbody.find_all("tr"):
            td=tr.find_all('td')
            if td[0].a:
                nameOf.append(td[0].a.string)               
            #else:
            #    nameOf.append(td[0].renderContents().strip())
            divORearn.append(td[5].text.replace("$", "").replace('\n', ' ').strip())        
    else:
        for tr in sp.table(id="messageTable3")[0].tbody.find_all("tr"):
            td=tr.find_all('td')
            if td[0].a:
                nameOf.append(td[0].a.string)    
            #else:
            #    nameOf.append(td[0].renderContents().strip()[1:])
            divORearn.append(td[1].text.replace("$", "").replace('\n', ' ').strip())                
    return nameOf, divORearn
def quote_details(name, divORearn): 
    urlOf="https://eresearch.fidelity.com/eresearch/evaluate/snapshot.jhtml?symbols="+str(name)
    detailsURL=requests.get(urlOf)
    details=BeautifulSoup(detailsURL.text, 'lxml')
    if len(details.find_all("span"))>3:
#        return('-','-',name,'-','-','-','-','-','-','-','-','-')
#    else:
        priceOf=details.find_all("span", id="lastPrice")[0].text
        netOf=details.find_all("span", id="netChgToday")[0].text
        pctOf=details.find_all("span", id="pctChgToday")[0].text
        slt=details.select("table.datatable-component.auto-width")[0].find_all("tr")
        opn=slt[4].td.text
        lst=slt[7].td.text
        high=slt[8].td.contents[0]
        low=slt[9].td.contents[0]
        perf=slt[10].td.contents[0]
        vol=slt[12].td.contents[0]
        #indicators of price changes within 5% of peaks
        f_netOf=float(netOf)
        f_priceOf=float(priceOf)
        f_high=float(high)
        f_low=float(low)
        if f_netOf==0:
            notes="0 |"
        if f_netOf < 0:
            notes="- |"
        if f_netOf > 0:
            notes="+ |"
        if float((f_priceOf-f_low)/f_low) < 0.05: #within 5% of 52 week low
            notes=notes+"/*"
        if float((f_high-f_priceOf)/f_high) <0.05: #within 5% of 52 week high
            notes=notes+"*/" 
        return(divORearn, notes, name, priceOf, netOf, pctOf, opn, lst, high, low, perf, vol)
        
def main():
    names=[]
    divs=[]
    earns=[]
    tbl_row=[]    
    if sys.argv[1]=="dividends":
        names, divs=eORd_list(sys.argv[1], sys.argv[2])
        tbl_row.append(['Dividends','Notes', 'Names', 'Prices', 'Changes', 'Percentages', 'Open','Close', '52Highs', '52Lows', '52Perf', 'Volumes'])
        for (name, div) in zip(names, divs):    
            tbl_row.append(quote_details(name, div))
    elif sys.argv[1]=="earnings":
        names, earns=eORd_list(sys.argv[1], sys.argv[2])
        tbl_row.append(['Earns Surprise','Notes', 'Names', 'Prices', 'Changes', 'Percentages', 'Open','Close', '52Highs', '52Lows', '52Perf', 'Volumes'])
        for (name, earn) in zip(names, earns):       
            tbl_row.append(quote_details(name, earn))
    print("date:"+sys.argv[2])
    print(tabulate(tbl_row, headers="firstrow", tablefmt="fancy_grid"))
    print("Note 1: + or -: current price increased or decreased;")
    print("Note 2: */: current price is within 5% of 52 week high;")
    print("Note 3: /*: current price is within 5% of 52 week low;")
if __name__ == "__main__":
    if len(sys.argv)<3:
        print("Please provide the key word 'earnings' or 'dividends' and a date in the format 'm/d/yyyy'!")
    else:    
        main()