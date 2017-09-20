import xlrd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
from pulp import *
import random
import time

def main():
    wordbook = xlrd.open_workbook("input.xls")
    sheet1, sheet2 = wordbook._sheet_list
    # print sheet1.name,sheet1.nrows,sheet1.ncols
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

    # print sheet2.name,sheet2.nrows,sheet2.ncols
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

    # for i in sort_zone_decre_list:
    #     print i, zone_od_dict[i], zone_traffic_dict[i], zone_min_decreod_dict[i]

    i = 880
    # print i, zone_od_dict[i], zone_traffic_dict[i], zone_min_decreod_dict[i], route_od_dict['3->880']+route_od_dict['880->3']+route_od_dict['1->880']+route_od_dict['880->1']+route_od_dict['2->880']+route_od_dict['880->2']+route_od_dict['4->880']+route_od_dict['880->4']

    zone_1_list = [793] + range(795, 799) + range(800, 803) + [804, 806, 807, 809, 810, 811] + range(813, 822) + [823, 827, 828, 830, 833, 834]
    zone_2_list = [791, 792, 794, 799, 803, 805, 808, 812, 822, 824, 825, 826, 829, 831, 832] + range(835, 841)
    zone_3_list = range(870, 901)
    zone_4_list = range(841, 870)
    origin_x = min(zone_x_dict.values())
    origin_y = min(zone_y_dict.values())
    for i in zone_list:
        zone_x_dict[i] = zone_x_dict[i] - origin_x
        zone_y_dict[i] = zone_y_dict[i] - origin_y
    # print "origin", origin_x, origin_y

    for i in range(1,5):
        zone_min_decreod_dict[i] = 0.0
    # print zone_x_dict.values()

    max_decreod_need = max(zone_min_decreod_dict.values())
    fig, ax = plt.subplots()
    color = [str(1 - zone_min_decreod_dict[zone]/max_decreod_need) for zone in zone_list]
    # color = []
    # for zone in zone_list:
    #     if zone in zone_1_list: color.append("red")
    #     elif zone in zone_2_list: color.append("black")
    #     elif zone in zone_3_list: color.append("orange")
    #     elif zone in zone_4_list: color.append("blue")
    #     else: color.append("yellow")


    ax.scatter([zone_x_dict[i] for i in zone_list], [zone_y_dict[i] for i in zone_list], c=color)


    # ax.set_xlabel('x')
    # ax.set_ylabel('y')
    # ax.set_aspect(1)
    # plt.show()

    one2zone_od_dict = {}
    for zone in zone_list:
        for k, v in route_od_dict.items():
            if k == '1->'+str(zone):
                one2zone_od_dict[zone] = v
    max_one2zone_od = max(one2zone_od_dict.values())

    two2zone_od_dict = {}
    for zone in zone_list:
        for k, v in route_od_dict.items():
            if k == '2->'+str(zone):
                two2zone_od_dict[zone] = v
    max_two2zone_od = max(two2zone_od_dict.values())

    three2zone_od_dict = {}
    for zone in zone_list:
        for k, v in route_od_dict.items():
            if k == '3->'+str(zone):
                three2zone_od_dict[zone] = v
    max_three2zone_od = max(three2zone_od_dict.values())

    four2zone_od_dict = {}
    for zone in zone_list:
        for k, v in route_od_dict.items():
            if k == '4->'+str(zone):
                four2zone_od_dict[zone] = v
    max_four2zone_od = max(four2zone_od_dict.values())

    centroid1_x = sum(one2zone_od_dict[i]*zone_x_dict[i] for i in zone_1_list)/sum(one2zone_od_dict[i] for i in zone_1_list)
    centroid1_y = sum(one2zone_od_dict[i]*zone_y_dict[i] for i in zone_1_list)/sum(one2zone_od_dict[i] for i in zone_1_list)
    # print 'centroid 1', centroid1_x+origin_x, centroid1_y+origin_y
    zone1_centroid_cir = Circle(xy=(centroid1_x, centroid1_y), radius=500, color='red')

    centroid2_x = sum(two2zone_od_dict[i]*zone_x_dict[i] for i in zone_2_list)/sum(two2zone_od_dict[i] for i in zone_2_list)
    centroid2_y = sum(two2zone_od_dict[i]*zone_y_dict[i] for i in zone_2_list)/sum(two2zone_od_dict[i] for i in zone_2_list)
    # print 'centroid 2', centroid2_x+origin_x, centroid2_y+origin_y
    zone2_centroid_cir = Circle(xy=(centroid2_x, centroid2_y), radius=500, color='red')

    centroid3_x = sum(three2zone_od_dict[i]*zone_x_dict[i] for i in zone_3_list)/sum(three2zone_od_dict[i] for i in zone_3_list)
    centroid3_y = sum(three2zone_od_dict[i]*zone_y_dict[i] for i in zone_3_list)/sum(three2zone_od_dict[i] for i in zone_3_list)
    # print 'centroid 3', centroid3_x+origin_x, centroid3_y+origin_y
    zone3_centroid_cir = Circle(xy=(centroid3_x, centroid3_y), radius=500, color='red')

    centroid4_x = sum(four2zone_od_dict[i]*zone_x_dict[i] for i in zone_4_list)/sum(four2zone_od_dict[i] for i in zone_4_list)
    centroid4_y = sum(four2zone_od_dict[i]*zone_y_dict[i] for i in zone_4_list)/sum(four2zone_od_dict[i] for i in zone_4_list)
    # print 'centroid 4', centroid4_x+origin_x, centroid4_y+origin_y
    zone4_centroid_cir = Circle(xy=(centroid4_x, centroid4_y), radius=500, color='red')

    ax.add_patch(zone1_centroid_cir)
    ax.add_patch(zone2_centroid_cir)
    ax.add_patch(zone3_centroid_cir)
    ax.add_patch(zone4_centroid_cir)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_aspect(1)

    # time.sleep(1000)
    # print 'zone 1 need decrease', sum(zone_min_decreod_dict[i] for i in zone_1_list)
    # print 'zone 2 need decrease', sum(zone_min_decreod_dict[i] for i in zone_2_list)
    # print 'zone 3 need decrease', sum(zone_min_decreod_dict[i] for i in zone_3_list)
    # print 'zone 4 need decrease', sum(zone_min_decreod_dict[i] for i in zone_4_list)
    #
    level2_list_1 = [807, 801, 810, 820, 811, 818]
    level2_list_2 = [826, 829, 824, 805, 832]
    level2_list_3 = [896, 900, 888, 891, 897, 871, 884, 894, 876]
    level2_list_4 = [829, 837, 826, 805, 832]

    for level2 in level2_list_1 + level2_list_2 + level2_list_3 + level2_list_4:
        add_cir = Circle(xy=(zone_x_dict[level2], zone_y_dict[level2]), radius=400, color='blue')
        ax.add_patch(add_cir)


    plt.show()

    park_name_list = [1, 2, 3, 4]
    # # print len(zone_1_list), len(zone_2_list), len(zone_3_list), len(zone_4_list)
    zone_1234_list_list = [zone_1_list, zone_2_list, zone_3_list, zone_4_list]

    point_this_park_od_dict = {}
    point_other_park_sumod_dict = {}

    point_park_od_dict = {
        str(point): {park:0 for park in park_name_list} for point in part_zone_list
    }

    for park, point_list in zip(park_name_list, zone_1234_list_list):
        for point in point_list:
            this_point_park_od_dict = {p:0 for p in park_name_list}
            this_point_need = zone_min_decreod_dict[point]
            for p in park_name_list:
                if str(point) + '->' + str(p) in route_od_dict:
                    this_point_park_od_dict[p] += route_od_dict[str(point) + '->' + str(p)]
                if str(p) + '->' + str(point) in route_od_dict:
                    this_point_park_od_dict[p] += route_od_dict[str(p) + '->' + str(point)]

            # print park, point, this_point_need, this_point_park_od_dict

            if this_point_need <= this_point_park_od_dict[park]:
                point_park_od_dict[str(point)][park] = this_point_need
            elif this_point_park_od_dict[park] < this_point_need <= sum([this_point_park_od_dict[p] for p in park_name_list]):
                point_park_od_dict[str(point)][park] = this_point_park_od_dict[park]
                sum_other_park_od = sum([this_point_park_od_dict[p] for p in park_name_list if p != park])
                remain_need = this_point_need - this_point_park_od_dict[park]
                for p in park_name_list:
                    if p != park:
                        point_park_od_dict[str(point)][p] = remain_need*this_point_park_od_dict[p]/sum_other_park_od
            else:
                for p in park_name_list:
                    point_park_od_dict[str(point)][p] = this_point_park_od_dict[p]
            # print point_park_od_dict[str(point)]

    ################calculate transport rate
    for park in park_name_list:
        denominator = sum(point_park_od_dict[str(point)][park] for point in part_zone_list)
        this_park_this_zone = sum(point_park_od_dict[str(point)][park] for point in zone_1234_list_list[park-1])
        # print park, (denominator - this_park_this_zone)/denominator
    #
    # for park, zone_list in zip(park_name_list, zone_1234_list_list):
    #     sum_park_zone_list = 0
    #     for zone in zone_list:
    #         route_in = str(park) + '->' + str(zone)
    #         if route_in in route_od_dict:
    #             sum_park_zone_list += route_od_dict[route_in]
    #         route_out = str(zone) + '->' + str(park)
    #         if route_out in route_od_dict:
    #             sum_park_zone_list += route_od_dict[route_out]
    #     print park, sum_park_zone_list

    # for index, zone_n_list in enumerate(zone_1234_list_list):
    #     sum_zone_inout, sum_zone_park_inout, sum_zone_need_dec = 0, 0, 0
    #     for point in zone_n_list:
    #         sum_zone_inout += zone_input_dict[point] + zone_output_dict[point]
    #         for park in park_name_list:
    #             route_in = str(park) + '->' + str(point)
    #             if route_in in route_od_dict:
    #                 sum_zone_park_inout += route_od_dict[route_in]
    #             route_out = str(point) + '->' + str(park)
    #             if route_out in route_od_dict:
    #                 sum_zone_park_inout += route_od_dict[route_out]
    #         sum_zone_need_dec += zone_min_decreod_dict[point]
    #     print str(index+1), sum_zone_park_inout, sum_zone_inout, sum_zone_need_dec
    #     print sum_zone_park_inout/sum_zone_inout

    # zone_park_inout_ratio_dict = {}
    #
    # for point in part_zone_list:
    #     sum_zone_park_inout = 0
    #     for park in park_name_list:
    #         route_in = str(park) + '->' + str(point)
    #         if route_in in route_od_dict:
    #             sum_zone_park_inout += route_od_dict[route_in]
    #         route_out = str(point) + '->' + str(park)
    #         if route_out in route_od_dict:
    #             sum_zone_park_inout += route_od_dict[route_out]
    #     # print str(point), zone_input_dict[point] + zone_output_dict[point], sum_zone_park_inout, zone_min_decreod_dict[point]
    #     zone_park_inout_ratio_dict[str(point)] = sum_zone_park_inout/(zone_input_dict[point] + zone_output_dict[point])
    # # print zone_park_inout_ratio_dict
    #
    # point_other_zone_ratio_dict = {}
    #
    # point_list_sorted_park_inout_ratio = sorted(zone_park_inout_ratio_dict.keys(), key=lambda x: zone_park_inout_ratio_dict[x])
    # for p in point_list_sorted_park_inout_ratio[:3]:
    #     print p, zone_park_inout_ratio_dict[p]
    #
    # for p in [833, 834]:
    #     sum_zone234 = 0
    #     for end in zone_2_list+zone_3_list+zone_4_list:
    #         if str(p) + '->' + str(end) in route_od_dict:
    #             sum_zone234 += route_od_dict[str(p) + '->' + str(end)]
    #         if str(end) + '->' + str(p) in route_od_dict:
    #             sum_zone234 += route_od_dict[str(end) + '->' + str(p)]
    #     print p, sum_zone234/(zone_input_dict[point] + zone_output_dict[point])
    #
    # for p in [835]:
    #     sum_zone134 = 0
    #     for end in zone_1_list+zone_3_list+zone_4_list:
    #         if str(p) + '->' + str(end) in route_od_dict:
    #             sum_zone134 += route_od_dict[str(p) + '->' + str(end)]
    #         if str(end) + '->' + str(p) in route_od_dict:
    #             sum_zone134 += route_od_dict[str(end) + '->' + str(p)]
    #     print p, sum_zone134/(zone_input_dict[point] + zone_output_dict[point])

    # time.sleep(1000)

    # sum_zone_12 = 0
    # for point1 in zone_1_list:
    #     for point2 in zone_2_list:
    #         route1 = str(point1) + '->' + str(point2)
    #         if route1 in route_od_dict: sum_zone_12 += route_od_dict[route1]
    #         route2 = str(point2) + '->' + str(point1)
    #         if route2 in route_od_dict: sum_zone_12 += route_od_dict[route2]
    # for point2 in zone_2_list:
    #     route1 = str(1) + '->' + str(point2)
    #     if route1 in route_od_dict: sum_zone_12 += route_od_dict[route1]
    #     route2 = str(point2) + '->' + str(1)
    #     if route2 in route_od_dict: sum_zone_12 += route_od_dict[route2]
    # for point1 in zone_1_list:
    #     route1 = str(2) + '->' + str(point1)
    #     if route1 in route_od_dict: sum_zone_12 += route_od_dict[route1]
    #     route2 = str(point1) + '->' + str(2)
    #     if route2 in route_od_dict: sum_zone_12 += route_od_dict[route2]
    # print sum_zone_12
    # 16724.8

    # sum_zone_23 = 0
    # for point2 in zone_2_list:
    #     for point3 in zone_3_list:
    #         route1 = str(point2) + '->' + str(point3)
    #         if route1 in route_od_dict: sum_zone_23 += route_od_dict[route1]
    #         route2 = str(point3) + '->' + str(point2)
    #         if route2 in route_od_dict: sum_zone_23 += route_od_dict[route2]
    # for point3 in zone_3_list:
    #     route1 = str(2) + '->' + str(point3)
    #     if route1 in route_od_dict: sum_zone_23 += route_od_dict[route1]
    #     route2 = str(point3) + '->' + str(2)
    #     if route2 in route_od_dict: sum_zone_23 += route_od_dict[route2]
    # for point2 in zone_2_list:
    #     route1 = str(3) + '->' + str(point2)
    #     if route1 in route_od_dict: sum_zone_23 += route_od_dict[route1]
    #     route2 = str(point2) + '->' + str(3)
    #     if route2 in route_od_dict: sum_zone_23 += route_od_dict[route2]
    # print sum_zone_23
    # 19762.401

    # sum_zone_14 = 0
    # for point1 in zone_1_list:
    #     for point4 in zone_4_list:
    #         route1 = str(point1) + '->' + str(point4)
    #         if route1 in route_od_dict: sum_zone_14 += route_od_dict[route1]
    #         route2 = str(point4) + '->' + str(point1)
    #         if route2 in route_od_dict: sum_zone_14 += route_od_dict[route2]
    # for point4 in zone_4_list:
    #     route1 = str(1) + '->' + str(point4)
    #     if route1 in route_od_dict: sum_zone_14 += route_od_dict[route1]
    #     route2 = str(point4) + '->' + str(1)
    #     if route2 in route_od_dict: sum_zone_14 += route_od_dict[route2]
    # for point3 in zone_3_list:
    #     route1 = str(1) + '->' + str(point3)
    #     if route1 in route_od_dict: sum_zone_14 += route_od_dict[route1]
    #     route2 = str(point3) + '->' + str(1)
    #     if route2 in route_od_dict: sum_zone_14 += route_od_dict[route2]
    # for point1 in zone_1_list:
    #     route1 = str(4) + '->' + str(point1)
    #     if route1 in route_od_dict: sum_zone_14 += route_od_dict[route1]
    #     route2 = str(point1) + '->' + str(4)
    #     if route2 in route_od_dict: sum_zone_14 += route_od_dict[route2]
    # for point1 in zone_1_list:
    #     route1 = str(3) + '->' + str(point1)
    #     if route1 in route_od_dict: sum_zone_14 += route_od_dict[route1]
    #     route2 = str(point1) + '->' + str(3)
    #     if route2 in route_od_dict: sum_zone_14 += route_od_dict[route2]
    # print sum_zone_14
    # 31964.898

    # sum_zone_43 = 0
    # for point4 in zone_4_list:
    #     for point3 in zone_3_list:
    #         route1 = str(point4) + '->' + str(point3)
    #         if route1 in route_od_dict: sum_zone_43 += route_od_dict[route1]
    #         route2 = str(point3) + '->' + str(point4)
    #         if route2 in route_od_dict: sum_zone_43 += route_od_dict[route2]
    # for point4 in zone_4_list:
    #     route1 = str(3) + '->' + str(point4)
    #     if route1 in route_od_dict: sum_zone_43 += route_od_dict[route1]
    #     route2 = str(point4) + '->' + str(3)
    #     if route2 in route_od_dict: sum_zone_43 += route_od_dict[route2]
    # for point3 in zone_3_list:
    #     route1 = str(4) + '->' + str(point3)
    #     if route1 in route_od_dict: sum_zone_43 += route_od_dict[route1]
    #     route2 = str(point3) + '->' + str(4)
    #     if route2 in route_od_dict: sum_zone_43 += route_od_dict[route2]
    # for point3 in zone_3_list:
    #     route1 = str(1) + '->' + str(point3)
    #     if route1 in route_od_dict: sum_zone_43 += route_od_dict[route1]
    #     route2 = str(point3) + '->' + str(1)
    #     if route2 in route_od_dict: sum_zone_43 += route_od_dict[route2]
    # print sum_zone_43
    # 19210.205

    # time.sleep(1000)

    # level2_list, point_od_dict = annealing(zone_1_list, 6, zone_min_decreod_dict, zone_x_dict, zone_y_dict, zone_x_dict[1], zone_y_dict[1], centroid1_x, centroid1_y)
    # for level2 in level2_list:
    #     level2_cir = Circle(xy=(zone_x_dict[level2], zone_y_dict[level2]), radius=200, color='blue')
    #     ax.add_patch(level2_cir)
    #     level2_scope_cir = Circle(xy=(zone_x_dict[level2], zone_y_dict[level2]), radius=3000, alpha=0.2)
    #     ax.add_patch(level2_scope_cir)
    # print 'zone 1', level2_list
    #
    # level2_list = annealing(zone_2_list, 5, zone_min_decreod_dict, zone_x_dict, zone_y_dict, zone_x_dict[2], zone_y_dict[2], centroid2_x, centroid2_y)
    # for level2 in level2_list:
    #     level2_cir = Circle(xy=(zone_x_dict[level2], zone_y_dict[level2]), radius=200, color='blue')
    #     ax.add_patch(level2_cir)
    #     level2_scope_cir = Circle(xy=(zone_x_dict[level2], zone_y_dict[level2]), radius=3000, alpha=0.2)
    #     ax.add_patch(level2_scope_cir)
    # print 'zone 2', level2_list
    #
    # level2_list = annealing(zone_3_list, 9, zone_min_decreod_dict, zone_x_dict, zone_y_dict, zone_x_dict[3], zone_y_dict[3], centroid3_x, centroid3_y)
    # for level2 in level2_list:
    #     level2_cir = Circle(xy=(zone_x_dict[level2], zone_y_dict[level2]), radius=200, color='blue')
    #     ax.add_patch(level2_cir)
    #     level2_scope_cir = Circle(xy=(zone_x_dict[level2], zone_y_dict[level2]), radius=3000, alpha=0.2)
    #     ax.add_patch(level2_scope_cir)
    # print 'zone 3', level2_list
    #
    # level2_list = annealing(zone_4_list, 5, zone_min_decreod_dict, zone_x_dict, zone_y_dict, zone_x_dict[4], zone_y_dict[4], centroid4_x, centroid4_y)
    # for level2 in level2_list:
    #     level2_cir = Circle(xy=(zone_x_dict[level2], zone_y_dict[level2]), radius=200, color='blue')
    #     ax.add_patch(level2_cir)
    #     level2_scope_cir = Circle(xy=(zone_x_dict[level2], zone_y_dict[level2]), radius=3000, alpha=0.2)
    #     ax.add_patch(level2_scope_cir)
    # print 'zone 4', level2_list
    #
    # centroid_scope_cir = Circle(xy=(centroid1_x, centroid1_y), radius=3000, alpha=0.2)
    # ax.add_patch(centroid_scope_cir)
    # centroid_scope_cir = Circle(xy=(centroid2_x, centroid2_y), radius=3000, alpha=0.2)
    # ax.add_patch(centroid_scope_cir)
    # centroid_scope_cir = Circle(xy=(centroid3_x, centroid3_y), radius=3000, alpha=0.2)
    # ax.add_patch(centroid_scope_cir)
    # centroid_scope_cir = Circle(xy=(centroid4_x, centroid4_y), radius=3000, alpha=0.2)
    # ax.add_patch(centroid_scope_cir)
    # plt.show()

# zone 1 [830, 800, 833, 818, 811, 814]
# zone 2 [812, 805, 824, 829, 838]
# zone 3 [893, 896, 898, 873, 870, 900, 891, 899, 876]
# zone 4 [861, 868, 858, 844, 846]
#     level2_list = [830, 800, 833, 818, 811, 814]

    # level2_list, point_od_dict, level2_service_list_dict = annealing(zone_1_list, 6, zone_min_decreod_dict, zone_x_dict, zone_y_dict, zone_x_dict[1], zone_y_dict[1], centroid1_x, centroid1_y)
    # level2_list, point_od_dict, level2_service_list_dict = annealing(zone_1_list, 6, zone_min_decreod_dict, zone_x_dict, zone_y_dict, zone_x_dict[1], zone_y_dict[1], centroid1_x, centroid1_y)

    level2_list, point_od_dict, level2_service_list_dict = annealing(zone_3_list, 9, zone_min_decreod_dict, zone_x_dict, zone_y_dict, zone_x_dict[3], zone_y_dict[3], centroid3_x, centroid3_y)
    # level2_list, point_od_dict, level2_service_list_dict = annealing(zone_4_list, 5, zone_min_decreod_dict, zone_x_dict, zone_y_dict, zone_x_dict[4], zone_y_dict[4], centroid4_x, centroid4_y)

    # level2_list, point_od_dict, level2_service_list_dict = annealing(zone_2_list, 5, zone_min_decreod_dict, zone_x_dict, zone_y_dict, zone_x_dict[2], zone_y_dict[2], centroid2_x, centroid2_y)
    # print 'zone 4', level2_list
    # print level2_service_list_dict
    # print point_od_dict
    # level2_list = [859, 863, 853, 858, 847]
    graph = minimize_total_length(level2_list, zone_x_dict, zone_y_dict, centroid3_x, centroid3_y)
    # print graph
    # time.sleep(1000)
    # print graph
    # point_od_dict = {str(i):3000 for i in level2_list}
    # point_od_dict['center'] = 4000
    edge_od_dict = calculate_edge_od(graph, point_od_dict, zone_x_dict, zone_y_dict, centroid3_x, centroid3_y)
    edge_length_dict = {}
    # print edge_od_dict
    total_cost = 0
    for edge, od in edge_od_dict.items():
        start, end = edge.split('->')
        if start != 'center':
            start = int(start)
            end = int(end)
            length = distance(zone_x_dict[start], zone_y_dict[start], zone_x_dict[end], zone_y_dict[end])
            edge_length_dict[edge] = length
            if od <= 7200: total_cost += 3*length
            elif od <= 14400: total_cost += 3.5*length
            else:
                print 'Wrong'
                total_cost += 1000*length
        else:
            end = int(end)
            length = distance(centroid3_x, centroid3_y, zone_x_dict[end], zone_y_dict[end])
            edge_length_dict[edge] = length
            if od <= 7200: total_cost += 3*length
            elif od <= 14400: total_cost += 3.5*length
            else:
                print 'Wrong'
                total_cost += 1000*length

    # print total_cost
    total_cost = total_cost*100000000/1000/365/100 + sum(edge_length_dict[edge]*edge_od_dict[edge] for edge in edge_length_dict.keys())/1000
    print total_cost
    # print edge_length_dict
    # print edge_od_dict
    return total_cost, level2_list, level2_service_list_dict, point_od_dict, edge_od_dict


def calculate_edge_od(graph, point_od_dict, zone_x_dict, zone_y_dict, centroid_x, centroid_y):
    point2father_od_dict = {}
    visited = []
    def dfs(point, visited, point2father_od_dict):
        visited.append(point)
        unvisited_next = [i for i in graph[point] if i not in visited]
        if not unvisited_next:
            point2father_od_dict[point] = point_od_dict[point]
        else:
            point2father_od_dict[point] = sum(dfs(next, visited, point2father_od_dict) for next in unvisited_next) + point_od_dict[point]
        return point2father_od_dict[point]

    dfs('center', visited, point2father_od_dict)
    edge_od_dict = {}
    visited = []
    def dfs2(point, visited, edge_od_dict, point2father_od_dict):
        visited.append(point)
        for next in [i for i in graph[point] if i not in visited]:
            edge_od_dict[point+'->'+next] = point2father_od_dict[next]
            dfs2(next, visited, edge_od_dict, point2father_od_dict)
    dfs2('center', visited, edge_od_dict, point2father_od_dict)
    return edge_od_dict


def distance(point1_x, point1_y, point2_x, point2_y):
    return ((point1_x-point2_x)**2 + (point1_y-point2_y)**2)**0.5

def minimize_total_length(level2_list,  zone_x_dict, zone_y_dict, centroid_x, centroid_y):
    edge_length_dict = {}
    for level2 in level2_list:
        edge_length_dict['center->'+str(level2)] = distance(zone_x_dict[level2], zone_y_dict[level2], centroid_x, centroid_y)
    for start in level2_list:
        for end in level2_list:
            if start != end and str(end)+'->'+str(start) not in edge_length_dict:
                edge_length_dict[str(start)+'->'+str(end)] = distance(zone_x_dict[start], zone_y_dict[start], zone_x_dict[end], zone_y_dict[end])
    edge_list = sorted(edge_length_dict.keys(), key=lambda x:edge_length_dict[x])
    # for e in edge_list:
    #     print e, edge_length_dict[e]
    graph = {str(k):[] for k in level2_list+['center']}
    while not isConnected(graph) and edge_list:
        min_edge = edge_list[0]
        start, end = min_edge.split('->')
        # print min_edge
        # print graph
        if hasLoop(graph, start, end):
            # print 'hasloop'
            edge_list.pop(0)
        else:
            edge_list.pop(0)
            graph[start].append(end)
            graph[end].append(start)
    return graph

def hasloop_dfs(start, graph, edge_start, edge_end, visited):
    flag = 0
    for next in graph[start]:
        if next not in visited:
            # print next, edge_end
            if next == edge_end:
                flag = 1
                return flag
            else:
                visited.append(next)
                flag += hasloop_dfs(next, graph, edge_start, edge_end, visited)
    return flag

def hasLoop(graph, edge_start, edge_end):
    # print graph, edge_start, edge_end
    visited = [edge_start]
    return hasloop_dfs(edge_start, graph, edge_start, edge_end, visited)
    # print has_loop
    # return True if has_loop else False

def isConnected(graph):
    # print graph
    start = 'center'
    visited = [start]

    def dfs(start):
        for next in graph[start]:
            if next not in visited:
                visited.append(next)
                dfs(next)

    dfs(start)
    # print visited
    return False if len(visited) < len(graph.keys()) else True

def annealing(zone_point_list, level2_num, zone_min_decreod_dict, zone_x_dict, zone_y_dict, goods_x, goods_y, centroid_x, centroid_y):
    point_od_dict = {}
    level2_service_list_dict = {}
    point_centroid_distance_dict = {i:((zone_x_dict[i]-centroid_x)**2 + (zone_y_dict[i]-centroid_y)**2)**0.5 for i in zone_point_list}
    sorted_point_list_accoring_centroid_distance = sorted(zone_point_list, key=lambda x: point_centroid_distance_dict[x])
    # for i in sorted_point_list_accoring_centroid_distance:
    #     print i, point_centroid_distance_dict[i], zone_min_decreod_dict[i]
    point_in_centroid_list = [i for i in sorted_point_list_accoring_centroid_distance if point_centroid_distance_dict[i] <= 3000]
    centroid_load = 4000
    while centroid_load and point_in_centroid_list:
        if 'center' in level2_service_list_dict:
            level2_service_list_dict['center'].append(point_in_centroid_list[0])
        else:
            level2_service_list_dict['center'] = [point_in_centroid_list[0]]
        if zone_min_decreod_dict[point_in_centroid_list[0]] <= centroid_load:
            centroid_load -= zone_min_decreod_dict[point_in_centroid_list[0]]
            zone_min_decreod_dict[point_in_centroid_list[0]] = 0
            point_in_centroid_list.pop(0)
        else:
            zone_min_decreod_dict[point_in_centroid_list[0]] -= centroid_load
            centroid_load = 0

    # for i in sorted_point_list_accoring_centroid_distance:
    #     print i, point_centroid_distance_dict[i], zone_min_decreod_dict[i]
    # print len(zone_point_list)
    point_od_dict['center'] = 4000-centroid_load
    initial_plan = []
    # initial_plan = [859, 863, 853, 858, 847]
    try_num = 0
    while not isVaild(initial_plan, zone_point_list, zone_min_decreod_dict, zone_x_dict, zone_y_dict, centroid_x,
                      centroid_y, point_od_dict, level2_service_list_dict):
        initial_plan = []
        while len(initial_plan) < level2_num:
            get_one = random.choice(zone_point_list)
            if get_one not in initial_plan:
                initial_plan.append(get_one)
        # initial_plan = [826, 824, 829, 803, 837]
        try_num += 1
        # print try_num, initial_plan
    return initial_plan, point_od_dict, level2_service_list_dict

def isVaild(level2_list, zone_point_list, zone_min_decreod_dict, zone_x_dict, zone_y_dict, centroid_x, centroid_y,
            point_od_dict, level2_service_list_dict):
    for i in zone_point_list:
        if not any([((zone_x_dict[i] - zone_x_dict[level2])**2 + (zone_y_dict[i] - zone_y_dict[level2])**2)**0.5 <= 3000 for level2 in level2_list] \
                   + [((zone_x_dict[i] - centroid_x)**2 + (zone_y_dict[i] - centroid_y)**2)**0.5 <= 3000]): return False
    zone_min_decreod_dict_local = zone_min_decreod_dict.copy()
    point_od_dict_local = point_od_dict.copy()
    level2_service_list_dict_local = level2_service_list_dict.copy()
    # for i in zone_point_list:
    #     print i, zone_min_decreod_dict_local[i]
    for level2 in level2_list:
        point_level2_distance_dict = {i:((zone_x_dict[i]-zone_x_dict[level2])**2 + (zone_y_dict[i]-zone_y_dict[level2])**2)**0.5 for i in zone_point_list}
        sorted_point_list_accoring_level2_distance = sorted(zone_point_list, key=lambda x: point_level2_distance_dict[x])
        point_in_level2_list = [i for i in sorted_point_list_accoring_level2_distance if point_level2_distance_dict[i] <= 3000]
        level2_load = 3000
        while level2_load and point_in_level2_list:
            if str(level2) in level2_service_list_dict_local:
                level2_service_list_dict_local[str(level2)].append(point_in_level2_list[0])
            else:
                level2_service_list_dict_local[str(level2)] = [point_in_level2_list[0]]
            if zone_min_decreod_dict_local[point_in_level2_list[0]] <= level2_load:
                level2_load -= zone_min_decreod_dict_local[point_in_level2_list[0]]
                zone_min_decreod_dict_local[point_in_level2_list[0]] = 0
                point_in_level2_list.pop(0)
            else:
                zone_min_decreod_dict_local[point_in_level2_list[0]] -= level2_load
                level2_load = 0
        point_od_dict_local[str(level2)] = 3000 - level2_load
    if any([zone_min_decreod_dict_local[i] for i in zone_point_list]): return False
    else:
        zone_min_decreod_dict.update(zone_min_decreod_dict_local)
        point_od_dict.update(point_od_dict_local)
        level2_service_list_dict.update(level2_service_list_dict_local)
    # for i in zone_point_list:
    #     print i, zone_min_decreod_dict_local[i]
    return True

def linear_programming(zone_point_list, level2_num, zone_min_decreod_dict, zone_x_dict, zone_y_dict, goods_x, goods_y):
    prob = LpProblem("ULS", LpMinimize)
    centroid_x = LpVariable("centroid_x")
    centroid_y = LpVariable("centroid_y")
    level2_sites = LpVariable.dicts("level2_site", (range(level2_num), ['x', 'y']))
    prob += 50*((centroid_x-goods_x)**2 + (centroid_y-goods_y)**2)**0.5 \
         + 30*sum(((level2_sites[i]['x']-centroid_x)**2 + (level2_sites[i]['y']-centroid_y)**2)**0.5 for i in range(level2_num))
    for i in range(level2_num):
        level2_site_load = 0
        for point in zone_point_list:
            if ((zone_x_dict[point] - level2_sites[i]['x'])**2 + (zone_y_dict[point] - level2_sites[i]['y'])**2)**0.5 <= 30000:
                level2_site_load += zone_min_decreod_dict[point]
        prob += level2_site_load <= 3000
    for point in zone_point_list:
        judge_list = []
        for i in range(level2_num):
            judge_list.append(((zone_x_dict[point] - level2_sites[i]['x'])**2 + (zone_y_dict[point] - level2_sites[i]['y'])**2)**0.5 <= 30000)
        prob += any(judge_list) == True
    prob.writeLP("ULS.lp")
    prob.solve()

    print "Status:", LpStatus[prob.status]



if __name__ == '__main__':
    main()
    # isConnected({'833': [], '830': [], 'center': ['811'], '818': [], '811': ['center'], '800': [], '814': []})

    # graph = {'847': ['853'], 'center': ['859', '863'], '853': ['859', '847'], '863': ['center'], '858': [], '859': ['center', '853']}
    # print hasLoop(graph, 'center','853')
