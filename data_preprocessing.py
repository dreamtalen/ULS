import xlrd

if __name__ == '__main__':
    wordbook = xlrd.open_workbook("input.xls")
    sheet1, sheet2 = wordbook._sheet_list
    print sheet1.name,sheet1.nrows,sheet1.ncols
    route_od_dict = {}
    zone_input_dict = {}
    zone_output_dict = {}
    for start_index, start in enumerate(sheet1.col_values(0)[1:]):
        for end_index, end in enumerate(sheet1.row_values(0)[1:]):
            start = int(start)
            end = int(end)
            route = str(start) + '->' + str(end)
            od = sheet1.row_values(start_index+1)[end_index+1]
            route_od_dict[route] = od
            if start not in zone_output_dict: zone_output_dict[start] = od
            else:   zone_output_dict[start] += od
            if end not in zone_input_dict: zone_input_dict[end] = od
            else:   zone_input_dict[end] += od
    zone_od_dict = {k:zone_input_dict[k] + zone_output_dict[k] for k in zone_input_dict.keys()}
    zone_list = zone_input_dict.keys()
    sort_zone_list = sorted(zone_list, key=lambda x:zone_od_dict[x], reverse=True)
    for i in sort_zone_list:
        print i, zone_od_dict[i]
    print sheet2.name,sheet2.nrows,sheet2.ncols
    zone_areakm_dict, zone_aream_dict = {}, {}
    zone_x_dict, zone_y_dict = {}, {}
    zone_traffic_dict = {}
    for index, zone in enumerate(sheet2.col_values(0)[1:]):
        zone = int(zone)
        zone_areakm_dict[zone] = sheet2.row_values(index+1)[1]
        zone_aream_dict[zone] = sheet2.row_values(index+1)[2]
        zone_x_dict[zone] = sheet2.row_values(index+1)[3]
        zone_y_dict[zone] = sheet2.row_values(index+1)[4]
        zone_traffic_dict[zone] = sheet2.row_values(index+1)[5]
    print zone_traffic_dict[897]


