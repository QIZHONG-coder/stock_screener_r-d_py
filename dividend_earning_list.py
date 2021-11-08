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
import datetime

def eORd_list(eORd, dt): #eORd=earnings or dividends dt= date in "m/d/yyyy" format
    nameOf=[]
    divORearn=[]
    url = "https://eresearch.fidelity.com/eresearch/conferenceCalls.jhtml?tab="+eORd+"&begindate="+dt
    dv_table=requests.get(url)
    sp = BeautifulSoup(dv_table.text, 'lxml')
    if eORd =="earnings":
        nameOf, divORearn=traceTR(5, sp.table(id="messageTableCurrentTimeOfDay")[0].tbody.find_all("tr"))      
    elif eORd =="dividends":
        nameOf, divORearn=traceTR(1, sp.table(id="messageTable3")[0].tbody.find_all("tr"))
    return nameOf, divORearn

def traceTR(n,trs):
    nmOf=[]
    dORe=[]
    for tr in trs:
        td=tr.find_all('td')
        if td[0].a:
            nmOf.append(td[0].a.string)
        dORe.append(td[n].text.replace("$", "").replace('\n', ' ').strip())
    return nmOf, dORe

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
    dORes=[]
    tbl_row=[] 
    names, dORes=eORd_list(sys.argv[-2], sys.argv[-1])
    if len(names)==0:
        print("Please use keyword 'dividends' or 'earnings'. ")
    else:
        dt=sys.argv[-1].split("/", 3)

        if datetime.date(int(dt[2]), int(dt[0]), int(dt[1])).weekday()>4:
            print("There is no reports on weekends")
        else:   
                if sys.argv[-2]=="dividends":
                    tbl_row.append(['Dividends','Notes', 'Names', 'Prices', 'Changes', 'Percentages', 'Open','Close', '52Highs', '52Lows', '52Perf', 'Volumes'])
                elif sys.argv[-2]=="earnings":
                    names, earns=eORd_list(sys.argv[-2], sys.argv[-1])
                    tbl_row.append(['Earns Surprises','Notes', 'Names', 'Prices', 'Changes', 'Percentages', 'Open','Close', '52Highs', '52Lows', '52Perf', 'Volumes'])
                for (name, dORe) in zip(names, dORes):       
                        tbl_row.append(quote_details(name, dORe))
                print("date:"+sys.argv[-1])
                print(tabulate(tbl_row, headers="firstrow", tablefmt="fancy_grid"))
                print("Note 1: + or -: current price increased or decreased;")
                print("Note 2: */: current price is within 5% of 52 week high;")
                print("Note 3: /*: current price is within 5% of 52 week low;")

if __name__ == "__main__":
    if len(sys.argv)<3:
        print("Please provide the key word 'earnings' or 'dividends' and a date in the format 'm/d/yyyy'!")
    else: 
        main()
