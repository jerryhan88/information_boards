import __init__
from init_project import *
#
import pandas as pd
import csv


html_template = \
"""
<html>
    <head>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
                google.charts.load('current', {'packages':['sankey']});
                google.charts.setOnLoadCallback(drawChart);

                function drawChart() {
                    var data = new google.visualization.DataTable();
                    data.addColumn('string', '%s');
                    data.addColumn('string', '%s');
                    data.addColumn('number', '%s');
                    data.addRows([
%s
                ]);
                // Sets chart options.
                var options = {
                  width: %d, height: %d,
                };
                // Instantiates and draws our chart, passing in some options.
                var chart = new google.visualization.Sankey(document.getElementById('sankey_basic'));
                chart.draw(data, options);
                }
        </script>
    </head>
    <body>
        <div id="sankey_basic";"></div>
    </body>
</html>
"""

WIDTH, HEIGHT = 600, 300


def run():
    csv_ofpath = opath.join(dpath['hJoinQRatio'], 'hJoinQRatio.csv')
    if not opath.exists(csv_ofpath):
        df = pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-2009.csv'))
        df = df.append(pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-2010.csv')))
        gdf = df.groupby(['year', 'locPrevDropoff', 'locPickup']).count()['did'].to_frame('numTrips').reset_index()
        tripSum2009 = gdf[(gdf['year'] == 2009)]['numTrips'].sum()
        tripSum2010 = gdf[(gdf['year'] == 2010)]['numTrips'].sum()
        gdf['ratio'] = gdf.apply(lambda row: row['numTrips'] / float(tripSum2009) 
                                if row['year'] == 2009 else row['numTrips'] / float(tripSum2010), axis=1)
        gdf.to_csv(csv_ofpath, index=False)
        df = gdf
    else:
        df = pd.read_csv(csv_ofpath)
    for year in [2009, 2010]:
        html_ofpath = opath.join(dpath['hJoinQRatio'], 'hJoinQRatio%d.html' % year)
        ydf = df[(df['year'] == year)]
        flow_str = ''
        for locPrevDropoff, locPickup, ratio in ydf[['locPrevDropoff', 'locPickup', 'ratio']].values:
            flow_str += '\t\t\t\t\t\t\t\t\t%s\n' % "['F %s', 'T %s', %.3f]," % (locPrevDropoff, locPickup, ratio)
        html_str = html_template % ('locPrevDropoff', 'locPickup', 'ratio', flow_str, WIDTH, HEIGHT)
        with open(html_ofpath, 'w') as f:
            f.write(html_str)
            
        
['%.2f' % (v * 100) for v in df[(df['year'] == 2010) & (df['locPrevDropoff'] == 'T1')]['ratio']]
        
        
if __name__ == '__main__':
    run()