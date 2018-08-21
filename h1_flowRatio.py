import os.path as opath
import os
import pandas as pd
import csv
import xlwt
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
#
from __path_organizer import aggr_dpath, h1data_dpath


HOURS = list(range(6, 24)) + [0, 1]
TERMINALS1 = ['T1', 'T2', 'T3', 'B', 'X']
TERMINALS2 = ['T1', 'T2', 'T3', 'T4', 'X']

cm_align=Alignment(horizontal='center',
                    vertical='center',
                    text_rotation=0,
                    wrap_text=False,
                    shrink_to_fit=False,
                    indent=0)
rm_align=Alignment(horizontal='right',
                    vertical='center',
                    text_rotation=0,
                    wrap_text=False,
                    shrink_to_fit=False,
                    indent=0)

def gen_xlsx_files():    
    yyyys = ['2009', '2010']
    yyyy = yyyys[0]
    wdf = None
    for yyyy in yyyys:
        terminals = TERMINALS1 if yyyy != '2018' else TERMINALS2
        df = pd.read_csv(opath.join(aggr_dpath, 'apTrip-%s.csv' % yyyy))
        df = df.groupby(['hour', 'previous_dropoff_loc', 'start_loc']).count()['taxi_id'].reset_index(name="count")
        hps_count = {}
        for hour, prevLoc, startLoc, count in df.values:
            hps_count[hour, prevLoc, startLoc] = count
        for h in HOURS:
            ofpath = opath.join(h1data_dpath, 'AirportFlow-%sH%02d.xlsx' % (yyyy, h))
            wb = Workbook()
            ws = wb.active
            ws.title = "RawNumber"
            ws.merge_cells(start_row=1, start_column=1, end_row=2, end_column=1)
            ws.merge_cells(start_row=1, start_column=2, end_row=1, end_column=7)
            ori_cell, dest_cell = ws.cell(row=1, column=1), ws.cell(row=1, column=2)
            ori_cell.value = 'Origin'
            dest_cell.value = 'Destination'
            for cell in [ori_cell, dest_cell]:
                cell.alignment = cm_align
            for i, tn in enumerate(terminals + ['Total']):
                o_cell, d_cell = ws.cell(row=i + 3, column=1), ws.cell(row=2, column=i + 2)
                for cell in [o_cell, d_cell]:
                    cell.value = tn
                    cell.alignment = cm_align
            for i, prevLoc in enumerate(terminals):
                for j, startLoc in enumerate(terminals):
                    k = h, prevLoc, startLoc
                    t_cell = ws.cell(row=i + 3, column=j + 2)
                    t_cell.value = hps_count[k] if k in hps_count else 0
                    t_cell.alignment = rm_align
                j += 1
                t_cell = ws.cell(row=i + 3, column=j + 2)
                bIndex = t_cell.col_idx - len(terminals)
                eIndex = t_cell.col_idx - 1
                t_cell.value = "=SUM(%s%d:%s%d)" % (get_column_letter(bIndex), t_cell.row, 
                                                     get_column_letter(eIndex), t_cell.row)                
            for i, tn in enumerate(terminals + ['Total']):
                t_cell = ws.cell(row=8, column=i + 2)
                bIndex = t_cell.row - len(terminals)
                eIndex = t_cell.row - 1
                colName = t_cell.column
                t_cell.value = "=SUM(%s%d:%s%d)" % (colName, bIndex, 
                                                     colName, eIndex)    
            #
            ws1 = wb.copy_worksheet(ws)
            ws1.title = "Ratio"
            totalCellCol = get_column_letter(2 + len(terminals) )            
            for i in range(len(terminals)):
                for j in range(len(terminals)):
                    cell = ws1.cell(row=i + 3, column=j + 2)                    
                    cell.value = "=%s!%s/%s!%s%d" % (ws.title, cell.coordinate, ws.title, totalCellCol, cell.row)
                    cell.number_format = '0.00%'

            totalCell = ws['G8']
            for i, tn in enumerate(terminals + ['Total']):
                cell = ws1.cell(row=8, column=i + 2)
                cell.value = "=%s!%s/%s!%s" % (ws.title, cell.coordinate, ws.title, totalCell.coordinate)
                cell.number_format = '0.00%'
                #
                cell = ws1.cell(row=i + 3, column=7)
                cell.value = "=%s!%s/%s!%s" % (ws.title, cell.coordinate, ws.title, totalCell.coordinate)
                cell.number_format = '0.00%'                
                
                
            
            wb.active = 2
            wb.save(filename=ofpath)
            
        
        


if __name__ == '__main__':
    gen_xlsx_files()