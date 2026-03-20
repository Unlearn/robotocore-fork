"""Forecast compatibility tests."""

import pytest
from botocore.exceptions import ClientError

from tests.compatibility.conftest import make_client


@pytest.fixture
def forecast():
    return make_client("forecast")


class TestForecastOperations:
    def test_list_dataset_groups(self, forecast):
        resp = forecast.list_dataset_groups()
        assert "DatasetGroups" in resp
        assert isinstance(resp["DatasetGroups"], list)

    def test_describe_nonexistent_dataset_group(self, forecast):
        with pytest.raises(ClientError) as exc:
            forecast.describe_dataset_group(
                DatasetGroupArn="arn:aws:forecast:us-east-1:123456789012:dataset-group/nonexist"
            )
        assert exc.value.response["Error"]["Code"] == "ResourceNotFoundException"


class TestForecastGapListOps:
    """Tests for newly-implemented list operations."""

    @pytest.fixture
    def client(self):
        return make_client("forecast")

    def test_list_datasets(self, client):
        resp = client.list_datasets()
        assert "Datasets" in resp

    def test_list_dataset_import_jobs(self, client):
        resp = client.list_dataset_import_jobs()
        assert "DatasetImportJobs" in resp

    def test_list_forecasts(self, client):
        resp = client.list_forecasts()
        assert "Forecasts" in resp

    def test_list_forecast_export_jobs(self, client):
        resp = client.list_forecast_export_jobs()
        assert "ForecastExportJobs" in resp

    def test_list_predictors(self, client):
        resp = client.list_predictors()
        assert "Predictors" in resp

    def test_list_predictor_backtest_export_jobs(self, client):
        resp = client.list_predictor_backtest_export_jobs()
        assert "PredictorBacktestExportJobs" in resp

    def test_list_explainabilities(self, client):
        resp = client.list_explainabilities()
        assert "Explainabilities" in resp

    def test_list_explainability_exports(self, client):
        resp = client.list_explainability_exports()
        assert "ExplainabilityExports" in resp

    def test_list_monitors(self, client):
        resp = client.list_monitors()
        assert "Monitors" in resp

    def test_list_what_if_analyses(self, client):
        resp = client.list_what_if_analyses()
        assert "WhatIfAnalyses" in resp

    def test_list_what_if_forecasts(self, client):
        resp = client.list_what_if_forecasts()
        assert "WhatIfForecasts" in resp

    def test_list_what_if_forecast_exports(self, client):
        resp = client.list_what_if_forecast_exports()
        assert "WhatIfForecastExports" in resp

    def test_list_tags_for_resource(self, client):
        arn = "arn:aws:forecast:us-east-1:123456789012:dataset-group/test"
        client.tag_resource(ResourceArn=arn, Tags=[{"Key": "env", "Value": "test"}])
        resp = client.list_tags_for_resource(ResourceArn=arn)
        assert "Tags" in resp
        assert any(t["Key"] == "env" for t in resp["Tags"])
