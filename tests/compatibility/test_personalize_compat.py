"""Personalize compatibility tests."""

import pytest
from botocore.exceptions import ClientError

from tests.compatibility.conftest import make_client


@pytest.fixture
def personalize():
    return make_client("personalize")


class TestPersonalizeOperations:
    def test_list_schemas(self, personalize):
        resp = personalize.list_schemas()
        assert "schemas" in resp
        assert isinstance(resp["schemas"], list)

    def test_describe_nonexistent_schema(self, personalize):
        with pytest.raises(ClientError) as exc:
            personalize.describe_schema(
                schemaArn="arn:aws:personalize:us-east-1:123456789012:schema/nonexist"
            )
        assert exc.value.response["Error"]["Code"] == "ResourceNotFoundException"


class TestPersonalizeGapListOps:
    """Tests for newly-implemented list operations."""

    @pytest.fixture
    def client(self):
        return make_client("personalize")

    def test_list_datasets(self, client):
        resp = client.list_datasets()
        assert "datasets" in resp

    def test_list_dataset_groups(self, client):
        resp = client.list_dataset_groups()
        assert "datasetGroups" in resp

    def test_list_campaigns(self, client):
        resp = client.list_campaigns()
        assert "campaigns" in resp

    def test_list_solutions(self, client):
        resp = client.list_solutions()
        assert "solutions" in resp

    def test_list_solution_versions(self, client):
        resp = client.list_solution_versions()
        assert "solutionVersions" in resp

    def test_list_recommenders(self, client):
        resp = client.list_recommenders()
        assert "recommenders" in resp

    def test_list_filters(self, client):
        resp = client.list_filters()
        assert "Filters" in resp

    def test_list_recipes(self, client):
        resp = client.list_recipes()
        assert "recipes" in resp

    def test_list_event_trackers(self, client):
        resp = client.list_event_trackers()
        assert "eventTrackers" in resp

    def test_list_batch_inference_jobs(self, client):
        resp = client.list_batch_inference_jobs()
        assert "batchInferenceJobs" in resp

    def test_list_batch_segment_jobs(self, client):
        resp = client.list_batch_segment_jobs()
        assert "batchSegmentJobs" in resp

    def test_list_metric_attributions(self, client):
        resp = client.list_metric_attributions()
        assert "metricAttributions" in resp

    def test_list_data_deletion_jobs(self, client):
        resp = client.list_data_deletion_jobs()
        assert "dataDeletionJobs" in resp

    def test_list_tags_for_resource(self, client):
        arn = "arn:aws:personalize:us-east-1:123456789012:solution/test"
        client.tag_resource(resourceArn=arn, tags=[{"tagKey": "env", "tagValue": "test"}])
        resp = client.list_tags_for_resource(resourceArn=arn)
        assert "tags" in resp
