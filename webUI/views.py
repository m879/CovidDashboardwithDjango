from django.shortcuts import render
import pandas as pd

df3=pd.read_json('https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')
# Create your views here.
def indexPage(request):
    confirmedGlobal=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    totalCount=confirmedGlobal[confirmedGlobal.columns[-1]].sum()
    barPlotData=confirmedGlobal[['Country/Region',confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
    barPlotData=barPlotData.reset_index()
    barPlotData.columns=['Country/Region','values']
    barPlotData=barPlotData.sort_values(by='values',ascending=False)
    barPlotVals=barPlotData['values'].values.tolist()
    countryNames=barPlotData['Country/Region'].values.tolist()
    dataForMap=getDataforMap(barPlotData,countryNames) 
    showMap="True"
    context={'totalCount':totalCount,'barPlotVals': barPlotVals,'countryNames':countryNames,'dataForMap': dataForMap,'showMap':showMap} 
    return render(request,'index.html',context)


def getDataforMap(barPlotData,countryNames):
    dataForMap=[]
    for i in countryNames:
        try:
            tempdf=df3[df3['name']==i]
            temp={}
            temp["code3"]=list(tempdf['code3'].values)[0]
            temp["name"]=i
            temp["value"]=barPlotData[barPlotData['Country/Region']==i]['values'].sum()
            temp["code"]=list(tempdf['code'].values)[0]
            dataForMap.append(temp)
        except:
            pass
    # print (len(dataForMap))
    return dataForMap    
# 
# def indiCountryData(request):
    # confirmedGlobal=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    # totalCount=confirmedGlobal[confirmedGlobal.columns[-1]].sum()
    # barPlotData=confirmedGlobal[['Country/Region',confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
    # barPlotData=barPlotData.reset_index()
    # barPlotData.columns=['Country/Region','values']
    # barPlotData=barPlotData.sort_values(by='values',ascending=False)
    # barPlotVals=barPlotData['values'].values.tolist()
    # countryNames=barPlotData['Country/Region'].values.tolist()
    # showMap="False"
# 
    # countryNameSe=request.POST.get('countryName')
    # countryDataSpe=pd.DataFrame(confirmedGlobal[confirmedGlobal['Country/Region']==countryNameSe][confirmedGlobal.columns[4:-1]].sum()).reset_index()
    # countryDataSpe.columns=['country','values']
    # countryDataSpe['lagVal']=countryDataSpe['values'].shift(1).fillna(0)
    # countryDataSpe['incrementVal']=countryDataSpe['values']-countryDataSpe['lagVal']
    # countryDataSpe['rollingMean']=countryDataSpe['incrementVal'].rolling(window=4).mean()
    # countryDataSpe=countryDataSpe.fillna(0)
    # datasetsForLine=[{'yAxisID': 'y-axis-1','label':'Daily Cumulated Data','data':countryDataSpe['values'].values.tolist(),'borderColor':'#03a9fc','backgroundColor':'#03a9fc','fill':'false'},
                    # {'yAxisID': 'y-axis-1','label':'Rolling Mean 4 days','data':countryDataSpe['rollingMean'].values.tolist(),'borderColor':'#fc5203','backgroundColor':'#fc5203','fill':'false'}]
    # axisvalues=countryDataSpe.index.tolist()
    # context={'axisvalues':axisvalues,'countryName':countryNameSe,'totalCount':totalCount,'barPlotVals': barPlotVals,'countryNames':countryNames,'showMap':showMap,' datasetsForLine': datasetsForLine} 
    # return render(request,'index.html',context)
