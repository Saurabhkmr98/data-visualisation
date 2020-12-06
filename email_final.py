def buildViz(from_dt, to_dt, ministryName, reportCode):
    date1 = psr.parse(str(from_dt))
    date2 = psr.parse(str(to_dt))
    #connecting to mongodb
    client = MongoClient('localhost', 27017)
    mydatabase = client['Sentiments']
    collection = mydatabase.SentimentData  
    query = {"PublishDate" : {"$gte" : date1, "$lte" : date2}}
    allData = pd.DataFrame(list(collection.find(query)))
    
    # Image path
    imgpath = ".\PyImages\{}"
    colour = {
        'Negative' : 'red', 'Neutral' : 'orange', 'Positive' : 'green', 'No-Comment' : 'blue'
        }
    # filtering data as per ministry
    allData = allData[allData.Ministry == ministryName]
    #pd.set_option('display.max_columns', None)
    allData = allData.dropna(how = 'all', axis = 1)
    
    # list of vis built successfully
    onlineViz = list()
    socialViz = list()
    printViz = list()
    tvViz = list()
    
    if not allData.empty:
        # ministry is empty or not
        flag_data = True
        
        # trend graph common for all reports
        try:
            trend_graph = True
            allData['date'] = allData.apply(lambda row: row['PublishDate'].date(), axis = 1)
            trend = allData.groupby(['date','Sentiment']).count().reset_index()
            trend = trend.pivot(columns = 'date', index = 'Sentiment', values = '_id')
            trend
            sent = trend.index.values
            senti = []
            for y in sent:
                if y in ['Negative','Neutral','Positive']:
                    senti.append(y)
            trend = trend.dropna(how = 'all', axis = 1)
            trend = trend.replace(np.nan,0,regex = True)
            Sentiment  = senti
            linestyle = {
                'Negative' : ':', 'Neutral' : '--', 'Positive' : '-', 'No-Comment' : '-.'
            }
            plt.figure(figsize=(20,8))
            for i in range(len(senti)):
                plt.plot(range(len(trend.columns)), trend.loc[Sentiment[i]], color = colour.get(Sentiment[i]), linestyle = linestyle.get(Sentiment[i]), marker = 'o')
            plt.tick_params(labelsize=14)
            plt.xticks(range(len(trend.columns)), labels = trend.columns, rotation = 60)
            plt.legend(Sentiment, prop = {'size':25})
            plt.xlabel('Date', fontsize = 20)
            plt.ylabel('No. of Articles', fontsize = 20)
            plt.title('No. of Articles per Day', fontsize =20)
            fig_size = plt.gcf().get_size_inches() #Get current size
            sizefactor = 2.5 #Set a zoom factor
            # Modify the current size by the factor
            #plt.gcf().set_size_inches(sizefactor * fig_size)
            plt.grid(axis = 'y')
            plt.box(None)
            plt.savefig(imgpath.format('Trend_Media'), bbox_inches='tight')
            plt.close()
        except:
            trend_graph = False
        
        if reportCode == 'onlineSocial':
            # dataS only social data
            dataS = allData[allData.Type == 'Social']
            dataO = allData[allData.Type == 'Online']
            allData = allData[(data.Sentiment != '')]
            
            if not dataS.empty:
                # Social_Media_1
                try:
                    # getting latest data for vis
                    # 1st vis of Social media
                    s = dataS.groupby(['Language']).count().reset_index()
                    b = s.sort_values(by = ['_id'], ascending = False)[:10].Language
                    a = dataS[dataS.Language.isin(b)]
                    a = a.groupby(['Language', 'Sentiment']).count().reset_index()
                    a = a.pivot(columns = 'Language', index = 'Sentiment', values = '_id')
                    sent = a.index.values
                    senti = []
                    for y in sent:
                        if y in ['Negative','Neutral','Positive']:
                            senti.append(y)
                    a = a.dropna(how = 'all', axis = 1)
                    a = a.replace(np.nan,0,regex=True) 
                    Sentiment  = senti
                    val = 0
                    for i in range(len(Sentiment)):
                        plt.bar(range(len(a.columns)), a.loc[Sentiment[i]], bottom = val, color = colour.get(Sentiment[i]))
                        val += a.loc[Sentiment[i]]
                    plt.tick_params(labelsize=14)
                    plt.xticks(range(len(a.columns)), labels = a.columns, rotation = 90)
                    top_value = 0
                    for i in range(len(Sentiment)):
                        top_value += np.array(a.loc[Sentiment[i]], dtype = int)
                    for index, value in enumerate(top_value):
                        plt.text(index , value + 0.5, str(value))
                    plt.legend(Sentiment, prop={'size':25} )
                    plt.xlabel('Language', fontsize = 20)
                    plt.ylabel('No. of sentiments reported', fontsize = 20)
                    plt.title('No. of Sentiments vs Language', fontsize = 20)
                    fig_size = plt.gcf().get_size_inches() #Get current size
                    #Set a zoom factor
                    # Modify the current size by the factor
                    plt.gcf().set_size_inches((24,12))
                    plt.grid(axis = 'y')
                    plt.savefig(imgpath.format('Social_Media_1'), bbox_inches='tight')
                    plt.close()
                    
                    # including image in successfully built viz
                    socialViz.append('Social_Media_1')
                except:
                    pass
                
                # Social Media 2
                try:
                    s = dataS.groupby(['Influencer']).count().reset_index()
                    b = s.sort_values(by = ['_id'], ascending = False)[:10].Influencer
                    a = dataS[dataS.Influencer.isin(b)]
                    a = a.groupby(['Influencer', 'Sentiment']).count().reset_index()
                    a = a.pivot(columns = 'Influencer', index = 'Sentiment', values = '_id')
                    sent = a.index.values
                    senti = []
                    for y in sent:
                        if y in ['Negative','Neutral','Positive']:
                            senti.append(y)
                    a = a.dropna(how = 'all', axis = 1)
                    a = a.replace(np.nan,0,regex=True) 
                    Sentiment  = senti
                    val = 0
                    for i in range(len(Sentiment)):
                        plt.bar(range(len(a.columns)), a.loc[Sentiment[i]], bottom = val, color = colour.get(Sentiment[i]))
                        val += a.loc[Sentiment[i]]
                    plt.tick_params(labelsize=14)
                    plt.xticks(range(len(a.columns)), labels = a.columns, rotation = 90)
                    top_value = 0
                    for i in range(len(Sentiment)):
                        top_value += np.array(a.loc[Sentiment[i]], dtype = int)
                    for index, value in enumerate(top_value):
                        plt.text(index , value + 0.5, str(value))
                    plt.legend(Sentiment, prop={'size':25} )
                    plt.xlabel('Influencer', fontsize = 20)
                    plt.ylabel('No. of sentiments reported', fontsize = 20)
                    plt.title('No. of Sentiments vs Influencer', fontsize = 20)
                    fig_size = plt.gcf().get_size_inches() #Get current size
                    #Set a zoom factor
                    # Modify the current size by the factor
                    plt.gcf().set_size_inches((24,12))
                    plt.grid(axis = 'y')
                    plt.savefig(imgpath.format('Social_Media_2'), bbox_inches='tight')
                    plt.close()
                    
                    # including image in successfully built viz
                    socialViz.append('Social_Media_2')
                except:
                    pass
                
                # Social Media 3
                try:
                    #3rd viz of Social Media
                    dataS.Reach = dataS.Reach.astype('int')
                    a = dataS.groupby('Sentiment').Reach.mean().reset_index()
                    senti = ['Negative','Positive','Neutral']
                    a = a[a.Sentiment.isin(senti)]
                    a = a.dropna(axis = 0, subset = ['Reach'])
                    plt.pie(a.Reach, labels = round(a.Reach), autopct = '%1.1f%%', colors = ['red','orange','green'], shadow = True, startangle = 90)
                    plt.axis('equal')
                    plt.gcf().set_size_inches((18,6))
                    plt.legend(a.Sentiment, prop = {'size':20}, loc = 'best')
                    plt.title('Share of Sentiments in Total Reach', fontsize = 20)
                    plt.savefig(imgpath.format('Social_Media_3'), bbox_inches='tight')
                    plt.close()
                    
                    # including image in successfully built viz
                    socialViz.append('Social_Media_3')
                except:
                    pass
                
            
            if not dataO.empty:
                
                # Online Media 1
                try:
                    s = dataO.groupby(['Language']).count().reset_index()
                    b = s.sort_values(by = ['_id'], ascending = False)[:5].Language
                    a = dataO[dataO.Language.isin(b)]
                    a = a.groupby(['Language', 'Sentiment']).count().reset_index()
                    a = a.pivot(columns = 'Language', index = 'Sentiment', values = '_id')
                    sent = a.index.values
                    senti = []
                    for y in sent:
                        if y in ['Negative','Neutral','Positive']:
                            senti.append(y)
                    a = a.dropna(how = 'all', axis = 1)
                    a = a.replace(np.nan,0,regex=True) 
                    Sentiment  = senti
                    val = 0
                    for i in range(len(Sentiment)):
                        plt.bar(range(len(a.columns)), a.loc[Sentiment[i]], bottom = val, color = colour.get(Sentiment[i]))
                        val += a.loc[Sentiment[i]]
                    plt.tick_params(labelsize=14)
                    plt.xticks(range(len(a.columns)), labels = a.columns, rotation = 90)
                    top_value = 0
                    for i in range(len(Sentiment)):
                        top_value += np.array(a.loc[Sentiment[i]], dtype = int)
                    for index, value in enumerate(top_value):
                        plt.text(index , value + 0.5, str(value))
                    plt.legend(Sentiment, prop={'size':25} )
                    plt.xlabel('Language', fontsize = 20)
                    plt.ylabel('No. of sentiments reported', fontsize = 20)
                    plt.title('No. of Sentiments vs Language', fontsize = 20)
                    fig_size = plt.gcf().get_size_inches() #Get current size
                    #Set a zoom factor
                    # Modify the current size by the factor
                    plt.gcf().set_size_inches((24,12))
                    plt.grid(axis = 'y')
                    plt.savefig(imgpath.format('Online_Media_1'), bbox_inches='tight')
                    plt.close()
                    
                    # including image in successfully built viz
                    onlineViz.append('Online_Media_1')
                except:
                    pass
                
                try:
                    # 2nd vis of Online media
                    s = dataO.groupby(['Influencer']).count().reset_index()
                    b = s.sort_values(by = ['_id'], ascending = False)[:10].Influencer
                    a = dataO.loc[(dataO.Influencer.isin(b)) & (dataO.Influencer != '')]
                    a = a.groupby(['Influencer', 'Sentiment']).count().reset_index()
                    a = a.pivot(columns = 'Influencer', index = 'Sentiment', values = '_id')
                    sent = a.index.values
                    senti = []
                    for y in sent:
                        if y in ['Negative','Neutral','Positive']:
                            senti.append(y)
                    a = a.dropna(how = 'all', axis = 1)
                    a = a.replace(np.nan,0,regex=True) 
                    Sentiment  = senti
                    val = 0
                    for i in range(len(Sentiment)):
                        plt.bar(range(len(a.columns)), a.loc[Sentiment[i]], bottom = val, color = colour.get(Sentiment[i]))
                        val += a.loc[Sentiment[i]]
                    plt.tick_params(labelsize=14)
                    plt.xticks(range(len(a.columns)), labels = a.columns, rotation = 90)
                    top_value = 0
                    for i in range(len(Sentiment)):
                        top_value += np.array(a.loc[Sentiment[i]], dtype = int)
                    for index, value in enumerate(top_value):
                        plt.text(index , value + 0.5, str(value))
                    plt.legend(Sentiment, prop={'size':25} )
                    plt.xlabel('Influencer', fontsize = 20)
                    plt.ylabel('No. of sentiments reported', fontsize = 20)
                    plt.title('No. of Sentiments vs Influencer', fontsize = 20)
                    fig_size = plt.gcf().get_size_inches() #Get current size
                    #Set a zoom factor
                    # Modify the current size by the factor
                    plt.gcf().set_size_inches((24,12))
                    plt.grid(axis = 'y')
                    plt.savefig(imgpath.format('Online_Media_2'), bbox_inches='tight')
                    plt.close()
                    
                    # including image in successfully built viz
                    onlineViz.append('Online_Media_2')
                except:
                    pass
                
                try:
                    dataO['AiringHour'] = dataO['AiringTime'].str.split(':').str[0]
                    At = dataO.groupby(['AiringHour', 'Sentiment']).count().reset_index()
                    At = At.pivot(columns = 'AiringHour', index = 'Sentiment', values = 'ClipId')
                    senti = []
                    for y in sent:
                        if y in ['Negative','Neutral','Positive']:
                            senti.append(y)
                    At = At.dropna(how = 'all', axis = 1)
                    At = At.replace(np.nan,0,regex = True)
                    Sentiment  = senti
                    linestyle = {
                        'Negative' : ':', 'Neutral' : '--', 'Positive' : '-', 'No-Comment' : '-.'
                    }
                    for i in range(len(senti)):
                        plt.plot(range(len(At.columns)), At.loc[Sentiment[i]], color = colour.get(Sentiment[i]), linestyle = linestyle.get(Sentiment[i]), marker = 'o')
                    
                    plt.tick_params(labelsize=14)
                    plt.xticks(range(len(At.columns)), labels = At.columns, rotation = 60)
                    plt.legend(Sentiment, prop = {'size':25})
                    plt.xlabel('Airing Hours', fontsize = 20)
                    plt.ylabel('No. of Sentiments Reported', fontsize = 20)
                    plt.title('No. of Sentiments vs Airing Hours', fontsize =20)
                    fig_size = plt.gcf().get_size_inches() #Get current size
                    sizefactor = 2.5 #Set a zoom factor
                    # Modify the current size by the factor
                    plt.gcf().set_size_inches(sizefactor * fig_size)
                    plt.grid(axis = 'both')
                    plt.savefig(imgpath.format('Online_Media_3'), bbox_inches='tight')
                    plt.close()
                    
                    # including image in successfully built viz
                    onlineViz.append('Online_Media_3')
                except:
                    pass
                
                # Top headlines content capture
                if not dataO.empty:
                    online_count = allData[allData.Type == 'Online']['Content'].count()
                    
                    # Top positive headlines
                    try:
                        onlinedfp = allData.loc[(allData.Type == 'Online') & (allData.Sentiment == 'Positive')]
                        onlinedfp['Reach'] = onlinedfp['Reach'].astype('int')
                        onlinedfp = onlinedfp.drop_duplicates(subset = ['Reach'])
                        online_pos_data = onlinedfp.sort_values(by = ['Reach'], ascending = False)[:5]
                        online_pos_data = online_pos_data[['PublishDate','Source','Content','URL','InputName','Reach']]
                        online_pos_data['Reach'] = online_pos_data['Reach']//1000000
                        online_pos_data['InputName'] = online_pos_data.apply(lambda row: row['InputName'].split('|')[0], axis = 1)
                        # captured online_pos_data
                    except:
                        pass
                    
                    # Top Negative Headlines
                    try:
                        onlinedfN = allData.loc[(allData.Type == 'Online') & (allData.Sentiment == 'Negative')]
                        onlinedfN['Reach'] = onlinedfN['Reach'].astype('int')
                        onlinedfN = onlinedfN.drop_duplicates(subset = ['Reach'])
                        online_neg_data = onlinedfN.sort_values(by = ['Reach'], ascending = False)[:5]
                        online_neg_data = online_neg_data[['PublishDate','Source','Content','URL','InputName','Reach']]
                        online_neg_data['Reach'] = online_neg_data['Reach']//1000000
                        online_neg_data['InputName'] = online_neg_data.apply(lambda row: row['InputName'].split('|')[0], axis = 1)
                        # captured online_neg_data
                    except:
                        pass
                    
                if not dataS.empty:
                    social_count = allData[allData.Type == 'Social']['Content'].count()
                        
                    # Top positive headlines
                    try:
                        socialdfp = data.loc[(data.Type == 'Social') & (data.Sentiment == 'Positive')]
                        socialdfp['Reach'] = socialdfp['Reach'].apply(pd.to_numeric)
                        socialdfp = socialdfp.drop_duplicates(subset = ['Reach'])
                        social_pos_data = socialdfp.sort_values(by = ['Reach'], ascending = False)[:5]
                        social_pos_data = social_pos_data[['PublishDate','Influencer','Content','URL','InputName','Reach']]
                        social_pos_data['Reach'] = social_pos_data['Reach']//1000000
                        social_pos_data['InputName'] = social_pos_data.apply(lambda row: row['InputName'].split('|')[0], axis = 1)
                        # Captured social_pos_data
                    except:
                        pass
                    
                    # Top Negative Headlines
                    try:
                        socialdfN = data.loc[(data.Type == 'Social') & (data.Sentiment == 'Negative')]
                        socialdfN['Reach'] = socialdfN['Reach'].astype('int')
                        socialdfN = socialdfN.drop_duplicates(subset = ['Reach'])
                        social_neg_data = socialdfN.sort_values(by = ['Reach'], ascending = False)[:5]
                        social_neg_data = social_neg_data[['PublishDate','Influencer','Content','URL','InputName','Reach']]
                        social_neg_data['Reach'] = social_neg_data['Reach']//1000000
                        social_neg_data['InputName'] = social_neg_data.apply(lambda row: row['InputName'].split('|')[0], axis = 1)
                        # Captured social_neg_data
                    except:
                        pass

        if reportCode == 'tvPrint':
            # dataS only social data
            dataT = allData[allData.Type == 'TV']
            dataP = allData[allData.Type == 'PRINT']
            allData = allData[(data.Sentiment != '')]
            
            if not dataP.empty:
                
                # Print Media 1
                # 1st vis of Print media
                try:
                    s = dataP.groupby(['Source']).count().reset_index()
                    b = s.sort_values(by = ['_id'], ascending = False)[:10].Source
                    a = dataP[dataP.Source.isin(b)]
                    a = a.groupby(['Source', 'Sentiment']).count().reset_index()
                    a = a.pivot(columns = 'Source', index = 'Sentiment', values = 'ClipId')
                    sent = a.index.values
                    senti = []
                    for y in sent:
                        if y in ['Negative','Neutral','Positive']:
                            senti.append(y)
                    a = a.dropna(how = 'all', axis = 1)
                    a = a.replace(np.nan,0,regex=True) 
                    Sentiment  = senti
                    val = 0
                    for i in range(len(Sentiment)):
                        plt.bar(range(len(a.columns)), a.loc[Sentiment[i]], bottom = val, color = colour.get(Sentiment[i]))
                        val += a.loc[Sentiment[i]]
                    plt.tick_params(labelsize=14)
                    plt.xticks(range(len(a.columns)), labels = a.columns, rotation = 90)
                    top_value = 0
                    for i in range(len(Sentiment)):
                        top_value += np.array(a.loc[Sentiment[i]], dtype = int)
                    for index, value in enumerate(top_value):
                        plt.text(index , value + 0.5, str(value))
                    plt.legend(Sentiment, prop={'size':25} )
                    plt.xlabel('Newspaper', fontsize = 20)
                    plt.ylabel('No. of sentiments reported', fontsize = 20)
                    plt.title('No. of Sentiments vs Newspaper', fontsize = 20)
                    fig_size = plt.gcf().get_size_inches() #Get current size
                    #Set a zoom factor
                    # Modify the current size by the factor
                    plt.gcf().set_size_inches((24,12))
                    plt.grid(axis = 'y')
                    plt.savefig(imgpath.format('Print_Media_1'), bbox_inches='tight')
                    plt.close()
                    
                    # including image in successfully built viz
                    printViz.append('Print_Media_1')
                except:
                    pass
                
                try:
                    # Print Media 2
                    s = dataP.groupby(['Subregion']).count().reset_index()
                    b = s.sort_values(by = ['_id'], ascending = False)[:10].Subregion
                    a = dataP[dataP.Subregion.isin(b)]
                    df2 = a.groupby(['Subregion','Sentiment']).count().reset_index()
                    df2 = df2.pivot(columns = 'Subregion', index = 'Sentiment',values='ClipId')
                    sent = df2.index.values
                    senti = []
                    for y in sent:
                        if y in ['Negative','Neutral','Positive']:
                            senti.append(y)
                    df2 = df2.dropna(how = 'all', axis = 1)
                    df2 = df2.replace(np.nan,0,regex=True)
                    Sentiment  = senti
                    val = 0
                    for i in range(len(Sentiment)):
                        plt.bar(range(len(df2.columns)), df2.loc[Sentiment[i]], bottom = val, color = colour.get(Sentiment[i]))
                        val += df2.loc[Sentiment[i]]
                    plt.tick_params(labelsize = 14)
                    plt.xticks(range(len(df2.columns)), labels = df2.columns, rotation = 45)
                    top_value = 0
                    for i in range(len(Sentiment)):
                        top_value += np.array(df2.loc[Sentiment[i]], dtype = int)
                    for index, value in enumerate(top_value):
                        plt.text(index, value + 0.5, str(value))
                    plt.legend(Sentiment, prop={'size':20} )
                    plt.xlabel('Subregion', fontsize = 20)
                    plt.ylabel('No. of sentiments reported', fontsize = 20)
                    plt.title('No. of Sentiments vs Subregion', fontsize = 20, pad = '20')
                    fig_size = plt.gcf().get_size_inches() #Get current size
                    sizefactor = 2.5 #Set a zoom factor
                    # Modify the current size by the factor
                    plt.gcf().set_size_inches(sizefactor * fig_size)
                    plt.grid(axis = 'y')
                    plt.savefig(imgpath.format('Print_Media_2'), bbox_inches='tight')
                    plt.close()
                    
                    # including image in successfully built viz
                    printViz.append('Print_Media_2')
                except:
                    pass
                
                try:
                    # 3rd vis of Print Media
                    s = dataP.groupby(['PublicationType']).count().reset_index()
                    b = s.sort_values(by = ['_id'], ascending = False)[:10].PublicationType
                    a = dataP[dataP.PublicationType.isin(b)]
                    df4 = a.groupby(['PublicationType', 'Sentiment']).count().reset_index()
                    df4 = df4.pivot(columns = 'PublicationType', index = 'Sentiment', values = 'ClipId')
                    sent = df4.index.values
                    senti = []
                    for y in sent:
                        if y in ['Negative','Neutral','Positive']:
                            senti.append(y)
                    df4 = df4.dropna(how = 'all')
                    df4 = df4.replace(np.nan,0,regex = True)
                    Sentiment  = senti
                    def get_ticks(n,t,w,d):
                        return [t*element + w*n for element in range(d)]
                    ticks = []
                    for i in range(len(Sentiment)):
                        ticks.append(get_ticks(i+1,len(Sentiment),0.8,len(df4.columns)))
                    for i in range(len(ticks)):
                        plt.bar(ticks[i],df4.loc[Sentiment[i]],color = colour.get(Sentiment[i]))
                    for i in range(len(ticks)):
                        for index, value in enumerate(df4.loc[Sentiment[i]]):
                            plt.text(ticks[i][index], value + 1, str(int(value)))
                    plt.tick_params(labelsize = 14)
                    plt.xticks([i + len(Sentiment)//2 for i in ticks[0]], labels = df4.columns)
                    plt.xlabel('Publication Type', fontsize =20)
                    plt.ylabel('Sentiment responses', fontsize =20)
                    plt.title('No. of Sentiments vs Publication Type', fontsize = 20)
                    plt.legend(Sentiment, prop={'size':20})
                    plt.grid(axis = 'y', alpha = 0.5)
                    fig_size = plt.gcf().get_size_inches() #Get current size
                    sizefactor = 2.5 #Set a zoom factor
                    # Modify the current size by the factor
                    plt.gcf().set_size_inches(sizefactor * fig_size)
                    plt.savefig(imgpath.format('Print_Media_3'), bbox_inches='tight')
                    plt.close()
                    
                    # including image in successfully built viz
                    printViz.append('Print_Media_3')
                except:
                    pass
                
                try:
                    # 4th vis of Print media
                    s = dataP.groupby(['Edition']).count().reset_index()
                    b = s.sort_values(by = ['_id'], ascending = False)[:10].Edition
                    a = dataP[dataP.Edition.isin(b)]
                    df3 = a.groupby(['Edition','Sentiment']).count().reset_index()
                    df3 = df3.pivot(columns = 'Edition', index = 'Sentiment',values='ClipId')
                    sent = df3.index.values
                    senti = []
                    for y in sent:
                        if y in ['Negative','Neutral','Positive']:
                            senti.append(y)
                    df3 = df3.dropna(how = 'all', axis = 1)
                    df3 = df3.replace(np.nan,0,regex=True)
                    Sentiment  = senti
                    val = 0
                    for i in range(len(Sentiment)):
                        plt.bar(range(len(df3.columns)), df3.loc[Sentiment[i]], bottom = val, color = colour.get(Sentiment[i]))
                        val += df3.loc[Sentiment[i]]
                    plt.tick_params(labelsize = 14)
                    plt.xticks(range(len(df3.columns)), labels = df3.columns, rotation = 45)
                    top_value = 0
                    for i in range(len(Sentiment)):
                        top_value += np.array(df3.loc[Sentiment[i]], dtype = int)
                    for index, value in enumerate(top_value):
                        plt.text(index, value + 1, str(value))
                    plt.legend(Sentiment, prop={'size':20} )
                    plt.xlabel('Edition', fontsize = 20)
                    plt.ylabel('No. of sentiments reported', fontsize = 20)
                    plt.title('No. of Sentiments vs Edition', fontsize = 20, pad = 20)
                    fig_size = plt.gcf().get_size_inches() #Get current size
                    sizefactor = 2.5 #Set a zoom factor
                    # Modify the current size by the factor
                    plt.gcf().set_size_inches(sizefactor * fig_size)
                    plt.grid(axis = 'y')
                    plt.savefig(imgpath.format('Print_Media_4'), bbox_inches='tight')
                    plt.close()
                    
                    # including image in successfully built viz
                    printViz.append('Print_Media_4')
                except:
                    pass
                
            if not dataT.empty:
                
                try:
                    # building 1st visualisation of TV media
                    s = dataT.groupby(['Source']).count().reset_index()
                    b = s.sort_values(by = ['_id'], ascending = False)[:10].Source
                    a = dataT[dataT.Source.isin(b)]
                    df5 = a.groupby(['Source', 'Sentiment']).count().reset_index()
                    df5 = df5.pivot(columns = 'Source', index = 'Sentiment', values = 'ClipId')
                    sent = df5.index.values
                    senti = []
                    for y in sent:
                        if y in ['Negative','Neutral','Positive']:
                            senti.append(y)
                    df5 = df5.dropna(how = 'all', axis = 1)
                    df5 = df5.replace(np.nan,0,regex=True)
                    Sentiment  = senti
                    val = 0
                    for i in range(len(Sentiment)):
                        plt.bar(range(len(df5.columns)), df5.loc[Sentiment[i]], bottom = val, color = colour.get(Sentiment[i]))
                        val += df5.loc[Sentiment[i]]
                    plt.tick_params(labelsize=14)
                    plt.xticks(range(len(df5.columns)), labels = df5.columns, rotation = 90)
                    top_value = 0
                    for i in range(len(Sentiment)):
                        top_value += np.array(df5.loc[Sentiment[i]], dtype = int)
                    for index, value in enumerate(top_value):
                        plt.text(index, value + 0.5, str(value))
                    plt.legend(Sentiment, prop={'size':25} )
                    plt.xlabel('TV-Channel', fontsize = 20)
                    plt.ylabel('No. of sentiments reported', fontsize = 20)
                    plt.title('No. of Sentiments vs TV-Channels', fontsize = 20, pad = 20)
                    fig_size = plt.gcf().get_size_inches() #Get current size
                    sizefactor = 2.5 #Set a zoom factor
                    # Modify the current size by the factor
                    plt.gcf().set_size_inches(24,12)
                    plt.grid(axis = 'y')
                    plt.savefig(imgpath.format('TV_Media_1'), bbox_inches='tight')
                    plt.close()
                    
                    # including image in successfully built viz
                    tvViz.append('TV_Media_1')
                except:
                    pass
                
                try:
                    # building 2nd vis of TV media
                    temp_data = dataT.loc[(dataT.ProName != 'News') & (dataT.ProName != 'news')]
                    s = temp_data.groupby(['ProName']).count().reset_index()
                    b = s.sort_values(by = ['_id'], ascending = False)[:10].ProName
                    a = dataT[dataT.ProName.isin(b)]
                    df6 = a.groupby(['ProName','Sentiment']).count().reset_index()
                    df6 = df6.pivot(columns = 'ProName', index = 'Sentiment',values='ClipId')
                    senti = []
                    for y in sent:
                        if y in ['Negative','Neutral','Positive']:
                            senti.append(y)
                    df6 = df6.dropna(how = 'all', axis = 1)
                    df6 = df6.replace(np.nan,0,regex=True)
                    Sentiment  = senti
                    val = 0
                    for i in range(len(Sentiment)):
                        plt.bar(range(len(df6.columns)), df6.loc[Sentiment[i]], bottom = val, color = colour.get(Sentiment[i]))
                        val += df6.loc[Sentiment[i]]
                    plt.tick_params(labelsize = 14)
                    plt.xticks(range(len(df6.columns)), labels = df6.columns, rotation = 45)
                    top_value = 0
                    for i in range(len(Sentiment)):
                        top_value += np.array(df6.loc[Sentiment[i]], dtype = int)
                    for index, value in enumerate(top_value):
                        plt.text(index, value + 0.5, str(value))
                    plt.legend(Sentiment, prop={'size':20} )
                    plt.xlabel('Program Name', fontsize = 20)
                    plt.ylabel('No. of sentiments reported', fontsize = 20)
                    plt.title('No. of Sentiments vs Program', fontsize = 20, pad = 20)
                    fig_size = plt.gcf().get_size_inches() #Get current size
                    sizefactor = 2.5 #Set a zoom factor
                    # Modify the current size by the factor
                    plt.gcf().set_size_inches(sizefactor * fig_size)
                    plt.grid(axis = 'y')
                    plt.savefig(imgpath.format('TV_Media_2'), bbox_inches='tight')
                    plt.close()
                    
                    # including image in successfully built viz
                    tvViz.append('TV_Media_2')
                except:
                    pass
                
                try:
                    # building 3rd vis of TV media
                    dataT['AiringHour'] = dataT['AiringTime'].str.split(':').str[0]
                    At = dataT.groupby(['AiringHour', 'Sentiment']).count().reset_index()
                    At = At.pivot(columns = 'AiringHour', index = 'Sentiment', values = 'ClipId')
                    senti = []
                    for y in sent:
                        if y in ['Negative','Neutral','Positive']:
                            senti.append(y)
                    At = At.dropna(how = 'all', axis = 1)
                    At = At.replace(np.nan,0,regex = True)
                    Sentiment  = senti
                    linestyle = {
                        'Negative' : ':', 'Neutral' : '--', 'Positive' : '-', 'No-Comment' : '-.'
                    }
                    for i in range(len(senti)):
                        plt.plot(range(len(At.columns)), At.loc[Sentiment[i]], color = colour.get(Sentiment[i]), linestyle = linestyle.get(Sentiment[i]), marker = 'o')

                    plt.tick_params(labelsize=14)
                    plt.xticks(range(len(At.columns)), labels = At.columns, rotation = 60)
                    plt.legend(Sentiment, prop = {'size':25})
                    plt.xlabel('Airing Hours', fontsize = 20)
                    plt.ylabel('No. of Sentiments Reported', fontsize = 20)
                    plt.title('No. of Sentiments vs Airing Hours', fontsize =20)
                    fig_size = plt.gcf().get_size_inches() #Get current size
                    sizefactor = 2.5 #Set a zoom factor
                    # Modify the current size by the factor
                    plt.gcf().set_size_inches(sizefactor * fig_size)
                    plt.grid(axis = 'both')
                    plt.savefig(imgpath.format('TV_Media_3'), bbox_inches='tight')
                    plt.close()
                    
                    # including image in successfully built viz
                    tvViz.append('TV_Media_3')
                except:
                    pass
    


    else:
        # Ministry data unavailable for particular date range
        flag_data = False
        
    returnDict = { "tvViz" : tvViz,
                   "printViz" : printViz,
                   "onlineViz" : onlineViz,
                   "socialViz" : socialViz,
                   "online_count" : online_count,
                   "social_count" : social_count,
                   "online_neg_data" : online_neg_data,
                   "online_pos_data" : online_pos_data,
                   "social_neg_data" : social_neg_data,
                   "social_pos_data" : social_pos_data,
                   "trend_graph" : trend_graph,
		   "flag_data" : flag_data
                    }


    
    return returnDict
                
                
                    
                    
                    
                    
                
                    
                                                    
                        
                    
                    
                    
                    
                
                
                
            
                
                
                
                
    
    