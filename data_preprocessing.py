import xlrd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
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

    print sheet2.name,sheet2.nrows,sheet2.ncols
    zone_areakm_dict, zone_aream_dict = {}, {}
    zone_x_dict, zone_y_dict = {}, {}
    zone_traffic_dict = {}
    for index, zone in enumerate(sheet2.col_values(0)[1:]):
        zone = int(zone)
        if zone > 4:
            zone_areakm_dict[zone] = sheet2.row_values(index+1)[1]
            zone_aream_dict[zone] = sheet2.row_values(index+1)[2]
            zone_x_dict[zone] = sheet2.row_values(index+1)[3]
            zone_y_dict[zone] = sheet2.row_values(index+1)[4]
            zone_traffic_dict[zone] = float(sheet2.row_values(index+1)[5])
        else:
            zone_x_dict[zone] = sheet2.row_values(index+1)[3]
            zone_y_dict[zone] = sheet2.row_values(index+1)[4]
    # print zone_traffic_dict[897]

    part_zone_list = [zone for zone in zone_list if zone > 4]
    zone_min_decreod_dict = {}
    for i in part_zone_list :
        if zone_traffic_dict[i] <= 4:
            zone_min_decreod_dict[i] = 0
        else:
            min_decreod = ((zone_traffic_dict[i] - 4)/zone_traffic_dict[i])*zone_od_dict[i]
            zone_min_decreod_dict[i] = min_decreod

    sort_zone_decre_list = sorted(part_zone_list, key=lambda x: zone_min_decreod_dict[x], reverse=True)

    for i in sort_zone_decre_list:
        print i, zone_od_dict[i], zone_traffic_dict[i], zone_min_decreod_dict[i]

    origin_x = min(zone_x_dict.values())
    origin_y = min(zone_y_dict.values())
    for i in zone_list:
        zone_x_dict[i] = zone_x_dict[i] - origin_x
        zone_y_dict[i] = zone_y_dict[i] - origin_y

    for i in range(1,5):
        zone_min_decreod_dict[i] = 0.0
    # print zone_x_dict.values()
    max_decreod_need = max(zone_min_decreod_dict.values())
    fig, ax = plt.subplots()
    color = [str(1 - zone_min_decreod_dict[zone]/max_decreod_need) for zone in zone_list]

    one2zone_od_dict = {}
    for zone in zone_list:
        for k, v in route_od_dict.items():
            if k == '1->'+str(zone):
                one2zone_od_dict[zone] = v
    max_one2zone_od = max(one2zone_od_dict.values())
    # color = [str(1 - one2zone_od_dict[zone]/max_one2zone_od) for zone in zone_list]

    two2zone_od_dict = {}
    for zone in zone_list:
        for k, v in route_od_dict.items():
            if k == '2->'+str(zone):
                two2zone_od_dict[zone] = v
    max_two2zone_od = max(two2zone_od_dict.values())
    color = [str(1 - two2zone_od_dict[zone]/max_two2zone_od) for zone in zone_list]

    three2zone_od_dict = {}
    for zone in zone_list:
        for k, v in route_od_dict.items():
            if k == '3->'+str(zone):
                three2zone_od_dict[zone] = v
    max_three2zone_od = max(three2zone_od_dict.values())
    # color = [str(1 - three2zone_od_dict[zone]/max_three2zone_od) for zone in zone_list]

    four2zone_od_dict = {}
    for zone in zone_list:
        for k, v in route_od_dict.items():
            if k == '4->'+str(zone):
                four2zone_od_dict[zone] = v
    max_four2zone_od = max(four2zone_od_dict.values())
    # color = [str(1 - four2zone_od_dict[zone]/max_four2zone_od) for zone in zone_list]

    ax.scatter([zone_x_dict[i] for i in zone_list], [zone_y_dict[i] for i in zone_list], c=color)

    # cir1 = Circle(xy = (zone_x_dict[1], zone_y_dict[1]), radius=10000, alpha=0.2)
    cir1 = Circle(xy = (zone_x_dict[2], zone_y_dict[2]), radius=13000, alpha=0.4)
    # cir1 = Circle(xy = (zone_x_dict[3], zone_y_dict[3]), radius=11000, alpha=0.4)
    # cir1 = Circle(xy = (zone_x_dict[4], zone_y_dict[4]), radius=14000, alpha=0.4)
    ax.add_patch(cir1)

    # plt.show()

    # in_circle1_zone_list = [zone for zone in zone_list if ((zone_x_dict[zone] - zone_x_dict[1])**2 + (zone_y_dict[zone] - zone_y_dict[1])**2)**0.5 <= 10000]
    # circle1_centroid_x = sum(one2zone_od_dict[i]*zone_x_dict[i] for i in in_circle1_zone_list)/sum(one2zone_od_dict[i] for i in in_circle1_zone_list)
    # circle1_centroid_y = sum(one2zone_od_dict[i]*zone_y_dict[i] for i in in_circle1_zone_list)/sum(one2zone_od_dict[i] for i in in_circle1_zone_list)
    # print circle1_centroid_x, circle1_centroid_y
    # circle1_centroid_cir = Circle(xy=(circle1_centroid_x, circle1_centroid_y), radius=500, color='red')
    # ax.add_patch(circle1_centroid_cir)

    in_circle2_zone_list = [zone for zone in zone_list if ((zone_x_dict[zone] - zone_x_dict[2])**2 + (zone_y_dict[zone] - zone_y_dict[2])**2)**0.5 <= 13000]
    circle2_centroid_x = sum(two2zone_od_dict[i]*zone_x_dict[i] for i in in_circle2_zone_list)/sum(two2zone_od_dict[i] for i in in_circle2_zone_list)
    circle2_centroid_y = sum(two2zone_od_dict[i]*zone_y_dict[i] for i in in_circle2_zone_list)/sum(two2zone_od_dict[i] for i in in_circle2_zone_list)
    circle2_centroid_cir = Circle(xy=(circle2_centroid_x, circle2_centroid_y), radius=500, color='red')
    ax.add_patch(circle2_centroid_cir)

    # in_circle3_zone_list = [zone for zone in zone_list if ((zone_x_dict[zone] - zone_x_dict[3])**2 + (zone_y_dict[zone] - zone_y_dict[3])**2)**0.5 <= 11000]
    # circle3_centroid_x = sum(three2zone_od_dict[i]*zone_x_dict[i] for i in in_circle3_zone_list)/sum(three2zone_od_dict[i] for i in in_circle3_zone_list)
    # circle3_centroid_y = sum(three2zone_od_dict[i]*zone_y_dict[i] for i in in_circle3_zone_list)/sum(three2zone_od_dict[i] for i in in_circle3_zone_list)
    # circle3_centroid_cir = Circle(xy=(circle3_centroid_x, circle3_centroid_y), radius=500, color='red')
    # ax.add_patch(circle3_centroid_cir)

    # in_circle4_zone_list = [zone for zone in zone_list if ((zone_x_dict[zone] - zone_x_dict[4])**2 + (zone_y_dict[zone] - zone_y_dict[4])**2)**0.5 <= 14000]
    # circle4_centroid_x = sum(four2zone_od_dict[i]*zone_x_dict[i] for i in in_circle4_zone_list)/sum(four2zone_od_dict[i] for i in in_circle4_zone_list)
    # circle4_centroid_y = sum(four2zone_od_dict[i]*zone_y_dict[i] for i in in_circle4_zone_list)/sum(four2zone_od_dict[i] for i in in_circle4_zone_list)
    # circle4_centroid_cir = Circle(xy=(circle4_centroid_x, circle4_centroid_y), radius=500, color='red')
    # ax.add_patch(circle4_centroid_cir)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_aspect(1)
    plt.show()
