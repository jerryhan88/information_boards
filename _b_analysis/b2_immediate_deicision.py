import h_hypothesisTest
from __path_organizer import *
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
    for yy in ['09', '10']:
        ifpath = opath.join(dpath['analysis'], 'decision-ap-20%s.csv' % yy)
        df = pd.read_csv(ifpath)
        group_df = df.groupby(['prevEndTerminal', 'pickUpTerminal']).count().reset_index()
        #
        csv_ofpath = opath.join(dpath['2_immediateDecision'], 'immediateDecision-20%s.csv' % yy)
        html_ofpath = opath.join(dpath['2_immediateDecision'], 'immediateDecision-20%s.html' % yy)
        with open(csv_ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_headers = ['prevEndTerminal', 'pickUpTerminal', 'numTrips']
            writer.writerow(new_headers)
        flow_str = ''
        for fromT, toT, num in group_df[['prevEndTerminal', 'pickUpTerminal', 'did']].values:
            with open(csv_ofpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow([fromT, toT, num])
            flow_str += '\t\t\t\t\t\t\t\t\t%s\n' % "['from %s', 'to %s', %d]," % (fromT, toT, num)
        html_str = html_template % ('prevEndTerminal', 'pickUpTerminal', 'numTrips', flow_str, WIDTH, HEIGHT)
        with open(html_ofpath, 'w') as f:
            f.write(html_str)

if __name__ == '__main__':
    run()
