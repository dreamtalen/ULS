from main import main

if __name__ == '__main__':
    min_cost = 369556.4662134837
    min_level2_list, min_level2_service_list_dict, min_point_od_dict, min_edge_od_dict = [], {}, {}, {}
    for i in range(100):
        total_cost, level2_list, level2_service_list_dict, point_od_dict, edge_od_dict = main()
        if total_cost < min_cost:
            min_cost = total_cost
            min_level2_list, min_level2_service_list_dict, min_point_od_dict, min_edge_od_dict = level2_list, level2_service_list_dict, point_od_dict, edge_od_dict
    print min_level2_list
    print min_level2_service_list_dict
    print min_point_od_dict
    print min_edge_od_dict
    print min_cost