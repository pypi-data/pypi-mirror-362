import pytest
import json
import responses

from pytos2.securetrack.cloud import JoinCloud
from pytos2.utils import get_api_node

from netaddr import IPAddress


class TestCloud:
    @responses.activate
    def test_get_clouds_200(self, st):
        responses.add(
            responses.GET,
            "https://198.18.0.1/securetrack/api/topology/clouds",
            json=json.load(
                open("tests/securetrack/json/clouds/all_non_joined_clouds.json")
            ),
            status=200,
        )

        clouds = st.get_clouds()
        cl = clouds[0]
        assert cl.id == 5
        assert cl.name == "Cloud 192.168.111.1"
        assert cl.domain == 1
        assert cl.type.value == "NON_JOINED"
        assert cl.ip == IPAddress("192.168.111.1")
        assert isinstance(cl.members, list)

    @responses.activate
    def test_get_cloud(self, st):
        responses.add(
            responses.GET,
            "https://198.18.0.1/securetrack/api/topology/clouds/4",
            json=json.load(open("tests/securetrack/json/clouds/cloud_4.json")),
            status=200,
        )

        cl = st.get_cloud(4)
        assert cl.id == 4
        assert cl.name == "Cloud 10.100.100.19"
        assert cl.domain == 1
        assert cl.type.value == "NON_JOINED"
        assert cl.ip == IPAddress("10.100.100.19")
        assert isinstance(cl.members, list)

    @responses.activate
    def test_get_cloud_internal_networks(self, st):
        responses.add(
            responses.GET,
            "https://198.18.0.1/securetrack/api/topology/cloud_internal_networks/58",
            json=json.load(
                open("tests/securetrack/json/clouds/cloud_internal_networks_58.json")
            ),
            status=200,
        )

        networks = st.get_cloud_internal_networks(58)
        ntwk = networks[0]
        assert ntwk.ip == IPAddress("192.168.74.1")
        assert ntwk.mask == IPAddress("255.255.255.0")

    @responses.activate
    def test_add_topology_cloud(self, st):
        responses.add(
            responses.POST,
            "https://198.18.0.1/securetrack/api/topology/clouds",
            status=200,
        )
        response = st.add_topology_cloud(cloud_name="Cloud 888", cloud_members=[49, 51])
        assert response is None

    @responses.activate
    def test_update_topology_cloud(self, st):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securetrack/api/topology/clouds/105",
            status=200,
        )

        response = st.update_topology_cloud(105, cloud_name="Cloud 888")
        assert response is None

        response = st.update_topology_cloud(105, cloud_members=[52])
        assert response is None

        response = st.update_topology_cloud(105, cloud_members=[52], action="remove")
        assert response is None

    @responses.activate
    def test_get_cloud_suggestions(self, st):
        responses.add(
            responses.GET,
            "https://198.18.0.1/securetrack/api/topology/cloud_suggestions",
            json=json.load(
                open("tests/securetrack/json/clouds/cloud_suggestions.json")
            ),
            status=200,
        )

        cloud_suggestions = st.get_cloud_suggestions()
        cl = cloud_suggestions[0]
        assert cl.management_name == "ACI Fabric"
        assert cl.management_id == 234
        assert cl.cloud_name == "Cloud 10.30.27.6"
        assert cl.cloud_id == 32
        assert cl.vertex_id == 485
        assert cl.ip == IPAddress("10.30.27.6")
        assert cl.routes_count == 134
        assert cl.is_parent is False

    @responses.activate
    def test_get_cloud_suggestions_by_id(self, st):
        responses.add(
            responses.GET,
            "https://198.18.0.1/securetrack/api/topology/cloud_suggestions/32",
            json=json.load(
                open("tests/securetrack/json/clouds/cloud_suggestions_32.json")
            ),
            status=200,
        )

        # This somewhat unexpectedly returns a list
        cl = st.get_cloud_suggestions_by_id(32)[0]
        assert cl.management_name == "ACI Fabric"
        assert cl.management_id == 234
        assert cl.cloud_name == "Cloud 10.30.27.6"
        assert cl.cloud_id == 32
        assert cl.vertex_id == 485
        assert cl.ip == IPAddress("10.30.27.6")
        assert cl.routes_count == 134
        assert cl.is_parent is False


class TestJoinCloud:
    cloud = json.load(open("tests/securetrack/json/join_clouds/cloud-67.json"))

    @responses.activate
    def test_add_join_cloud_200(self, st):
        """Add cloud"""
        responses.add(
            responses.POST,
            "https://198.18.0.1/securetrack/api/topology/join/clouds",
            status=201,
        )

        """Add single cloud"""
        newCloud = st.add_join_cloud(
            name=self.cloud["name"], clouds=self.cloud["clouds"]
        )
        assert newCloud is None

    @responses.activate
    def test_add_join_cloud_400(self, st):
        """Add cloud"""
        responses.add(
            responses.POST,
            "https://198.18.0.1/securetrack/api/topology/join/clouds",
            status=400,
        )

        """Add single cloud"""
        with pytest.raises(ValueError) as exception:
            st.add_join_cloud(name=self.cloud["name"], clouds=self.cloud["clouds"])
        assert "Bad Request" in str(exception.value)

    @responses.activate
    def test_add_join_cloud_404(self, st):
        """Add cloud"""
        responses.add(
            responses.POST,
            "https://198.18.0.1/securetrack/api/topology/join/clouds",
            status=404,
        )

        """Add single cloud"""
        with pytest.raises(ValueError) as exception:
            st.add_join_cloud(name=self.cloud["name"], clouds=self.cloud["clouds"])
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_get_join_cloud(self, st, join_cloud_mock):
        """Get cloud by device id"""
        join_cloud = JoinCloud.kwargify(self.cloud)
        cloudByInt = st.get_join_cloud(67)
        cloudByStr = st.get_join_cloud("67")
        assert cloudByInt == join_cloud
        assert cloudByStr == join_cloud

        with pytest.raises(ValueError) as exception:
            st.get_join_cloud(404)
        assert "Not Found" in str(exception.value)

        with pytest.raises(ValueError) as exception:
            st.delete_join_cloud("404")
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_update_join_cloud_200(self, st):
        """Update cloud"""
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securetrack/api/topology/join/clouds",
            status=200,
        )

        """Update single cloud"""
        cloud_to_update = JoinCloud.kwargify(self.cloud)
        newCloud = st.update_join_cloud(cloud_to_update)
        assert newCloud is None

    @responses.activate
    def test_update_join_cloud_400(self, st):
        """PUT bad request"""
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securetrack/api/topology/join/clouds",
            status=400,
        )

        with pytest.raises(ValueError) as exception:
            cloud_to_update = JoinCloud.kwargify(self.cloud)
            st.update_join_cloud(cloud_to_update)
        assert "Bad Request" in str(exception.value)

    @responses.activate
    def test_update_join_cloud_404(self, st):
        """PUT device id not found"""
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securetrack/api/topology/join/clouds",
            status=404,
        )

        with pytest.raises(ValueError) as exception:
            cloud_to_update = JoinCloud.kwargify(self.cloud)
            st.update_join_cloud(cloud_to_update)
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_delete_join_cloud(self, st, join_cloud_mock):
        """Delete cloud by cloud id"""
        cloudByInt = st.delete_join_cloud(67)
        cloudByStr = st.delete_join_cloud("67")
        assert cloudByInt is None
        assert cloudByStr is None

        with pytest.raises(ValueError) as exception:
            st.delete_join_cloud(404)
        assert "Not Found" in str(exception.value)

        with pytest.raises(ValueError) as exception:
            st.delete_join_cloud("404")
        assert "Not Found" in str(exception.value)
