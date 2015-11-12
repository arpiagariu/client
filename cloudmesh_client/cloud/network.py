from __future__ import print_function

from pprint import pprint
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.Printer import attribute_printer
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider


class Network(ListResource):
    @classmethod
    def get_fixed_ip(cls, cloud, fixed_ip):
        pass

    @classmethod
    def get_floating_ip(cls, cloudname, floating_ip_id):
        try:
            cloud_provider = CloudProvider(cloudname).provider
            result = cloud_provider.get_floating_ip(floating_ip_id=floating_ip_id)

            return attribute_printer(result,
                                     header=[
                                         "name",
                                         "value"
                                     ])
        except Exception as ex:
            Console.error(ex.message, ex)

        return

    @classmethod
    def fixed_ip_reserve(cls, cloud, fixed_ip):
        pass

    @classmethod
    def fixed_ip_unreserve(cls, cloud, fixed_ip):
        pass

    @classmethod
    def floating_ip_associate(cls, cloud, server, floating_ip):
        pass

    @classmethod
    def floating_ip_disassociate(cls, cloud, server, floating_ip):
        pass

    @classmethod
    def floating_ip_create(cls, cloud, floating_pool=None):
        pass

    @classmethod
    def floating_ip_delete(cls, cloud, floating_ip):
        pass

    @classmethod
    def list_floating_ip(cls, cloudname):
        try:
            cloud_provider = CloudProvider(cloudname).provider
            floating_ips = cloud_provider.list_floating_ips()

            (order, header) = CloudProvider(cloudname).get_attributes("floating_ip")

            return dict_printer(floating_ips,
                                order=order,
                                header=header)
        except Exception as ex:
            Console.error(ex.message, ex)

        return

    @classmethod
    def floating_ip_pool_list(cls, cloud):
        pass
