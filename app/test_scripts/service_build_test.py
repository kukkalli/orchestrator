from templates.service_profile_template import ServiceProfileTemplate


def service_built(service: ServiceProfileTemplate):
    flavor = service.flavor_id_map["2"]
    print(f"Flavor: id: {flavor.id}, name: {flavor.name}, vcpus: {flavor.vcpus}, ram: {flavor.ram}")
    for network_function in service.get_network_functions():
        print(f"VM Requirement: {network_function.name}, int_id: {network_function.image_name}")

    for link in service.get_nfv_v_links_list():
        print(f"link name: {link['out']}, int_id: {link['in']}")
